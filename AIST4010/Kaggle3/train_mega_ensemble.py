import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, SAGEConv, GINConv, TransformerConv
from torch_geometric.nn import global_mean_pool, LayerNorm, BatchNorm
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

# 加载数据
def load_data():
    print("1. 加载特征...")
    # 加载特征 - 第一列是节点ID，其余是特征
    features = pd.read_csv('features.txt', sep=' ', header=None)
    node_ids = features.iloc[:, 0].astype(str).values
    feature_matrix = features.iloc[:, 1:].values.astype(float)
    node_features = torch.FloatTensor(feature_matrix)
    
    # 创建节点ID到索引的映射
    node_mapping = {node_id: idx for idx, node_id in enumerate(node_ids)}
    num_nodes = len(node_ids)
    print(f"   节点数: {num_nodes}, 特征维度: {feature_matrix.shape[1]}")
    
    print("2. 加载边...")
    # 加载边并映射到索引
    edges = pd.read_csv('edges.txt', sep='\t', header=None, names=['source', 'target'])
    edges['source'] = edges['source'].astype(str)
    edges['target'] = edges['target'].astype(str)
    
    edge_list = []
    for _, row in edges.iterrows():
        src, tgt = row['source'], row['target']
        if src in node_mapping and tgt in node_mapping:
            edge_list.append([node_mapping[src], node_mapping[tgt]])
            edge_list.append([node_mapping[tgt], node_mapping[src]])  # 无向图
    
    edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
    print(f"   边数: {edge_index.shape[1]}")
    
    print("3. 加载标签...")
    # 加载训练标签
    train_df = pd.read_csv('train_labels.csv')
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_labels = torch.full((num_nodes,), -1, dtype=torch.long)
    
    for _, row in train_df.iterrows():
        node_id = str(int(float(row['id'])))
        if node_id in node_mapping:
            idx = node_mapping[node_id]
            label = int(row['label'].split('_')[1])
            train_mask[idx] = True
            train_labels[idx] = label
    
    # 加载验证标签
    val_df = pd.read_csv('val_labels.csv')
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_labels = torch.full((num_nodes,), -1, dtype=torch.long)
    
    for _, row in val_df.iterrows():
        node_id = str(int(float(row['id'])))
        if node_id in node_mapping:
            idx = node_mapping[node_id]
            label = int(row['label'].split('_')[1])
            val_mask[idx] = True
            val_labels[idx] = label
    
    # 加载测试节点
    test_df = pd.read_csv('test_idx.csv')
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_node_ids = []
    
    for idx_val in test_df['id'].values:
        node_id = str(int(float(idx_val)))
        if node_id in node_mapping:
            idx = node_mapping[node_id]
            test_mask[idx] = True
            test_node_ids.append(node_id)
    
    print(f"   训练样本: {train_mask.sum()}, 验证样本: {val_mask.sum()}, 测试样本: {test_mask.sum()}")
    
    return node_features, edge_index, train_mask, train_labels, val_mask, val_labels, test_mask, node_mapping, test_node_ids


# 1. 增强的GCN模型（带残差连接）
class ResGCN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=4, dropout=0.5):
        super().__init__()
        self.convs = nn.ModuleList()
        self.bns = nn.ModuleList()
        
        self.convs.append(GCNConv(in_channels, hidden_channels))
        self.bns.append(BatchNorm(hidden_channels))
        
        for _ in range(num_layers - 2):
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
            self.bns.append(BatchNorm(hidden_channels))
        
        self.convs.append(GCNConv(hidden_channels, out_channels))
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        for i, conv in enumerate(self.convs[:-1]):
            x_new = conv(x, edge_index)
            x_new = self.bns[i](x_new)
            x_new = F.relu(x_new)
            x_new = F.dropout(x_new, p=self.dropout, training=self.training)
            if i > 0:  # 残差连接
                x = x + x_new
            else:
                x = x_new
        x = self.convs[-1](x, edge_index)
        return F.log_softmax(x, dim=1)


