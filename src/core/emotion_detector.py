import torch
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
from pathlib import Path
import streamlit as st

from PIL import Image
from src.core.repvgg import create_RepVGG_A0 as create

# Lazy-loaded model — NOT created at import time
_model = None
_device = None

# 8 Emotions
emotions = ("anger","contempt","disgust","fear","happy","neutral","sad","surprise")

def init(device):
    """Initialize the RepVGG emotion model (lazy — only creates model on first call)."""
    global _model, _device
    _device = device

    if _model is None:
        _model = create(deploy=True)

    _model.to(device)
    # load weights from package-relative path
    # Updated weights_path
    weights_path = Path(__file__).resolve().parent.parent.parent / "models" / "weights" / "repvgg.pth"
    try:
        if not weights_path.exists():
            st.error(f"FATAL ERROR: RepVGG emotion model weights not found at {weights_path}. Emotion detection will not work correctly. Please ensure 'repvgg.pth' is in the 'models/weights/' directory.")
            # Optionally, you might want to raise an exception here to halt execution
            # Or, set a flag so that `detect_emotion` can return an error
            raise FileNotFoundError(f"RepVGG weights not found at {weights_path}")
        state = torch.load(str(weights_path), map_location=device, weights_only=False)
        _model.load_state_dict(state)
        print(f"RepVGG weights loaded from {weights_path}") # Confirmation
    except FileNotFoundError as fnfe:
        # Re-raise the specific FileNotFoundError to ensure it's handled upstream if necessary
        raise fnfe
    except Exception as e:
        # log error and continue with uninitialized weights (random)
        st.error(f"ERROR: Could not load emotion model weights (RepVGG): {e}. Emotion detection will not work correctly.")
        print(f"Warning: could not load emotion model weights: {e}")

    # Save to eval
    cudnn.benchmark = True
    _model.eval()

def detect_emotion(images, device=None, conf=True):
    """Detect emotions from a list of face crop images using RepVGG model."""
    used_device = device if device is not None else _device
    with torch.no_grad():
        # Normalise and transform images
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
        x = torch.stack([transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                normalize,
            ])(Image.fromarray(image)) for image in images])
        # Feed through the model
        y = _model(x.to(used_device))
        result = []
        for i in range(y.size()[0]):
            max_val, predicted_idx = y[i].max(0)
            emotion_idx = predicted_idx.item()
            result.append([emotions[emotion_idx], y[i][emotion_idx].item() * 100])
    return result
