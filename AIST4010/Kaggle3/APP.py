import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch_geometric.data import Data
from torch_geometric.nn import APPNP # 导入 APPNP
from torch_geometric.utils import to_undirected
import torch_geometric.transforms as T
from pathlib import Path
from collections import Counter
import sys

# --- 1. 超参数和配置 (APPNP) ---
CONFIG = {
    "data_dir": "Data",
    "hidden_dim": 64,      # MLP 隐藏层维度
    "propagation_K": 10,   # 传播步数 K
    "propagation_alpha": 0.1, # 传送概率 alpha (Cora的标准值)
    "learning_rate": 0.01,   # APPNP 通常使用稍高的学习率
    "weight_decay": 5e-4,  # L2 正则化 (仍然至关重要!)
    "dropout": 0.5,        # Dropout
    "epochs": 300,         # 最大训练轮数
    "patience": 30,        # 早停的耐心值
    "best_model_path": "best_appnp_model.pt" # 保存为不同的模型
}

def load_data(data_dir):
    """
    加载所有数据, 执行SOTA预处理, 并构建PyTorch Geometric的Data对象。
    (与 GATv2 脚本中的函数相同)
    """
    print("--- 1. 正在加载和预处理数据... ---")
    base_path = Path(data_dir)

    # --- 加载特征 ---
    features_df = pd.read_csv(base_path / 'features.txt', sep='\s+', header=None)
    node_ids_raw = features_df.iloc[:, 0].values
    
    # SOTA 技巧: 对稀疏BoW特征进行行归一化 (Row-normalization)
    features = features_df.iloc[:, 1:].values
    features_normalized = F.normalize(torch.FloatTensor(features), p=1, dim=1)
    
    N = features_normalized.shape[0]
    D = features_normalized.shape[1]
    print(f"节点数: {N}, 特征维度: {D}")

    # --- 节点ID映射 ---
    node_map = {node_id: i for i, node_id in enumerate(node_ids_raw)}

    # --- 加载边 ---
    edges_df = pd.read_csv(base_path / 'edges.txt', sep='\s+', header=None)
    src = edges_df.iloc[:, 0].map(node_map).values
    dst = edges_df.iloc[:, 1].map(node_map).values
    edge_index = torch.LongTensor(np.vstack([src, dst]))

    # SOTA 技巧: 将有向图转换为无向图
    edge_index = to_undirected(edge_index)

    # --- 加载标签 ---
    train_df = pd.read_csv(base_path / 'train_labels.csv')
    val_df = pd.read_csv(base_path / 'val_labels.csv')
    test_df = pd.read_csv(base_path / 'test_idx.csv')

    all_labels = sorted(train_df['label'].unique())
    label_map = {label: i for i, label in enumerate(all_labels)}
    num_classes = len(all_labels)
    print(f"类别数: {num_classes} (映射: {label_map})")

    y = torch.full((N,), -1, dtype=torch.long)
    train_mask = torch.zeros(N, dtype=torch.bool)
    val_mask = torch.zeros(N, dtype=torch.bool)
    test_mask = torch.zeros(N, dtype=torch.bool)

    train_indices = train_df['id'].map(node_map).values
    train_labels = train_df['label'].map(label_map).values
    y[train_indices] = torch.LongTensor(train_labels)
    train_mask[train_indices] = True

    val_indices = val_df['id'].map(node_map).values
    val_labels = val_df['label'].map(label_map).values
    y[val_indices] = torch.LongTensor(val_labels)
    val_mask[val_indices] = True

    test_indices = test_df['id'].map(node_map).values
    test_mask[test_indices] = True
    
    # --- SOTA 技巧: 计算加权损失 (解决标签不平衡) ---
    label_counts = Counter(train_labels)
    counts = torch.FloatTensor([label_counts.get(i, 1) for i in range(num_classes)])
    weights = 1.0 / counts
    weights = weights / weights.sum()
    print(f"损失权重 (解决不平衡): {weights.numpy()}")

    # --- 构建 PyG Data 对象 ---
    data = Data(x=features_normalized, edge_index=edge_index, y=y)
    data.train_mask = train_mask
    data.val_mask = val_mask
    data.test_mask = test_mask

    # SOTA 技巧: 添加自环
    # APPNP 的传播明确需要自环 (GCNConv/GATConv 会自动添加)
    data = T.AddSelfLoops()(data)
    
    print("--- 数据加载完毕 ---")
    return data, num_classes, weights, node_map

class APPNPNet(nn.Module):
    """
    SOTA 模型: APPNP (解耦的GNN)
    它包含一个MLP特征提取器 和 一个固定的图传播层
    """
    def __init__(self, in_channels, hidden_channels, out_channels, dropout, K, alpha):
        super().__init__()
        self.dropout = dropout
        
        # 1. 特征提取器 (MLP)
        self.lin1 = nn.Linear(in_channels, hidden_channels)
        self.lin2 = nn.Linear(hidden_channels, out_channels)
        
        # 2. 传播层
        # cached=True 表示它会预先计算传播矩阵, 速度非常快
        self.prop = APPNP(K=K, alpha=alpha, cached=True)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        # 1. 通过MLP运行特征
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.relu(self.lin1(x))
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.lin2(x) # 得到初始的logits
        
        # 2. 传播 logits
        # 注意: APPNP 传播的是 MLP 的输出 (logits), 而不是中间层的嵌入
        x = self.prop(x, edge_index)
        
        # 3. LogSoftmax (与 NLLLoss 配合)
        return F.log_softmax(x, dim=1)

