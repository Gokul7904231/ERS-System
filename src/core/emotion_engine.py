"""
Emotion Detection Engine
Centralized detection pipeline: face detection, emotion classification, fusion, text analysis.
Extracted from app.py to separate ML logic from UI.
"""

import numpy as np
import torch
import cv2
import streamlit as st
from PIL import Image

from src.core.fer_detector import detect_emotion_fer
from src.core.utils.general import non_max_suppression, scale_coords
from src.utils.constants import EMOTION_COLORS, EMOTION_EMOJIS

# Module-level cached Haar cascade — loaded once, reused everywhere
_FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


# ===============================
# Core Detection
# ===============================

def detect_faces_and_emotions(image, conf_thres=0.5, iou_thres=0.45):
    """Detect faces and classify emotions in an image.
    
    Args:
        image: PIL Image or numpy array (RGB format)
        conf_thres: Confidence threshold for YOLO detection
        iou_thres: IoU threshold for NMS
        
    Returns:
        (results_list, error_string) — results is a list of dicts with
        'bbox', 'emotion', 'confidence', 'face_conf' keys.
    """
    if not st.session_state.models_loaded:
        return None, "Models not loaded"

    # --- Advanced pipeline (EfficientNet+CBAM) if available ---
    adv = st.session_state.get("advanced_detector")
    if adv is not None and adv.is_loaded:
        results, err = _detect_advanced(image, adv)
        if results is not None:
            return results, err
        # If advanced detection returned None, fall through to legacy pipeline


    try:
        device = st.session_state.device
        face_model = st.session_state.face_model

        if isinstance(image, Image.Image):
            img0 = np.array(image)
        else:
            img0 = image

        # Ensure 3-channel RGB
        if img0.ndim == 2:
            img0 = cv2.cvtColor(img0, cv2.COLOR_GRAY2RGB)
        elif img0.shape[2] == 4:
            img0 = cv2.cvtColor(img0, cv2.COLOR_RGBA2RGB)

        results = []
        face_crops = []
        boxes = []
        confidences = []

        # --- OpenCV Haar Cascade detection (primary) ---
        gray = cv2.cvtColor(img0, cv2.COLOR_RGB2GRAY)
        gray_eq = cv2.equalizeHist(gray)
        faces = _FACE_CASCADE.detectMultiScale(gray_eq, 1.05, 3, minSize=(40, 40))

        if faces is not None and len(faces) > 0:
            for (x, y, w, h) in faces:
                pad_w = int(w * 0.25)
                pad_h = int(h * 0.25)
                x1 = max(0, x - pad_w)
                y1 = max(0, y - pad_h)
                x2 = min(img0.shape[1], x + w + pad_w)
                y2 = min(img0.shape[0], y + h + pad_h)

                boxes.append((x1, y1, x2, y2))
                confidences.append(0.9)

                crop = img0[y1:y2, x1:x2]
                if crop.size and crop.shape[0] > 0 and crop.shape[1] > 0:
                    crop = cv2.resize(crop, (224, 224))
                    face_crops.append(crop)

        # --- YOLO fallback if Haar found nothing ---
        if len(face_crops) == 0:
            img_size = 640
            img = cv2.resize(img0, (img_size, img_size))
            img = torch.from_numpy(img).to(device)
            img = img.half() if device.type != 'cpu' else img.float()
            img /= 255.0
            if img.ndimension() == 3:
                img = img.permute(2, 0, 1).unsqueeze(0)

            with torch.no_grad():
                pred = face_model(img)[0]
                pred = non_max_suppression(pred, conf_thres, iou_thres)

            for det in pred:
                if det is not None and len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
                    for d in det:
                        xyxy = d[:4]
                        conf = d[4]
                        x1, y1, x2, y2 = map(int, xyxy)
                        w = x2 - x1
                        h = y2 - y1
                        pad_w = int(w * 0.15)
                        pad_h = int(h * 0.15)
                        x1 = max(0, x1 - pad_w)
                        y1 = max(0, y1 - pad_h)
                        x2 = min(img0.shape[1], x2 + pad_w)
                        y2 = min(img0.shape[0], y2 + pad_h)

                        boxes.append((x1, y1, x2, y2))
                        confidences.append(conf.item())
                        crop = img0[y1:y2, x1:x2]
                        if crop.size and crop.shape[0] > 0 and crop.shape[1] > 0:
                            crop = cv2.resize(crop, (224, 224))
                            face_crops.append(crop)

        if len(face_crops) == 0:
            return [], None

        # --- Emotion classification ---
        try:
            emotions = detect_emotion_fer(face_crops) if face_crops else []
        except Exception as e:
            st.error(f"Emotion detection error: {e}")
            emotions = []

        for i, box in enumerate(boxes):
            emotion = 'neutral'
            confidence = 50.0
            if i < len(emotions) and emotions[i]:
                emotion = emotions[i][0] if len(emotions[i]) > 0 else 'neutral'
                raw_conf = emotions[i][1] if len(emotions[i]) > 1 else 0.5

                if raw_conf <= 1.0:
                    confidence = raw_conf * 100.0
                else:
                    confidence = raw_conf

                confidence = max(0.0, min(100.0, confidence))

            results.append({
                'bbox': box,
                'emotion': emotion,
                'confidence': confidence,
                'face_conf': float(confidences[i]) * 100 if i < len(confidences) else 90.0,
            })

        return results, None
    except Exception as e:
        return None, str(e)


