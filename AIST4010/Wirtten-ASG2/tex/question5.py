import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import time
import copy
import os
from tqdm import tqdm
import numpy as np

# --- 1. Hyperparameters and Setup ---

# Set seed for reproducibility
torch.manual_seed(42)
np.random.seed(42)

# Training settings
EPOCHS = 10
BATCH_SIZE = 64
LEARNING_RATE = 1e-3

# IMPORTANT: Set this to the root directory where the 'FashionMNIST' folder is
# One level UP from the 'raw' folder
DATA_ROOT = r'C:\Users\31670\Desktop\Study-Material\AIST4010\Wirtten-ASG2\tex\data'

# --- 2. Helper Functions (Data, Training, Evaluation) ---

def get_data_loaders(batch_size, data_root):
    """
    Loads and prepares the Fashion-MNIST dataset.
    Assumes data is already downloaded at data_root.
    """
    # Normalize with the mean and std of Fashion-MNIST
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.2860,), (0.3530,)) 
        # Using pre-computed mean/std for FashionMNIST is slightly better
        # than (0.5,), (0.5,)
    ])

    # Check if path exists
    if not os.path.exists(os.path.join(data_root, "FashionMNIST")):
        print(f"Error: Data not found at {data_root}")
        print("Please ensure the 'FashionMNIST' folder is in that directory.")
        return None, None

    train_dataset = datasets.FashionMNIST(
        root=data_root,
        train=True,
        download=False, # Set to False as per prompt
        transform=transform
    )
    
    test_dataset = datasets.FashionMNIST(
        root=data_root,
        train=False,
        download=False, # Set to False as per prompt
        transform=transform
    )
    
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2
    )
    
    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2
    )
    
    return train_loader, test_loader

def train_epoch(model, device, train_loader, optimizer, criterion):
    """Trains the model for one epoch."""
    model.train()
    for data, target in train_loader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

def evaluate(model, device, test_loader, criterion):
    """Evaluates the model on the test dataset."""
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item() * data.size(0)
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            
    test_loss /= len(test_loader.dataset)
    accuracy = 100. * correct / len(test_loader.dataset)
    return test_loss, accuracy

def run_experiment(model_name, model_instance, device, train_loader, test_loader):
    """
    Runs a full training and evaluation experiment for a given model.
    """
    print("-" * 50)
    print(f"🚀 Starting Experiment: {model_name}")
    print("-" * 50)
    
    # Deep copy the model instance to avoid weight leakage between experiments
    model = copy.deepcopy(model_instance).to(device)
    
    # Setup optimizer and loss function
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss()
    
    best_acc = 0.0
    start_time = time.time()
    
    for epoch in range(1, EPOCHS + 1):
        # Use tqdm for a nice progress bar
        train_loader_tqdm = tqdm(train_loader, desc=f"Epoch {epoch}/{EPOCHS}", leave=False)
        train_epoch(model, device, train_loader_tqdm, optimizer, criterion)
        
        test_loss, test_acc = evaluate(model, device, test_loader, criterion)
        
        if test_acc > best_acc:
            best_acc = test_acc
            
        if epoch == 1 or epoch == EPOCHS:
            print(f"  Epoch: {epoch:2d} | Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.2f}%")

    end_time = time.time()
    print(f"✅ Finished Experiment: {model_name}")
    print(f"   Best Test Accuracy: {best_acc:.2f}%")
    print(f"   Total Time: {end_time - start_time:.2f}s")
    print("-" * 50 + "\n")
    
    return best_acc


# --- 3. Model Definitions ---

# Baseline: LeNet-5 style with ReLU and MaxPool
# Input: 1x28x28
class LeNet_Baseline(nn.Module):
    def __init__(self):
        super().__init__()
        # C1: 1x28x28 -> 6x28x28 (k=5, p=2)
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2)
        # S2: 6x28x28 -> 6x14x14
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        # C3: 6x14x14 -> 16x10x10 (k=5, p=0)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        # S4: 16x10x10 -> 16x5x5
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        # Flatten: 16*5*5 = 400
        # F5: 400 -> 120
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        # F6: 120 -> 84
        self.fc2 = nn.Linear(120, 84)
        # F7: 84 -> 10
        self.fc3 = nn.Linear(84, 10)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5) # Flatten
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x) # No activation on output layer
        return x

