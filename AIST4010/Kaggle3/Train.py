import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch_geometric.data import Data
from torch_geometric.nn import GATv2Conv
from torch_geometric.utils import to_undirected
import torch_geometric.transforms as T
from pathlib import Path
from collections import Counter
import sys

# --- 1. 超参数和配置 (Hyperparameters & Config) ---
CONFIG = {
    "data_dir": "Data",
    "hidden_dim": 8,       # GAT 隐藏层维度
    "heads": 8,            # GAT 多头注意力
    "learning_rate": 0.005,  # 学习率 (Cora 喜欢稍高的学习率)
    "weight_decay": 5e-4,  # L2 正则化 (在Cora上至关重要!)
    "dropout": 0.6,        # Dropout (高 dropout 防止过拟合)
    "epochs": 300,         # 最大训练轮数
    "patience": 30,        # 早停的耐心值
    "best_model_path": "best_gat_model.pt"
}

def load_data(data_dir):
    """
    加载所有数据, 执行SOTA预处理, 并构建PyTorch Geometric的Data对象。
    """
    print("--- 1. 正在加载和预处理数据... ---")
    base_path = Path(data_dir)

    # --- 加载特征 ---
    # 使用 sep='\s+' 来处理空格/Tab, 避免 FutureWarning
    features_df = pd.read_csv(base_path / 'features.txt', sep=r'\s+', header=None)
    node_ids_raw = features_df.iloc[:, 0].values
    
    # SOTA 技巧: 对稀疏BoW特征进行行归一化 (Row-normalization)
    features = features_df.iloc[:, 1:].values
    features_normalized = F.normalize(torch.FloatTensor(features), p=1, dim=1)
    
    N = features_normalized.shape[0]
    D = features_normalized.shape[1]
    print(f"节点数: {N}, 特征维度: {D}")

    # --- 节点ID映射 ---
    # 创建一个从原始ID (str/int) 到 tensor索引 (0到N-1) 的映射
    node_map = {node_id: i for i, node_id in enumerate(node_ids_raw)}

    # --- 加载边 ---
    edges_df = pd.read_csv(base_path / 'edges.txt', sep=r'\s+', header=None)
    # 将原始ID映射到 (0到N-1) 的索引
    src = edges_df.iloc[:, 0].map(node_map).values
    dst = edges_df.iloc[:, 1].map(node_map).values
    edge_index = torch.LongTensor(np.vstack([src, dst]))

    # SOTA 技巧: 将有向图转换为无向图 (解决侦察到的"有向图"问题)
    edge_index = to_undirected(edge_index)

    # --- 加载标签 ---
    train_df = pd.read_csv(base_path / 'train_labels.csv')
    val_df = pd.read_csv(base_path / 'val_labels.csv')
    test_df = pd.read_csv(base_path / 'test_idx.csv')

    # 创建标签到整数 (0-6) 的映射
    all_labels = sorted(train_df['label'].unique())
    label_map = {label: i for i, label in enumerate(all_labels)}
    num_classes = len(all_labels)
    print(f"类别数: {num_classes} (映射: {label_map})")

    y = torch.full((N,), -1, dtype=torch.long) # -1 表示未知
    train_mask = torch.zeros(N, dtype=torch.bool)
    val_mask = torch.zeros(N, dtype=torch.bool)
    test_mask = torch.zeros(N, dtype=torch.bool)

    # 填充训练集
    train_indices = train_df['id'].map(node_map).values
    train_labels = train_df['label'].map(label_map).values
    y[train_indices] = torch.LongTensor(train_labels)
    train_mask[train_indices] = True

    # 填充验证集
    val_indices = val_df['id'].map(node_map).values
    val_labels = val_df['label'].map(label_map).values
    y[val_indices] = torch.LongTensor(val_labels)
    val_mask[val_indices] = True

    # 填充测试集
    test_indices = test_df['id'].map(node_map).values
    test_mask[test_indices] = True
    
    # --- SOTA 技巧: 计算加权损失 (解决标签不平衡) ---
    label_counts = Counter(train_labels)
    counts = torch.FloatTensor([label_counts.get(i, 1) for i in range(num_classes)]) # 避免除以0
    weights = 1.0 / counts
    weights = weights / weights.sum()
    print(f"损失权重 (解决不平衡): {weights.numpy()}")

    # --- 构建 PyG Data 对象 ---
    data = Data(x=features_normalized, edge_index=edge_index, y=y)
    data.train_mask = train_mask
    data.val_mask = val_mask
    data.test_mask = test_mask

    # SOTA 技巧: 添加自环 (GAT也从中受益)
    data = T.AddSelfLoops()(data)
    
    print("--- 数据加载完毕 ---")
    return data, num_classes, weights, node_map

