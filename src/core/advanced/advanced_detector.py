"""
Advanced Emotion Detector — Full Pipeline Orchestrator

Wires together:
    RetinaFace → Alignment → Preprocessing → EfficientNet+CBAM → TTA → Confidence Filter

Provides a drop-in replacement for the existing detection function.
Falls back to the original pipeline if the advanced model is not available.
"""

import cv2
import numpy as np
import torch
import torchvision.transforms.functional as TF
from pathlib import Path

from src.core.advanced.face_detector import detect_faces
from src.core.advanced.face_align import align_face, crop_face_with_padding
from src.core.advanced.face_preprocess import preprocess_face
from src.core.advanced.efficientnet_emotion import EfficientNetEmotionModel, EMOTION_CLASSES
from src.core.advanced.temporal_smoother import TemporalEmotionSmoother, CONFIDENCE_THRESHOLD

# Project paths
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_WEIGHTS_PATH = _PROJECT_ROOT / "models" / "weights" / "efficientnet_emotion.pth"


class AdvancedEmotionDetector:
    """
    Full upgraded emotion detection pipeline.

    Pipeline:
        1. RetinaFace face detection (+ Haar fallback)
        2. Face alignment via eye landmarks
        3. CLAHE + bilateral preprocessing
        4. EfficientNet-B4 + CBAM inference
        5. Test-Time Augmentation (TTA)
        6. Confidence filtering
    """

    def __init__(self):
        self.model = None
        self.device = None
        self.is_loaded = False
        self.use_tta = True  # enable TTA by default

    def init(self, device):
        """Load the EfficientNet+CBAM model if weights exist."""
        self.device = device

        if not _WEIGHTS_PATH.exists():
            print(f"[AdvancedDetector] Weights not found at {_WEIGHTS_PATH}")
            print("[AdvancedDetector] Will fall back to existing pipeline.")
            print("[AdvancedDetector] Train with: python src/core/advanced/train_efficientnet.py")
            self.is_loaded = False
            return False

        try:
            self.model = EfficientNetEmotionModel(num_classes=8, pretrained=False)
            state = torch.load(str(_WEIGHTS_PATH), map_location=device, weights_only=True)
            self.model.load_state_dict(state)
            self.model.to(device)
            self.model.eval()
            self.is_loaded = True
            print(f"[AdvancedDetector] EfficientNet+CBAM loaded from {_WEIGHTS_PATH}")
            return True
        except Exception as e:
            print(f"[AdvancedDetector] Failed to load model: {e}")
            self.is_loaded = False
            return False

    def detect(self, image):
        """
        Run the full advanced detection pipeline on an RGB image.

        Args:
            image: RGB numpy array (H, W, 3)

        Returns:
            list[dict] with keys: bbox, emotion, confidence, face_conf
        """
        if not self.is_loaded:
            return []

        # 1. Face detection (RetinaFace → Haar fallback)
        face_detections = detect_faces(image)
        if not face_detections:
            return []

        results = []

        for det in face_detections:
            bbox = det["bbox"]
            landmarks = det["landmarks"]
            face_conf = det["confidence"]

            # 2. Face alignment (380×380 for EfficientNet-B4)
            try:
                aligned = align_face(image, landmarks, output_size=380)
            except Exception:
                # Fallback: simple crop + resize
                crop = crop_face_with_padding(image, bbox)
                aligned = cv2.resize(crop, (380, 380))

            # 3. Preprocess
            tensor = preprocess_face(aligned)

            # 4. Inference (with optional TTA)
            with torch.no_grad():
                if self.use_tta:
                    probs = self._inference_with_tta(tensor)
                else:
                    batch = tensor.unsqueeze(0).to(self.device)
                    probs = self.model.get_probabilities(batch)[0]

            # 5. Get top prediction
            confidence, pred_idx = probs.max(0)
            emotion_idx = pred_idx.item()
            conf_val = confidence.item()

            # 6. Confidence filtering
            emotion = EMOTION_CLASSES[emotion_idx]
            if conf_val < CONFIDENCE_THRESHOLD:
                emotion = "neutral"
                conf_val = max(conf_val, CONFIDENCE_THRESHOLD)

            results.append({
                "bbox": bbox,
                "emotion": emotion,
                "confidence": conf_val * 100.0,
                "face_conf": face_conf * 100.0,
            })

        return results

    def _inference_with_tta(self, tensor):
        """
        Test-Time Augmentation: run inference on original + augmented
        versions, then average the probability distributions.

        Augmentations:
          1. Original
          2. Horizontal flip
          3. Slight brightness adjustment
        """
        augmented = [tensor]

        # Horizontal flip
        flipped = TF.hflip(tensor)
        augmented.append(flipped)

        # Slight brightness boost (+10%)
        bright = TF.adjust_brightness(tensor, brightness_factor=1.1)
        augmented.append(bright)

        # Stack and run batch inference
        batch = torch.stack(augmented).to(self.device)
        probs = self.model.get_probabilities(batch)

        # Average across augmentations
        avg_probs = probs.mean(dim=0)
        return avg_probs


# =====================================================================
# Module-level convenience function (drop-in for emotion_engine.py)
# =====================================================================

_detector_instance = AdvancedEmotionDetector()


def init_advanced_detector(device):
    """Initialize the global advanced detector. Returns True if loaded."""
    return _detector_instance.init(device)


def detect_emotions_advanced(image):
    """
    Drop-in advanced detection function.

    Args:
        image: RGB numpy array or PIL Image

    Returns:
        (results_list, error_string) matching the signature of
        emotion_engine.detect_faces_and_emotions()
    """
    from PIL import Image as PILImage

    if not _detector_instance.is_loaded:
        return None, "Advanced model not loaded"

    try:
        if isinstance(image, PILImage.Image):
            img = np.array(image)
        else:
            img = image

        # Ensure RGB
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        results = _detector_instance.detect(img)
        return results, None

    except Exception as e:
        return None, str(e)