# 2. 多头GAT模型
class MultiHeadGAT(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, heads=8, dropout=0.6):
        super().__init__()
        self.conv1 = GATConv(in_channels, hidden_channels, heads=heads, dropout=dropout)
        self.conv2 = GATConv(hidden_channels * heads, hidden_channels, heads=heads, dropout=dropout)
        self.conv3 = GATConv(hidden_channels * heads, out_channels, heads=1, concat=False, dropout=dropout)
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.elu(self.conv2(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.conv3(x, edge_index)
        return F.log_softmax(x, dim=1)


# 3. GraphSAGE with Mean Pooling
class DeepSAGE(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=3, dropout=0.5):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(SAGEConv(in_channels, hidden_channels))
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden_channels, hidden_channels))
        self.convs.append(SAGEConv(hidden_channels, out_channels))
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.convs[-1](x, edge_index)
        return F.log_softmax(x, dim=1)


# 4. GIN (Graph Isomorphism Network)
class DeepGIN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=3, dropout=0.5):
        super().__init__()
        self.convs = nn.ModuleList()
        
        nn1 = nn.Sequential(
            nn.Linear(in_channels, hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, hidden_channels)
        )
        self.convs.append(GINConv(nn1))
        
        for _ in range(num_layers - 2):
            nn_temp = nn.Sequential(
                nn.Linear(hidden_channels, hidden_channels),
                nn.ReLU(),
                nn.Linear(hidden_channels, hidden_channels)
            )
            self.convs.append(GINConv(nn_temp))
        
        nn_final = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, out_channels)
        )
        self.convs.append(GINConv(nn_final))
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = conv(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.convs[-1](x, edge_index)
        return F.log_softmax(x, dim=1)


# 5. Transformer-based GNN
class GraphTransformer(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, heads=4, dropout=0.5):
        super().__init__()
        self.conv1 = TransformerConv(in_channels, hidden_channels, heads=heads, dropout=dropout)
        self.conv2 = TransformerConv(hidden_channels * heads, hidden_channels, heads=heads, dropout=dropout)
        self.conv3 = TransformerConv(hidden_channels * heads, out_channels, heads=1, concat=False, dropout=dropout)
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.conv3(x, edge_index)
        return F.log_softmax(x, dim=1)


# 6. 混合模型：GCN + GAT
class HybridGNN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, dropout=0.5):
        super().__init__()
        self.gcn1 = GCNConv(in_channels, hidden_channels)
        self.gat1 = GATConv(hidden_channels, hidden_channels, heads=4)
        self.gcn2 = GCNConv(hidden_channels * 4, hidden_channels)
        self.gat2 = GATConv(hidden_channels, out_channels, heads=1, concat=False)
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        x = F.relu(self.gcn1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.relu(self.gat1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.relu(self.gcn2(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.gat2(x, edge_index)
        return F.log_softmax(x, dim=1)


# 7. JK-Net (Jumping Knowledge Network)
class JKNet(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=4, dropout=0.5):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(GCNConv(in_channels, hidden_channels))
        for _ in range(num_layers - 1):
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
        
        # Jumping Knowledge: 连接所有层的输出
        self.lin = nn.Linear(hidden_channels * num_layers, out_channels)
        self.dropout = dropout
    
    def forward(self, x, edge_index):
        xs = []
        for conv in self.convs:
            x = F.relu(conv(x, edge_index))
            x = F.dropout(x, p=self.dropout, training=self.training)
            xs.append(x)
        
        x = torch.cat(xs, dim=-1)
        x = self.lin(x)
        return F.log_softmax(x, dim=1)


# 训练函数
def train(model, x, edge_index, train_mask, labels, optimizer):
    model.train()
    optimizer.zero_grad()
    out = model(x, edge_index)
    loss = F.nll_loss(out[train_mask], labels[train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()


# 评估函数
def evaluate(model, x, edge_index, mask, labels):
    model.eval()
    with torch.no_grad():
        out = model(x, edge_index)
        pred = out[mask].max(1)[1]
        acc = accuracy_score(labels[mask].cpu(), pred.cpu())
    return acc


# 主训练流程
# 主训练流程
def main():
    print("加载数据...")
    x, edge_index, train_mask, train_labels, val_mask, val_labels, test_mask, node_mapping, test_node_ids = load_data()
    
    # 使用CUDA加速
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    x = x.to(device)
    edge_index = edge_index.to(device)
    train_mask = train_mask.to(device)
    train_labels = train_labels.to(device)
    val_mask = val_mask.to(device)
    val_labels = val_labels.to(device)
    test_mask = test_mask.to(device)
    
    in_channels = x.size(1)
    out_channels = 7
    
    # 定义所有模型
    models_config = [
        ("ResGCN", ResGCN(in_channels, 128, out_channels, num_layers=4, dropout=0.5)),
        ("MultiHeadGAT", MultiHeadGAT(in_channels, 64, out_channels, heads=8, dropout=0.6)),
        ("DeepSAGE", DeepSAGE(in_channels, 128, out_channels, num_layers=4, dropout=0.5)),
        ("DeepGIN", DeepGIN(in_channels, 128, out_channels, num_layers=3, dropout=0.5)),
        ("GraphTransformer", GraphTransformer(in_channels, 64, out_channels, heads=4, dropout=0.5)),
        ("HybridGNN", HybridGNN(in_channels, 128, out_channels, dropout=0.5)),
        ("JKNet", JKNet(in_channels, 128, out_channels, num_layers=4, dropout=0.5)),
    ]
    
    trained_models = []
    model_weights = []
    
    for model_name, model in models_config:
        print(f"\n{'='*50}")
        print(f"训练模型: {model_name}")
        print(f"{'='*50}")
        
        model = model.to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
        
        best_val_acc = 0
        best_state = None
        
        for epoch in range(1, 1001):
            loss = train(model, x, edge_index, train_mask, train_labels, optimizer)
            train_acc = evaluate(model, x, edge_index, train_mask, train_labels)
            val_acc = evaluate(model, x, edge_index, val_mask, val_labels)
            
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                # 保存最佳模型状态
                best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            
            if epoch % 50 == 0:
                print(f'Epoch: {epoch:04d}, Loss: {loss:.4f}, Train: {train_acc:.4f}, Val: {val_acc:.4f}, Best Val: {best_val_acc:.4f}')
        
        # 加载最佳模型
        model.load_state_dict(best_state)
        model = model.to(device)
        
        print(f"{model_name} 最佳验证准确率: {best_val_acc:.4f}")
        
        # 为每个模型生成单独的提交文件
        model.eval()
        with torch.no_grad():
            out = model(x, edge_index)
            pred = out.max(1)[1].cpu().numpy()
        
        test_indices = torch.where(test_mask)[0].cpu().numpy()
        test_predictions = pred[test_indices]
        
        model_submission = pd.DataFrame({
            'id': test_node_ids,
            'label': [f'Class_{p}' for p in test_predictions]
        })
        
        submission_filename = f'{model_name.lower()}_submission.csv'
        model_submission.to_csv(submission_filename, index=False)
        print(f"   ✓ 已保存: {submission_filename}")
        
        trained_models.append((model_name, model))
        model_weights.append(best_val_acc)
    
    # 归一化权重
    total_weight = sum(model_weights)
    model_weights = [w / total_weight for w in model_weights]
    
    print(f"\n{'='*50}")
    print("集成模型权重:")
    for (name, _), weight in zip(trained_models, model_weights):
        print(f"{name}: {weight:.4f}")
    
    # 集成预测 - 加权平均
    print("\n生成加权集成预测...")
    all_preds_weighted = []
    
    for (model_name, model), weight in zip(trained_models, model_weights):
        model.eval()
        with torch.no_grad():
            out = model(x, edge_index)
            pred_probs = torch.exp(out)  # 转换log_softmax为概率
            all_preds_weighted.append(pred_probs.cpu().numpy() * weight)
    
    # 加权平均
    ensemble_probs_weighted = np.sum(all_preds_weighted, axis=0)
    ensemble_pred_weighted = np.argmax(ensemble_probs_weighted, axis=1)
    
    # 验证集上的加权集成准确率
    val_indices = val_mask.cpu().numpy()
    val_ensemble_acc_weighted = accuracy_score(val_labels.cpu().numpy()[val_indices], ensemble_pred_weighted[val_indices])
    print(f"加权集成验证准确率: {val_ensemble_acc_weighted:.4f}")
    
    # 生成加权集成提交文件
    test_indices = torch.where(test_mask)[0].cpu().numpy()
    test_predictions_weighted = ensemble_pred_weighted[test_indices]
    
    submission_weighted = pd.DataFrame({
        'id': test_node_ids,
        'label': [f'Class_{pred}' for pred in test_predictions_weighted]
    })
    
    submission_weighted.to_csv('weighted_ensemble_submission.csv', index=False)
    print("✓ 已保存: weighted_ensemble_submission.csv")
    
    # 投票集成 - 简单多数投票
    print("\n生成投票集成预测...")
    all_preds_vote = []
    
    for (model_name, model), weight in zip(trained_models, model_weights):
        model.eval()
        with torch.no_grad():
            out = model(x, edge_index)
            pred = out.max(1)[1].cpu().numpy()
            all_preds_vote.append(pred)
    
    # 多数投票
    all_preds_vote = np.array(all_preds_vote)  # shape: (n_models, n_nodes)
    ensemble_pred_vote = []
    
    for i in range(all_preds_vote.shape[1]):
        votes = all_preds_vote[:, i]
        # 统计每个类别的票数
        vote_counts = np.bincount(votes, minlength=7)
        ensemble_pred_vote.append(np.argmax(vote_counts))
    
    ensemble_pred_vote = np.array(ensemble_pred_vote)
    
    # 验证集上的投票集成准确率
    val_ensemble_acc_vote = accuracy_score(val_labels.cpu().numpy()[val_indices], ensemble_pred_vote[val_indices])
    print(f"投票集成验证准确率: {val_ensemble_acc_vote:.4f}")
    
    # 生成投票集成提交文件
    test_predictions_vote = ensemble_pred_vote[test_indices]
    
    submission_vote = pd.DataFrame({
        'id': test_node_ids,
        'label': [f'Class_{pred}' for pred in test_predictions_vote]
    })
    
    submission_vote.to_csv('voting_ensemble_submission.csv', index=False)
    print("✓ 已保存: voting_ensemble_submission.csv")
    
    # 选择最佳方法
    print(f"\n{'='*50}")
    print("集成方法对比:")
    print(f"加权集成: {val_ensemble_acc_weighted:.4f}")
    print(f"投票集成: {val_ensemble_acc_vote:.4f}")
    
    if val_ensemble_acc_weighted >= val_ensemble_acc_vote:
        best_method = "加权集成"
        best_submission = submission_weighted
        best_acc = val_ensemble_acc_weighted
        best_filename = 'weighted_ensemble_submission.csv'
    else:
        best_method = "投票集成"
        best_submission = submission_vote
        best_acc = val_ensemble_acc_vote
        best_filename = 'voting_ensemble_submission.csv'
    
    print(f"\n🏆 最佳方法: {best_method} (验证准确率: {best_acc:.4f})")
    
    # 保存最佳提交文件
    best_submission.to_csv('best_ensemble_submission.csv', index=False)
    print(f"✓ 最佳提交已保存: best_ensemble_submission.csv (来自 {best_filename})")
    
    print(f"\n{'='*50}")
    print("所有生成的提交文件:")
    print("单模型提交文件:")
    for (name, _), weight in zip(trained_models, model_weights):
        print(f"  - {name.lower()}_submission.csv (验证准确率: {weight * sum(model_weights):.4f})")
    print("\n集成提交文件:")
    print(f"  - weighted_ensemble_submission.csv (加权集成: {val_ensemble_acc_weighted:.4f})")
    print(f"  - voting_ensemble_submission.csv (投票集成: {val_ensemble_acc_vote:.4f})")
    print(f"  - best_ensemble_submission.csv (最佳方法: {best_acc:.4f}) ⭐")
    
    # 显示预测示例
    print("\n预测示例 (best_ensemble_submission.csv):")
    print(best_submission.head(10))


if __name__ == '__main__':
    main()