class GAT(nn.Module):
    """
    SOTA 模型: 2层 GATv2
    """
    def __init__(self, in_channels, hidden_channels, out_channels, heads, dropout):
        super().__init__()
        self.dropout = dropout
        
        # GATv2Conv 通常比 GATConv 更具表现力
        self.conv1 = GATv2Conv(in_channels, hidden_channels, heads=heads, 
                             dropout=dropout, add_self_loops=False)
        
        # 注意: GATv2Conv 的输入维度是 hidden * heads
        self.conv2 = GATv2Conv(hidden_channels * heads, out_channels, heads=1, 
                             concat=False, dropout=dropout, add_self_loops=False)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        # 1. 输入 Dropout (GAT论文推荐)
        x = F.dropout(x, p=self.dropout, training=self.training)
        
        # 2. 第一个 GATv2 层
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        
        # 3. 中间 Dropout
        x = F.dropout(x, p=self.dropout, training=self.training)
        
        # 4. 第二个 (输出) GATv2 层
        x = self.conv2(x, edge_index)
        
        # 5. LogSoftmax (与 NLLLoss 配合)
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
    model = GAT(
        in_channels=data.num_node_features,
        hidden_channels=CONFIG['hidden_dim'],
        out_channels=num_classes,
        heads=CONFIG['heads'],
        dropout=CONFIG['dropout']
    ).to(device)

    # SOTA 技巧: 使用加权 NLLLoss
    criterion = nn.NLLLoss(weight=loss_weights)
    
    # SOTA 技巧: Adam + 关键的 Weight Decay
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
        final_pred = final_out.argmax(dim=1)
    
    # 获取测试集的预测
    test_node_indices_tensor = torch.where(data.test_mask)[0]
    test_predictions_tensor = final_pred[data.test_mask]

    # 将预测 (0-6) 转换回原始标签 ('Class_0', ...)
    int_to_label_map = {i: label for label, i in label_map.items()}
    test_labels_str = [int_to_label_map[pred.item()] for pred in test_predictions_tensor]
    
    # 获取原始测试ID
    test_df = pd.read_csv(Path(CONFIG['data_dir']) / 'test_idx.csv')
    test_ids = test_df['id'].values
    
    # 确保预测和ID对齐 (尽管在这里它们应该已经是)
    test_node_indices = data.test_mask.nonzero(as_tuple=True)[0].cpu().numpy()
    tensor_idx_to_original_id_map = {
        idx: original_id for original_id, idx in node_map.items() 
        if idx in test_node_indices
    }
    # 这步有点多余, 因为 test_df 里的顺序就是我们需要的顺序
    # 但我们还是基于 test_df 来构建
    
    # 获取 test_df 中ID对应的 tensor 索引
    test_indices_mapped = torch.LongTensor(test_df['id'].map(node_map).values)
    # 从这些索引中获取预测
    test_predictions_for_df = final_pred[test_indices_mapped.to(device)].cpu().numpy()
    
    test_labels_str_final = [int_to_label_map[pred] for pred in test_predictions_for_df]
    
    submission_df = pd.DataFrame({
        'id': test_df['id'],
        'label': test_labels_str_final
    })
    
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