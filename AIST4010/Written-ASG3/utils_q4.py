import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset

np.random.seed(42)
torch.manual_seed(42)
def data_generator(noise_parameter):
    # generate 1,000 points from 0 to 100 with step 0.1
    x = np.arange(0, 100, 0.1)
    # sine values plus gaussian noise
    y = np.sin(x) + np.random.normal(loc=0.0, scale=noise_parameter, size=x.shape)
    return x, y

class MyDataset(Dataset):
    def __init__(self, x, y):
        self.x = torch.from_numpy(x)
        self.y = torch.from_numpy(y)

    def __len__(self):
        return self.x.shape[0]
    
    def __getitem__(self, idx):
        return self.x[idx].float(), self.y[idx].float()

class RNN(nn.Module):
    
    def __init__(self, input_size: int = 1, hidden_size: int = 64, num_layers: int = 1):
        super().__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x: (B, T, 1)
        out, h_n = self.rnn(x)  # out: (B, T, H)
        last = out[:, -1, :]    # (B, H)
        y = self.fc(last)       # (B, 1)
        return y

    
class GRU(nn.Module):
    
    def __init__(self, input_size: int = 1, hidden_size: int = 64, num_layers: int = 1):
        super().__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x: (B, T, 1)
        out, h_n = self.gru(x)  # out: (B, T, H)
        last = out[:, -1, :]    # (B, H)
        y = self.fc(last)       # (B, 1)
        return y
    
    
class Attention(nn.Module):
    
    def __init__(self, input_size: int = 1, hidden_size: int = 64):
        super().__init__()
        # simple encoder with GRU
        self.encoder = nn.GRU(input_size=input_size, hidden_size=hidden_size, num_layers=1, batch_first=True)
        # final prediction head
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x: (B, T, 1)
        enc_out, h_n = self.encoder(x)  # enc_out: (B, T, H), h_n: (1, B, H)
        query = h_n[-1]                 # (B, H)
        # dot-product attention: scores = enc_out · query
        # enc_out: (B, T, H), query: (B, H) -> (B, T)
        scores = torch.bmm(enc_out, query.unsqueeze(2)).squeeze(2)
        attn = torch.softmax(scores, dim=1)  # (B, T)
        context = torch.bmm(attn.unsqueeze(1), enc_out).squeeze(1)  # (B, H)
        y = self.fc(context)  # (B, 1)
        return y
    
class LogisticRegression(nn.Module):
    
    def __init__(self, input_len: int = 10):
        super().__init__()
        # classic logistic regression: linear + sigmoid
        self.linear = nn.Linear(input_len, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x can be (B, T, 1) or (B, T)
        if x.dim() == 3:
            x = x.view(x.size(0), -1)  # flatten to (B, T)
        out = self.linear(x)           # (B, 1)
        out = self.sigmoid(out)        # (B, 1) in [0,1]
        # map back to [-1, 1] to match sine range
        out = 2.0 * out - 1.0
        return out
