import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
import sys

def print_sep(title=""):
    """打印一个格式化的分隔符"""
    print(f"\n--- {title} {'-'* (70-len(title))}")

def run_recon(data_dir="data"):
    """
    执行GNN数据的战术性侦察。
    """
    print_sep("开始战术性数据侦察")
    base_path = Path(data_dir)

    # --- 0. 检查文件是否存在 ---
    files = {
        'edges': base_path / 'edges.txt',
        'features': base_path / 'features.txt',
        'train': base_path / 'train_labels.csv',
        'val': base_path / 'val_labels.csv',
        'test': base_path / 'test_idx.csv'
    }

    all_files_found = True
    for name, path in files.items():
        if not path.exists():
            print(f"错误: 文件未找到 {path}")
            all_files_found = False
    if not all_files_found:
        print("请确保所有文件都在 'data/' 目录中。")
        sys.exit(1)

    print(f"所有文件均已在 '{data_dir}' 目录中找到。")

    try:
        # --- 1. 加载标签和基本大小 ---
        print_sep("1. 加载标签和数据集大小")
        train_df = pd.read_csv(files['train'])
        val_df = pd.read_csv(files['val'])
        test_df = pd.read_csv(files['test'])

        print(f"训练集节点数:   {len(train_df)}")
        print(f"验证集节点数:   {len(val_df)}")
        print(f"测试集节点数:       {len(test_df)}")
        print(f"总标签节点数:   {len(train_df) + len(val_df)}")

        # --- 2. 加载特征和节点统计 ---
        print_sep("2. 加载特征和节点统计")
        # delim_whitespace=True 自动处理空格或Tab作为分隔符
        features_df = pd.read_csv(files['features'], delim_whitespace=True, header=None)
        
        N = len(features_df)
        D = features_df.shape[1] - 1
        print(f"总节点数 (N):     {N}")
        print(f"特征维度 (D):     {D}")

        # 计算稀疏度
        features_matrix = features_df.iloc[:, 1:].values
        sparsity = 1.0 - (np.count_nonzero(features_matrix) / features_matrix.size)
        print(f"特征稀疏度:       {sparsity:.4f} (1.0 = 全0, 0.0 = 全非0)")
        if sparsity > 0.8:
            print("  -> 特征非常稀疏 (例如: 词袋模型)。")
        
        all_nodes_set = set(features_df.iloc[:, 0])

        # --- 3. 加载边和图统计 ---
        print_sep("3. 加载边和图统计")
        edges_df = pd.read_csv(files['edges'], delim_whitespace=True, header=None)
        M = len(edges_df)
        print(f"总边数 (M):       {M}")
        print(f"平均度数:         {M / N:.4f} (如果是无向图)")

        # 检查图的对称性 (有向 vs 无向)
        edges_set = set(zip(edges_df[0], edges_df[1]))
        symmetric_count = sum(1 for u, v in edges_set if (v, u) in edges_set)
        
        print(f"对称性检查:       {symmetric_count} 条边存在反向边 (总共 {len(edges_set)} 条)")
        if symmetric_count == len(edges_set):
            print("  -> 图似乎是 无向的 (或包含自环)。")
        else:
            print("  -> 图似乎是 有向的。")

        # 检查孤立节点
        nodes_in_edges = set(edges_df[0]) | set(edges_df[1])
        isolated_nodes = all_nodes_set - nodes_in_edges
        print(f"孤立节点数:       {len(isolated_nodes)} (节点存在于特征中, 但不存在于边中)")

        # --- 4. 标签分布 (训练集) ---
        print_sep("4. 训练集标签分布")
        label_counts = Counter(train_df['label'])
        print(f"标签数量统计: {sorted(label_counts.items())}")
        if len(set(label_counts.values())) > 1:
            print("  -> 标签分布 不平衡。 (策略: 考虑使用类权重或 Focal Loss)")
        else:
            print("  -> 标签分布 相对平衡。")

        # --- 5. 边同质性 (关键指标) ---
        print_sep("5. 边同质性计算 (Kaggle策略关键)")
        # 我们使用所有已知的标签 (train + val) 来获得对图同质性的最佳估计
        all_labels_df = pd.concat([train_df, val_df])
        label_map = dict(zip(all_labels_df['id'], all_labels_df['label']))
        
        same_label_edges = 0
        total_edges_checked = 0

        # 遍历所有边
        for u, v in edges_df.values:
            # 仅检查我们同时知道两个节点标签的边
            if u in label_map and v in label_map:
                total_edges_checked += 1
                if label_map[u] == label_map[v]:
                    same_label_edges += 1
        
        if total_edges_checked > 0:
            homophily_ratio = same_label_edges / total_edges_checked
            print(f"已检查的边 (两端均有标签): {total_edges_checked}")
            print(f"边同质性比率: {homophily_ratio:.4f}")
            
            print("\n  --- 冠军策略指南 ---")
            if homophily_ratio > 0.6:
                print("  -> 高同质性 (High Homophily)。这是'标准'图。")
                print("  -> 推荐策略: GATv2, GCNII, APPNP。")
            elif homophily_ratio < 0.3:
                print("  -> 低同质性 (Heterophily)。这是一个'陷阱'图!")
                print("  -> 推荐策略: H2GCN, Geom-GCN, GPR-GNN (解耦模型)。")
                print("  -> (警告: GCN/GAT 在此表现会很差!)")
            else:
                print("  -> 中等同质性 (Mild Homophily)。")
                print("  -> 推荐策略: GAT, APPNP, 或同时尝试两种策略。")
        else:
            print("  -> 无法计算同质性 (在已标记的节点之间没有找到边)。")
            print("  -> 这很罕见, 可能意味着训练/验证集非常稀疏。")

        print_sep("侦察完毕")

    except pd.errors.EmptyDataError as e:
        print(f"错误: {e}. 文件为空或格式错误。")
    except Exception as e:
        print(f"发生意外错误: {e}")

# --- 脚本入口 ---
if __name__ == "__main__":
    # 假设数据文件夹名为 "data"
    run_recon("Data")