"""
FER2013 Dataset Training Script
Trains a CNN model on the FER2013 dataset for high-accuracy emotion recognition
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class FER2013Dataset(Dataset):
    """
    Custom Dataset for FER2013 emotion recognition.
    Loads images from train/test directories.
    """
    
    # Emotion labels matching FER2013
    EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    EMOTION_TO_IDX = {emo: idx for idx, emo in enumerate(EMOTION_LABELS)}
    IDX_TO_EMOTION = {idx: emo for idx, emo in enumerate(EMOTION_LABELS)}
    
    def __init__(self, root_dir, split='train', transform=None):
        """
        Args:
            root_dir: Root directory containing 'train' and 'test' folders
            split: 'train' or 'test'
            transform: Optional transform to be applied on images
        """
        self.root_dir = Path(root_dir)
        self.split = split
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load images from the appropriate directory
        split_dir = self.root_dir / split
        
        if not split_dir.exists():
            raise ValueError(f"Directory not found: {split_dir}")
        
        # Load each emotion class directory
        for emotion in self.EMOTION_LABELS:
            emotion_dir = split_dir / emotion
            if emotion_dir.exists():
                # Get all image files in this emotion directory
                image_files = list(emotion_dir.glob('*.jpg')) + list(emotion_dir.glob('*.png'))
                for img_path in image_files:
                    self.images.append(img_path)
                    self.labels.append(self.EMOTION_TO_IDX[emotion])
        
        print(f"Loaded {len(self.images)} images from {split} set")
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # Load and convert image
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            # Return a black image as fallback
            image = Image.new('RGB', (48, 48), (0, 0, 0))
        
        if self.transform:
            image = self.transform(image)
        
        return image, label


class FER2013CNN(nn.Module):
    """
    Simple CNN model for FER2013 emotion recognition.
    Optimized for faster training while maintaining good accuracy.
    """
    
    def __init__(self, num_classes=7):
        super(FER2013CNN, self).__init__()
        
        # Feature extraction layers - simpler architecture
        self.features = nn.Sequential(
            # Block 1: 48x48 -> 24x24
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            
            # Block 2: 24x24 -> 12x12
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            
            # Block 3: 12x12 -> 6x6
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 6 * 6, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )
        
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


def get_transforms(train=True):
    """Get data transforms for training and testing"""
    
    if train:
        return transforms.Compose([
            transforms.Resize((48, 48)),
            transforms.Grayscale(num_output_channels=1),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((48, 48)),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for batch_idx, (images, labels) in enumerate(dataloader):
        images = images.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        if (batch_idx + 1) % 10 == 0:
            print(f'  Batch {batch_idx + 1}/{len(dataloader)}, Loss: {loss.item():.4f}')
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """Validate the model"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc


def count_images_in_dataset(root_dir):
    """Count total images in train and test sets"""
    train_count = 0
    test_count = 0
    
    for emotion in FER2013Dataset.EMOTION_LABELS:
        train_dir = Path(root_dir) / 'train' / emotion
        test_dir = Path(root_dir) / 'test' / emotion
        
        if train_dir.exists():
            train_count += len(list(train_dir.glob('*.jpg'))) + len(list(train_dir.glob('*.png')))
        if test_dir.exists():
            test_count += len(list(test_dir.glob('*.jpg'))) + len(list(test_dir.glob('*.png')))
    
    return train_count, test_count


def main():
    """Main training function"""
    
    print("=" * 60)
    print("FER2013 Emotion Recognition Training")
    print("=" * 60)
    
    # Configuration
    DATA_DIR = PROJECT_ROOT / "fer2013"
    MODEL_DIR = PROJECT_ROOT / "models" / "weights"
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Training hyperparameters - optimized for faster training
    BATCH_SIZE = 32
    NUM_EPOCHS = 10
    LEARNING_RATE = 0.001
    WEIGHT_DECAY = 1e-4
    
    # Check dataset
    train_count, test_count = count_images_in_dataset(DATA_DIR)
    print(f"\nDataset: {train_count} training images, {test_count} test images")
    
    if train_count == 0:
        print("ERROR: No training images found!")
        return
    
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nUsing device: {device}")
    
    # Create datasets
    train_dataset = FER2013Dataset(
        root_dir=DATA_DIR,
        split='train',
        transform=get_transforms(train=True)
    )
    
    test_dataset = FER2013Dataset(
        root_dir=DATA_DIR,
        split='test',
        transform=get_transforms(train=False)
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=2,
        pin_memory=True if torch.cuda.is_available() else False
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2,
        pin_memory=True if torch.cuda.is_available() else False
    )
    
    print(f"\nTraining batches: {len(train_loader)}")
    print(f"Test batches: {len(test_loader)}")
    
    # Create model
    model = FER2013CNN(num_classes=7).to(device)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nTotal parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    
    # Loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)
    
    # Training loop
    print("\n" + "=" * 60)
    print("Starting Training...")
    print("=" * 60)
    
    best_test_acc = 0.0
    best_model_state = None
    
    for epoch in range(NUM_EPOCHS):
        print(f"\nEpoch {epoch + 1}/{NUM_EPOCHS}")
        print("-" * 40)
        
        # Train
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        
        # Validate
        val_loss, val_acc = validate(model, test_loader, criterion, device)
        print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        
        # Update learning rate
        scheduler.step(val_loss)
        
        # Save best model
        if val_acc > best_test_acc:
            best_test_acc = val_acc
            best_model_state = model.state_dict().copy()
            print(f"*** New best model! Val Acc: {val_acc:.2f}% ***")
            
            # Save best model immediately
            best_model_path = MODEL_DIR / "fer2013_cnn_best.pth"
            torch.save(best_model_state, best_model_path)
            print(f"Saved best model to {best_model_path}")
    
    # Load best model and save final
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    
    final_model_path = MODEL_DIR / "fer2013_cnn.pth"
    torch.save(model.state_dict(), final_model_path)
    print(f"\nFinal model saved to {final_model_path}")
    
    # Final evaluation
    print("\n" + "=" * 60)
    print("Final Evaluation on Test Set")
    print("=" * 60)
    
    final_loss, final_acc = validate(model, test_loader, criterion, device)
    print(f"Final Test Accuracy: {final_acc:.2f}%")
    
    # Per-class accuracy
    model.eval()
    class_correct = [0] * 7
    class_total = [0] * 7
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            
            for i in range(len(labels)):
                label = labels[i].item()
                class_total[label] += 1
                if predicted[i] == labels[i]:
                    class_correct[label] += 1
    
    print("\nPer-class accuracy:")
    for i in range(7):
        emotion = FER2013Dataset.IDX_TO_EMOTION[i]
        acc = 100. * class_correct[i] / class_total[i] if class_total[i] > 0 else 0
        print(f"  {emotion}: {acc:.2f}%")
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print(f"Best Test Accuracy: {best_test_acc:.2f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()

