"""
FER2013-based Emotion Detection
Uses a pre-trained model trained on the FER2013 dataset for accurate emotion recognition
"""

import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import os
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class FER2013CNN(nn.Module):
    """
    CNN model for FER2013 emotion recognition.
    Architecture designed for the 48x48 grayscale input of FER2013.
    """
    def __init__(self, num_classes=7):
        super(FER2013CNN, self).__init__()
        
        # Convert to grayscale first
        self.grayscale = nn.Conv2d(3, 1, kernel_size=1)
        
        # Feature extraction layers
        self.features = nn.Sequential(
            # Block 1: 48x48 -> 24x24
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25),
            
            # Block 2: 24x24 -> 12x12
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25),
            
            # Block 3: 12x12 -> 6x6
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25),
            
            # Block 4: 6x6 -> 3x3
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25),
        )
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512 * 3 * 3, 2048),
            nn.BatchNorm1d(2048),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(2048, 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(1024, num_classes),
        )
        
    def forward(self, x):
        # Convert to grayscale
        x = self.grayscale(x)
        x = self.features(x)
        x = self.classifier(x)
        return x


class FER2013Detector:
    """
    Emotion detector using FER2013-trained model.
    Maps 7 emotions: angry, disgust, fear, happy, sad, surprise, neutral
    """
    
    # FER2013 emotion labels
    EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.model_path = None
        self.is_loaded = False
        
        # Image preprocessing for FER2013
        self.transform = transforms.Compose([
            transforms.Resize((48, 48)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        
    def load_model(self):
        """Load the FER2013 trained model"""
        if self.is_loaded:
            return True
            
        # Create model
        self.model = FER2013CNN(num_classes=7).to(self.device)
        
        # Model path - check for trained model first
        self.model_path = PROJECT_ROOT / "models" / "weights" / "fer2013_cnn.pth"
        best_model_path = PROJECT_ROOT / "models" / "weights" / "fer2013_cnn_best.pth"
        
        # Try to load the best model first, then regular model
        load_path = None
        if best_model_path.exists():
            load_path = best_model_path
            print(f"Loading best trained model from {load_path}")
        elif self.model_path.exists():
            load_path = self.model_path
            print(f"Loading trained model from {load_path}")
        
        if load_path and load_path.exists():
            try:
                state_dict = torch.load(load_path, map_location=self.device, weights_only=True)
                self.model.load_state_dict(state_dict)
                print("Successfully loaded FER2013 trained model!")
            except Exception as e:
                print(f"Could not load trained model weights: {e}")
                print("Using untrained model - results may be less accurate")
        else:
            print("No trained model found. Model will use random weights.")
            print("Run train_fer2013.py to train the model on FER2013 dataset.")
            
        self.model.eval()
        self.is_loaded = True
        return True
    
    def preprocess_face(self, face_image):
        """Preprocess face image for the model"""
        if face_image is None or (isinstance(face_image, np.ndarray) and face_image.size == 0):
            return None
            
        try:
            # Convert to PIL Image if needed
            if isinstance(face_image, np.ndarray):
                face_image = Image.fromarray(face_image)
                
            # Apply transforms
            tensor = self.transform(face_image)
            return tensor
        except Exception as e:
            print(f"Preprocessing error: {e}")
            return None
    
    def detect_emotion(self, face_crops):
        """
        Detect emotions from face crops using FER2013 model.
        
        Args:
            face_crops: List of face image arrays (BGR format)
            
        Returns:
            List of [emotion, confidence] pairs
        """
        # Load model if not already loaded
        if not self.is_loaded:
            self.load_model()
            
        results = []
        
        for face_image in face_crops:
            if face_image is None or (isinstance(face_image, np.ndarray) and face_image.size == 0):
                results.append(['neutral', 50.0])
                continue
            
            try:
                # Convert BGR to RGB if needed
                if isinstance(face_image, np.ndarray) and len(face_image.shape) == 3:
                    if face_image.shape[2] == 3:
                        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                
                # Preprocess
                tensor = self.preprocess_face(face_image)
                if tensor is None:
                    results.append(['neutral', 50.0])
                    continue
                    
                # Add batch dimension
                tensor = tensor.unsqueeze(0).to(self.device)
                
                # Get prediction
                with torch.no_grad():
                    output = self.model(tensor)
                    probabilities = torch.nn.functional.softmax(output, dim=1)
                    
                # Get top prediction
                confidence, predicted_idx = torch.max(probabilities, 1)
                emotion_idx = predicted_idx.item()
                confidence_val = confidence.item() * 100
                
                # Map to emotion label
                emotion = self.EMOTION_LABELS[emotion_idx]
                
                results.append([emotion, confidence_val])
                
            except Exception as e:
                print(f"Detection error: {e}")
                results.append(['neutral', 50.0])
                continue
        
        return results


# Global instance
fer_detector = FER2013Detector()


def detect_emotion_fer(face_crops):
    """Wrapper function for FER2013-based emotion detection"""
    return fer_detector.detect_emotion(face_crops)

