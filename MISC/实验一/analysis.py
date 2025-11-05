import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils import resample

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)

def load_and_clean(path='dataset_demo.csv'):
    try:
        df = pd.read_csv(path, encoding='gbk')
    except Exception:
        df = pd.read_csv(path, encoding='utf-8', errors='ignore')
    df = df.dropna(how='all')
    # 找到血压列并拆分
    bp_cols = [c for c in df.columns if '血压' in str(c) or 'mmHg' in str(c) or 'mmhg' in str(c)]
    if len(bp_cols)==0:
        bp_cols = [c for c in df.columns if df[c].astype(str).str.contains('/').any()]
    bp_col = bp_cols[0] if bp_cols else None
    if bp_col:
        df[['右侧收缩压','右侧舒张压']] = df[bp_col].astype(str).str.split('/', expand=True)
        df['右侧收缩压'] = pd.to_numeric(df['右侧收缩压'], errors='coerce')
        df['右侧舒张压'] = pd.to_numeric(df['右侧舒张压'], errors='coerce')

    # 合并描述列的简化实现
    def merge_ecg_description(x):
        if pd.isna(x):
            return 'NA'
        s = str(x)
        if 'T' in s or 'ST' in s or 'T波' in s:
            return 'ST异常'
        if '过缓' in s or '缓' in s:
            return '过缓'
        if '正常' in s:
            return '正常'
        return '其他'

    def merge_us_description(x):
        if pd.isna(x):
            return 'NA'
        s = str(x)
        for k in ['肝','胆','肺','血管','结石','心']:
            if k in s:
                return k
        if '正常' in s:
            return '正常'
        return '其他'

    ecg_cols = [c for c in df.columns if '心电' in str(c) or '心电图' in str(c)]
    us_cols = [c for c in df.columns if 'B超' in str(c) or '超声' in str(c) or 'B��' in str(c)]
    if ecg_cols:
        df['合并心电图描述'] = df[ecg_cols[0]].apply(merge_ecg_description)
    if us_cols:
        df['合并B超描述'] = df[us_cols[0]].apply(merge_us_description)

    # 简化风险判定
    def categorize_risk(row):
        try:
            if (row.get('右侧收缩压', 0) >= 160 or
                row.get('右侧舒张压', 0) >= 100 or
                float(row.get('血清低密度脂蛋白胆固醇', 0) or 0) >= 4.14 or
                float(row.get('血淸高密度脂蛋白胆固醇', 999) or 999) < 0.78 or
                float(row.get('十年心血管病患病风险', 0) or 0) >= 20):
                return '高风险'
        except Exception:
            def plot_and_train(df):
                # Plot: risk distribution (use English labels for plots)
                vc = df['风险类别'].value_counts()
                plt.figure(figsize=(6,4))
                eng_index = [ 'Low Risk' if x=='低风险' else ('High Risk' if x=='高风险' else str(x)) for x in vc.index ]
                sns.barplot(x=eng_index, y=vc.values, palette='pastel')
                plt.title('Risk Category Distribution')
                plt.ylabel('Count')
                plt.savefig('fig_distribution.png', bbox_inches='tight')

                # Blood pressure scatter (use English legend labels)
                if '右侧收缩压' in df.columns and '右侧舒张压' in df.columns:
                    plt.figure(figsize=(6,5))
                    # ensure English legend exists
                    if 'risk_label' not in df.columns:
                        df['risk_label'] = df['风险类别'].map({'低风险': 'Low Risk', '高风险': 'High Risk'}).fillna(df['风险类别'].astype(str))
                    sns.scatterplot(data=df, x='右侧收缩压', y='右侧舒张压', hue='risk_label', alpha=0.7)
                    plt.title('Systolic vs Diastolic Blood Pressure (samples)')
                    plt.savefig('fig_bp_scatter.png', bbox_inches='tight')

                # Prepare features
                num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                features = [c for c in num_cols if c not in []]
                if len(features) < 2:
                    for name in ['年龄','身高','体重','体质指数','空腹血糖MMOL','总胆固醇','甘油三酯','血清低密度脂蛋白胆固醇','血淸高密度脂蛋白胆固醇']:
                        if name in df.columns and name not in features:
                            features.append(name)

                le = LabelEncoder()
                if df['风险类别'].dtype == object:
                    y = le.fit_transform(df['风险类别'].astype(str))
                else:
                    y = df['风险类别'].values

                X = df[features].copy()
                X = X.fillna(X.median())
                scaler = StandardScaler()
                Xs = scaler.fit_transform(X)

                # Hold-out
                X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y))>1 else None)
                clf = LogisticRegression(max_iter=200)
                clf.fit(X_train, y_train)
                y_pred = clf.predict(X_test)
                cm = confusion_matrix(y_test, y_pred)
                from sklearn.metrics import ConfusionMatrixDisplay
                plt.figure(figsize=(5,4))
                ConfusionMatrixDisplay(cm).plot(cmap='Blues', values_format='d')
                plt.title('Confusion Matrix (Hold-out)')
                plt.savefig('fig_confusion.png', bbox_inches='tight')

                # ROC
                if len(np.unique(y))==2:
                    y_score = clf.predict_proba(X_test)[:,1]
                    fpr, tpr, _ = roc_curve(y_test, y_score)
                    roc_auc = auc(fpr, tpr)
                    plt.figure(figsize=(5,4))
                    plt.plot(fpr,tpr,label=f'AUC={roc_auc:.2f}')
                    plt.plot([0,1],[0,1],'k--')
                    plt.xlabel('False Positive Rate')
                    plt.ylabel('True Positive Rate')
                    plt.title('ROC (Hold-out)')
                    plt.legend()
                    plt.savefig('fig_roc.png', bbox_inches='tight')

                # Cross-validation
                skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
                accs = []
                for tr_idx, te_idx in skf.split(Xs, y):
                    m = LogisticRegression(max_iter=200)
                    m.fit(Xs[tr_idx], y[tr_idx])
                    accs.append(m.score(Xs[te_idx], y[te_idx]))

                # Bootstrap
                n_boot = 30
                boot_scores = []
                for i in range(n_boot):
                    Xb, yb = resample(Xs, y, replace=True, n_samples=len(y), random_state=42+i)
                    oob_mask = ~np.isin(range(len(y)), np.unique(resample(range(len(y)), replace=True, n_samples=len(y), random_state=42+i)))
                    if oob_mask.sum() < 5:
                        continue
                    clf_b = LogisticRegression(max_iter=200)
                    clf_b.fit(Xb, yb)
                    try:
                        score = clf_b.score(Xs[oob_mask], y[oob_mask])
                        boot_scores.append(score)
                    except Exception:
                        pass

                # Save intermediates
                X.head(10).to_csv('cleaned_sample_features.csv', index=False)
                pd.DataFrame(df['风险类别'].value_counts()).reset_index().to_csv('risk_counts.csv', index=False, header=['风险类别','count'])

                return {
                    'cv_mean': np.mean(accs) if accs else None,
                    'cv_std': np.std(accs) if accs else None,
                    'bootstrap_mean': np.mean(boot_scores) if boot_scores else None,
                    'bootstrap_std': np.std(boot_scores) if boot_scores else None,
                    'confusion_matrix': cm.tolist() if 'cm' in locals() else None
                }
    # 保存中间结果
    X.head(10).to_csv('cleaned_sample_features.csv', index=False)
    pd.DataFrame(df['风险类别'].value_counts()).reset_index().to_csv('risk_counts.csv', index=False, header=['风险类别','count'])

    return {
        'cv_mean': np.mean(accs) if accs else None,
        'cv_std': np.std(accs) if accs else None,
        'bootstrap_mean': np.mean(boot_scores) if boot_scores else None,
        'bootstrap_std': np.std(boot_scores) if boot_scores else None,
        'confusion_matrix': cm.tolist() if 'cm' in locals() else None
    }

if __name__ == '__main__':
    df = load_and_clean('dataset_demo.csv')
    stats = plot_and_train(df)
    print('Done. stats:', stats)