# a. Add or remove CONV layers
class LeNet_A1_RemoveConv(nn.Module):
    def __init__(self):
        super().__init__()
        # Only one CONV layer
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2) # 6x28x28
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)    # 6x14x14
        # Flatten: 6*14*14 = 1176
        self.fc1 = nn.Linear(6 * 14 * 14, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = x.view(-1, 6 * 14 * 14) # Flatten
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

class LeNet_A2_AddConv(nn.Module):
    def __init__(self):
        super().__init__()
        # Baseline layers
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2) # 6x28x28
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)    # 6x14x14
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)          # 16x10x10
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)    # 16x5x5
        # Added layer
        self.conv3 = nn.Conv2d(16, 32, kernel_size=3, padding=1) # 32x5x5
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)     # 32x2x2 (5//2=2)
        # Flatten: 32*2*2 = 128
        self.fc1 = nn.Linear(32 * 2 * 2, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = self.pool3(self.activation(self.conv3(x))) # Added block
        x = x.view(-1, 32 * 2 * 2) # Flatten
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

# b. Add or remove FC layers
class LeNet_B1_RemoveFC(LeNet_Baseline): # Inherit baseline conv part
    def __init__(self):
        super().__init__()
        # Redefine FC layers
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        # self.fc2 is removed
        self.fc3 = nn.Linear(120, 10) # Connect fc1 directly to output

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = self.activation(self.fc1(x))
        # fc2 is skipped
        x = self.fc3(x)
        return x

class LeNet_B2_AddFC(LeNet_Baseline): # Inherit baseline
    def __init__(self):
        super().__init__()
        # Redefine FC layers
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc_added = nn.Linear(84, 42) # Added layer
        self.fc3 = nn.Linear(42, 10) # Output layer

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc_added(x)) # Added layer
        x = self.fc3(x)
        return x

# c. Add Dropout
class LeNet_C_Dropout(LeNet_Baseline):
    def __init__(self, p=0.5):
        super().__init__()
        self.dropout1 = nn.Dropout(p)
        self.dropout2 = nn.Dropout(p)

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = self.activation(self.fc1(x))
        x = self.dropout1(x) # Dropout after fc1
        x = self.activation(self.fc2(x))
        x = self.dropout2(x) # Dropout after fc2
        x = self.fc3(x)
        return x

# d. Adjust Pooling
class LeNet_D_AvgPool(LeNet_Baseline):
    def __init__(self):
        super().__init__()
        # Replace MaxPool with AvgPool
        self.pool1 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.pool2 = nn.AvgPool2d(kernel_size=2, stride=2)
        
class LeNet_D_LargePool(LeNet_Baseline):
    def __init__(self):
        super().__init__()
        # Replace 2x2 pool with 3x3 overlapping pool
        # 28x28 -> k=3,s=2,p=1 -> 14x14
        # 10x10 -> k=3,s=2,p=1 -> 5x5
        # Output size is the same! 16*5*5 = 400
        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

# e. Adjust convolution window size
class LeNet_E_SmallConv(nn.Module):
    def __init__(self):
        super().__init__()
        # C1: 1x28x28 -> 6x28x28 (k=3, p=1)
        self.conv1 = nn.Conv2d(1, 6, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2) # 6x14x14
        # C3: 6x14x14 -> 16x14x14 (k=3, p=1)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2) # 16x7x7
        # Flatten: 16*7*7 = 784
        self.fc1 = nn.Linear(16 * 7 * 7, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 7 * 7) # Flatten
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x
        
class LeNet_E_LargeConv(LeNet_Baseline):
    def __init__(self):
        super().__init__()
        # C1: 1x28x28 -> 6x28x28 (k=7, p=3)
        self.conv1 = nn.Conv2d(1, 6, kernel_size=7, padding=3)
        # S2: 6x28x28 -> 6x14x14
        # C3: 6x14x14 -> 16x10x10 (k=5, p=0)
        # S4: 16x10x10 -> 16x5x5
        # Output size is the same! 16*5*5 = 400

# f. Adjust number of output channels
class LeNet_F_Narrow(nn.Module):
    def __init__(self):
        super().__init__()
        # C1: 1x28x28 -> 4x28x28
        self.conv1 = nn.Conv2d(1, 4, kernel_size=5, padding=2)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2) # 4x14x14
        # C3: 4x14x14 -> 8x10x10
        self.conv2 = nn.Conv2d(4, 8, kernel_size=5)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2) # 8x5x5
        # Flatten: 8*5*5 = 200
        self.fc1 = nn.Linear(8 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.activation = nn.ReLU()
        
    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 8 * 5 * 5) # Flatten
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

class LeNet_F_Wide(nn.Module):
    def __init__(self):
        super().__init__()
        # C1: 1x28x28 -> 12x28x28
        self.conv1 = nn.Conv2d(1, 12, kernel_size=5, padding=2)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2) # 12x14x14
        # C3: 12x14x14 -> 32x10x10
        self.conv2 = nn.Conv2d(12, 32, kernel_size=5)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2) # 32x5x5
        # Flatten: 32*5*5 = 800
        self.fc1 = nn.Linear(32 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.activation = nn.ReLU()
        
    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 32 * 5 * 5) # Flatten
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x
        
