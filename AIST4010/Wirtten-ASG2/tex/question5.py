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
def train_and_evaluate(model, train_loader, test_loader, model_name, epochs=10):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

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
train_loader = DataLoader(train_set, batch_size=64, shuffle=True)

test_set = torchvision.datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)
test_loader = DataLoader(test_set, batch_size=1000, shuffle=False)


if __name__ == '__main__':
    results = {}

    # Baseline
    baseline_model = LeNet5()
    results['Baseline (Sigmoid, AvgPool)'] = train_and_evaluate(baseline_model, train_loader, test_loader, "Baseline")

    # a. CONV layers
    results['More CONV'] = train_and_evaluate(LeNet_MoreConv(), train_loader, test_loader, "More CONV")
    results['Less CONV'] = train_and_evaluate(LeNet_LessConv(), train_loader, test_loader, "Less CONV")

    # b. FC layers
    results['More FC'] = train_and_evaluate(LeNet_MoreFC(), train_loader, test_loader, "More FC")
    results['Less FC'] = train_and_evaluate(LeNet_LessFC(), train_loader, test_loader, "Less FC")

    # c. Dropout
    results['Dropout (0.25)'] = train_and_evaluate(LeNet_Dropout(0.25), train_loader, test_loader, "Dropout (0.25)")
    results['Dropout (0.5)'] = train_and_evaluate(LeNet_Dropout(0.5), train_loader, test_loader, "Dropout (0.5)")

    # d. Pooling Layer
    lenet_maxpool = LeNet5()
    lenet_maxpool.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
    lenet_maxpool.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
    results['MaxPool'] = train_and_evaluate(lenet_maxpool, train_loader, test_loader, "MaxPool")

    lenet_pool_ks3 = LeNet5()
    lenet_pool_ks3.pool1 = nn.AvgPool2d(kernel_size=3, stride=2, padding=1) # Adjust to maintain size
    lenet_pool_ks3.pool2 = nn.AvgPool2d(kernel_size=3, stride=2, padding=1)
    results['AvgPool (Kernel=3)'] = train_and_evaluate(lenet_pool_ks3, train_loader, test_loader, "AvgPool (Kernel=3)")

    # e. Convolution window size
    lenet_conv_ks3 = LeNet5()
    lenet_conv_ks3.conv1 = nn.Conv2d(1, 6, kernel_size=3, padding=1)
    lenet_conv_ks3.conv2 = nn.Conv2d(6, 16, kernel_size=3)
    # Adjust fc1 input size due to different conv kernel
    # After conv1 (3x3, p=1): 28x28 -> 28x28. Pool: 14x14
    # After conv2 (3x3): 14x14 -> 12x12. Pool: 6x6
    lenet_conv_ks3.fc1 = nn.Linear(16 * 6 * 6, 120)
    results['Conv Kernel=3'] = train_and_evaluate(lenet_conv_ks3, train_loader, test_loader, "Conv Kernel=3")

    lenet_conv_ks7 = LeNet5()
    lenet_conv_ks7.conv1 = nn.Conv2d(1, 6, kernel_size=7, padding=3)
    lenet_conv_ks7.conv2 = nn.Conv2d(6, 16, kernel_size=7)
    # After conv1 (7x7, p=3): 28x28 -> 28x28. Pool: 14x14
    # After conv2 (7x7): 14x14 -> 8x8. Pool: 4x4
    lenet_conv_ks7.fc1 = nn.Linear(16 * 4 * 4, 120)
    results['Conv Kernel=7'] = train_and_evaluate(lenet_conv_ks7, train_loader, test_loader, "Conv Kernel=7")

    # f. Number of output channels
    lenet_ch_more = LeNet5()
    lenet_ch_more.conv1 = nn.Conv2d(1, 12, kernel_size=5, padding=2)
    lenet_ch_more.conv2 = nn.Conv2d(12, 32, kernel_size=5)
    lenet_ch_more.fc1 = nn.Linear(32 * 5 * 5, 120)
    results['More Channels (12, 32)'] = train_and_evaluate(lenet_ch_more, train_loader, test_loader, "More Channels")

    lenet_ch_less = LeNet5()
    lenet_ch_less.conv1 = nn.Conv2d(1, 4, kernel_size=5, padding=2)
    lenet_ch_less.conv2 = nn.Conv2d(4, 8, kernel_size=5)
    lenet_ch_less.fc1 = nn.Linear(8 * 5 * 5, 120)
    results['Less Channels (4, 8)'] = train_and_evaluate(lenet_ch_less, train_loader, test_loader, "Less Channels")

    # g. Activation function
    lenet_relu = LeNet5(activation_fn=nn.ReLU)
    results['ReLU Activation'] = train_and_evaluate(lenet_relu, train_loader, test_loader, "ReLU Activation")

    lenet_leaky_relu = LeNet5(activation_fn=nn.LeakyReLU)
    results['LeakyReLU Activation'] = train_and_evaluate(lenet_leaky_relu, train_loader, test_loader, "LeakyReLU Activation")

    # --- Print Final Results ---
    print("\n--- All Experiment Results ---")
    for name, acc in results.items():
        print(f"{name}: {acc:.2f}%")

    best_model = max(results, key=results.get)
    print(f"\nBest performing model: {best_model} with accuracy {results[best_model]:.2f}%")
