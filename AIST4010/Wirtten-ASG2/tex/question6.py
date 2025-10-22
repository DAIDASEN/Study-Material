import os
import json
import numpy as np
import matplotlib.pyplot as plt

# --- Adam Optimizer Implementation ---
class Adam:
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.t = 0

    def update(self, params, grads):
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]

        self.t += 1
        updated_params = []

        for i in range(len(params)):
            # Update biased first moment estimate
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            # Update biased second raw moment estimate
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grads[i] ** 2)

            # Compute bias-corrected first moment estimate
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            # Compute bias-corrected second raw moment estimate
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            # Update parameters
            param_update = self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
            updated_params.append(params[i] - param_update)

        return updated_params

# --- SGD Optimizer Implementation ---
class SGD:
    def __init__(self, learning_rate=0.0001):
        self.learning_rate = learning_rate

    def update(self, params, grads):
        updated_params = []
        for i in range(len(params)):
            param_update = self.learning_rate * grads[i]
            updated_params.append(params[i] - param_update)
        return updated_params

# --- Logistic Regression Model (from A1) ---
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, optimizer, epochs=1000):
    n_samples, n_features = X.shape
    weights = np.zeros(n_features)
    bias = 0
    losses = []

    for epoch in range(epochs):
        # Linear model
        linear_model = np.dot(X, weights) + bias
        y_predicted = sigmoid(linear_model)

        # Compute loss
        loss = - (1 / n_samples) * np.sum(y * np.log(y_predicted) + (1 - y) * np.log(1 - y_predicted))
        losses.append(loss)

        # Compute gradients
        dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
        db = (1 / n_samples) * np.sum(y_predicted - y)

        # Update parameters
        params = [weights, bias]
        grads = [dw, db]
        weights, bias = optimizer.update(params, grads)

        if epoch % 100 == 0:
            print(f'Epoch {epoch}: Loss = {loss:.4f}')

    return losses

# --- Main Execution ---
if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(__file__), 'generated')
    os.makedirs(out_dir, exist_ok=True)
    # Generate some synthetic data for demonstration
    np.random.seed(42)
    X_train = np.random.rand(100, 2) * 10
    # Create a linear decision boundary: y = 1 if x1 + x2 > 10, else 0
    y_train = (X_train[:, 0] + X_train[:, 1] > 10).astype(int)

    # Add a bias term to X_train for simplicity in the model function
    X_b = np.c_[np.ones((X_train.shape[0], 1)), X_train]

    # --- Train with Adam ---
    print("--- Training with Adam Optimizer ---")
    adam_optimizer = Adam(learning_rate=0.01) # A higher LR is often used for Adam
    # Re-implementing the logistic regression logic to fit the optimizer class structure
    n_samples, n_features = X_train.shape
    adam_weights = np.zeros(n_features)
    adam_bias = 0
    adam_losses = []

    for epoch in range(1000):
        linear_model = np.dot(X_train, adam_weights) + adam_bias
        y_predicted = sigmoid(linear_model)
        loss = - (1 / n_samples) * np.sum(y_train * np.log(y_predicted) + (1 - y_train) * np.log(1 - y_predicted))
        adam_losses.append(loss)
        dw = (1 / n_samples) * np.dot(X_train.T, (y_predicted - y_train))
        db = (1 / n_samples) * np.sum(y_predicted - y_train)
        [adam_weights, adam_bias] = adam_optimizer.update([adam_weights, adam_bias], [dw, db])

    # --- Train with SGD ---
    print("\n--- Training with SGD Optimizer ---")
    sgd_optimizer = SGD(learning_rate=1e-4)
    sgd_weights = np.zeros(n_features)
    sgd_bias = 0
    sgd_losses = []

    for epoch in range(1000):
        linear_model = np.dot(X_train, sgd_weights) + sgd_bias
        y_predicted = sigmoid(linear_model)
        loss = - (1 / n_samples) * np.sum(y_train * np.log(y_predicted) + (1 - y_train) * np.log(1 - y_predicted))
        sgd_losses.append(loss)
        dw = (1 / n_samples) * np.dot(X_train.T, (y_predicted - y_train))
        db = (1 / n_samples) * np.sum(y_predicted - y_train)
        [sgd_weights, sgd_bias] = sgd_optimizer.update([sgd_weights, sgd_bias], [dw, db])


    # --- Plotting the results ---
    plt.figure(figsize=(7, 4))
    plt.plot(adam_losses, label='Adam Optimizer (lr=0.01)')
    plt.plot(sgd_losses, label='SGD Optimizer (lr=1e-4)')
    plt.title('Convergence Speed: Adam vs. SGD')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plot_path = os.path.join(out_dir, 'convergence_comparison.png')
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)

    # Save brief summary (final losses)
    summary = {
        "adam_final_loss": float(adam_losses[-1]),
        "sgd_final_loss": float(sgd_losses[-1])
    }
    with open(os.path.join(out_dir, 'question6_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    # Write LaTeX snippet for inclusion
    with open(os.path.join(out_dir, 'question6_summary.tex'), 'w', encoding='utf-8') as f:
        f.write("% Auto-generated by question6.py\n")
        f.write(f"Adam final loss: {summary['adam_final_loss']:.4f}\\\\\n")
        f.write(f"SGD final loss: {summary['sgd_final_loss']:.4f}\\\n")
