#!/usr/bin/env python3
import argparse
from pathlib import Path
import numpy as np
import json
import joblib
import xgboost as xgb
import pandas as pd


def load_concat_test(feat_dirs):
    X_te_list = []
    test_ids = None
    for d in feat_dirs:
        d = Path(d)
        X_te = np.load(d / 'test_feats.npy')
        ids = [line.strip() for line in (d / 'test_ids.csv').read_text().splitlines()]
        if test_ids is None:
            test_ids = ids
        else:
            assert test_ids == ids, 'Test ids mismatch across feature dirs'
        X_te_list.append(X_te)
    X_test = np.concatenate(X_te_list, axis=1)
    return X_test, test_ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--feat_dirs', nargs='+', required=True)
    ap.add_argument('--model_dir', type=Path, required=True)
    ap.add_argument('--out_csv', type=Path, default=Path('submission_esm_embed_xgb_cv.csv'))
    args = ap.parse_args()

    X_test, test_ids = load_concat_test(args.feat_dirs)

    # find fold subdirs
    folds = sorted([p for p in args.model_dir.iterdir() if p.is_dir() and p.name.startswith('fold_')], key=lambda p: int(p.name.split('_')[-1]))
    assert len(folds) > 0, 'No fold_* directories found in model_dir'

    # infer num_class
    config_path = args.model_dir / 'config.json'
    if config_path.exists():
        cfg = json.loads(config_path.read_text())
        num_class = int(cfg.get('num_class', 0))
    else:
        num_class = 0

    test_prob = None
    for fold_dir in folds:
        scaler = joblib.load(fold_dir / 'scaler.pkl')
        X_te_s = scaler.transform(X_test)
        pca_path = fold_dir / 'pca.pkl'
        if pca_path.exists():
            pca = joblib.load(pca_path)
            X_te_s = pca.transform(X_te_s)

        dte = xgb.DMatrix(X_te_s)
        bst = xgb.Booster()
        bst.load_model(fold_dir / 'model.json')
        best_meta = json.loads((fold_dir / 'meta.json').read_text())
        best_iter = best_meta.get('best_iteration')
        prob = bst.predict(dte, iteration_range=(0, int(best_iter) + 1)) if best_iter is not None else bst.predict(dte)
        if test_prob is None:
            test_prob = prob
            if num_class == 0:
                num_class = prob.shape[1]
        else:
            test_prob += prob
    test_prob /= len(folds)

    pred = test_prob.argmax(axis=1)
    pd.DataFrame({'id': test_ids, 'label': pred}).to_csv(args.out_csv, index=False)
    print(f'Saved CV ensemble submission to {args.out_csv}')


if __name__ == '__main__':
    main()
