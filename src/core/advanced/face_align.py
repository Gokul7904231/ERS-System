"""
Face Alignment using 5-point Landmarks

Aligns detected faces so both eyes are horizontal, then crops
and resizes to 224×224 for the emotion classification model.
"""

import cv2
import numpy as np


def align_face(image, landmarks, output_size=380):
    """
    Align a face using left_eye and right_eye landmarks.

    Args:
        image: RGB numpy array (H, W, 3)
        landmarks: dict with at least 'left_eye' and 'right_eye' as (x, y) tuples
        output_size: square output dimension (default 380 for EfficientNet-B4)

    Returns:
        Aligned, cropped face as numpy array (output_size, output_size, 3)
    """
    left_eye = np.array(landmarks["left_eye"], dtype=np.float32)
    right_eye = np.array(landmarks["right_eye"], dtype=np.float32)

    # Compute rotation angle to make eyes horizontal
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dy, dx))

    # Center of rotation = midpoint between eyes
    eye_center = ((left_eye[0] + right_eye[0]) / 2.0,
                  (left_eye[1] + right_eye[1]) / 2.0)

    # Inter-eye distance → determines crop scale
    eye_dist = np.linalg.norm(right_eye - left_eye)
    if eye_dist < 1.0:
        eye_dist = 1.0

    # Desired inter-eye distance in the output image (~35% of output width)
    desired_eye_dist = output_size * 0.35
    scale = desired_eye_dist / eye_dist

    # Rotation matrix
    M = cv2.getRotationMatrix2D(eye_center, angle, scale)

    # Shift so the eye center lands at a good position in the output
    # Eyes at roughly 35% from top, centered horizontally
    M[0, 2] += (output_size * 0.5 - eye_center[0])
    M[1, 2] += (output_size * 0.35 - eye_center[1])

    # Apply affine transform
    aligned = cv2.warpAffine(
        image, M, (output_size, output_size),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101,
    )

    return aligned


def crop_face_with_padding(image, bbox, padding_pct=0.25):
    """
    Crop face from image with percentage-based padding.
    Used as a simpler alternative when landmarks are not available.

    Args:
        image: RGB numpy array
        bbox: (x1, y1, x2, y2)
        padding_pct: padding as fraction of face size

    Returns:
        Cropped face as numpy array
    """
    h, w = image.shape[:2]
    x1, y1, x2, y2 = bbox
    fw, fh = x2 - x1, y2 - y1

    pad_w = int(fw * padding_pct)
    pad_h = int(fh * padding_pct)

    x1 = max(0, x1 - pad_w)
    y1 = max(0, y1 - pad_h)
    x2 = min(w, x2 + pad_w)
    y2 = min(h, y2 + pad_h)

    crop = image[y1:y2, x1:x2]
    if crop.size == 0:
        return image  # safety fallback
    return crop