# g. Use a different activation function
class LeNet_G_Tanh(LeNet_Baseline):
    def __init__(self):
        super().__init__()
        self.activation = nn.Tanh() # Use Tanh

class LeNet_G_Sigmoid(LeNet_Baseline):
    def __init__(self):
        super().__init__()
        self.activation = nn.Sigmoid() # Use Sigmoid

# --- 4. Main Execution ---

if __name__ == "__main__":
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}\n")
    
    train_loader, test_loader = get_data_loaders(BATCH_SIZE, DATA_ROOT)
    
    if train_loader is None:
        exit() # Stop if data wasn't found

    # Dictionary to store all results
    results = {}

    # --- Run Baseline ---
    baseline_model = LeNet_Baseline()
    results["Baseline (ReLU, MaxPool)"] = run_experiment(
        "Baseline (ReLU, MaxPool)", 
        baseline_model, device, train_loader, test_loader
    )

    # --- Experiment (a) CONV Layers ---
    results["a1. Remove CONV (1 total)"] = run_experiment(
        "a1. Remove CONV (1 total)",
        LeNet_A1_RemoveConv(), device, train_loader, test_loader
    )
    results["a2. Add CONV (3 total)"] = run_experiment(
        "a2. Add CONV (3 total)",
        LeNet_A2_AddConv(), device, train_loader, test_loader
    )

    # --- Experiment (b) FC Layers ---
    results["b1. Remove FC (2 total)"] = run_experiment(
        "b1. Remove FC (2 total)",
        LeNet_B1_RemoveFC(), device, train_loader, test_loader
    )
    results["b2. Add FC (4 total)"] = run_experiment(
        "b2. Add FC (4 total)",
        LeNet_B2_AddFC(), device, train_loader, test_loader
    )

    # --- Experiment (c) Dropout ---
    results["c1. Dropout (p=0.25)"] = run_experiment(
        "c1. Dropout (p=0.25)",
        LeNet_C_Dropout(p=0.25), device, train_loader, test_loader
    )
    results["c2. Dropout (p=0.5)"] = run_experiment(
        "c2. Dropout (p=0.5)",
        LeNet_C_Dropout(p=0.5), device, train_loader, test_loader
    )

    # --- Experiment (d) Pooling ---
    results["d1. AvgPool (k=2)"] = run_experiment(
        "d1. AvgPool (k=2)",
        LeNet_D_AvgPool(), device, train_loader, test_loader
    )
    results["d2. MaxPool (k=3, overlap)"] = run_experiment(
        "d2. MaxPool (k=3, overlap)",
        LeNet_D_LargePool(), device, train_loader, test_loader
    )

    # --- Experiment (e) CONV Window Size ---
    results["e1. Small CONV (k=3)"] = run_experiment(
        "e1. Small CONV (k=3)",
        LeNet_E_SmallConv(), device, train_loader, test_loader
    )
    results["e2. Large CONV (k=7)"] = run_experiment(
        "e2. Large CONV (k=7)",
        LeNet_E_LargeConv(), device, train_loader, test_loader
    )
    
    # --- Experiment (f) Output Channels ---
    results["f1. Narrow (4/8 channels)"] = run_experiment(
        "f1. Narrow (4/8 channels)",
        LeNet_F_Narrow(), device, train_loader, test_loader
    )
    results["f2. Wide (12/32 channels)"] = run_experiment(
        "f2. Wide (12/32 channels)",
        LeNet_F_Wide(), device, train_loader, test_loader
    )
    
    # --- Experiment (g) Activation Function ---
    results["g1. Tanh Activation"] = run_experiment(
        "g1. Tanh Activation",
        LeNet_G_Tanh(), device, train_loader, test_loader
    )
    results["g2. Sigmoid Activation"] = run_experiment(
        "g2. Sigmoid Activation",
        LeNet_G_Sigmoid(), device, train_loader, test_loader
    )

    # --- 5. Final Report ---
    print("\n" + "=" * 50)
    print("🏆 FINAL EXPERIMENT RESULTS 🏆")
    print("=" * 50)
    
    # Find the best result
    best_setting = ""
    best_acc = 0.0
    
    for setting, acc in results.items():
        print(f"  {setting:<30} | Best Test Accuracy: {acc:.2f}%")
        if acc > best_acc:
            best_acc = acc
            best_setting = setting
            
    print("-" * 50)
    print(f"🥇 Best Result: {best_setting}")
    print(f"🥇 Best Accuracy: {best_acc:.2f}%")
    print("=" * 50)