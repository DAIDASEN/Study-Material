#!/usr/bin/env python3
import argparse
from pathlib import Path
import json
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
import joblib
import xgboost as xgb
from tqdm import tqdm


def load_concat_features(feat_dirs):
    # load train+val and test from multiple directories and concat horizontally
    X_tr_list, y_tr_list = [], []
    X_val_list, y_val_list = [], []
    X_te_list = []
    test_ids = None
    for d in feat_dirs:
        d = Path(d)
        X_tr = np.load(d / 'train_feats.npy')
        y_tr = np.load(d / 'train_labels.npy')
        X_val = np.load(d / 'val_feats.npy')
        y_val = np.load(d / 'val_labels.npy')
        X_te = np.load(d / 'test_feats.npy')
        ids = [line.strip() for line in (d / 'test_ids.csv').read_text().splitlines()]
        if test_ids is None:
            test_ids = ids
        else:
            assert test_ids == ids, 'Test ids mismatch across feature dirs'
        X_tr_list.append(X_tr)
        y_tr_list.append(y_tr)
        X_val_list.append(X_val)
        y_val_list.append(y_val)
        X_te_list.append(X_te)
    X_train = np.concatenate([np.concatenate(X_tr_list, axis=1), np.concatenate(X_val_list, axis=1)], axis=0)
    y_train = np.concatenate([y_tr_list[0], y_val_list[0]], axis=0)  # assume same labels
    X_test = np.concatenate(X_te_list, axis=1)
    return X_train, y_train, X_test, test_ids


