"""
Face Preprocessing Pipeline

Standardizes face images before emotion model inference:
  1. CLAHE contrast enhancement
  2. Bilateral noise reduction
  3. Resize to 224×224
  4. ImageNet normalization → tensor
"""

import cv2
import numpy as np
import torch
import torchvision.transforms as T

# ImageNet normalization constants (used by EfficientNet pretrained weights)
_IMAGENET_MEAN = [0.485, 0.456, 0.406]
_IMAGENET_STD = [0.229, 0.224, 0.225]

# Reusable transform: tensor conversion + normalize
_to_tensor_and_normalize = T.Compose([
    T.ToTensor(),
    T.Normalize(mean=_IMAGENET_MEAN, std=_IMAGENET_STD),
])


def preprocess_face(face_image, output_size=380):
    """
    Full preprocessing pipeline: enhance → denoise → resize → normalize.

    Args:
        face_image: RGB numpy array of a cropped/aligned face
        output_size: target spatial size (default 380 for EfficientNet-B4)

    Returns:
        torch.Tensor of shape (3, output_size, output_size), normalized
    """
    img = face_image.copy()

    # --- 1. CLAHE contrast enhancement (on L channel of LAB) ---
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l_channel = lab[:, :, 0]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(l_channel)
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    # --- 2. Bilateral filter for noise reduction (preserves edges) ---
    img = cv2.bilateralFilter(img, d=5, sigmaColor=50, sigmaSpace=50)

    # --- 3. Resize to target size ---
    img = cv2.resize(img, (output_size, output_size), interpolation=cv2.INTER_LINEAR)

    # --- 4. Convert to tensor + ImageNet normalize ---
    tensor = _to_tensor_and_normalize(img)

    return tensor


def preprocess_batch(face_images, output_size=380):
    """
    Preprocess a list of face images into a stacked batch tensor.

    Args:
        face_images: list of RGB numpy arrays
        output_size: target spatial size

    Returns:
        torch.Tensor of shape (N, 3, output_size, output_size)
    """
    tensors = [preprocess_face(f, output_size) for f in face_images]
    return torch.stack(tensors)
