# Question 4
# Import libraries
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import random
import matplotlib.pyplot as plt
import torch

## First, write your name and SID here!
name = "Your Name"
SID = "Your SID"

## a. Data Generation
"""Generation function"""
def generate_data(num_features=100, num_samples=1000):
    """
    please fix the seed before generating the data
    data: (num_samples, num_features) 2D np.array
    labels: (num_samples, ) 1D np.array
    """
    # Generate two classes
    # Class 0: centered around -1
    # Class 1: centered around +1
    
    # Generate class 0
    mean_0 = np.ones(num_features) * (-1)
    cov_0 = np.eye(num_features)
    data_0 = np.random.multivariate_normal(mean_0, cov_0, num_samples)
    labels_0 = np.zeros(num_samples)
    
    # Generate class 1
    mean_1 = np.ones(num_features) * 1
    cov_1 = np.eye(num_features)
    data_1 = np.random.multivariate_normal(mean_1, cov_1, num_samples)
    labels_1 = np.ones(num_samples)
    
    # Combine the data
    data = np.vstack([data_0, data_1])
    labels = np.hstack([labels_0, labels_1])
    
    # Shuffle the data
    indices = np.random.permutation(len(data))
    data = data[indices]
    labels = labels[indices]

    return data, labels

## 4.b Logistic Regression and GD
"""Notice that you may need to define additional function for LR and GD"""

def sigmoid(z):
    """Sigmoid activation function"""
    return 1 / (1 + np.exp(-z))

def compute_loss(X, y, W, b):
    """Compute binary cross-entropy loss"""
    m = len(y)
    z = np.dot(X, W) + b
    predictions = sigmoid(z)
    # Add small epsilon to prevent log(0)
    epsilon = 1e-15
    predictions = np.clip(predictions, epsilon, 1 - epsilon)
    loss = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
    return loss

def compute_gradients(X, y, W, b):
    """Compute gradients for W and b"""
    m = len(y)
    z = np.dot(X, W) + b
    predictions = sigmoid(z)
    
    dW = np.dot(X.T, (predictions - y)) / m
    db = np.mean(predictions - y)
    
    return dW, db

"""Training of GD"""
def train_gd(X_train, y_train, X_test, y_test, W, b, epochs, lr):
    # Train logistic regression using gradient descent
    # X_train: (num_samples, num_features) 2D np.array
    # y_train: (num_samples, ) 1D np.array
    # X_test: (num_samples, num_features) 2D np.array
    # y_test: (num_samples, ) 1D np.array
    # W: (num_features, ) 1D np.array
    # b: (1, ) 1D np.array
    # lr: learning rate set to be 0.001
    # epochs: number of epochs set to be 100

    # train_loss_history: (epochs, ) 1D np.array
    # test_loss_history: (epochs, ) 1D np.array

    train_loss_history = np.zeros(epochs)
    test_loss_history = np.zeros(epochs)
    
    for epoch in range(epochs):
        # Compute gradients using all training data
        dW, db = compute_gradients(X_train, y_train, W, b)
        
        # Update parameters
        W = W - lr * dW
        b = b - lr * db
        
        # Compute and record losses
        train_loss = compute_loss(X_train, y_train, W, b)
        test_loss = compute_loss(X_test, y_test, W, b)
        
        train_loss_history[epoch] = train_loss
        test_loss_history[epoch] = test_loss

    return train_loss_history, test_loss_history, W, b

"""calculate the test accuracy"""
def cal_accuracy(X, y, W, b):
    # Calculate the accuracy of logistic regression
    # X: (num_samples, num_features) 2D np.array
    # y: (num_samples, ) 1D np.array
    # W: (num_features, ) 1D np.array
    # b: (1, ) 1D np.array
    # accuracy: float
    z = np.dot(X, W) + b
    predictions = sigmoid(z)
    predicted_labels = (predictions >= 0.5).astype(int)
    accuracy = np.mean(predicted_labels == y)
    return accuracy

## 4.c SGD
"""Training function of SGD"""
def train_sgd(X_train, y_train, X_test, y_test, W, b, epochs, lr):
    # Train logistic regression using stochastic gradient descent
    # X_train: (num_samples, num_features) 2D np.array
    # y_train: (num_samples, ) 1D np.array
    # X_test: (num_samples, num_features) 2D np.array
    # y_test: (num_samples, ) 1D np.array
    # W: (num_features, ) 1D np.array
    # b: (1, ) 1D np.array
    # lr: learning rate set to be 0.001
    # epochs: number of epochs set to be 100

    # train_loss_history: (epochs, ) 1D np.array
    # test_loss_history: (epochs, ) 1D np.array

    train_loss_history = np.zeros(epochs)
    test_loss_history = np.zeros(epochs)
    
    m = len(y_train)
    
    for epoch in range(epochs):
        # Shuffle the training data
        indices = np.random.permutation(m)
        X_train_shuffled = X_train[indices]
        y_train_shuffled = y_train[indices]
        
        # Update parameters for each sample
        for i in range(m):
            xi = X_train_shuffled[i:i+1]  # Keep as 2D array
            yi = y_train_shuffled[i:i+1]
            
            # Compute gradient for single sample
            z = np.dot(xi, W) + b
            pred = sigmoid(z)
            
            dW = xi.T.flatten() * (pred - yi)
            db = (pred - yi)[0]
            
            # Update parameters
            W = W - lr * dW
            b = b - lr * db
        
        # Compute and record losses at the end of each epoch
        train_loss = compute_loss(X_train, y_train, W, b)
        test_loss = compute_loss(X_test, y_test, W, b)
        
        train_loss_history[epoch] = train_loss
        test_loss_history[epoch] = test_loss

    return train_loss_history, test_loss_history, W, b

