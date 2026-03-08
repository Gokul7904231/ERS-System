import sys
import os
import time
import tempfile
import numpy as np
import torch
import pandas as pd
from pathlib import Path
from datetime import datetime
from io import BytesIO
from PIL import Image

import streamlit as st
import cv2

# ===============================
# Path Configuration
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# The project root is one level up from src/
PROJECT_ROOT = Path(BASE_DIR).parent
sys.path.insert(0, str(PROJECT_ROOT)) # Add project root to path for src package

# ===============================
# Emotion Detection Modules
# ===============================
from src.core.emotion_detector import detect_emotion as detect_emotion_nn, init
from src.core.facial_emotion_detector import detect_emotion_geometric
from src.core.deep_emotion_detector import detect_emotion_deep
from src.core.fer_detector import detect_emotion_fer, FER2013Detector
from src.core.utils.general import attempt_load, check_img_size, non_max_suppression, scale_coords
from src.core.utils.torch_utils import select_device

# ===============================
# Recommendation & UI Modules
# ===============================
from src.features.music_recommender import music_recommender
from src.ui.music_player import (
    display_enhanced_music_recommendations
)
from src.ui.professional_music_player import (
    create_current_player
)
from src.ui.enhanced_ui import (
    apply_enhanced_styling,
    create_enhanced_header,
    create_soothing_navigation,
    create_soothing_section,
    create_enhanced_footer
)
from src.ui.compact_sidebar import create_compact_sidebar
from src.ui.resources_section import create_resources_section
from src.features.reading_recommender import reading_recommender
from src.ui.reading_display import (
    display_reading_recommendations,
    display_quick_reading_links,
    display_reading_insights
)
from src.features.wellness_features import wellness_features
from src.ui.breathing_exercises import display_breathing_exercise
from src.ui.coloring_display import display_coloring_game
from src.ui.mood_journaling import display_mood_journal
from src.ui.mental_health_display import show_chatbot, display_mental_health_resources, display_quick_mental_health_links
from src.ers.ers_engine import update_ers
from src.ers.aeisa import select_intervention

