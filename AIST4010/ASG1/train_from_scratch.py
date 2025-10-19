#!/usr/bin/env python3
"""
从头训练人脸分类模型（不使用预训练权重）
针对暗光、多人干扰场景优化
"""
import argparse
import json
import os
import math
from pathlib import Path
from typing import Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from tqdm import tqdm


# ============================================================================
# 数据增强策略（针对暗光和遮挡问题）
# ============================================================================
def build_dataloaders(data_dir: str, img_size: int, batch_size: int, num_workers: int) -> Tuple[DataLoader, DataLoader]:
    """构建数据加载器，使用强化的增强策略"""
    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')
    
    # 训练集增强：针对暗光、遮挡问题
    train_tfms = transforms.Compose([
        transforms.Lambda(lambda img: img.convert('RGB')),
        transforms.RandomResizedCrop(img_size, scale=(0.7, 1.0)),  # 处理多人场景
        transforms.RandomHorizontalFlip(p=0.5),
        # 强化光照增强（针对暗光问题）
        transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.3, hue=0),
        transforms.RandomGrayscale(p=0.1),  # 10% 转灰度，增强鲁棒性
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),  # 简单归一化到[-1,1]
        # 模拟遮挡（必须在 ToTensor 之后）
        transforms.RandomErasing(p=0.3, scale=(0.02, 0.15), ratio=(0.3, 3.3), value='random'),
    ])
    
    # 验证集：简单处理
    val_tfms = transforms.Compose([
        transforms.Lambda(lambda img: img.convert('RGB')),
        transforms.Resize(int(img_size * 1.15)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    
    train_set = datasets.ImageFolder(train_dir, transform=train_tfms)
    val_set = datasets.ImageFolder(val_dir, transform=val_tfms)
    
    pin = torch.cuda.is_available()
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, 
                             num_workers=num_workers, pin_memory=pin, drop_last=True)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, 
                           num_workers=num_workers, pin_memory=pin)
    
    return train_loader, val_loader


# ============================================================================
# 注意力模块（帮助模型聚焦人脸区域）
# ============================================================================
class ChannelAttention(nn.Module):
    """通道注意力机制"""
    def __init__(self, channels: int, reduction: int = 16):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, channels // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction, channels, bias=False)
        )
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        b, c, _, _ = x.size()
        avg_out = self.fc(self.avg_pool(x).view(b, c))
        max_out = self.fc(self.max_pool(x).view(b, c))
        out = self.sigmoid(avg_out + max_out).view(b, c, 1, 1)
        return x * out


class SpatialAttention(nn.Module):
    """空间注意力机制"""
    def __init__(self, kernel_size: int = 7):
        super().__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=kernel_size // 2, bias=False)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        out = torch.cat([avg_out, max_out], dim=1)
        out = self.sigmoid(self.conv(out))
        return x * out


class CBAM(nn.Module):
    """组合通道和空间注意力"""
    def __init__(self, channels: int):
        super().__init__()
        self.channel_att = ChannelAttention(channels)
        self.spatial_att = SpatialAttention()
    
    def forward(self, x):
        x = self.channel_att(x)
        x = self.spatial_att(x)
        return x


# ============================================================================
# ResNet34 从头实现（不使用预训练）
# ============================================================================
class BasicBlock(nn.Module):
    """ResNet 基础块"""
    expansion = 1
    
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1, downsample=None):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample
    
    def forward(self, x):
        identity = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        if self.downsample is not None:
            identity = self.downsample(x)
        out += identity
        out = self.relu(out)
        return out


