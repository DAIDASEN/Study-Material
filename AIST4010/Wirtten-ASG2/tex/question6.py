import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility (as in A1)
np.random.seed(42)

# --- Functions from A1 (Logistic Regression) ---

def generate_data(n_samples=1000, n_features=100, n_test=100):
    """Generates a linearly separable dataset with noise."""
    # Class 0
    mean0 = np.ones(n_features) * -0.5
    cov0 = np.eye(n_features)
    X0 = np.random.multivariate_normal(mean0, cov0, n_samples)
    y0 = np.zeros(n_samples)
    
    # Class 1
    mean1 = np.ones(n_features) * 0.5
    cov1 = np.eye(n_features)
    X1 = np.random.multivariate_normal(mean1, cov1, n_samples)
    y1 = np.ones(n_samples)
    
    # Combine training data
    X_train = np.vstack((X0, X1))
    y_train = np.hstack((y0, y1)).reshape(-1, 1)
    
    # Shuffle training data
    indices = np.arange(X_train.shape[0])
    np.random.shuffle(indices)
    X_train = X_train[indices]
    y_train = y_train[indices]
    
    # Generate testing data (approx 50/50 split)
    n_test_per_class = n_test // 2
    X_test0 = np.random.multivariate_normal(mean0, cov0, n_test_per_class)
    y_test0 = np.zeros(n_test_per_class)
    X_test1 = np.random.multivariate_normal(mean1, cov1, n_test - n_test_per_class)
    y_test1 = np.ones(n_test - n_test_per_class)
    
    X_test = np.vstack((X_test0, X_test1))
    y_test = np.hstack((y_test0, y_test1)).reshape(-1, 1)
    
    return X_train, y_train, X_test, y_test

def sigmoid(z):
    """Sigmoid activation function."""
    return 1 / (1 + np.exp(-z))

def compute_loss(y, y_hat):
    """Binary Cross-Entropy Loss."""
    m = y.shape[0]
    # Add epsilon for numerical stability (to avoid log(0))
    epsilon = 1e-9
    loss = -1/m * np.sum(y * np.log(y_hat + epsilon) + (1 - y) * np.log(1 - y_hat + epsilon))
    return loss

def forward(X, W, b):
    """Forward pass: computes y_hat."""
    z = np.dot(X, W) + b
    y_hat = sigmoid(z)
    return y_hat

def backward(X, y, y_hat):
    """Backward pass: computes gradients."""
    m = X.shape[0]
    dz = y_hat - y
    dW = 1/m * np.dot(X.T, dz)
    db = 1/m * np.sum(dz)
    return dW, db

def accuracy(y, y_pred):
    """Calculates prediction accuracy."""
    y_pred_class = (y_pred > 0.5).astype(int)
    return np.mean(y_pred_class == y) * 100

# --- Optimizer Implementations ---

def train_sgd(X_train, y_train, X_test, y_test, epochs, learning_rate):
    """Trains logistic regression using (Batch) SGD."""
    n_samples, n_features = X_train.shape
    
    # Initialize parameters
    W = np.zeros((n_features, 1))
    b = 0.0
    
    train_loss_history = []
    test_loss_history = []
    
    for epoch in range(epochs):
        # Forward pass (Training)
        y_hat_train = forward(X_train, W, b)
        train_loss = compute_loss(y_train, y_hat_train)
        train_loss_history.append(train_loss)
        
        # Backward pass (Gradients)
        dW, db = backward(X_train, y_train, y_hat_train)
        
        # --- SGD Update Rule ---
        W -= learning_rate * dW
        b -= learning_rate * db
        
        # Evaluate on test set
        y_hat_test = forward(X_test, W, b)
        test_loss = compute_loss(y_test, y_hat_test)
        test_loss_history.append(test_loss)
        
        if (epoch + 1) % 100 == 0:
            print(f"SGD Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}")

    return W, b, train_loss_history, test_loss_history

