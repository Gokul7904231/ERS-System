"""
Model Manager
Centralized model loading with proper caching.
Ensures models are loaded once and cached across Streamlit reruns.
"""

import streamlit as st

from src.core.utils.torch_utils import select_device


@st.cache_resource
def load_models():
    """Load and cache all ML models.
    
    Returns a dict of model resources. The caller assigns to session_state.
    This function is cached by Streamlit — models are loaded once per session.
    """
    import torch
    from src.core.emotion_detector import init
    from src.core.fer_detector import FER2013Detector
    from src.core.utils.general import attempt_load
    from pathlib import Path

    # Disable gradient computation globally — inference only, saves memory
    torch.set_grad_enabled(False)

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

    # Select device
    device = select_device('')

    # Initialize RepVGG emotion model
    init(device)

    # Load YOLOv7 face detection model
    weights_path = PROJECT_ROOT / "models" / "weights" / "yolov7-tiny-face.pt"
    if not weights_path.exists():
        weights_path = PROJECT_ROOT / "models" / "weights" / "yolov7-tiny.pt"
        if not weights_path.exists():
            raise FileNotFoundError(
                f"YOLOv7 model weights not found. "
                f"Please place yolov7-tiny-face.pt or yolov7-tiny.pt "
                f"in {PROJECT_ROOT / 'models' / 'weights'}"
            )

    face_model = attempt_load(str(weights_path), map_location=device)
    face_model.eval()

    # Initialize FER2013 detector
    fer_detector = FER2013Detector()
    fer_detector.load_model()

    # --- Advanced pipeline (EfficientNet-B4 + CBAM) ---
    advanced_detector = None
    emotion_smoother = None
    try:
        from src.core.advanced.advanced_detector import AdvancedEmotionDetector
        from src.core.advanced.temporal_smoother import TemporalEmotionSmoother

        adv = AdvancedEmotionDetector()
        loaded = adv.init(device)
        if loaded:
            advanced_detector = adv
            emotion_smoother = TemporalEmotionSmoother(buffer_size=15)
            print("[ModelManager] Advanced EfficientNet+CBAM pipeline activated.")
        else:
            print("[ModelManager] Advanced weights not found — using RepVGG/FER fallback.")
    except Exception as e:
        print(f"[ModelManager] Advanced pipeline unavailable: {e}")

    return {
        "device": device,
        "face_model": face_model,
        "fer": fer_detector,
        "advanced_detector": advanced_detector,
        "emotion_smoother": emotion_smoother,
    }

