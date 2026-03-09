"""
Training Script: EfficientNet-B4 + CBAM on FER2013 (+ optional RAF-DB)

Usage:
    python src/core/advanced/train_efficientnet.py

Features:
    - Transfer learning from ImageNet-pretrained EfficientNet-B4
    - CBAM attention module
    - Heavy data augmentation (flip, rotate, jitter, blur)
    - Weighted CrossEntropyLoss for class imbalance
    - ReduceLROnPlateau scheduler
    - Saves best model to models/weights/efficientnet_emotion.pth
"""

import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
from pathlib import Path
from collections import Counter

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.advanced.efficientnet_emotion import EfficientNetEmotionModel, EMOTION_CLASSES


# =====================================================================
# Dataset
# =====================================================================

class EmotionDataset(Dataset):
    """
    Loads emotion images from a directory structure:
        root/train/<emotion_name>/*.jpg
        root/test/<emotion_name>/*.jpg

    Supports both FER2013 and RAF-DB label conventions.
    """

    # Map common label variations to our canonical 8 classes
    LABEL_MAP = {
        "angry": "anger", "anger": "anger",
        "contempt": "contempt",
        "disgust": "disgust",
        "fear": "fear", "scared": "fear",
        "happy": "happy", "happiness": "happy",
        "neutral": "neutral",
        "sad": "sad", "sadness": "sad",
        "surprise": "surprise", "surprised": "surprise",
    }

    def __init__(self, root_dir, split="train", transform=None):
        self.transform = transform
        self.images = []
        self.labels = []

        split_dir = Path(root_dir) / split
        if not split_dir.exists():
            raise FileNotFoundError(f"Dataset split not found: {split_dir}")

        emo_to_idx = {e: i for i, e in enumerate(EMOTION_CLASSES)}

        for subdir in sorted(split_dir.iterdir()):
            if not subdir.is_dir():
                continue
            canonical = self.LABEL_MAP.get(subdir.name.lower())
            if canonical is None:
                print(f"  [skip] Unknown emotion folder: {subdir.name}")
                continue
            idx = emo_to_idx[canonical]
            for img_path in subdir.glob("*"):
                if img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}:
                    self.images.append(str(img_path))
                    self.labels.append(idx)

        print(f"  Loaded {len(self.images)} images from {split_dir}")

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        try:
            img = Image.open(self.images[idx]).convert("RGB")
        except Exception:
            img = Image.new("RGB", (224, 224), (0, 0, 0))
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]


# =====================================================================
# Transforms
# =====================================================================

def get_train_transforms():
    return transforms.Compose([
        transforms.Resize((400, 400)),
        transforms.RandomCrop(380),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
        transforms.RandomApply([transforms.GaussianBlur(3)], p=0.3),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])


def get_val_transforms():
    return transforms.Compose([
        transforms.Resize((380, 380)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])


# =====================================================================
# Training helpers
# =====================================================================

def compute_class_weights(dataset):
    """Compute inverse-frequency weights for imbalanced classes."""
    counts = Counter(dataset.labels)
    total = len(dataset.labels)
    num_classes = len(EMOTION_CLASSES)
    weights = []
    for i in range(num_classes):
        c = counts.get(i, 1)
        weights.append(total / (num_classes * c))
    return torch.FloatTensor(weights)


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (images, labels) in enumerate(loader):
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, preds = outputs.max(1)
        total += labels.size(0)
        correct += preds.eq(labels).sum().item()

        if (batch_idx + 1) % 20 == 0:
            print(f"    batch {batch_idx+1}/{len(loader)}  loss={loss.item():.4f}")

    return running_loss / len(loader), 100.0 * correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        running_loss += loss.item()
        _, preds = outputs.max(1)
        total += labels.size(0)
        correct += preds.eq(labels).sum().item()

    return running_loss / len(loader), 100.0 * correct / total


# =====================================================================
# Main
# =====================================================================

def main():
    print("=" * 60)
    print("EfficientNet-B4 + CBAM  —  Emotion Recognition Training")
    print("=" * 60)

    # ---- Config ----
    DATA_DIR = PROJECT_ROOT / "fer2013"
    SAVE_PATH = PROJECT_ROOT / "models" / "weights" / "efficientnet_emotion.pth"
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)

    BATCH_SIZE = 32
    NUM_EPOCHS = 30
    LR = 1e-4
    WEIGHT_DECAY = 1e-4

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nDevice: {device}")

    # ---- Datasets ----
    print("\nLoading datasets...")
    train_ds = EmotionDataset(DATA_DIR, "train", get_train_transforms())
    val_ds = EmotionDataset(DATA_DIR, "test", get_val_transforms())

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                              num_workers=2, pin_memory=(device.type == "cuda"))
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False,
                            num_workers=2, pin_memory=(device.type == "cuda"))

    print(f"Train batches: {len(train_loader)},  Val batches: {len(val_loader)}")

    # ---- Model ----
    model = EfficientNetEmotionModel(num_classes=8, pretrained=True).to(device)
    total_params = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nParameters: {total_params:,} total, {trainable:,} trainable")

    # ---- Loss (weighted for imbalance) ----
    class_weights = compute_class_weights(train_ds).to(device)
    print(f"Class weights: {class_weights.tolist()}")
    criterion = nn.CrossEntropyLoss(weight=class_weights)

    # ---- Optimizer + Scheduler ----
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min",
                                                      factor=0.5, patience=3)

    # ---- Training loop ----
    best_val_acc = 0.0

    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60)

    for epoch in range(1, NUM_EPOCHS + 1):
        print(f"\nEpoch {epoch}/{NUM_EPOCHS}")
        print("-" * 40)

        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step(val_loss)

        lr_now = optimizer.param_groups[0]["lr"]
        print(f"  Train loss={train_loss:.4f}  acc={train_acc:.2f}%")
        print(f"  Val   loss={val_loss:.4f}  acc={val_acc:.2f}%  lr={lr_now:.1e}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), str(SAVE_PATH))
            print(f"  *** Saved best model (val acc {val_acc:.2f}%) ***")

    # ---- Final evaluation ----
    print("\n" + "=" * 60)
    print(f"Training complete.  Best val accuracy: {best_val_acc:.2f}%")
    print(f"Model saved to: {SAVE_PATH}")
    print("=" * 60)

    # Per-class accuracy
    model.load_state_dict(torch.load(str(SAVE_PATH), map_location=device, weights_only=True))
    model.eval()
    class_correct = [0] * 8
    class_total = [0] * 8

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            _, preds = model(images).max(1)
            for i in range(len(labels)):
                lab = labels[i].item()
                class_total[lab] += 1
                if preds[i] == labels[i]:
                    class_correct[lab] += 1

    print("\nPer-class accuracy:")
    for i, emo in enumerate(EMOTION_CLASSES):
        acc = 100.0 * class_correct[i] / class_total[i] if class_total[i] > 0 else 0
        print(f"  {emo:>10s}: {acc:6.2f}%  ({class_correct[i]}/{class_total[i]})")


if __name__ == "__main__":
    main()
