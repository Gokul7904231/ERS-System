"""
EfficientNet-B4 + CBAM Emotion Classification Model

Transfer-learning backbone pretrained on ImageNet.
CBAM attention inserted after the backbone features.
Classifier head maps to 8 emotion classes.
"""

import torch
import torch.nn as nn
import torchvision.models as models

from src.core.advanced.cbam import CBAM


# Same 8 classes used throughout the project
EMOTION_CLASSES = (
    "anger", "contempt", "disgust", "fear",
    "happy", "neutral", "sad", "surprise",
)


class EfficientNetEmotionModel(nn.Module):
    """EfficientNet-B4 backbone + CBAM + FC head for 8-class emotion recognition."""

    def __init__(self, num_classes=8, pretrained=True):
        super().__init__()

        # Load EfficientNet-B4 backbone
        weights = models.EfficientNet_B4_Weights.DEFAULT if pretrained else None
        backbone = models.efficientnet_b4(weights=weights)

        # Extract feature layers (everything except the classifier)
        self.features = backbone.features  # Output: (B, 1792, 12, 12) for 380×380 input

        # CBAM attention on top of backbone features
        self.attention = CBAM(in_channels=1792, reduction=16, spatial_kernel=7)

        # Global average pooling
        self.pool = nn.AdaptiveAvgPool2d(1)

        # Classifier head
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.4),
            nn.Linear(1792, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.attention(x)
        x = self.pool(x)
        x = x.flatten(1)
        x = self.classifier(x)
        return x

    def get_probabilities(self, x):
        """Forward pass + softmax → probability distribution."""
        logits = self.forward(x)
        return torch.softmax(logits, dim=1)