## 4.d Plot the losses
"""Plot the training loss and test loss"""
def plot_curves(train_loss_history, test_loss_history, name):
    # Plot the training loss and test loss
    # train_loss_history: (epochs, ) 1D np.array
    # test_loss_history: (epochs, ) 1D np.array

    # save the figure as 'loss.png' and insert into your report
    plt.figure(figsize=(10, 6))
    plt.plot(train_loss_history, label='Training Loss', linewidth=2)
    plt.plot(test_loss_history, label='Test Loss', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title(f'Training and Test Loss - {name.upper()}', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'loss_{name}.png', dpi=300, bbox_inches='tight')
    plt.close()
    return

## 4.e PyTorch version
"""Define the LR module"""
class LogisticRegression(torch.nn.Module):
    def __init__(self, num_features):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(num_features, 1)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        predictions = self.sigmoid(self.linear(x))
        return predictions

"""Training function of PyTorch version"""
def train_torch(X_train, y_train, X_test, y_test, model, criterion, optimizer, epochs):
    # Train logistic regression using stochastic gradient descent
    # X_train: (num_samples, num_features) 2D np.array
    # y_train: (num_samples, ) 1D np.array
    # X_test: (num_samples, num_features) 2D np.array
    # y_test: (num_samples, ) 1D np.array
    # model: LogisticRegression
    # criterion: torch.nn.BCELoss
    # optimizer: torch.optim.SGD
    # epochs: number of epochs set to be 100
    # lr: learning rate set to be 0.001

    # train_loss_history: (epochs, ) 1D np.array
    # test_loss_history: (epochs, ) 1D np.array

    train_loss_history = np.zeros(epochs)
    test_loss_history = np.zeros(epochs)
    
    # Convert numpy arrays to PyTorch tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train).reshape(-1, 1)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test).reshape(-1, 1)
    
    for epoch in range(epochs):
        # Training mode
        model.train()
        
        # Forward pass - using batch operations, no explicit for loop over samples
        train_predictions = model(X_train_tensor)
        train_loss = criterion(train_predictions, y_train_tensor)
        
        # Backward pass and optimization
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()
        
        # Evaluation mode
        model.eval()
        with torch.no_grad():
            test_predictions = model(X_test_tensor)
            test_loss = criterion(test_predictions, y_test_tensor)
        
        # Record losses
        train_loss_history[epoch] = train_loss.item()
        test_loss_history[epoch] = test_loss.item()

    return train_loss_history, test_loss_history

"""calculate the test accuracy"""
def cal_accuracy_torch(X, y, model):
    # Calculate the accuracy of logistic regression
    # X: (num_samples, num_features) 2D np.array
    # y: (num_samples, ) 1D np.array
    # model: torch
    # accuracy: float
    model.eval()
    with torch.no_grad():
        X_tensor = torch.FloatTensor(X)
        predictions = model(X_tensor)
        predicted_labels = (predictions >= 0.5).float().numpy().flatten()
        accuracy = np.mean(predicted_labels == y)
    return accuracy

if __name__ == '__main__':
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    epochs = 100
    lr = 0.001

    ## a. Data Generation
    """Generate training set (1000 samples for each class)"""
    X_train, y_train = generate_data(num_features=100, num_samples=1000)

    """Generate testing set (50 samples for each class)"""
    X_test, y_test = generate_data(num_features=100, num_samples=50)

    ## 4.b Logistic Regression and GD
    """Training"""
    W_gd = np.zeros(100)
    b_gd = 0.0
    gd_train_loss_history, gd_test_loss_history, W_gd, b_gd = train_gd(X_train, y_train, X_test, y_test, W_gd, b_gd, epochs, lr)

    """calculate the test accuracy"""
    gd_accuracy = cal_accuracy(X_test, y_test, W_gd, b_gd)
    print(f"GD Test Accuracy: {gd_accuracy:.4f}")

    ## 4.c SGD
    """Training"""
    W_sgd = np.zeros(100)
    b_sgd = 0.0
    sgd_train_loss_history, sgd_test_loss_history, W_sgd, b_sgd = train_sgd(X_train, y_train, X_test, y_test, W_sgd, b_sgd, epochs, lr)

    """calculate the test accuracy"""
    sgd_accuracy = cal_accuracy(X_test, y_test, W_sgd, b_sgd)
    print(f"SGD Test Accuracy: {sgd_accuracy:.4f}")

    ## 4.d Plot the losses
    """Plot the training loss and test loss of GD"""
    plot_curves(gd_train_loss_history, gd_test_loss_history, 'gd')

    """Plot the training loss and test loss of SGD"""
    plot_curves(sgd_train_loss_history, sgd_test_loss_history, 'sgd')

    ## 4.e PyTorch version
    model = LogisticRegression(num_features=100)
    criterion = torch.nn.BCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    torch_train_loss_history, torch_test_loss_history = train_torch(X_train, y_train, X_test, y_test, model, criterion, optimizer, epochs)

    """Plot the training loss and test loss of PyTorch version"""
    plot_curves(torch_train_loss_history, torch_test_loss_history, 'torch')
    """calculate the test accuracy"""
    torch_accuracy = cal_accuracy_torch(X_test, y_test, model)
    print(f"PyTorch Test Accuracy: {torch_accuracy:.4f}")
    
    print("\nAll training completed! Loss curves saved as:")
