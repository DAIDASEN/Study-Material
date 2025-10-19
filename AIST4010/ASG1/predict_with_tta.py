#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from tqdm import tqdm

import sys
sys.path.insert(0, os.path.dirname(__file__))
from train_from_scratch import FaceClassifier


def load_model(checkpoint_path: str, device):
    checkpoint = torch.load(checkpoint_path, map_location=device)
    
    num_classes = checkpoint['num_classes']
    use_arcface = checkpoint.get('use_arcface', False)
    use_attention = checkpoint.get('use_attention', True)
    
    model = FaceClassifier(
        num_classes=num_classes,
        use_arcface=use_arcface,
        use_attention=use_attention
    )
    
    state_dict = checkpoint['model_state']
    if list(state_dict.keys())[0].startswith('module.'):
        state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}
    
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    
    return model


def get_tta_transforms(img_size: int):
    normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    
    base_tfm = transforms.Compose([
        transforms.Resize(int(img_size * 1.15)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        normalize
    ])
    
    hflip_tfm = transforms.Compose([
        transforms.Resize(int(img_size * 1.15)),
        transforms.CenterCrop(img_size),
        transforms.RandomHorizontalFlip(p=1.0),
        transforms.ToTensor(),
        normalize
    ])
    
    zoom_tfm = transforms.Compose([
        transforms.Resize(int(img_size * 1.25)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        normalize
    ])
    
    shrink_tfm = transforms.Compose([
        transforms.Resize(int(img_size * 1.05)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        normalize
    ])
    
    return [base_tfm, hflip_tfm, zoom_tfm, shrink_tfm]


def predict_with_tta(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    print(f"Loading model from {args.checkpoint}")
    model = load_model(args.checkpoint, device)
    
    with open(args.classes, 'r') as f:
        classes = json.load(f)
    print(f"Number of classes: {len(classes)}")
    
    with open(args.test_list, 'r') as f:
        test_files = [line.strip() for line in f if line.strip()]
    print(f"Number of test images: {len(test_files)}")
    
    if args.tta:
        transforms_list = get_tta_transforms(args.img_size)
        print(f"Using TTA with {len(transforms_list)} augmentations")
    else:
        transforms_list = [transforms.Compose([
            transforms.Resize(int(args.img_size * 1.15)),
            transforms.CenterCrop(args.img_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])]
        print("Using single inference (no TTA)")
    
    results = []
    with torch.no_grad():
        for filename in tqdm(test_files, desc='Predicting'):
            img_path = os.path.join(args.test_dir, filename)
            
            try:
                img = Image.open(img_path).convert('RGB')
                
                all_outputs = []
                for tfm in transforms_list:
                    img_tensor = tfm(img).unsqueeze(0).to(device)
                    outputs = model(img_tensor, None)
                    all_outputs.append(outputs)
                
                avg_output = torch.stack(all_outputs).mean(dim=0)
                _, predicted = avg_output.max(1)
                pred_class = classes[predicted.item()]
                
                results.append((filename, pred_class))
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                results.append((filename, classes[0]))
    
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = out_dir / 'submission.csv'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('id,label\n')
        for img_id, label in results:
            f.write(f'{img_id},{label}\n')
    
    print(f"\n✓ Predictions saved to {output_file}")
    print(f"Total predictions: {len(results)}")
    print(f"\nPreview (first 5 rows):")
    print("=" * 40)
    for i, (img_id, label) in enumerate(results[:5]):
        print(f"{img_id},{label}")
    print("=" * 40)


def parse_args():
    p = argparse.ArgumentParser(description='Predict with optional TTA')
    p.add_argument('--checkpoint', type=str, required=True, help='Model checkpoint')
    p.add_argument('--classes', type=str, required=True, help='Classes JSON file')
    p.add_argument('--test-dir', type=str, required=True, help='Test images directory')
    p.add_argument('--test-list', type=str, required=True, help='Test list file')
    p.add_argument('--img-size', type=int, default=224, help='Image size')
    p.add_argument('--out-dir', type=str, default='predictions', help='Output directory')
    p.add_argument('--tta', action='store_true', help='Use Test Time Augmentation')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    predict_with_tta(args)