def draw_results(image, results):
    """Draw bounding boxes and emotion labels on an image."""
    if not results:
        return image
    res_img = image.copy()
    for res in results:
        x1, y1, x2, y2 = res['bbox']
        emo, conf = res['emotion'], res['confidence']
        color = EMOTION_COLORS.get(emo, (255, 255, 255))
        cv2.rectangle(res_img, (x1, y1), (x2, y2), color, 2)
        label = f"{EMOTION_EMOJIS.get(emo, '😐')} {emo.title()} ({conf:.1f}%)"
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.rectangle(res_img, (x1, y1 - t_size[1] - 10), (x1 + t_size[0], y1), color, -1)
        cv2.putText(res_img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return res_img


# ===============================
# Emotion Fusion
# ===============================

def standardize_emotion_result(emotion, confidence, source):
    """Standardize emotion detection result format."""
    conf_value = float(confidence) if confidence is not None else 50.0
    conf_value = max(0.0, min(100.0, conf_value))
    return {
        "emotion": str(emotion).lower() if emotion else "neutral",
        "confidence": conf_value,
        "source": str(source),
    }


def fuse_emotions(results):
    """Fuse multiple emotion results into a single dominant emotion.
    
    Accepts either:
      - list of {'emotion': ..., 'confidence': ...} dicts (from standardize_emotion_result)
      - list of {'emotion': ..., 'confidence': ..., 'bbox': ...} dicts (from detect_faces_and_emotions)
    """
    if not results:
        return ("neutral", 50.0)

    emotion_scores = {}
    emotion_counts = {}

    for res in results:
        emotion = res['emotion'].lower()
        conf = res['confidence']
        conf = max(0.0, min(100.0, conf))

        emotion_scores[emotion] = emotion_scores.get(emotion, 0) + conf
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

    dominant_emotion = None
    max_score = -1
    for emotion, score in emotion_scores.items():
        if score > max_score:
            max_score = score
            dominant_emotion = emotion
        elif score == max_score and dominant_emotion:
            if emotion_counts.get(emotion, 0) > emotion_counts.get(dominant_emotion, 0):
                dominant_emotion = emotion

    if not dominant_emotion:
        return ("neutral", 50.0)

    avg_confidence = emotion_scores[dominant_emotion] / emotion_counts[dominant_emotion]
    avg_confidence = max(0.0, min(100.0, avg_confidence))

    return (dominant_emotion, avg_confidence)


# ===============================
# Text-based Emotion Detection
# ===============================

def detect_emotion_from_text_simple(text):
    """Simple keyword-based emotion detection from text."""
    text_lower = text.lower()
    emotion_keywords = {
        "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic",
                  "love", "good", "positive", "cheerful", "delighted", "thrilled", "ecstatic"],
        "sad": ["sad", "depressed", "down", "blue", "melancholy", "upset", "crying",
                "tears", "hurt", "disappointed", "grief", "sorrow", "unhappy", "miserable"],
        "anger": ["anger", "mad", "furious", "rage", "irritated", "annoyed", "frustrated",
                  "pissed", "livid", "fuming", "outraged", "hostile", "bitter"],
        "fear": ["anxious", "worried", "nervous", "scared", "afraid", "fear", "panic",
                 "stress", "overwhelmed", "tense", "uneasy", "apprehensive", "terrified"],
        "surprise": ["surprised", "shocked", "amazed", "astonished", "stunned",
                     "bewildered", "confused", "unexpected", "wow", "incredible", "unbelievable"],
        "disgust": ["disgusted", "grossed", "repulsed", "revolted", "sick",
                    "nauseous", "appalled", "horrified", "disturbed", "offended"],
    }
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    return max(emotion_scores.items(), key=lambda x: x[1])[0] if emotion_scores else "neutral"


# ===============================
# Advanced Pipeline Helper
# ===============================

def _detect_advanced(image, advanced_detector):
    """Run the advanced EfficientNet+CBAM pipeline with temporal smoothing.
    
    Returns (results, error) matching detect_faces_and_emotions() signature.
    Returns (None, msg) to signal fallback to the legacy pipeline.
    """
    try:
        if isinstance(image, Image.Image):
            img = np.array(image)
        else:
            img = image.copy()

        # Ensure RGB
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        raw_results = advanced_detector.detect(img)
        if not raw_results:
            return None, "No faces detected by advanced pipeline"

        # Apply temporal smoothing if available
        smoother = st.session_state.get("emotion_smoother")
        if smoother is not None:
            for res in raw_results:
                smoothed_emo, smoothed_conf = smoother.update(
                    res["emotion"], res["confidence"]
                )
                res["emotion"] = smoothed_emo
                res["confidence"] = smoothed_conf

        return raw_results, None
    except Exception as e:
        return None, str(e)
