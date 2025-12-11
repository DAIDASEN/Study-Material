import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm

from config import Config
from models import AneurysmClassifier, HybridLoss
from dataset import IADataset

def train():
    # Setup
    device = torch.device(Config.DEVICE if torch.cuda.is_available() else "cpu")
    
    # Data Loading
    train_dataset = IADataset(
        metadata_csv="./data/processed/train_meta.csv", 
        root_dir=Config.ROI_DIR
    )
    train_loader = DataLoader(
        train_dataset, 
        batch_size=Config.BATCH_SIZE, 
        shuffle=True, 
        num_workers=4
    )

    # Model Initialization
    model = AneurysmClassifier(num_classes=Config.NUM_CLASSES).to(device)
    
    # Loss and Optimizer
    criterion = HybridLoss()
    optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE)

    # Training Loop
    model.train()
    print(f"Starting training on {device}...")
    
    for epoch in range(Config.EPOCHS):
        epoch_loss = 0.0
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{Config.EPOCHS}")

        for images, labels in progress_bar:
            images = images.to(device)
            labels = labels.to(device)

            # Forward
            optimizer.zero_grad()
            outputs = model(images)

            # Backward
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            progress_bar.set_postfix(loss=loss.item())

        avg_loss = epoch_loss / len(train_loader)
        print(f"Epoch {epoch+1} Complete. Avg Loss: {avg_loss:.4f}")
        
        # Save checkpoint
        torch.save(model.state_dict(), f"checkpoints/epoch_{epoch+1}.pth")

if __name__ == "__main__":
    train()