class ResNet34FromScratch(nn.Module):
    """ResNet34 从头实现，添加注意力机制"""
    def __init__(self, num_classes: int = 1000, use_attention: bool = True):
        super().__init__()
        self.in_channels = 64
        self.use_attention = use_attention
        
        # 初始卷积层
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        
        # ResNet 层（3, 4, 6, 3）
        self.layer1 = self._make_layer(64, 3, stride=1)
        self.layer2 = self._make_layer(128, 4, stride=2)
        self.layer3 = self._make_layer(256, 6, stride=2)
        self.layer4 = self._make_layer(512, 3, stride=2)
        
        # 注意力模块
        if use_attention:
            self.attention = CBAM(512)
        
        # 全局平均池化
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        
        # 分类头（Softmax）
        self.fc = nn.Linear(512, num_classes)
        
        # 权重初始化
        self._initialize_weights()
    
    def _make_layer(self, out_channels: int, blocks: int, stride: int = 1):
        downsample = None
        if stride != 1 or self.in_channels != out_channels:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, out_channels, 1, stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        
        layers = []
        layers.append(BasicBlock(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels
        for _ in range(1, blocks):
            layers.append(BasicBlock(out_channels, out_channels))
        
        return nn.Sequential(*layers)
    
    def _initialize_weights(self):
        """Kaiming 初始化"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        if self.use_attention:
            x = self.attention(x)
        
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


# ============================================================================
# 分类器（纯 Softmax 版本）
# ============================================================================
class FaceClassifier(nn.Module):
    """完整的人脸分类器（纯 Softmax）"""
    def __init__(self, num_classes: int, use_attention: bool = True, **kwargs):
        super().__init__()
        # 忽略 use_arcface 参数以保持向后兼容
        self.backbone = ResNet34FromScratch(num_classes=num_classes, use_attention=use_attention)
    
    def forward(self, x, labels=None):
        # labels 参数保留以兼容旧代码，但不使用
        return self.backbone(x)


# ============================================================================
# 训练和评估
# ============================================================================
def train_epoch(model, loader, criterion, optimizer, device):
    """训练一个 epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc='Training')
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({
            'loss': f'{running_loss / (pbar.n + 1):.4f}',
            'acc': f'{100. * correct / total:.2f}%'
        })
    
    return running_loss / len(loader), 100. * correct / total


def evaluate(model, loader, criterion, device):
    """评估模型"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in tqdm(loader, desc='Evaluating'):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    return running_loss / len(loader), 100. * correct / total


def train(args):
    """主训练函数"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # 数据加载
    train_loader, val_loader = build_dataloaders(
        args.data_dir, args.img_size, args.batch_size, args.workers
    )
    num_classes = len(train_loader.dataset.classes)
    print(f"Number of classes: {num_classes}")
    
    # 模型
    model = FaceClassifier(
        num_classes=num_classes,
        use_attention=args.use_attention
    )
    
    # 多GPU
    if torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs")
        model = nn.DataParallel(model)
    model.to(device)
    
    # 保存类别映射
    save_dir = Path(args.out_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    with open(save_dir / 'classes.json', 'w') as f:
        json.dump(train_loader.dataset.classes, f, indent=2)
    
    # 优化器和调度器
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.9, 
                         weight_decay=args.weight_decay, nesterov=True)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)
    criterion = nn.CrossEntropyLoss(label_smoothing=args.label_smoothing)
    
    # 恢复训练
    start_epoch = 1
    best_acc = 0.0
    
    if args.resume:
        if os.path.exists(args.resume):
            print(f"\n{'='*60}")
            print(f"Loading checkpoint from {args.resume}")
            checkpoint = torch.load(args.resume, map_location=device)
            
            # 加载模型权重
            model.load_state_dict(checkpoint['model_state'])
            
            # 加载优化器和调度器
            if not args.reset_optimizer:
                optimizer.load_state_dict(checkpoint['optimizer_state'])
                print("✓ Optimizer state loaded")
            else:
                print("✓ Optimizer state RESET (fresh start)")
            
            if not args.reset_scheduler:
                scheduler.load_state_dict(checkpoint['scheduler_state'])
                print("✓ Scheduler state loaded")
            else:
                print("✓ Scheduler state RESET (fresh LR schedule)")
            
            # 恢复 epoch 和 best_acc
            start_epoch = checkpoint['epoch'] + 1
            best_acc = checkpoint.get('val_acc', 0.0)
            
            print(f"✓ Resuming from epoch {start_epoch}, best_acc={best_acc:.2f}%")
            print(f"{'='*60}\n")
        else:
            print(f"Warning: Resume checkpoint not found at {args.resume}, starting from scratch")
    
    # 训练循环
    for epoch in range(start_epoch, args.epochs + 1):
        print(f"\n{'='*60}")
        print(f"Epoch {epoch}/{args.epochs}, LR: {optimizer.param_groups[0]['lr']:.6f}")
        print(f"{'='*60}")
        
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device, False
        )
        val_loss, val_acc = evaluate(
            model, val_loader, criterion, device, False
        )
        
        print(f"\nTrain Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        
        scheduler.step()
        
        # 保存检查点
        checkpoint = {
            'epoch': epoch,
            'model_state': model.state_dict(),
            'optimizer_state': optimizer.state_dict(),
            'scheduler_state': scheduler.state_dict(),
            'val_acc': val_acc,
            'num_classes': num_classes,
            'use_arcface': False,
            'use_attention': args.use_attention
        }
        
        torch.save(checkpoint, save_dir / f'epoch_{epoch}.pt')
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(checkpoint, save_dir / 'best.pt')
            print(f"✓ Best model saved! (Acc: {best_acc:.2f}%)")
    
    print(f"\n{'='*60}")
    print(f"Training completed! Best Val Acc: {best_acc:.2f}%")
    print(f"{'='*60}")


def parse_args():
    p = argparse.ArgumentParser(description='Train face classifier from scratch')
    p.add_argument('--data-dir', type=str, default='.', help='Data directory')
    p.add_argument('--out-dir', type=str, default='outputs_scratch', help='Output directory')
    p.add_argument('--img-size', type=int, default=224, help='Image size')
    p.add_argument('--batch-size', type=int, default=64, help='Batch size')
    p.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    p.add_argument('--lr', type=float, default=0.1, help='Initial learning rate')
    p.add_argument('--weight-decay', type=float, default=5e-4, help='Weight decay')
    p.add_argument('--workers', type=int, default=8, help='Number of workers')
    p.add_argument('--label-smoothing', type=float, default=0.1, help='Label smoothing')
    p.add_argument('--use-attention', action='store_true', help='Use CBAM attention')
    # 恢复训练相关
    p.add_argument('--resume', type=str, default='', help='Path to checkpoint to resume from')
    p.add_argument('--reset-optimizer', action='store_true', help='Reset optimizer state when resuming')
    p.add_argument('--reset-scheduler', action='store_true', help='Reset scheduler state when resuming')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    train(args)