def train(model, data, criterion, optimizer):
    model.train()
    optimizer.zero_grad()
    out = model(data)
    # 仅在训练集上计算损失
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()

@torch.no_grad()
def test(model, data):
    model.eval()
    out = model(data)
    pred = out.argmax(dim=1)
    
    accs = {}
    for mask_name in ['train', 'val']:
        mask = data[f"{mask_name}_mask"]
        correct = (pred[mask] == data.y[mask]).sum()
        acc = int(correct) / int(mask.sum())
        accs[mask_name] = acc
        
    return accs

def main():
    # --- 1. 加载数据 ---
    data, num_classes, loss_weights, node_map = load_data(CONFIG['data_dir'])
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n--- 2. 运行在 {device} 设备上 ---")

    data = data.to(device)
    loss_weights = loss_weights.to(device)

    # --- 2. 初始化模型, 损失和优化器 ---
    model = APPNPNet(
        in_channels=data.num_node_features,
        hidden_channels=CONFIG['hidden_dim'],
        out_channels=num_classes,
        dropout=CONFIG['dropout'],
        K=CONFIG['propagation_K'],
        alpha=CONFIG['propagation_alpha']
    ).to(device)

    # SOTA 技巧: 使用加权 NLLLoss
    criterion = nn.NLLLoss(weight=loss_weights)
    
    # SOTA 技巧: Adam + 关键的 Weight Decay
    # 注意: APPNP 的论文建议只对MLP层进行 L2 正则化
    # (但为简单起见, 我们对所有参数应用, 效果依然很好)
    optimizer = optim.Adam(model.parameters(), 
                           lr=CONFIG['learning_rate'], 
                           weight_decay=CONFIG['weight_decay'])

    print("\n--- 3. 开始训练 (带早停) ---")
    best_val_acc = 0.0
    patience_counter = 0

    for epoch in range(1, CONFIG['epochs'] + 1):
        loss = train(model, data, criterion, optimizer)
        accs = test(model, data)
        
        print(f'Epoch: {epoch:03d} | Loss: {loss:.4f} | '
              f'Train Acc: {accs["train"]:.4f} | Val Acc: {accs["val"]:.4f}')

        # SOTA 技巧: 早停 (Early Stopping)
        if accs['val'] > best_val_acc:
            best_val_acc = accs['val']
            patience_counter = 0
            # 保存最好的模型
            torch.save(model.state_dict(), CONFIG['best_model_path'])
            print(f"  -> 新的最佳验证集准确率: {best_val_acc:.4f}. 模型已保存。")
        else:
            patience_counter += 1

        if patience_counter >= CONFIG['patience']:
            print(f"\n--- 验证集准确率在 {CONFIG['patience']} 轮内未提升, 触发早停 ---")
            break

    print("\n--- 4. 训练结束 ---")
    print(f"最佳验证集准确率: {best_val_acc:.4f}")

    # --- 5. 生成提交文件 ---
    print("\n--- 5. 加载最佳模型并生成提交文件 ---")
    
    # 加载最佳模型
    model.load_state_dict(torch.load(CONFIG['best_model_path']))
    model.eval()

    with torch.no_grad():
        final_out = model(data)
    
    # 获取 test_df 中ID对应的 tensor 索引
    test_df = pd.read_csv(Path(CONFIG['data_dir']) / 'test_idx.csv')
    test_indices_mapped = torch.LongTensor(test_df['id'].map(node_map).values)
    
    # 从这些索引中获取预测
    test_predictions_for_df = final_out[test_indices_mapped.to(device)].argmax(dim=1).cpu().numpy()
    
    # 将预测 (0-6) 转换回原始标签 ('Class_0', ...)
    # (我们从数据加载中重新获取映射)
    train_df = pd.read_csv(Path(CONFIG['data_dir']) / 'train_labels.csv')
    all_labels = sorted(train_df['label'].unique())
    label_map = {label: i for i, label in enumerate(all_labels)}
    int_to_label_map = {i: label for label, i in label_map.items()}

    test_labels_str_final = [int_to_label_map[pred] for pred in test_predictions_for_df]
    
    submission_df = pd.DataFrame({
        'id': test_df['id'],
        'label': test_labels_str_final
    })
    
    # 注意: 这个脚本也会覆盖 'submission.csv'
    # 你可能想把 GATv2 的提交保存为 'submission_gat.csv'
    # 或者把这个保存为 'submission_appnp.csv'
    submission_path = 'submission.csv'
    submission_df.to_csv(submission_path, index=False)
    print(f"提交文件已保存到: {submission_path}")
    print("--- 任务完成 ---")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"\n错误: 找不到文件 {e.filename}.")
        print("请确保 'Data' 文件夹在同一目录下, 并且包含所有 .txt 和 .csv 文件。")
    except ImportError as e:
        print(f"\n错误: 缺少库 {e.name}.")
        print("请使用 pip install torch torch_geometric pandas 安装所需库。")
    except Exception as e:
        print(f"\n发生意外错误: {e}")