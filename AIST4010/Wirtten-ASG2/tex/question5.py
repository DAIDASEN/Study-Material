import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# --- Model Definitions ---

# Baseline LeNet-5
class LeNet5(nn.Module):
    def __init__(self, activation_fn=nn.Sigmoid):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2) # 28x28 -> 32x32 -> 28x28
        self.pool1 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.pool2 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.activation = activation_fn()

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

# Experiment a: Add/Remove CONV layers
class LeNet_MoreConv(LeNet5):
    def __init__(self):
        super().__init__()
        self.conv_extra = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 5 * 5, 120) # Adjusted for new conv layer

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.activation(self.conv2(x))
        x = self.pool2(self.activation(self.conv_extra(x))) # Added layer
        x = x.view(-1, 32 * 5 * 5)
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

class LeNet_LessConv(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)
        self.pool1 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(16 * 14 * 14, 120) # Only one conv layer
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.activation = nn.Sigmoid()

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = x.view(-1, 16 * 14 * 14)
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

# Experiment b: Add/Remove FC layers
class LeNet_MoreFC(LeNet5):
    def __init__(self):
        super().__init__()
        self.fc_extra = nn.Linear(84, 42)
        self.fc3 = nn.Linear(42, 10)

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc_extra(x)) # Added layer
        x = self.fc3(x)
        return x

class LeNet_LessFC(LeNet5):
    def __init__(self):
        super().__init__()
        self.fc2 = nn.Linear(120, 10) # Removed one FC layer

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = self.activation(self.fc1(x))
        x = self.fc2(x) # Directly to output
        return x

# Experiment c: Add Dropout
class LeNet_Dropout(LeNet5):
    def __init__(self, dropout_rate=0.5):
        super().__init__()
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, x):
        x = self.pool1(self.activation(self.conv1(x)))
        x = self.pool2(self.activation(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = self.dropout(self.activation(self.fc1(x)))
        x = self.dropout(self.activation(self.fc2(x)))
        x = self.fc3(x)
        return x

# --- Training and Evaluation Function ---
def train_and_evaluate(model, train_loader, test_loader, model_name, epochs=3):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(
        model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-7
    )

    print(f"--- Training {model_name} ---")
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {running_loss / len(train_loader):.3f}")

    # Evaluation
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Accuracy of {model_name} on the test set: {accuracy:.2f} %")
    return accuracy

# --- Data Loading ---
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_set = torchvision.datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_set, batch_size=256, shuffle=True, num_workers=0)

test_set = torchvision.datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)
test_loader = DataLoader(test_set, batch_size=1000, shuffle=False, num_workers=0)


if __name__ == '__main__':
    # Ensure output dir exists (relative to tex folder)
    out_dir = os.path.join(os.path.dirname(__file__), 'generated')
    os.makedirs(out_dir, exist_ok=True)

    results = {}

    # As per clarification: implement two networks with different number of CONV layers (plus baseline)
    baseline_model = LeNet5()
    results['Baseline (Sigmoid, AvgPool)'] = train_and_evaluate(baseline_model, train_loader, test_loader, "Baseline", epochs=5)

    results['More CONV (extra 3x3)'] = train_and_evaluate(LeNet_MoreConv(), train_loader, test_loader, "More CONV", epochs=5)
    results['Less CONV (single conv)'] = train_and_evaluate(LeNet_LessConv(), train_loader, test_loader, "Less CONV", epochs=5)

    # --- Print Final Results ---
    print("\n--- All Experiment Results ---")
    for name, acc in results.items():
        print(f"{name}: {acc:.2f}%")

    best_model = max(results, key=results.get)
    print(f"\nBest performing model: {best_model} with accuracy {results[best_model]:.2f}%")

    # Save JSON
    json_path = os.path.join(out_dir, 'question5_results.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({"results": results, "best": {"name": best_model, "acc": results[best_model]}}, f, indent=2)

    # Write LaTeX table snippet
    table_path = os.path.join(out_dir, 'question5_results_table.tex')
    with open(table_path, 'w', encoding='utf-8') as f:
        f.write("% Auto-generated by question5.py\n")
        f.write("\\begin{tabular}{@{}llc@{}}\\toprule\n")
        f.write("Experiment & Setting & Test Acc (\\%) \\ \\midrule\n")
        for k, v in results.items():
            exp = 'Conv layers'
            f.write(f"{exp} & {k} & {v:.2f} \\ \n")
        f.write("\\midrule\n")
        f.write(f"\\multicolumn{{2}}{{l}}{{Best}} & {results[best_model]:.2f} \\ \\bottomrule\n")
        f.write("\\end{tabular}\n")