# Page configuration
st.set_page_config(
    page_title="🧠 MOOD DRIVEN PERSONALIZED RECOMMENDATION SYSTEM",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
EMOTIONS = ("anger", "contempt", "disgust", "fear", "happy", "neutral", "sad", "surprise")
EMOTION_COLORS = {
    "anger": (0, 0, 255), "contempt": (128, 0, 128), "disgust": (0, 128, 0),
    "fear": (255, 255, 0), "happy": (0, 255, 0), "neutral": (128, 128, 128),
    "sad": (255, 0, 0), "surprise": (0, 255, 255)
}
EMOTION_EMOJIS = {
    "anger": "😠", "contempt": "😏", "disgust": "🤢", "fear": "😨",
    "happy": "😊", "neutral": "😐", "sad": "😢", "surprise": "😲"
}

# ===============================
# Session State Initialization
# ===============================
def init_session_state():
    defaults = {
        'playlist': [],
        'models_loaded': False,
        'device': None,
        'face_model': None,
        'emotion_history': [],
        'processed_frames': [],
        'all_results': [],
        'input_mode': 'single',
        'multimodal_results': [],
        'current_track': None,
        'webcam_active': False,
        'coloring_progress': {},
        'show_multimodal_recommendations': False,
        'final_emotion': None,
        'final_confidence': None,
        'journal_entries': [] 
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# ===============================
# Core Logic Functions
# ===============================

def standardize_emotion_result(emotion, confidence, source):
    """Standardize emotion detection result format."""
    # Ensure confidence is within valid range [0, 100]
    conf_value = float(confidence) if confidence is not None else 50.0
    conf_value = max(0.0, min(100.0, conf_value))  # Clamp to 0-100
    
    return {
        "emotion": str(emotion).lower() if emotion else "neutral",
        "confidence": conf_value,
        "source": str(source)
    }

def fuse_emotions(results):
    """Fuse multiple emotion results into a single dominant emotion."""
    if not results:
        return ("neutral", 50.0)
    
    # Normalize all confidences to be within 0-100 range first
    normalized_results = []
    for res in results:
        conf = res['confidence']
        # If confidence is clearly out of range (>100), normalize it
        if conf > 100:
            conf = 100  # Cap at 100
        elif conf < 0:
            conf = 0  # Floor at 0
        normalized_results.append({
            'emotion': res['emotion'],
            'confidence': conf
        })
    
    # Calculate weighted average confidence for each emotion
    emotion_scores = {} # Stores sum of confidence for each emotion
    emotion_counts = {} # Stores count of detections for each emotion

    for res in normalized_results:
        emotion = res['emotion'].lower()
        confidence = res['confidence']
        
        emotion_scores[emotion] = emotion_scores.get(emotion, 0) + confidence
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Find dominant emotion based on total score (or count if scores are tied)
    dominant_emotion = None
    max_score = -1
    
    for emotion, score in emotion_scores.items():
        if score > max_score:
            max_score = score
            dominant_emotion = emotion
        elif score == max_score and dominant_emotion: # Tie-breaking: if scores are equal, prefer more counts
            if emotion_counts.get(emotion, 0) > emotion_counts.get(dominant_emotion, 0):
                dominant_emotion = emotion

    if not dominant_emotion:
        return ("neutral", 50.0) # Fallback if no valid emotions
    
    # Calculate average confidence for the dominant emotion
    avg_confidence = emotion_scores[dominant_emotion] / emotion_counts[dominant_emotion]
    
    # Ensure final confidence is within valid range
    avg_confidence = max(0.0, min(100.0, avg_confidence))
    
    return (dominant_emotion, avg_confidence)


@st.cache_resource
def load_models():
    """Load YOLOv7 face detection and RepVGG emotion models."""
    try:
        with st.spinner("Loading AI models..."):
            device = select_device('')
            init(device) # Initializes emotion model in emotion_detector.py
            
            # Use the face-specific model for better face detection
            weights_path = PROJECT_ROOT / "models" / "weights" / "yolov7-tiny-face.pt"
            if not weights_path.exists():
                st.warning(f"YOLOv7 face model not found at {weights_path}. Trying yolov7-tiny.pt instead.")
                weights_path = PROJECT_ROOT / "models" / "weights" / "yolov7-tiny.pt"
                if not weights_path.exists():
                    st.error(f"FATAL ERROR: YOLOv7 model weights not found at {weights_path}. Face detection will not work correctly.")
                    return False
                
            face_model = attempt_load(str(weights_path), map_location=device)
            
            # Initialize FER2013 emotion detector (trained CNN model)
            fer_detector_instance = FER2013Detector()
            fer_detector_instance.load_model()
            
            st.session_state.device = device
            st.session_state.face_model = face_model
            st.session_state.fer_detector = fer_detector_instance
            st.session_state.models_loaded = True
        return True
    except Exception as e:
        st.error(f"Model load error: {e}")
        return False

def detect_faces_and_emotions(image, conf_thres=0.5, iou_thres=0.45):
    """Detect faces and classify emotions in an image. Assumes input is RGB."""
    if not st.session_state.models_loaded:
        return None, "Models not loaded"

    try:
        device = st.session_state.device
        face_model = st.session_state.face_model
        
        if isinstance(image, Image.Image):
            img0 = np.array(image)
        else:
            img0 = image

        # Ensure we have a 3-channel RGB image for the model
        if img0.ndim == 2:  # Grayscale
            img0 = cv2.cvtColor(img0, cv2.COLOR_GRAY2RGB)
        elif img0.shape[2] == 4:  # RGBA
            img0 = cv2.cvtColor(img0, cv2.COLOR_RGBA2RGB)
        
        # Try YOLO detection first
        results = []
        face_crops = []
        boxes = []
        confidences = []
        
        # Use OpenCV Haar Cascade for more reliable face detection
        # Load the face detection cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img0, cv2.COLOR_RGB2GRAY)
        
        # Apply histogram equalization for better face detection
        gray_eq = cv2.equalizeHist(gray)
        
        # Detect faces using Haar Cascade with adjusted parameters
        # Lower scaleFactor and minNeighbors for better detection
        faces = face_cascade.detectMultiScale(gray_eq, 1.05, 3, minSize=(40, 40))
        
        # Check if faces were detected (faces is an empty array if none found)
        if faces is not None and len(faces) > 0:
            for (x, y, w, h) in faces:
                # Add padding to the face region (more padding for better context)
                pad_w = int(w * 0.25)
                pad_h = int(h * 0.25)
                x1 = max(0, x - pad_w)
                y1 = max(0, y - pad_h)
                x2 = min(img0.shape[1], x + w + pad_w)
                y2 = min(img0.shape[0], y + h + pad_h)
                
                boxes.append((x1, y1, x2, y2))
                confidences.append(0.9)  # Haar cascade doesn't provide confidence
                
                crop = img0[y1:y2, x1:x2]
                if crop.size and crop.shape[0] > 0 and crop.shape[1] > 0:
                    # Resize crop to consistent size for better emotion detection
                    crop = cv2.resize(crop, (224, 224))
                    face_crops.append(crop)
        
        # If OpenCV didn't find faces, try YOLO as fallback
        if len(face_crops) == 0:
            # Try YOLO detection with optimized parameters
            img_size = 640  # Increased for better detection
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
                        # Add padding around face
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
                            # Resize to consistent size
                            crop = cv2.resize(crop, (224, 224))
                            face_crops.append(crop)

        # If still no faces detected, return empty
        if len(face_crops) == 0:
            return [], None

        # Load face cascade for geometric emotion detection
        emotion_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect emotions from face crops using FER2013-trained CNN model (high accuracy)
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
                
                # FER2013 model already returns confidence as percentage (0-100)
                # Do NOT multiply by 100 - just ensure it stays in valid range
                # If raw_conf is between 0-1, treat as probability and convert to percentage
                if raw_conf <= 1.0:
                    confidence = raw_conf * 100.0
                else:
                    confidence = raw_conf  # Already a percentage
                
                # Clamp to valid range [0, 100]
                confidence = max(0.0, min(100.0, confidence))
            
            results.append({
                'bbox': box,
                'emotion': emotion,
                'confidence': confidence,
                'face_conf': float(confidences[i]) * 100 if i < len(confidences) else 90.0
            })
        return results, None
    except Exception as e:
        return None, str(e)

def draw_results(image, results):
    """Draw bounding boxes and emotion labels."""
    if not results: return image
    res_img = image.copy()
    for res in results:
        x1, y1, x2, y2 = res['bbox']
        emo, conf = res['emotion'], res['confidence']
        color = EMOTION_COLORS.get(emo, (255, 255, 255))
        cv2.rectangle(res_img, (x1, y1), (x2, y2), color, 2)
        label = f"{EMOTION_EMOJIS.get(emo, '😐')} {emo.title()} ({conf:.1f}%)"
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.rectangle(res_img, (x1, y1 - t_size[1] - 10), (x1 + t_size[0], y1), color, -1)
        cv2.putText(res_img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    return res_img

def detect_emotion_from_text_simple(text):
    """Simple keyword-based emotion detection from text"""
    text_lower = text.lower()
    emotion_keywords = {
        "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic", "love", "good", "positive", "cheerful", "delighted", "thrilled", "ecstatic"],
        "sad": ["sad", "depressed", "down", "blue", "melancholy", "upset", "crying", "tears", "hurt", "disappointed", "grief", "sorrow", "unhappy", "miserable"],
        "anger": ["anger", "mad", "furious", "rage", "irritated", "annoyed", "frustrated", "pissed", "livid", "fuming", "outraged", "hostile", "bitter"],
        "fear": ["anxious", "worried", "nervous", "scared", "afraid", "fear", "panic", "stress", "overwhelmed", "tense", "uneasy", "apprehensive", "terrified"],
        "surprise": ["surprised", "shocked", "amazed", "astonished", "stunned", "bewildered", "confused", "unexpected", "wow", "incredible", "unbelievable"],
        "disgust": ["disgusted", "grossed", "repulsed", "revolted", "sick", "nauseous", "appalled", "horrified", "disturbed", "offended"]
    }
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0: emotion_scores[emotion] = score
    return max(emotion_scores.items(), key=lambda x: x[1])[0] if emotion_scores else "neutral"

# ===============================
# Standardized UI Components
# ===============================

def display_final_emotion_card(emotion, confidence):
    """Polished card for the final emotion result."""
    emoji = EMOTION_EMOJIS.get(emotion.lower(), "😐")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; color: white; margin-bottom: 25px; 
                text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <div style="font-size: 60px; margin-bottom: 10px;">{emoji}</div>
        <h2 style="margin: 0; color: white; text-transform: capitalize; font-size: 32px;">{emotion}</h2>
        <p style="margin: 5px 0; font-size: 20px; opacity: 0.9;">Confidence: {confidence:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

def display_unified_recommendation_panel(emotion, confidence):
    """Unified panel for all recommendations."""
    # Sanitize the emotion string to ensure it's a clean key, preventing KeyErrors.
    clean_emotion = str(emotion).split('(')[0].strip().lower()

    display_final_emotion_card(clean_emotion, confidence)
    
    ers_value = update_ers(clean_emotion)
    intervention_data = select_intervention(clean_emotion, ers_value)

    # Robustly determine the intervention name
    if isinstance(intervention_data, dict):
        intervention_name = intervention_data.get('intervention', intervention_data.get('name', 'general support'))
    else:
        intervention_name = str(intervention_data)

    st.markdown(f"### 🛡️ ERS Primary Intervention: **{intervention_name.title()}**")
    
    # New Tab Layout
    tabs = st.tabs([
"🎵 Music",
"📚 Reading",
"🧘 Wellness",
"🎨 Coloring Game",
"💬 AI Chatbot",
"📝 Mood Journal",
"🆘 Support"
])
    
    # Mood Goal Mapping for Music
    mood_goal_mapping = {
        "sad": "Hopeful & Energetic",
        "anger": "Calm & Relaxed",
        "fear": "Safe & Grounded",
        "neutral": "Motivated & Focused",
        "happy": "Joyful & Energetic",
        "disgust": "Cleansed & Refreshed",
        "surprise": "Curious & Engaged",
        "contempt": "Open & Empathetic"
    }
    target_mood = mood_goal_mapping.get(clean_emotion, "Balanced")
    
    with tabs[0]: # Music
        st.subheader(f"🎵 {clean_emotion.title()} → Mood Lift: {target_mood}")
        music_recs = music_recommender.get_enhanced_recommendations(clean_emotion, count=5)
        if music_recs:
            st.session_state.playlist = music_recs
            display_enhanced_music_recommendations(music_recs, clean_emotion, f"Music for a {target_mood} Mood")
        else:
            st.info("No music recommendations available.")

    with tabs[1]: # Reading
        st.subheader("📚 Reading Suggestions")
        reading_recs = reading_recommender.get_reading_recommendations(clean_emotion, 4)
        display_reading_recommendations(reading_recs, clean_emotion, f"Reading for {clean_emotion.title()}")
        display_reading_insights(clean_emotion)

    with tabs[2]: # Wellness
        st.subheader("🧘 Wellness & Mindfulness")
        wellness_recs = wellness_features.get_wellness_recommendations(clean_emotion, confidence)
        if wellness_recs:
            for rec in wellness_recs:
                priority_color = "#E74C3C" if rec.get('priority') == 'high' else "#F39C12" if rec.get('priority') == 'medium' else "#27AE60"
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid {priority_color};">
                    <h4 style="margin: 0; color: {priority_color};">{rec.get('title', 'Activity')}</h4>
                    <p style="margin: 5px 0; color: #666;">{rec.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Breathing exercise is now permanently in the Wellness tab
        display_breathing_exercise(clean_emotion, wellness_features, key_prefix="rec_panel")

    with tabs[3]: # Coloring Game
        display_coloring_game(clean_emotion, key_prefix="rec_panel")  
        
    with tabs[4]:  # AI Chatbot
         st.subheader("💬 AI Wellness Companion")
         show_chatbot(clean_emotion)
         st.info("Talk with your AI wellness assistant about how you feel.")        

    with tabs[5]:  # Mood Journal
        display_mood_journal(clean_emotion, wellness_features)

    with tabs[6]: # Support
        st.subheader("🆘 Mental Health Resources")
        display_mental_health_resources(clean_emotion, int(confidence), f"Support for {clean_emotion.title()}")
        display_quick_mental_health_links(clean_emotion, int(confidence))



# ===============================
# UI Logic and Handlers
# ===============================

def process_emotion_result(emotion, confidence, source):
    """Handle the final emotion result based on current input mode."""
    result = standardize_emotion_result(emotion, confidence, source)
    st.session_state.emotion_history.append({'timestamp': datetime.now(), 'emotion': emotion, 'confidence': confidence, 'source': source})
    
    if st.session_state.input_mode == "single":
        display_unified_recommendation_panel(result["emotion"], result["confidence"])
    else: # multimodal
        st.session_state.multimodal_results.append(result)
        st.success(f"✅ Added **{result['emotion'].title()}** ({result['confidence']:.1f}%) from {source.title()}")

def render_single_mode_ui():
    """Renders the UI for single-shot emotion detection and recommendation."""
    create_soothing_section("Single-Mode Emotion Analysis", "Directly analyze an input and get immediate recommendations.", "pastel-blue")
    
    method = st.radio("Select Input Method:", ["📸 Photo", "🎬 Video", "📹 Webcam"], horizontal=True, key="single_mode_method")
    
    conf_thres = st.sidebar.slider("Face Confidence Threshold", 0.1, 1.0, 0.5, 0.05)
    iou_thres = st.sidebar.slider("IoU Threshold", 0.1, 1.0, 0.45, 0.05)

    if method == "📸 Photo":
        uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
        if uploaded_file:
            if st.button("Analyze Photo", type="primary", use_container_width=True):
                with st.spinner("Analyzing..."):
                    image = Image.open(uploaded_file)
                    results, error = detect_faces_and_emotions(image, conf_thres, iou_thres)
                    if error:
                        st.error(f"Analysis failed: {error}")
                    elif results:
                        st.image(draw_results(np.array(image), results), caption="Analysis Result", width=600)
                        dom_emotion = max(results, key=lambda x: x['confidence'])
                        process_emotion_result(dom_emotion['emotion'], dom_emotion['confidence'], "photo")
                    else:
                        st.warning("No faces were detected in the image.")

    elif method == "🎬 Video":
        uploaded_video = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])
        if uploaded_video:
            if st.button("Process Video", type="primary", use_container_width=True):
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_video.read())
                process_video_single_mode(tfile.name, conf_thres, iou_thres)

    elif method == "📹 Webcam":
        display_webcam_single_mode(conf_thres, iou_thres)

def process_video_single_mode(path, conf_t, iou_t):
    """Processes a video for emotion analysis in single mode."""
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        st.error("Error opening video file.")
        return

    progress_bar = st.progress(0)
    video_placeholder = st.empty()
    all_res = []
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for frame_count in range(total_frames):
        ret, frame = cap.read()
        if not ret: break
        
        # Process every Nth frame to be efficient
        if frame_count % 5 == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results, _ = detect_faces_and_emotions(frame_rgb, conf_t, iou_t)
            if results:
                res_frame = draw_results(frame_rgb, results)
                video_placeholder.image(res_frame, caption=f"Frame: {frame_count}")
                # Append all detected emotions from all faces in this frame
                all_res.extend(results)
        
        progress_bar.progress((frame_count + 1) / total_frames)
    
    cap.release()
    os.unlink(path)
    
    if all_res:
        # Fuse emotions from all collected results
        dom_emo, avg_conf = fuse_emotions(all_res)
        st.success(f"Video analysis complete. Dominant emotion: {dom_emo.title()}")
        process_emotion_result(dom_emo, avg_conf, "video")
    else:
        st.warning("No faces detected during video processing.")

def display_webcam_single_mode(conf_t, iou_t):
    """Handles live webcam detection for single mode."""
    st.info("The webcam will capture a short burst of frames for analysis. Multiple faces will be considered for a comprehensive emotion assessment.")
    if st.button("Start Webcam Analysis", type="primary", use_container_width=True):
        st.session_state.webcam_active = True

    if st.session_state.webcam_active:
        cap = cv2.VideoCapture(0) # Removed CAP_DSHOW for cross-platform compatibility
        if not cap.isOpened():
            st.error("Error: Could not access webcam. Please ensure it is connected and not in use by another application.")
            st.session_state.webcam_active = False
            return
            
        placeholder = st.empty()
        status_text = st.empty()
        all_webcam_results = [] # To store all detected faces and their emotions
        
        num_frames_to_capture = 30
        
        for i in range(num_frames_to_capture):
            ret, frame = cap.read()
            if not ret: 
                status_text.error("Failed to capture frame from webcam.")
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results, _ = detect_faces_and_emotions(frame_rgb, conf_t, iou_t)
            
            if results:
                processed_frame = draw_results(frame_rgb, results)
                placeholder.image(processed_frame, caption=f"Processing frame {i+1}/{num_frames_to_capture} (Detected {len(results)} face(s))")
                all_webcam_results.extend(results) # Extend with all detected faces
            else:
                placeholder.image(frame_rgb, caption=f"Processing frame {i+1}/{num_frames_to_capture} (No faces detected)")
            
            status_text.info(f"Capturing frame {i+1}/{num_frames_to_capture}...")
            time.sleep(0.05) # Small delay
            
        cap.release()
        st.session_state.webcam_active = False
        status_text.empty() # Clear status message after capture
        
        if all_webcam_results:
            dom_emo, avg_conf = fuse_emotions(all_webcam_results)
            st.success(f"Webcam analysis complete. Dominant emotion: {dom_emo.title()} (Avg Confidence: {avg_conf:.1f}%)")
            process_emotion_result(dom_emo, avg_conf, "webcam")
        else:
            st.warning("No faces were detected during webcam analysis. Please ensure your face is clearly visible in the camera frame.")


def render_multimodal_mode_ui():
    """Renders the UI for collecting multiple inputs and fusing them."""
    create_soothing_section("Multimodal Emotion Fusion", "Combine inputs from different sources for a more holistic analysis.", "pastel-purple")
    st.info("ℹ️ **Multimodal Mode Active:** Add emotion data from multiple sources below. When you're ready, click 'Get Final Recommendations' at the bottom.")
    
    conf_thres = st.sidebar.slider("Face Confidence Threshold", 0.1, 1.0, 0.5, 0.05)
    iou_thres = st.sidebar.slider("IoU Threshold", 0.1, 1.0, 0.45, 0.05)

    # --- Input Sections ---
    with st.expander("📸 Add from Photo", expanded=True):
        uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'], key="multi_photo")
        if uploaded_file:
            if st.button("Add Photo Emotion", use_container_width=True):
                image = Image.open(uploaded_file)
                with st.spinner("Analyzing photo..."):
                    results, error = detect_faces_and_emotions(image, conf_thres, iou_thres)
                    if error: st.error(error)
                    elif results:
                        # For multimodal, we can process all faces
                        for res in results:
                            process_emotion_result(res['emotion'], res['confidence'], "photo")
                    else: st.warning("No faces detected.")
    
    with st.expander("💬 Add from Text", expanded=True):
        mood_text = st.text_area("How are you feeling?", placeholder="Describe your day...", height=100, key="multi_text")
        if st.button("Add Text Emotion", use_container_width=True):
            if mood_text:
                emo = detect_emotion_from_text_simple(mood_text)
                process_emotion_result(emo, 75.0, "text")
            else: st.warning("Please enter some text.")

    with st.expander("📹 Add from Webcam", expanded=True):
        st.info("Captures a single frame for quick analysis.")
        if st.button("Add Webcam Emotion", use_container_width=True):
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Error: Could not access webcam. Please ensure it is connected and not in use by another application.")
            else:
                ret, frame = cap.read()
                cap.release()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    with st.spinner("Analyzing webcam frame..."):
                        results, error = detect_faces_and_emotions(frame_rgb, conf_thres, iou_thres)
                        if error: st.error(error)
                        elif results:
                            # For multimodal webcam, process all faces
                            for res in results:
                                process_emotion_result(res['emotion'], res['confidence'], "webcam")
                        else: st.warning("No face detected in the webcam frame.")
                else:
                    st.error("Failed to capture frame from webcam.")
    
    st.markdown("---")
    
    # --- Collected Inputs & Final Analysis ---
    if st.session_state.multimodal_results:
        st.subheader("📊 Collected Inputs")
        for i, res in enumerate(st.session_state.multimodal_results):
            emoji = EMOTION_EMOJIS.get(res['emotion'], '😐')
            st.markdown(f"- **{res['source'].title()}**: {emoji} {res['emotion'].title()} ({res['confidence']:.1f}%)")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Get Final Recommendations", type="primary", use_container_width=True):
                final_emo, final_conf = fuse_emotions(st.session_state.multimodal_results)
                st.session_state.final_emotion = final_emo
                st.session_state.final_confidence = final_conf
                st.session_state.show_multimodal_recommendations = True

        with col2:
            if st.button("Clear Inputs", use_container_width=True):
                st.session_state.multimodal_results = []
                st.session_state.show_multimodal_recommendations = False
                st.session_state.final_emotion = None
                st.session_state.final_confidence = None
                # No need for st.rerun() - Streamlit handles button click automatically
    else:
        st.write("No inputs collected yet. Use the sections above to add data.")

    # Conditionally display the recommendations panel
    if st.session_state.show_multimodal_recommendations:
        st.markdown("---")
        st.header("Fusion Analysis & Recommendations")
        display_unified_recommendation_panel(
            st.session_state.final_emotion, 
            st.session_state.final_confidence
        )

# ===============================
# Main Application
# ===============================
def main():
    apply_enhanced_styling()
    create_enhanced_header()
    create_compact_sidebar()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔄 Input Mode")
    mode_options = ["Single", "Multimodal"]
    # Safer code to prevent crashes if session state has unexpected value
    current_mode_index = 0 if st.session_state.input_mode == "single" else 1
    mode_label = st.sidebar.radio("Select analysis mode:", mode_options, index=current_mode_index)
    
    # Streamlit auto-reruns on radio button change, no need for manual rerun
    if st.session_state.input_mode != mode_label.lower():
        st.session_state.input_mode = mode_label.lower()
        # Clear multimodal results when switching modes
        st.session_state.multimodal_results = []

    if not st.session_state.models_loaded:
        if st.sidebar.button("🚀 Load AI Models", type="primary", use_container_width=True):
            if load_models():
                st.rerun()
        st.warning("Please load the AI models using the button in the sidebar to begin.")
        return

    # Global music player
    if st.session_state.get('current_track'):
        create_current_player(st.session_state.current_track)

    if st.session_state.input_mode == 'single':
        render_single_mode_ui()
    else:
        render_multimodal_mode_ui()
    
    st.markdown("---")
    
    # Footer and history
    if st.session_state.emotion_history:
        with st.expander("📈 Your Emotional Journey History"):
            hist_df = pd.DataFrame(st.session_state.emotion_history)
            hist_df['timestamp'] = pd.to_datetime(hist_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(hist_df, use_container_width=True)

    create_resources_section()
    create_enhanced_footer()

if __name__ == "__main__":
    main()
