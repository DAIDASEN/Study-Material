import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models.video as models

class AneurysmClassifier(nn.Module):
    def __init__(self, num_classes=14):
        super(AneurysmClassifier, self).__init__()
        # Use r3d_18 backbone
        self.backbone = models.r3d_18(pretrained=True)
        
        # Modify the first layer to accept 1 channel (grayscale) instead of 3 (RGB)
        # Original: nn.Conv3d(3, 64, kernel_size=(3, 7, 7), stride=(1, 2, 2), padding=(1, 3, 3), bias=False)
        old_stem = self.backbone.stem[0]
        self.backbone.stem[0] = nn.Conv3d(
            in_channels=1, 
            out_channels=old_stem.out_channels, 
            kernel_size=old_stem.kernel_size, 
            stride=old_stem.stride, 
            padding=old_stem.padding, 
            bias=False
        )

        # Replace the final fully connected layer
        # Output: 1 Global Probability + 13 Local Probabilities
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(in_features, num_classes)

    def forward(self, x):
        # x shape: (Batch, 1, D, H, W)
        logits = self.backbone(x)
        return logits

class HybridLoss(nn.Module):
    def __init__(self, lambda_loc=1.0, alpha=0.25, gamma=2.0):
        super(HybridLoss, self).__init__()
        self.lambda_loc = lambda_loc
        self.alpha = alpha
        self.gamma = gamma
        self.bce = nn.BCEWithLogitsLoss()

    def focal_loss(self, inputs, targets):
        bce_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        pt = torch.exp(-bce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * bce_loss
        return focal_loss.mean()

    def forward(self, preds, targets):
        # preds/targets shape: (Batch, 14)
        
        # Global task (Index 0) - Standard BCE
        loss_global = self.bce(preds[:, 0], targets[:, 0])
        
        # Local tasks (Index 1-13) - Focal Loss
        loss_local = self.focal_loss(preds[:, 1:], targets[:, 1:])
        
        return loss_global + self.lambda_loc * loss_local