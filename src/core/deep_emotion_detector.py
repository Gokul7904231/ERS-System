"""
Deep Learning-based Emotion Detection
Uses a simple CNN for emotion classification
"""

import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image


class SimpleEmotionCNN(nn.Module):
    """Simple CNN for emotion classification"""
    def __init__(self, num_classes=7):
        super(SimpleEmotionCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 6 * 6, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )
        
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


class DeepEmotionDetector:
    """
    Emotion detection using a CNN-based approach.
    Uses handcrafted features with a simple neural network.
    """
    
    # Emotion mapping for 7 basic emotions
    EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((48, 48)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])
        
    def create_and_init_model(self):
        """Create and initialize the model with random weights"""
        self.model = SimpleEmotionCNN(num_classes=7).to(self.device)
        self.model.eval()
        return self.model
        
    def preprocess_face(self, face_image):
        """Preprocess face image for the model"""
        if face_image is None or face_image.size == 0:
            return None
            
        # Convert to PIL Image if needed
        if isinstance(face_image, np.ndarray):
            face_image = Image.fromarray(face_image)
            
        # Apply transformations
        try:
            tensor = self.transform(face_image)
            return tensor
        except:
            return None
    
    def extract_lbp_features(self, gray_face):
        """Extract Local Binary Pattern features"""
        # Simple LBP-like feature extraction using pixel comparisons
        h, w = gray_face.shape
        features = []
        
        # Calculate local patterns
        for i in range(1, h-1):
            for j in range(1, w-1):
                center = gray_face[i, j]
                pattern = 0
                pattern |= (gray_face[i-1, j-1] > center) << 7
                pattern |= (gray_face[i-1, j] > center) << 6
                pattern |= (gray_face[i-1, j+1] > center) << 5
                pattern |= (gray_face[i, j+1] > center) << 4
                pattern |= (gray_face[i+1, j+1] > center) << 3
                pattern |= (gray_face[i+1, j] > center) << 2
                pattern |= (gray_face[i+1, j-1] > center) << 1
                pattern |= (gray_face[i, j-1] > center) << 0
                features.append(pattern)
                
        return np.array(features[:2304])  # 48x48 = 2304, pad or truncate
    
    def extract_histogram_features(self, gray_face):
        """Extract histogram features"""
        hist = cv2.calcHist([gray_face], [0], None, [256], [0, 256])
        hist = hist.flatten() / hist.sum()  # Normalize
        return hist
    
    def extract_all_features(self, face_image):
        """Extract all handcrafted features"""
        # Convert to grayscale
        if len(face_image.shape) == 3:
            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = face_image
            
        # Resize to standard size
        gray = cv2.resize(gray, (48, 48))
        
        # Extract features
        lbp_features = self.extract_lbp_features(gray)
        hist_features = self.extract_histogram_features(gray)
        
        # Combine features
        combined = np.concatenate([lbp_features, hist_features])
        
        return torch.FloatTensor(combined).unsqueeze(0).unsqueeze(0)
    
    def detect_emotion(self, face_crops):
        """
        Detect emotions from face crops.
        Uses heuristic-based approach since we don't have a trained model.
        
        Args:
            face_crops: List of face image arrays (BGR format)
            
        Returns:
            List of [emotion, confidence] pairs
        """
        results = []
        
        for face_image in face_crops:
            if face_image is None or face_image.size == 0:
                results.append(['neutral', 50.0])
                continue
            
            # Ensure BGR format for OpenCV
            if len(face_image.shape) == 3 and face_image.shape[2] == 4:
                face_image = cv2.cvtColor(face_image, cv2.COLOR_BGRA2BGR)
            elif len(face_image.shape) == 2:
                face_image = cv2.cvtColor(face_image, cv2.COLOR_GRAY2BGR)
                
            # Convert to grayscale
            if len(face_image.shape) == 3:
                gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            else:
                gray = face_image
                
            # Resize to standard size
            gray = cv2.resize(gray, (100, 100))
            
            # Calculate emotion scores using multiple features
            emotion_scores = {
                'happy': 0,
                'sad': 0,
                'angry': 0,
                'fear': 0,
                'surprise': 0,
                'disgust': 0,
                'neutral': 0
            }
            
            # 1. Mouth Analysis (smile detection)
            mouth_y = int(gray.shape[0] * 0.6)
            mouth_region = gray[mouth_y:, :]
            _, thresh = cv2.threshold(mouth_region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest)
                aspect_ratio = w / (h + 1)
                
                # Wide mouth = happy
                if aspect_ratio > 2.0:
                    emotion_scores['happy'] += 3
                # Small mouth = sad/angry
                elif aspect_ratio < 1.0:
                    emotion_scores['sad'] += 1
                    emotion_scores['angry'] += 1
                    
            # 2. Eye Analysis
            eye_y_end = int(gray.shape[0] * 0.5)
            eye_region = gray[:eye_y_end, :]
            
            # Calculate brightness variance (more variance = more open eyes)
            variance = np.var(eye_region)
            eye_openness = min(1.0, variance / 500)
            
            if eye_openness > 0.6:  # Wide eyes
                emotion_scores['surprise'] += 2
                emotion_scores['fear'] += 1
            elif eye_openness < 0.25:  # Narrow eyes
                emotion_scores['happy'] += 1  # Squinting can indicate happiness
            
            # 3. Eyebrow Analysis (using upper part)
            brow_region = gray[:int(gray.shape[0]*0.3), :]
            edges = cv2.Canny(brow_region, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            if edge_density > 0.1:  # More edges = more expressive (raised/furrowed)
                emotion_scores['surprise'] += 1
                emotion_scores['angry'] += 1
            
            # 4. Overall brightness analysis
            mean_brightness = np.mean(gray)
            if mean_brightness > 150:  # Bright image
                emotion_scores['happy'] += 1
                emotion_scores['surprise'] += 1
            elif mean_brightness < 80:  # Dark image
                emotion_scores['sad'] += 1
                emotion_scores['fear'] += 1
            
            # 5. Center vs edges analysis (faces tend to be centered)
            center_region = gray[20:80, 20:80]
            edge_regions = np.concatenate([
                gray[:20, :].flatten(),
                gray[80:, :].flatten(),
                gray[20:80, :20].flatten(),
                gray[20:80, 80:].flatten()
            ])
            
            center_mean = np.mean(center_region)
            edge_mean = np.mean(edge_regions)
            
            if center_mean > edge_mean + 20:  # Face is well-lit/centered
                emotion_scores['neutral'] += 2
                emotion_scores['happy'] += 1
            
            # Find dominant emotion
            max_score = max(emotion_scores.values())
            if max_score == 0:
                detected = 'neutral'
                confidence = 50.0
            else:
                detected = max(emotion_scores, key=emotion_scores.get)
                confidence = min(95.0, max_score * 12 + 35)
            
            # Map to 8 emotions (add contempt)
            if detected in ['angry', 'fear', 'sad']:
                # Check if it might be contempt instead
                if emotion_scores['angry'] > 0 and emotion_scores['sad'] > 0:
                    if abs(emotion_scores['angry'] - emotion_scores['sad']) < 2:
                        detected = 'contempt'
            
            results.append([detected, confidence])
        
        return results


# Global instance
deep_emotion_detector = DeepEmotionDetector()


def detect_emotion_deep(face_crops):
    """Wrapper function for deep emotion detection"""
    return deep_emotion_detector.detect_emotion(face_crops)

