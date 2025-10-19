import argparse
import json
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from pathlib import Path
from tqdm import tqdm


def get_strong_augmentation(img_size: int):
    normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    
    train_tfms = transforms.Compose([
        transforms.Lambda(lambda img: img.convert('RGB')),
        transforms.RandomResizedCrop(img_size, scale=(0.6, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.4, hue=0),
        transforms.RandomGrayscale(p=0.2), 
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        normalize,
        transforms.RandomErasing(p=0.4, scale=(0.02, 0.2), ratio=(0.3, 3.3), value='random'),
    ])
    
    return train_tfms


def build_dataloaders_strong_aug(data_dir: str, img_size: int, batch_size: int, num_workers: int):
    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')
    
    train_tfms = get_strong_augmentation(img_size)
    
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


def add_dropout_to_model(model, dropout_rate=0.3):
    if isinstance(model, nn.DataParallel):
        actual_model = model.module
    else:
        actual_model = model
    
    if hasattr(actual_model, 'backbone'):
        backbone = actual_model.backbone
        if hasattr(backbone, 'fc'):
            original_fc = backbone.fc
            backbone.fc = nn.Sequential(
                nn.Dropout(p=dropout_rate),
                original_fc
            )
            print(f"✓ Added Dropout({dropout_rate}) before backbone.fc")
    
    return model


def train_epoch_with_mixup(model, loader, criterion, optimizer, device, mixup_alpha=0.2):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc='Training')
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        if mixup_alpha > 0:
            lam = torch.distributions.Beta(mixup_alpha, mixup_alpha).sample().item()
            batch_size = images.size(0)
            index = torch.randperm(batch_size).to(device)
            
            mixed_images = lam * images + (1 - lam) * images[index]
            labels_a, labels_b = labels, labels[index]
            
            optimizer.zero_grad()
            outputs = model(mixed_images)
            loss = lam * criterion(outputs, labels_a) + (1 - lam) * criterion(outputs, labels_b)
        else:
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


def regularize_overfitted_model(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    print("Building dataloaders with STRONG augmentation...")
    train_loader, val_loader = build_dataloaders_strong_aug(
        args.data_dir, args.img_size, args.batch_size, args.workers
    )
    num_classes = len(train_loader.dataset.classes)
    print(f"Number of classes: {num_classes}")
    
    print(f"\n{'='*60}")
    print(f"Loading overfitted model from {args.pretrained}")
    checkpoint = torch.load(args.pretrained, map_location='cpu')
    
    from train_from_scratch import FaceClassifier
    model = FaceClassifier(
        num_classes=num_classes,
        use_arcface=checkpoint.get('use_arcface', False),
        use_attention=checkpoint.get('use_attention', True)
    )
    
    state_dict = checkpoint['model_state']
    if list(state_dict.keys())[0].startswith('module.'):
        state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}
    model.load_state_dict(state_dict)
    
    prev_acc = checkpoint.get('val_acc', 0.0)
    print(f"Previous validation accuracy: {prev_acc:.2f}%")
    print(f"{'='*60}\n")
    
    if args.add_dropout:
        model = add_dropout_to_model(model, dropout_rate=args.dropout_rate)
    
    if torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs")
        model = nn.DataParallel(model)
    model.to(device)
    
    save_dir = Path(args.out_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    with open(save_dir / 'classes.json', 'w') as f:
        json.dump(train_loader.dataset.classes, f, indent=2)
    
    optimizer = optim.SGD(
        model.parameters(), 
        lr=args.lr,
        momentum=0.9, 
        weight_decay=args.weight_decay, 
        nesterov=True
    )
    
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-7)
    
    criterion = nn.CrossEntropyLoss(label_smoothing=args.label_smoothing)
    
    print(f"\n{'='*60}")
    print(f"Regularization Strategy:")
    print(f"  - Strong data augmentation (RandomErasing 40%, ColorJitter++)")
    print(f"  - Mixup alpha: {args.mixup_alpha}")
    print(f"  - Label smoothing: {args.label_smoothing}")
    print(f"  - Weight decay: {args.weight_decay}")
    print(f"  - Dropout: {args.dropout_rate if args.add_dropout else 'None'}")
    print(f"  - Small learning rate: {args.lr}")
    print(f"{'='*60}\n")
    
    best_acc = prev_acc
    
    for epoch in range(1, args.epochs + 1):
        print(f"\n{'='*60}")
        print(f"Epoch {epoch}/{args.epochs}, LR: {optimizer.param_groups[0]['lr']:.6f}")
        print(f"{'='*60}")
        
        train_loss, train_acc = train_epoch_with_mixup(
            model, train_loader, criterion, optimizer, device, 
            mixup_alpha=args.mixup_alpha
        )
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        
        print(f"\nTrain Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        
        gap = train_acc - val_acc
        print(f"Overfitting gap: {gap:.2f}%")
        
        scheduler.step()
        
        checkpoint_new = {
            'epoch': epoch,
            'model_state': model.state_dict(),
            'optimizer_state': optimizer.state_dict(),
            'scheduler_state': scheduler.state_dict(),
            'val_acc': val_acc,
            'train_acc': train_acc,
            'num_classes': num_classes,
            'use_arcface': checkpoint.get('use_arcface', False),
            'use_attention': checkpoint.get('use_attention', True)
        }
        
        torch.save(checkpoint_new, save_dir / f'epoch_{epoch}.pt')
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(checkpoint_new, save_dir / 'best.pt')
            print(f"✓ New best! (Acc: {best_acc:.2f}%)")
    
    print(f"\n{'='*60}")
    print(f"Regularization completed!")
    print(f"Previous best: {prev_acc:.2f}%")
    print(f"New best: {best_acc:.2f}%")
    print(f"Improvement: {best_acc - prev_acc:+.2f}%")
    print(f"{'='*60}")


def parse_args():
    p = argparse.ArgumentParser(description='Regularize overfitted model')
    p.add_argument('--pretrained', type=str, required=True, help='Path to overfitted model')
    p.add_argument('--data-dir', type=str, default='.', help='Data directory')
    p.add_argument('--out-dir', type=str, default='outputs_regularized', help='Output directory')
    p.add_argument('--img-size', type=int, default=224, help='Image size')
    p.add_argument('--batch-size', type=int, default=128, help='Batch size')
    p.add_argument('--epochs', type=int, default=20, help='Number of epochs')
    p.add_argument('--lr', type=float, default=0.001, help='Learning rate (small for fine-tuning)')
    p.add_argument('--weight-decay', type=float, default=1e-3, help='Weight decay (larger to fight overfitting)')
    p.add_argument('--workers', type=int, default=12, help='Number of workers')
    p.add_argument('--label-smoothing', type=float, default=0.2, help='Label smoothing (larger for overfitting)')
    p.add_argument('--mixup-alpha', type=float, default=0.3, help='Mixup alpha (0 to disable)')
    p.add_argument('--add-dropout', action='store_true', help='Add dropout layer')
    p.add_argument('--dropout-rate', type=float, default=0.3, help='Dropout rate')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    regularize_overfitted_model(args)
