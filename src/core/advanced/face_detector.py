"""
RetinaFace-based Face Detection

Primary face detector providing:
  - High-accuracy bounding boxes
  - 5-point facial landmarks (left_eye, right_eye, nose, mouth_left, mouth_right)

Falls back to OpenCV Haar Cascade if RetinaFace is unavailable.
"""

import cv2
import numpy as np

# Try importing RetinaFace — graceful fallback if not installed
_RETINAFACE_AVAILABLE = False
try:
    from retinaface import RetinaFace as _RF
    _RETINAFACE_AVAILABLE = True
except ImportError:
    _RF = None

# Haar cascade fallback (always available via OpenCV)
_HAAR_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_faces(image):
    """
    Detect faces and landmarks in an RGB numpy image.

    Returns:
        list[dict] with keys:
            bbox  — (x1, y1, x2, y2)
            landmarks — dict with left_eye, right_eye, nose, mouth_left, mouth_right (each (x,y))
            confidence — float 0–1
    """
    if _RETINAFACE_AVAILABLE:
        return _detect_retinaface(image)
    return _detect_haar(image)


def _detect_retinaface(image):
    """Detect faces using the RetinaFace library."""
    results = []
    try:
        detections = _RF.detect_faces(image)
        if not detections:
            return _detect_haar(image)  # fallback

        for _key, det in detections.items():
            facial_area = det.get("facial_area", [])
            if len(facial_area) < 4:
                continue

            x1, y1, x2, y2 = int(facial_area[0]), int(facial_area[1]), int(facial_area[2]), int(facial_area[3])

            landmarks_raw = det.get("landmarks", {})
            landmarks = {
                "left_eye": tuple(map(int, landmarks_raw.get("left_eye", (0, 0)))),
                "right_eye": tuple(map(int, landmarks_raw.get("right_eye", (0, 0)))),
                "nose": tuple(map(int, landmarks_raw.get("nose", (0, 0)))),
                "mouth_left": tuple(map(int, landmarks_raw.get("mouth_left", (0, 0)))),
                "mouth_right": tuple(map(int, landmarks_raw.get("mouth_right", (0, 0)))),
            }

            results.append({
                "bbox": (x1, y1, x2, y2),
                "landmarks": landmarks,
                "confidence": float(det.get("score", 0.99)),
            })

    except Exception as e:
        print(f"[RetinaFace] Detection error: {e}, falling back to Haar")
        return _detect_haar(image)

    if not results:
        return _detect_haar(image)

    return results


def _detect_haar(image):
    """Fallback face detection using OpenCV Haar Cascade."""
    results = []
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_eq = cv2.equalizeHist(gray)
    faces = _HAAR_CASCADE.detectMultiScale(gray_eq, scaleFactor=1.05, minNeighbors=3, minSize=(40, 40))

    if faces is None or len(faces) == 0:
        return results

    for (x, y, w, h) in faces:
        x1, y1, x2, y2 = x, y, x + w, y + h

        # Estimate landmark positions from bounding box geometry
        cx, cy = x + w // 2, y + h // 2
        landmarks = {
            "left_eye": (x + int(w * 0.3), y + int(h * 0.35)),
            "right_eye": (x + int(w * 0.7), y + int(h * 0.35)),
            "nose": (cx, y + int(h * 0.55)),
            "mouth_left": (x + int(w * 0.35), y + int(h * 0.75)),
            "mouth_right": (x + int(w * 0.65), y + int(h * 0.75)),
        }

        results.append({
            "bbox": (x1, y1, x2, y2),
            "landmarks": landmarks,
            "confidence": 0.90,
        })

    return results
