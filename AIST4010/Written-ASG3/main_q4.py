import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from utils_q4 import Attention,LogisticRegression,GRU,RNN,data_generator,MyDataset
np.random.seed(42)
torch.manual_seed(42)


# visualize the samples

dir = "./results/"
os.makedirs(dir,exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device')

torch.backends.cudnn.benchmark = True if device == 'cuda' else False

hidden_size = 64  # model hidden dimension

batch_size = 256
epochs = 30  # at least 20 epochs per requirement
lr = 1e-3


x,y = data_generator(0.02)
plt.figure(figsize=(15, 5))
plt.scatter(x,y)
plt.grid()
plt.title('samples from sine function with Gaussian noises')
plt.savefig(dir + "samples.png")
plt.cla()

seq_len = 10
x_slices = []
y_slices = []

# create sliding windows of length 10 to predict the next value
for i in range(len(y) - seq_len):
    x_slices.append(y[i:i+seq_len])
    y_slices.append(y[i+seq_len])

x_slices = np.array(x_slices, dtype=np.float32).reshape(-1, seq_len, 1)
y_slices = np.array(y_slices, dtype=np.float32).reshape(-1, 1)

train_ds = MyDataset(x_slices, y_slices)
train_loader = DataLoader(
    train_ds,
    batch_size=batch_size,
    shuffle=True,
    drop_last=False,
    pin_memory=True if device == 'cuda' else False,
)

def train(train_loader, device, model, criterion, optimizer, epoch):
    model.train()
    running_loss = 0.0
    n = 0
    for xb, yb in train_loader:
        xb = xb.to(device)
        yb = yb.to(device)
        optimizer.zero_grad()
        preds = model(xb)
        loss = criterion(preds, yb)
        loss.backward()
        optimizer.step()
        bs = xb.size(0)
        running_loss += loss.item() * bs
        n += bs
    return running_loss / max(n, 1)

# RNN

rnn = RNN(input_size=1, hidden_size=hidden_size).to(device)
print(rnn)
optim_rnn = torch.optim.Adam(rnn.parameters(), lr=lr)
criterion = nn.MSELoss()
rnn_history = []  

for epoch in tqdm(range(epochs)):
    rnn_loss = train(train_loader, device, rnn, criterion, optim_rnn, epoch)
    rnn_history.append(rnn_loss)

print(f'RNN loss = {rnn_loss}')
plt.plot(np.arange(epochs), np.array(rnn_history))
plt.title('Running loss history with RNN')
plt.grid()
plt.savefig(dir + "rnn.png")
plt.cla()

# GRU
gru = GRU(input_size=1, hidden_size=hidden_size).to(device)
print(gru)
optim_gru = torch.optim.Adam(gru.parameters(), lr=lr)
criterion = nn.MSELoss()
gru_history = []

for epoch in tqdm(range(epochs)):
    gru_loss = train(train_loader, device, gru, criterion, optim_gru, epoch)
    gru_history.append(gru_loss)

print(f'GRU loss = {gru_loss}')
plt.plot(np.arange(epochs), np.array(gru_history))
plt.title('Running loss history with GRU')
plt.grid()
plt.savefig(dir + "gru.png")
plt.cla()

attention = Attention(input_size=1, hidden_size=hidden_size).to(device)
print(attention)
optim_attention = torch.optim.Adam(attention.parameters(), lr=lr)
criterion = nn.MSELoss()
attention_history = []

for epoch in tqdm(range(epochs)):
    attention_loss = train(train_loader, device, attention, criterion, optim_attention, epoch)
    attention_history.append(attention_loss)
    
print(f'Attention loss = {attention_loss}')
plt.plot(np.arange(epochs), np.array(attention_history))
plt.title('Running loss history with Attention')
plt.grid()
plt.savefig(dir + "attention.png")
plt.cla()


logistic = LogisticRegression(input_len=seq_len).to(device)
print(logistic)
optim_logistic = torch.optim.Adam(logistic.parameters(), lr=lr)
criterion = nn.MSELoss()
logistic_history = []

for epoch in tqdm(range(epochs)):
    logistic_loss = train(train_loader, device, logistic, criterion, optim_logistic, epoch)
    logistic_history.append(logistic_loss)
    
print(f'Logistic regression loss = {logistic_loss}')
plt.plot(np.arange(epochs), np.array(logistic_history))
plt.title('Running loss history with logistic regression')
plt.grid()
plt.savefig(dir + "lr.png")
plt.cla()

def predict(model, title):
    
    model.eval()
    preds = []
    with torch.no_grad():
        # start from y_991..y_1000 (last 10 points)
        window = y[-seq_len:].astype(np.float32).reshape(1, seq_len, 1)
        window_t = torch.from_numpy(window).to(device)
        for _ in range(200):
            out = model(window_t)
            next_val = out.squeeze().item()
            preds.append(next_val)
            # update window with new prediction
            new_seq = torch.cat([window_t[:, 1:, :], torch.tensor([[[next_val]]], dtype=window_t.dtype, device=device)], dim=1)
            window_t = new_seq
    
    plt.plot(np.arange(0, 200, 1), preds)
    plt.grid()
    plt.title(f'prediction results using {title}')
    plt.savefig(dir + "pred_" + title + ".png")
    plt.cla()   
     
start = time.time()
predict(rnn, 'RNN')
end = time.time()
print(f'{end - start:.4f}s')

start = time.time()
predict(gru, 'GRU')
end = time.time()
print(f'{end - start:.4f}s')

start = time.time()
predict(attention, 'Attention')
end = time.time()
print(f'{end - start:.4f}s')

start = time.time()
predict(logistic, 'logistic regression')
end = time.time()
print(f'{end - start:.4f}s')