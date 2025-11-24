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

# --- 1. Hyperparameters & Config ---
CONFIG = {
    "data_dir": "Data",
    "hidden_dim": 8,       # GAT hidden dimension
    "heads": 8,            # GAT multi-head attention
    "learning_rate": 0.005,  # Learning rate (Cora prefers slightly higher LR)
    "weight_decay": 5e-4,  # L2 regularization (critical on Cora!)
    "dropout": 0.6,        # Dropout (high dropout helps avoid overfitting)
    "epochs": 300,         # Max training epochs
    "patience": 30,        # Early stopping patience
    "best_model_path": "best_gat_model.pt"
}

def load_data(data_dir):
    """
    Load all data, apply SOTA preprocessing, and build PyTorch Geometric Data object.
    """
    print("--- 1. Loading and preprocessing data... ---")
    base_path = Path(data_dir)

    # --- Load features ---
    features_df = pd.read_csv(base_path / 'features.txt', sep=r'\s+', header=None)
    node_ids_raw = features_df.iloc[:, 0].values

    # SOTA trick: row-normalization for sparse BoW features
    features = features_df.iloc[:, 1:].values
    features_normalized = F.normalize(torch.FloatTensor(features), p=1, dim=1)

    N = features_normalized.shape[0]
    D = features_normalized.shape[1]
    print(f"Number of nodes: {N}, Feature dimension: {D}")

    # --- Node ID mapping ---
    node_map = {node_id: i for i, node_id in enumerate(node_ids_raw)}

    # --- Load edges ---
    edges_df = pd.read_csv(base_path / 'edges.txt', sep=r'\s+', header=None)
    src = edges_df.iloc[:, 0].map(node_map).values
    dst = edges_df.iloc[:, 1].map(node_map).values
    edge_index = torch.LongTensor(np.vstack([src, dst]))

    # SOTA trick: convert directed graph to undirected
    edge_index = to_undirected(edge_index)

    # --- Load labels ---
    train_df = pd.read_csv(base_path / 'train_labels.csv')
    val_df = pd.read_csv(base_path / 'val_labels.csv')
    test_df = pd.read_csv(base_path / 'test_idx.csv')

    # Create label → integer (0–6)
    all_labels = sorted(train_df['label'].unique())
    label_map = {label: i for i, label in enumerate(all_labels)}
    num_classes = len(all_labels)
    print(f"Number of classes: {num_classes} (mapping: {label_map})")

    y = torch.full((N,), -1, dtype=torch.long)
    train_mask = torch.zeros(N, dtype=torch.bool)
    val_mask = torch.zeros(N, dtype=torch.bool)
    test_mask = torch.zeros(N, dtype=torch.bool)

    # Train set
    train_indices = train_df['id'].map(node_map).values
    train_labels = train_df['label'].map(label_map).values
    y[train_indices] = torch.LongTensor(train_labels)
    train_mask[train_indices] = True

    # Validation set
    val_indices = val_df['id'].map(node_map).values
    val_labels = val_df['label'].map(label_map).values
    y[val_indices] = torch.LongTensor(val_labels)
    val_mask[val_indices] = True

    # Test set
    test_indices = test_df['id'].map(node_map).values
    test_mask[test_indices] = True

    # --- SOTA trick: compute class-balanced loss weights ---
    label_counts = Counter(train_labels)
    counts = torch.FloatTensor([label_counts.get(i, 1) for i in range(num_classes)])
    weights = 1.0 / counts
    weights = weights / weights.sum()
    print(f"Loss weights (for class imbalance): {weights.numpy()}")

    # --- Build PyG Data object ---
    data = Data(x=features_normalized, edge_index=edge_index, y=y)
    data.train_mask = train_mask
    data.val_mask = val_mask
    data.test_mask = test_mask

    # Add self-loops (helps GAT)
    data = T.AddSelfLoops()(data)

    print("--- Data loading complete ---")
    return data, num_classes, weights, node_map, label_map