def explained_pca_fit(X, var_ratio, n_components=None):
    # Prefer explicit n_components if provided
    if n_components is not None and n_components > 0:
        pca = PCA(n_components=n_components, svd_solver='randomized', whiten=False, iterated_power=3)
        pca.fit(X)
        return pca
    # Fit PCA selecting n_components to reach var_ratio
    if var_ratio <= 0 or var_ratio >= 1:
        return None
    # First fit with randomized to obtain variance spectrum quickly
    probe = PCA(svd_solver='randomized', whiten=False, iterated_power=3)
    probe.fit(X)
    csum = np.cumsum(probe.explained_variance_ratio_)
    n_comp = int(np.searchsorted(csum, var_ratio) + 1)
    pca = PCA(n_components=n_comp, svd_solver='randomized', whiten=False, iterated_power=3)
    pca.fit(X)
    return pca


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--feat_dirs', nargs='+', required=True, help='One or more feature directories to concatenate')
    ap.add_argument('--out_dir', type=Path, default=Path('checkpoints/xgb_cv'))
    ap.add_argument('--folds', type=int, default=5)
    ap.add_argument('--rounds', type=int, default=600)
    ap.add_argument('--early_stopping', type=int, default=60)
    ap.add_argument('--pca_var', type=float, default=0.99, help='Explained variance to keep, 0 to disable')
    ap.add_argument('--pca_components', type=int, default=None, help='If set, use fixed PCA components instead of variance target')
    ap.add_argument('--use_gpu', action='store_true', help='Use XGBoost gpu_hist and gpu_predictor')
    ap.add_argument('--n_jobs', type=int, default=max(1, (os.cpu_count() or 4) // 2), help='CPU threads for XGBoost and preprocessing')
    ap.add_argument('--seed', type=int, default=42)
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    X, y, X_test, test_ids = load_concat_features(args.feat_dirs)
    # Set numpy / joblib threading if needed
    os.environ.setdefault('OMP_NUM_THREADS', str(args.n_jobs))
    num_class = int(np.max(y)) + 1

    skf = StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=args.seed)
    oof_prob = np.zeros((len(X), num_class), dtype=np.float32)
    fold_models = []

    # simple grid
    grid = [
        {'eta': 0.05, 'max_depth': 8, 'min_child_weight': 1, 'subsample': 0.9, 'colsample_bytree': 0.9},
        {'eta': 0.05, 'max_depth': 10, 'min_child_weight': 1, 'subsample': 0.9, 'colsample_bytree': 0.9},
        {'eta': 0.03, 'max_depth': 10, 'min_child_weight': 1, 'subsample': 0.9, 'colsample_bytree': 0.9},
    ]

    fold_iter = enumerate(skf.split(X, y), start=1)
    for fold, (tr_idx, va_idx) in tqdm(list(fold_iter), total=args.folds, desc='CV folds'):
        X_tr, y_tr = X[tr_idx], y[tr_idx]
        X_va, y_va = X[va_idx], y[va_idx]

        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_tr)
        X_va_s = scaler.transform(X_va)

        pca = explained_pca_fit(X_tr_s, args.pca_var, n_components=args.pca_components)
        if pca is not None:
            X_tr_s = pca.transform(X_tr_s)
            X_va_s = pca.transform(X_va_s)

        dtr = xgb.DMatrix(X_tr_s, label=y_tr)
        dva = xgb.DMatrix(X_va_s, label=y_va)

        best = None
        best_pred = None
        for gi, hp in enumerate(tqdm(grid, desc=f'fold {fold} grid', leave=False)):
            params = {
                'objective': 'multi:softprob',
                'num_class': num_class,
                'eta': hp['eta'],
                'max_depth': hp['max_depth'],
                'min_child_weight': hp['min_child_weight'],
                'subsample': hp['subsample'],
                'colsample_bytree': hp['colsample_bytree'],
                'tree_method': 'gpu_hist' if args.use_gpu else 'hist',
                'predictor': 'gpu_predictor' if args.use_gpu else 'auto',
                'eval_metric': 'mlogloss',
                'seed': args.seed,
                'nthread': args.n_jobs,
            }
            evals = [(dtr, 'train'), (dva, 'val')]

            class TqdmCallback(xgb.callback.TrainingCallback):
                def __init__(self, total, desc):
                    self.total = total
                    self.desc = desc
                    self.pbar = None
                def before_training(self, model):
                    self.pbar = tqdm(total=self.total, desc=self.desc, leave=False)
                    return model
                def after_iteration(self, model, epoch, evals_log):
                    if self.pbar is not None:
                        self.pbar.update(1)
                    return False
                def after_training(self, model):
                    if self.pbar is not None:
                        self.pbar.close()
                    return model

            callbacks = [
                xgb.callback.EarlyStopping(rounds=args.early_stopping, save_best=True, data_name='val', metric_name='mlogloss'),
                TqdmCallback(args.rounds, desc=f'fold {fold} grid{gi} rounds')
            ]

            bst = xgb.train(params, dtr, num_boost_round=args.rounds, evals=evals, callbacks=callbacks, verbose_eval=False)
            best_iter = getattr(bst, 'best_iteration', None)
            if best_iter is not None:
                prob = bst.predict(dva, iteration_range=(0, best_iter + 1))
            else:
                prob = bst.predict(dva)
            pred = prob.argmax(axis=1)
            f1 = f1_score(y_va, pred, average='macro')
            if (best is None) or (f1 > best[0]):
                best = (f1, params, best_iter, bst)
                best_pred = prob

        # save best fold artifacts
        fold_dir = args.out_dir / f'fold_{fold}'
        fold_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(scaler, fold_dir / 'scaler.pkl')
        if pca is not None:
            joblib.dump(pca, fold_dir / 'pca.pkl')
        best[3].save_model(fold_dir / 'model.json')
        meta = {'val_macro_f1': float(best[0]), 'params': best[1], 'best_iteration': int(best[2]) if best[2] is not None else None}
        (fold_dir / 'meta.json').write_text(json.dumps(meta))

        oof_prob[va_idx] = best_pred
        fold_models.append((fold_dir, num_class))

    # OOF metric
    oof_pred = oof_prob.argmax(axis=1)
    macro_f1 = f1_score(y, oof_pred, average='macro')
    (args.out_dir / 'oof_metrics.json').write_text(json.dumps({'macro_f1': float(macro_f1)}))
    print(f'OOF macro F1: {macro_f1:.4f}')

    # Save train config
    (args.out_dir / 'config.json').write_text(json.dumps({'feat_dirs': list(map(str, args.feat_dirs)), 'pca_var': args.pca_var, 'folds': args.folds, 'num_class': num_class}))

    # Prepare test transforms and average
    # Fit scaler/pca on full data for test transformation per fold? We'll reuse per-fold scaler/pca to avoid leakage.
    # Load and predict test per fold
    test_prob = np.zeros((len(X_test), num_class), dtype=np.float32)
    for fold, (fold_dir, num_class) in enumerate(fold_models, start=1):
        scaler = joblib.load(fold_dir / 'scaler.pkl')
        pca_path = fold_dir / 'pca.pkl'
        has_pca = pca_path.exists()

        X_te_s = scaler.transform(X_test)
        if has_pca:
            pca = joblib.load(pca_path)
            X_te_s = pca.transform(X_te_s)

        dte = xgb.DMatrix(X_te_s)
        bst = xgb.Booster()
        bst.load_model(fold_dir / 'model.json')
        best_meta = json.loads((fold_dir / 'meta.json').read_text())
        best_iter = best_meta.get('best_iteration')
        if best_iter is not None:
            prob = bst.predict(dte, iteration_range=(0, int(best_iter) + 1))
        else:
            prob = bst.predict(dte)
        test_prob += prob / len(fold_models)

    # Save test probabilities and a default submission
    np.save(args.out_dir / 'test_prob.npy', test_prob)
    pred = test_prob.argmax(axis=1)
    with open(args.out_dir / 'test_ids.csv', 'w') as f:
        for i in test_ids:
            f.write(str(i) + '\n')
    import pandas as pd
    pd.DataFrame({'id': test_ids, 'label': pred}).to_csv(args.out_dir / 'submission_esm_embed_xgb_cv.csv', index=False)
    print(f"Saved CV submission to {args.out_dir / 'submission_esm_embed_xgb_cv.csv'}")


if __name__ == '__main__':
    main()