def train_adam(X_train, y_train, X_test, y_test, epochs, alpha, delta, gamma, epsilon):
    """Trains logistic regression using Adam optimizer."""
    n_samples, n_features = X_train.shape
    
    # Initialize parameters
    W = np.zeros((n_features, 1))
    b = 0.0
    
    # --- Adam Initialization ---
    m_W = np.zeros_like(W)
    v_W = np.zeros_like(W)
    m_b = 0.0
    v_b = 0.0
    t = 0  # Time step
    
    train_loss_history = []
    test_loss_history = []
    
    for epoch in range(epochs):
        t += 1  # Increment time step
        
        # Forward pass (Training)
        y_hat_train = forward(X_train, W, b)
        train_loss = compute_loss(y_train, y_hat_train)
        train_loss_history.append(train_loss)
        
        # Backward pass (Gradients)
        dW, db = backward(X_train, y_train, y_hat_train)
        
        # --- Adam Update Rule ---
        
        # 1. Update biased first moment estimate
        m_W = delta * m_W + (1 - delta) * dW
        m_b = delta * m_b + (1 - delta) * db
        
        # 2. Update biased second moment estimate
        v_W = gamma * v_W + (1 - gamma) * (dW ** 2)
        v_b = gamma * v_b + (1 - gamma) * (db ** 2)
        
        # 3. Compute bias-corrected first moment estimate
        m_hat_W = m_W / (1 - delta ** t)
        m_hat_b = m_b / (1 - delta ** t)
        
        # 4. Compute bias-corrected second moment estimate
        v_hat_W = v_W / (1 - gamma ** t)
        v_hat_b = v_b / (1 - gamma ** t)
        
        # 5. Update parameters
        W -= alpha * m_hat_W / (np.sqrt(v_hat_W) + epsilon)
        b -= alpha * m_hat_b / (np.sqrt(v_hat_b) + epsilon)
        
        # Evaluate on test set
        y_hat_test = forward(X_test, W, b)
        test_loss = compute_loss(y_test, y_hat_test)
        test_loss_history.append(test_loss)
        
        if (epoch + 1) % 100 == 0:
            print(f"Adam Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}")

    return W, b, train_loss_history, test_loss_history

# --- Plotting Function ---

def plot_loss_comparison(sgd_history, adam_history, epochs):
    """Plots the training loss curves for SGD and Adam."""
    plt.figure(figsize=(10, 6))
    plt.plot(range(epochs), sgd_history, label=f"SGD (lr={SGD_LR})", color="blue")
    plt.plot(range(epochs), adam_history, label=f"Adam (lr={ADAM_ALPHA})", color="red")
    plt.xlabel("Epoch")
    plt.ylabel("Training Loss (Binary Cross-Entropy)")
    plt.title("SGD vs. Adam Convergence Comparison")
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 0.7) # Start y-axis at 0 for better comparison
    plt.show()

# --- Main Execution ---

if __name__ == "__main__":
    # Hyperparameters
    EPOCHS = 1000
    
    # SGD (as requested)
    SGD_LR = 1e-4
    
    # Adam (default params)
    ADAM_ALPHA = 0.001   # Learning rate (α)
    ADAM_DELTA = 0.9     # First moment decay (δ)
    ADAM_GAMMA = 0.999   # Second moment decay (γ)
    ADAM_EPSILON = 1e-7  # Numerical stability (ε)

    # 1. Generate Data
    X_train, y_train, X_test, y_test = generate_data()
    print(f"Data shapes: X_train: {X_train.shape}, y_train: {y_train.shape}, X_test: {X_test.shape}, y_test: {y_test.shape}")

    # 2. Run SGD
    print("\n--- Training with SGD ---")
    W_sgd, b_sgd, train_loss_sgd, test_loss_sgd = train_sgd(
        X_train, y_train, X_test, y_test, EPOCHS, SGD_LR
    )

    # 3. Run Adam
    print("\n--- Training with Adam ---")
    W_adam, b_adam, train_loss_adam, test_loss_adam = train_adam(
        X_train, y_train, X_test, y_test, EPOCHS,
        ADAM_ALPHA, ADAM_DELTA, ADAM_GAMMA, ADAM_EPSILON
    )
    
    # 4. Calculate and Print Final Accuracy
    y_pred_sgd = forward(X_test, W_sgd, b_sgd)
    acc_sgd = accuracy(y_test, y_pred_sgd)
    
    y_pred_adam = forward(X_test, W_adam, b_adam)
    acc_adam = accuracy(y_test, y_pred_adam)
    
    print("\n--- Final Results ---")
    print(f"SGD (lr={SGD_LR}) Final Test Accuracy: {acc_sgd:.2f}%")
    print(f"Adam (default) Final Test Accuracy: {acc_adam:.2f}%")

    # 5. Plot Comparison
    plot_loss_comparison(train_loss_sgd, train_loss_adam, EPOCHS)