class GAT(nn.Module):
    """
    SOTA model: 2-layer GATv2
    """
    def __init__(self, in_channels, hidden_channels, out_channels, heads, dropout):
        super().__init__()
        self.dropout = dropout

        self.conv1 = GATv2Conv(in_channels, hidden_channels, heads=heads,
                               dropout=dropout, add_self_loops=False)

        self.conv2 = GATv2Conv(hidden_channels * heads, out_channels, heads=1,
                               concat=False, dropout=dropout, add_self_loops=False)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        # Input dropout
        x = F.dropout(x, p=self.dropout, training=self.training)

        # First GATv2 layer
        x = self.conv1(x, edge_index)
        x = F.elu(x)

        # Middle dropout
        x = F.dropout(x, p=self.dropout, training=self.training)

        # Second GATv2 layer
        x = self.conv2(x, edge_index)

        # LogSoftmax (for NLLLoss)
        return F.log_softmax(x, dim=1)

def train(model, data, criterion, optimizer):
    model.train()
    optimizer.zero_grad()
    out = model(data)
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
    # --- 1. Load data ---
    data, num_classes, loss_weights, node_map, label_map = load_data(CONFIG['data_dir'])
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n--- 2. Running on device: {device} ---")

    data = data.to(device)
    loss_weights = loss_weights.to(device)

    # --- Model, criterion, optimizer ---
    model = GAT(
        in_channels=data.num_node_features,
        hidden_channels=CONFIG['hidden_dim'],
        out_channels=num_classes,
        heads=CONFIG['heads'],
        dropout=CONFIG['dropout']
    ).to(device)

    criterion = nn.NLLLoss(weight=loss_weights)

    optimizer = optim.Adam(model.parameters(),
                           lr=CONFIG['learning_rate'],
                           weight_decay=CONFIG['weight_decay'])

    print("\n--- 3. Training with Early Stopping ---")
    best_val_acc = 0.0
    patience_counter = 0

    for epoch in range(1, CONFIG['epochs'] + 1):
        loss = train(model, data, criterion, optimizer)
        accs = test(model, data)

        print(f'Epoch: {epoch:03d} | Loss: {loss:.4f} | '
              f'Train Acc: {accs["train"]:.4f} | Val Acc: {accs["val"]:.4f}')

        if accs['val'] > best_val_acc:
            best_val_acc = accs['val']
            patience_counter = 0
            torch.save(model.state_dict(), CONFIG['best_model_path'])
            print(f"  -> New best validation accuracy: {best_val_acc:.4f}. Model saved.")
        else:
            patience_counter += 1

        if patience_counter >= CONFIG['patience']:
            print(f"\n--- Early Stopping triggered after {CONFIG['patience']} epochs without improvement ---")
            break

    print("\n--- 4. Training completed ---")
    print(f"Best validation accuracy: {best_val_acc:.4f}")

    # --- 5. Generate submission file ---
    print("\n--- 5. Loading best model and generating submission file ---")

    model.load_state_dict(torch.load(CONFIG['best_model_path']))
    model.eval()

    with torch.no_grad():
        final_out = model(data)
        final_pred = final_out.argmax(dim=1)

    # Get test predictions
    test_node_indices_tensor = torch.where(data.test_mask)[0]
    test_predictions_tensor = final_pred[data.test_mask]

    int_to_label_map = {i: label for label, i in label_map.items()}
    test_labels_str = [int_to_label_map[pred.item()] for pred in test_predictions_tensor]

    test_df = pd.read_csv(Path(CONFIG['data_dir']) / 'test_idx.csv')

    test_indices_mapped = torch.LongTensor(test_df['id'].map(node_map).values)
    test_predictions_for_df = final_pred[test_indices_mapped.to(device)].cpu().numpy()

    test_labels_str_final = [int_to_label_map[pred] for pred in test_predictions_for_df]

    submission_df = pd.DataFrame({
        'id': test_df['id'],
        'label': test_labels_str_final
    })

    submission_path = 'submission.csv'
    submission_df.to_csv(submission_path, index=False)
    print(f"Submission file saved to: {submission_path}")
    print("--- Task completed ---")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"\nError: File not found: {e.filename}.")
        print("Please ensure the 'Data' folder is in the same directory and contains all .txt and .csv files.")
    except ImportError as e:
        print(f"\nError: Missing library {e.name}.")
        print("Please install required libraries using: pip install torch torch_geometric pandas")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
