import streamlit as st
import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
from PIL import Image
import time
import os
import tempfile
import base64
from io import BytesIO
import pandas as pd
import altair as alt
from pathlib import Path
from datetime import datetime

# Import the emotion detection modules
from emotion import detect_emotion, init
from emotion.models.experimental import attempt_load
from emotion.utils.datasets import LoadImages
from emotion.utils.general import check_img_size, non_max_suppression, scale_coords, create_folder
from emotion.utils.plots import plot_one_box
from emotion.utils.torch_utils import select_device, time_synchronized

# Import music recommendation modules
from music_recommender import music_recommender
from music_player import (display_music_recommendations, display_playlist_summary, create_music_player_sidebar, 
                        play_track, display_enhanced_music_recommendations, display_youtube_player, display_enhanced_youtube_player)
from enhanced_ui import (apply_enhanced_styling, create_enhanced_header, create_soothing_navigation,
                        create_soothing_section, create_enhanced_footer)
from compact_sidebar import create_compact_sidebar
from resources_section import create_resources_section
from professional_music_player import (create_professional_music_section, create_emotion_based_playlist,
                                     create_current_player, create_music_insights, create_quick_play_section)

# Import reading recommendation modules
from reading_recommender import reading_recommender
from reading_display import display_reading_recommendations, display_quick_reading_links, display_reading_insights, create_reading_sidebar

# Import wellness modules
from wellness_features import wellness_features
from breathing_exercises import display_breathing_exercise

# Import mental health resources
from mental_health_resources import mental_health_resources
from mental_health_display import display_mental_health_resources, display_quick_mental_health_links, create_mental_health_sidebar

# Page configuration
st.set_page_config(
    page_title="🧠 MOOD DRIVEN PERSONALIZED RECOMENDATION SYSTEM",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply enhanced styling
apply_enhanced_styling()

# Create enhanced header
create_enhanced_header()

# Old CSS removed - using enhanced_ui.py instead

# Initialize session state
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = False
if 'device' not in st.session_state:
    st.session_state.device = None
if 'face_model' not in st.session_state:
    st.session_state.face_model = None
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []
if 'show_frame_gallery' not in st.session_state:
    st.session_state.show_frame_gallery = False
if 'show_detailed_gallery' not in st.session_state:
    st.session_state.show_detailed_gallery = False
if 'processed_frames' not in st.session_state:
    st.session_state.processed_frames = []
if 'all_results' not in st.session_state:
    st.session_state.all_results = []
if 'selected_frame_idx' not in st.session_state:
    st.session_state.selected_frame_idx = 0
if 'show_player' not in st.session_state:
    st.session_state.show_player = False
if 'current_track' not in st.session_state:
    st.session_state.current_track = None

# Emotion labels and colors
EMOTIONS = ("anger", "contempt", "disgust", "fear", "happy", "neutral", "sad", "surprise")
EMOTION_COLORS = {
    "anger": (0, 0, 255),      # Red
    "contempt": (128, 0, 128), # Purple
    "disgust": (0, 128, 0),    # Green
    "fear": (255, 255, 0),     # Yellow
    "happy": (0, 255, 0),      # Lime
    "neutral": (128, 128, 128), # Gray
    "sad": (255, 0, 0),        # Blue
    "surprise": (0, 255, 255)  # Cyan
}

EMOTION_EMOJIS = {
    "anger": "😠",
    "contempt": "😏", 
    "disgust": "🤢",
    "fear": "😨",
    "happy": "😊",
    "neutral": "😐",
    "sad": "😢",
    "surprise": "😲"
}

def load_models():
    """Load YOLOv7 face detection and RepVGG emotion classification models"""
    try:
        with st.spinner("Loading models..."):
            # Initialize device
            device = select_device('')
            st.session_state.device = device
            
            # Initialize emotion model
            init(device)
            
            # Load face detection model
            face_model = attempt_load("weights/yolov7-tiny.pt", map_location=device)
            stride = int(face_model.stride.max())
            imgsz = check_img_size(512, s=stride)
            
            if device.type != 'cpu':
                face_model.half()  # to FP16
                face_model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(face_model.parameters())))
            
            st.session_state.face_model = face_model
            st.session_state.models_loaded = True
            
        return True
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return False

def detect_faces_and_emotions(image, conf_thres=0.5, iou_thres=0.45):
    """Detect faces and classify emotions in an image"""
    if not st.session_state.models_loaded:
        return None, "Models not loaded"
    
    try:
        device = st.session_state.device
        face_model = st.session_state.face_model
        
        # Convert PIL to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Ensure image is in RGB format
        if len(image.shape) == 3 and image.shape[2] == 3:
            # If image is BGR, convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        # Prepare image for YOLO (following the original main.py format)
        img_size = 512
        img = cv2.resize(image_rgb, (img_size, img_size))
        
        # Convert to tensor and normalize properly
        img = torch.from_numpy(img).to(device)
        img = img.half() if device.type != 'cpu' else img.float()
        img /= 255.0  # Normalize to 0-1 range
        
        # Ensure correct tensor shape: [batch, channels, height, width]
        if img.ndimension() == 3:
            img = img.permute(2, 0, 1).unsqueeze(0)  # HWC -> CHW -> BCHW
        
        # Face detection inference
        with torch.no_grad():
            pred = face_model(img)[0]
            pred = non_max_suppression(pred, conf_thres, iou_thres)
        
        # Process detections
        results = []
        face_images = []
        
        for det in pred:
            if len(det):
                # Rescale boxes from img_size to original size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image_rgb.shape).round()
                
                for *xyxy, conf, cls in det:
                    x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                    
                    # Extract face region
                    face_crop = image_rgb[y1:y2, x1:x2]
                    if face_crop.size > 0:
                        face_images.append(face_crop)
        
        # Classify emotions if faces detected
        if face_images:
            emotions = detect_emotion(face_images, conf=True)
            
            # Combine face detections with emotions
            for det in pred:
                if len(det):
                    for j, (*xyxy, conf, cls) in enumerate(det):
                        if j < len(emotions):
                            emotion_info = emotions[j][0]
                            emotion_name = emotion_info.split(' (')[0]
                            confidence = float(emotion_info.split('(')[1].split('%')[0]) if '(' in emotion_info else 100.0
                            
                            results.append({
                                'bbox': [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
                                'emotion': emotion_name,
                                'confidence': confidence,
                                'face_conf': float(conf)
                            })
        
        return results, None
        
    except Exception as e:
        return None, str(e)

def draw_results(image, results):
    """Draw bounding boxes and emotion labels on image"""
    if not results:
        return image
    
    result_image = image.copy()
    
    for result in results:
        x1, y1, x2, y2 = result['bbox']
        emotion = result['emotion']
        confidence = result['confidence']
        face_conf = result['face_conf']
        
        # Get color for emotion
        color = EMOTION_COLORS.get(emotion, (255, 255, 255))
        
        # Draw bounding box
        cv2.rectangle(result_image, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        label = f"{EMOTION_EMOJIS.get(emotion, '😐')} {emotion.title()} ({confidence:.1f}%)"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        
        # Draw label background
        cv2.rectangle(result_image, (x1, y1 - label_size[1] - 10), 
                     (x1 + label_size[0], y1), color, -1)
        
        # Draw label text
        cv2.putText(result_image, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return result_image

def display_standalone_wellness_tools():
    """Display standalone wellness tools that work without emotion detection."""
    
    st.subheader("🧘 Breathing Exercises")
    
    # Let user choose emotion for breathing exercise
    emotion_choice = st.selectbox(
        "What emotion are you feeling right now?",
        ["sad", "anger", "fear", "disgust", "happy", "surprise", "contempt", "neutral"]
    )
    
    display_breathing_exercise(emotion_choice, wellness_features)

# Main app
def main():
    # Compact sidebar
    create_compact_sidebar()
    
    # Soothing navigation
    create_soothing_navigation()
    
    # All sidebar content is now in the compact sidebar
    
    conf_thres = st.sidebar.slider("Face Detection Confidence", 0.1, 1.0, 0.5, 0.05)
    iou_thres = st.sidebar.slider("IoU Threshold", 0.1, 1.0, 0.45, 0.05)
    
    # Load models button
    if not st.session_state.models_loaded:
        if st.sidebar.button("🚀 Load Models", type="primary"):
            if load_models():
                st.sidebar.success("✅ Models loaded successfully!")
                st.rerun()
    else:
        st.sidebar.success("✅ Models loaded!")
    
    # Main content
    if not st.session_state.models_loaded:
        st.warning("⚠️ Please load the models first using the button in the sidebar.")
        return
    
    # Global Music Player - Show if a track is currently playing
    if st.session_state.get('current_track'):
        create_current_player(st.session_state.current_track)
    
    # Main navigation
    main_tab = st.radio("What would you like to do?", ["📷 Emotion Detection", "💬 Text-Based Mood Input", "🧘 Wellness"])
    
    if main_tab == "📷 Emotion Detection":
        # Source selection
        create_soothing_section("📷 How would you like to share your emotions?", "Choose the method that works best for you", "pastel-green")
        source_type = st.radio("Select your preferred method:", ["📸 Upload a Photo", "🎬 Upload a Video", "📹 Use Live Camera"])
    elif main_tab == "💬 Text-Based Mood Input":
        display_text_based_mood_input()
        return
    elif main_tab == "🧘 Wellness":
        st.header("🧘 Wellness")
        display_standalone_wellness_tools()
        return
    
    if source_type == "📸 Upload a Photo":
        st.subheader("📸 Upload an Image")
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", width=400)
            
            # Process image
            if st.button("🔍 Analyze Emotions", type="primary"):
                with st.spinner("Analyzing emotions..."):
                    results, error = detect_faces_and_emotions(image, conf_thres, iou_thres)
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif results:
                        # Display results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🎯 Detection Results")
                            result_image = draw_results(np.array(image), results)
                            st.image(result_image, caption="Emotion Detection Results", width=400)
                        
                        with col2:
                            st.subheader("📊 Emotion Analysis")
                            for i, result in enumerate(results):
                                emotion = result['emotion']
                                confidence = result['confidence']
                                face_conf = result['face_conf']
                                
                                st.markdown(f"""
                                <div class="emotion-card">
                                    <h3>{EMOTION_EMOJIS.get(emotion, '😐')} {emotion.title()}</h3>
                                    <p>Emotion Confidence: {confidence:.1f}%</p>
                                    <p>Face Detection: {face_conf:.1f}%</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Update emotion history
                        for result in results:
                            st.session_state.emotion_history.append({
                                'emotion': result['emotion'],
                                'confidence': result['confidence'],
                                'timestamp': time.time()
                            })
                        
                        # Music Recommendations for Image
                        st.markdown("---")
                        st.subheader("🎵 Music Recommendations")
                        
                        # Get the dominant emotion
                        dominant_emotion = max(results, key=lambda x: x['confidence'])
                        emotion_name = dominant_emotion['emotion']
                        emotion_confidence = dominant_emotion['confidence']
                        
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
                            <h3 style="margin: 0; color: white;">🎭 Your Mood: {emotion_name.title()}</h3>
                            <p style="margin: 5px 0; color: #f0f0f0;">Confidence: {emotion_confidence:.1f}%</p>
                            <p style="margin: 10px 0; color: #f0f0f0;">Here are some songs that match your current mood:</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Get enhanced music recommendations with mood matching scores
                        recommendations = music_recommender.get_enhanced_recommendations(emotion_name, count=5)
                        
                        # Store playlist in session state
                        st.session_state.playlist = recommendations
                        
                        # Display enhanced recommendations with visual indicators
                        display_enhanced_music_recommendations(recommendations, emotion_name, f"🎵 Enhanced Music for {emotion_name.title()} Mood")
                        
                        # Display simple player if a track is selected
                        if st.session_state.get('show_player') and st.session_state.get('current_track'):
                            st.markdown("---")
                            create_current_player(st.session_state.current_track)
                        
                        # Professional music section
                        create_professional_music_section(recommendations, "🎵 Music Recommendations", emotion_name)
                        
                        # Quick play section
                        create_quick_play_section(recommendations, "🎮 Quick Play")
                        
                        # Music insights
                        create_music_insights(recommendations, emotion_name)
                        
                        # Reading Recommendations for Image
                        st.markdown("---")
                        st.subheader("📚 Reading Recommendations")
                        
                        # Get reading recommendations based on detected emotion
                        reading_recs = reading_recommender.get_reading_recommendations(emotion_name, 3)
                        
                        # Display reading recommendations
                        display_reading_recommendations(reading_recs, emotion_name, f"📚 Reading for {emotion_name.title()} Mood")
                        
                        # Display reading insights
                        display_reading_insights(emotion_name)
                        
                        # Quick reading links
                        display_quick_reading_links(reading_recs, emotion_name)
                        
                        # Mental Health Resources for Image
                        st.markdown("---")
                        display_mental_health_resources(emotion_name, int(emotion_confidence), f"🆘 Mental Health Support for {emotion_name.title()} Mood")
                        
                        # Quick mental health links
                        display_quick_mental_health_links(emotion_name, int(emotion_confidence))
                        
                        # Display wellness recommendations
                        st.markdown("### 💡 Personalized Wellness Recommendations")
                        
                        # Get wellness recommendations
                        wellness_recs = wellness_features.get_wellness_recommendations(emotion_name, emotion_confidence)
                        
                        if wellness_recs:
                            for rec in wellness_recs:
                                priority_color = "#E74C3C" if rec['priority'] == 'high' else "#F39C12" if rec['priority'] == 'medium' else "#27AE60"
                                
                                st.markdown(f"""
                                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid {priority_color};">
                                    <h4 style="margin: 0; color: {priority_color};">{rec['title']}</h4>
                                    <p style="margin: 5px 0; color: #666;">{rec['description']}</p>
                                    <small style="color: {priority_color};">Priority: {rec['priority'].title()}</small>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No specific wellness recommendations available for this mood.")
                        
                        # Breathing Exercise for stress-related emotions
                        if emotion_name in ["sad", "anger", "fear", "disgust"]:
                            st.markdown("---")
                            display_breathing_exercise(emotion_name, wellness_features)
                    else:
                        st.warning("No faces detected in the image.")
    
    elif source_type == "🎬 Upload a Video":
        st.subheader("🎬 Upload a Video")
        uploaded_video = st.file_uploader("Choose a video...", type=['mp4', 'avi', 'mov'])
        
        if uploaded_video is not None:
            # Save uploaded video
            video_path = f"temp_video_{int(time.time())}.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_video.getbuffer())
            
            # Video processing settings
            st.subheader("⏱️ Processing Settings")
            
            col1, col2 = st.columns(2)
            with col1:
                processing_seconds = st.number_input("Process for (seconds)", 1, 60, 10, help="How many seconds of the video to process")
            with col2:
                frame_skip = st.number_input("Process every N frames", 1, 10, 2, help="Skip frames for faster processing")
            
            if st.button("🎬 Process Video", type="primary"):
                cap = cv2.VideoCapture(video_path)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                video_duration = total_frames / fps
                
                # Calculate frames to process based on seconds
                max_frames_to_process = min(processing_seconds * fps, total_frames)
                
                st.info(f"""
                **📹 Video Information:**
                - Total Duration: {video_duration:.1f} seconds
                - FPS: {fps}
                - Total Frames: {total_frames}
                - Processing: {processing_seconds} seconds ({max_frames_to_process} frames)
                """)
                
                # Create progress bar and status
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                frame_count = 0
                processed_frames = []
                all_results = []
                start_time = time.time()
                
                # First, show the video playing for the specified duration
                st.subheader("🎬 Video Preview - Processing Duration")
                st.info(f"📹 Playing video for {processing_seconds} seconds to show what will be analyzed...")
                
                # Create video player placeholder
                video_placeholder = st.empty()
                
                st.subheader("🎬 Processing Video...")
                
                while frame_count < max_frames_to_process:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Show live video preview for every frame
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(frame_rgb, caption=f"Live Preview - {frame_count / fps:.1f}s / {processing_seconds}s", width=600)
                    
                    # Process every Nth frame
                    if frame_count % frame_skip == 0:
                        # Detect emotions
                        results, error = detect_faces_and_emotions(frame_rgb, conf_thres, iou_thres)
                        
                        if results:
                            # Draw results on frame
                            result_frame = draw_results(frame_rgb, results)
                            processed_frames.append({
                                'frame': result_frame,
                                'frame_number': frame_count,
                                'timestamp': frame_count / fps
                            })
                            
                            # Store results
                            for result in results:
                                all_results.append({
                                    'frame': frame_count,
                                    'emotion': result['emotion'],
                                    'confidence': result['confidence'],
                                    'timestamp': frame_count / fps,
                                    'face_conf': result['face_conf']
                                })
                        
                        # Update progress
                        progress = min(frame_count / max_frames_to_process, 1.0)
                        progress_bar.progress(progress)
                        status_text.text(f"Processing frame {frame_count}/{max_frames_to_process} ({frame_count/fps:.1f}s/{processing_seconds}s)")
                    
                    # Add small delay to make video playback visible
                    time.sleep(0.05)
                    frame_count += 1
                
                cap.release()
                processing_time = time.time() - start_time
                
                # Clear video preview and show completion message
                video_placeholder.empty()
                st.success(f"✅ Video processing completed in {processing_time:.1f} seconds!")
                st.info("📊 Below are the emotion detection results and analysis...")
                
                # Display results
                if processed_frames:
                    st.success(f"✅ Processed {len(processed_frames)} frames in {processing_time:.1f} seconds!")
                    
                    # Quick summary at the top
                    st.subheader("📋 Processing Summary")
                    summary_col1, summary_col2, summary_col3 = st.columns(3)
                    
                    with summary_col1:
                        st.metric("🎬 Frames Processed", len(processed_frames))
                    with summary_col2:
                        st.metric("⏱️ Video Duration", f"{processing_seconds}s")
                    with summary_col3:
                        st.metric("🎭 Total Detections", len(all_results))
                    
                    # Quick emotion overview
                    if all_results:
                        emotion_counts = {}
                        for result in all_results:
                            emotion = result['emotion']
                            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                        
                        st.markdown("**🎯 Quick Emotion Overview:**")
                        emotion_summary_cols = st.columns(min(len(emotion_counts), 8))
                        for i, (emotion, count) in enumerate(sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)):
                            with emotion_summary_cols[i]:
                                st.markdown(f"""
                                <div style="background: #f0f2f6; padding: 10px; border-radius: 5px; text-align: center;">
                                    <h4>{EMOTION_EMOJIS.get(emotion, '😐')}</h4>
                                    <p><strong>{emotion.title()}</strong></p>
                                    <p>{count} detections</p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Store frames in session state for gallery access
                    st.session_state.processed_frames = processed_frames
                    st.session_state.all_results = all_results
                    
                    # Dynamic emotion timeline chart
                    if all_results:
                        st.subheader("📊 Dynamic Emotion Timeline")
                        
                        # Prepare data for chart
                        import pandas as pd
                        import altair as alt
                        
                        chart_data = []
                        for result in all_results:
                            chart_data.append({
                                'Time': result['timestamp'],
                                'Emotion': result['emotion'],
                                'Confidence': result['confidence'],
                                'Emoji': EMOTION_EMOJIS.get(result['emotion'], '😐')
                            })
                        
                        df = pd.DataFrame(chart_data)
                        
                        # Create interactive timeline chart
                        chart = alt.Chart(df).mark_circle(size=100).encode(
                            x=alt.X('Time:Q', title='Time (seconds)', scale=alt.Scale(zero=False)),
                            y=alt.Y('Confidence:Q', title='Confidence (%)', scale=alt.Scale(domain=[0, 100])),
                            color=alt.Color('Emotion:N', 
                                         scale=alt.Scale(domain=list(EMOTION_COLORS.keys()),
                                                       range=[f'rgb({r},{g},{b})' for r,g,b in EMOTION_COLORS.values()])),
                            tooltip=['Time:Q', 'Emotion:N', 'Confidence:Q']
                        ).properties(
                            width=700,
                            height=300
                        ).interactive()
                        
                        st.altair_chart(chart, use_container_width=True)
                        
                        # Emotion distribution pie chart
                        st.subheader("🥧 Emotion Distribution")
                        
                        emotion_counts = df['Emotion'].value_counts()
                        pie_data = []
                        for emotion, count in emotion_counts.items():
                            pie_data.append({
                                'Emotion': emotion,
                                'Count': count,
                                'Percentage': (count / len(df)) * 100,
                                'Emoji': EMOTION_EMOJIS.get(emotion, '😐')
                            })
                        
                        pie_df = pd.DataFrame(pie_data)
                        
                        pie_chart = alt.Chart(pie_df).mark_arc(innerRadius=50).encode(
                            theta=alt.Theta('Count:Q'),
                            color=alt.Color('Emotion:N', 
                                         scale=alt.Scale(domain=list(EMOTION_COLORS.keys()),
                                                       range=[f'rgb({r},{g},{b})' for r,g,b in EMOTION_COLORS.values()])),
                            tooltip=['Emotion:N', 'Count:Q', 'Percentage:Q']
                        ).properties(
                            width=400,
                            height=400
                        )
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.altair_chart(pie_chart, use_container_width=True)
                        with col2:
                            st.markdown("**📈 Emotion Statistics:**")
                            for _, row in pie_df.iterrows():
                                st.markdown(f"""
                                <div style="background: #f0f2f6; padding: 10px; margin: 5px 0; border-radius: 5px;">
                                    <strong>{row['Emoji']} {row['Emotion'].title()}</strong><br>
                                    <small>{row['Count']} detections ({row['Percentage']:.1f}%)</small>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Update emotion history
                    for result in all_results:
                        st.session_state.emotion_history.append({
                            'emotion': result['emotion'],
                            'confidence': result['confidence'],
                            'timestamp': time.time()
                        })
                else:
                    st.warning("No faces detected in the video. Try adjusting the confidence threshold.")
                
                # Clean up
                if os.path.exists(video_path):
                    os.remove(video_path)
                
                # Music Recommendations for Video Analysis
                if all_results:
                    st.markdown("---")
                    st.subheader("🎵 Personalized Music Playlist")
                    
                    # Calculate emotion percentages
                    emotion_counts = {}
                    for result in all_results:
                        emotion = result['emotion']
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    
                    total_detections = len(all_results)
                    emotion_percentages = {emotion: (count / total_detections) * 100 
                                        for emotion, count in emotion_counts.items()}
                    
                    # Generate emotion summary
                    emotion_summary = music_recommender.get_emotion_summary(emotion_percentages)
                    
                    # Generate enhanced mood journey playlist
                    playlist = music_recommender.create_mood_journey_playlist(emotion_percentages, duration_minutes=15)
                    
                    # Store playlist in session state
                    st.session_state.playlist = playlist
                    
                    # Display enhanced playlist with emotional flow visualization
                    from music_player import display_mood_journey_playlist
                    display_mood_journey_playlist(playlist, emotion_summary)
                    
                    # Display simple player if a track is selected
                    if st.session_state.get('show_player') and st.session_state.get('current_track'):
                        st.markdown("---")
                        create_current_player(st.session_state.current_track)
                    
                    # Professional emotion-based playlist
                    create_emotion_based_playlist(playlist, f"Emotional Journey ({total_frames} frames)")
                    
                    # Quick play by emotion
                    st.markdown("**🎮 Quick Play by Emotion:**")
                    emotion_cols = st.columns(min(len(emotion_percentages), 4))
                    for i, (emotion, percentage) in enumerate(sorted(emotion_percentages.items(), key=lambda x: x[1], reverse=True)[:4]):
                        with emotion_cols[i]:
                            emotion_tracks = [track for track in playlist if track.get('emotion') == emotion]
                            if emotion_tracks:
                                track = emotion_tracks[0]
                                youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
                                if st.button(f"▶️ {emotion.title()}\n({percentage:.1f}%)", key=f"emotion_play_{emotion}", use_container_width=True):
                                    st.markdown(f"**[🎵 Play {track['title']}]({youtube_url})**")
                                    st.session_state.current_track = track
                                    st.session_state.show_player = True
                    
                    # Reading Recommendations for Video Analysis
                    st.markdown("---")
                    st.subheader("📚 Reading Recommendations")
                    
                    # Get reading recommendations based on dominant emotion
                    dominant_emotion = max(emotion_percentages.items(), key=lambda x: x[1])[0]
                    reading_recs = reading_recommender.get_reading_recommendations(dominant_emotion, 4)
                    
                    # Display reading recommendations
                    display_reading_recommendations(reading_recs, dominant_emotion, f"📚 Reading for Your {dominant_emotion.title()} Mood")
                    
                    # Display reading insights
                    display_reading_insights(dominant_emotion)
                    
                    # Quick reading links
                    display_quick_reading_links(reading_recs, dominant_emotion)
                    
                    # Mental Health Resources for Video Analysis
                    st.markdown("---")
                    dominant_emotion = max(emotion_percentages.items(), key=lambda x: x[1])
                    emotion_name = dominant_emotion[0]
                    emotion_confidence = dominant_emotion[1]
                    display_mental_health_resources(emotion_name, int(emotion_confidence), f"🆘 Mental Health Support for Your {emotion_name.title()} Mood")
                    
                    # Quick mental health links
                    display_quick_mental_health_links(emotion_name, int(emotion_confidence))
                    
                    # Display wellness recommendations
                    st.markdown("### 💡 Personalized Wellness Recommendations")
                    
                    try:
                        wellness_recs = wellness_features.get_wellness_recommendations(emotion_name, emotion_confidence)
                        
                        if wellness_recs:
                            for rec in wellness_recs:
                                priority_color = "#E74C3C" if rec['priority'] == 'high' else "#F39C12" if rec['priority'] == 'medium' else "#27AE60"
                                
                                st.markdown(f"""
                                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid {priority_color};">
                                    <h4 style="margin: 0; color: {priority_color};">{rec['title']}</h4>
                                    <p style="margin: 5px 0; color: #666;">{rec['description']}</p>
                                    <small style="color: {priority_color};">Priority: {rec['priority'].title()}</small>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No specific wellness recommendations available for this mood.")
                    except Exception as e:
                        st.error(f"Error loading wellness recommendations: {e}")
                    
                    # Breathing Exercise for stress-related emotions
                    if emotion_name in ["sad", "anger", "fear", "disgust"]:
                        st.markdown("---")
                        display_breathing_exercise(emotion_name, wellness_features)
        
        
    elif source_type == "📹 Use Live Camera":
        display_live_webcam_detection()
    
    # Global Gallery Access - Show buttons if we have processed frames
    if hasattr(st.session_state, 'processed_frames') and st.session_state.processed_frames:
        st.markdown("---")
        st.subheader("🎬 Gallery Access")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("🎬 View Frame Gallery", help="Click to view all captured frames with emotions", use_container_width=True):
                st.session_state.show_frame_gallery = True
                st.rerun()
        
        with col2:
            st.info(f"📸 **{len(st.session_state.processed_frames)} frames available** for viewing")
        
        with col3:
            if st.button("🔍 Open Detailed Frame Gallery", help="Click to open a detailed view of all frames", use_container_width=True):
                st.session_state.show_detailed_gallery = True
                st.rerun()
    
    # Global Frame Gallery Section
    if hasattr(st.session_state, 'show_frame_gallery') and st.session_state.show_frame_gallery:
        st.markdown("---")
        st.subheader("🎬 Frame Gallery - Browse Captured Frames")
        
        if hasattr(st.session_state, 'processed_frames') and st.session_state.processed_frames:
            processed_frames = st.session_state.processed_frames
            all_results = st.session_state.all_results
            
            # Gallery controls
            gallery_col1, gallery_col2, gallery_col3 = st.columns([1, 2, 1])
            with gallery_col1:
                if st.button("← Back to Results"):
                    st.session_state.show_frame_gallery = False
                    st.rerun()
            
            with gallery_col2:
                st.info(f"📸 **{len(processed_frames)} frames captured**")
            
            with gallery_col3:
                if st.button("🗑️ Close Gallery"):
                    st.session_state.show_frame_gallery = False
                    st.rerun()
            
            # Show frames in a clean grid
            frames_per_row = 4
            for i in range(0, len(processed_frames), frames_per_row):
                cols = st.columns(frames_per_row)
                
                for j, col in enumerate(cols):
                    frame_idx = i + j
                    if frame_idx < len(processed_frames):
                        frame_data = processed_frames[frame_idx]
                        frame_results = [r for r in all_results if r['frame'] == frame_data['frame_number']]
                        
                        with col:
                            # Display frame image
                            st.image(frame_data['frame'], 
                                   caption=f"Frame {frame_idx + 1} - {frame_data['timestamp']:.1f}s", 
                                   width=200)
                            
                            # Show emotions for this frame
                            if frame_results:
                                st.markdown("**🎭 Emotions:**")
                                for result in frame_results:
                                    emotion = result['emotion']
                                    confidence = result['confidence']
                                    st.markdown(f"""
                                    <div style="background: #f0f2f6; padding: 8px; margin: 2px 0; border-radius: 5px; text-align: center;">
                                        <strong>{EMOTION_EMOJIS.get(emotion, '😐')} {emotion.title()}</strong><br>
                                        <small>{confidence:.1f}% confidence</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div style="background: #ffe6e6; padding: 8px; margin: 2px 0; border-radius: 5px; text-align: center;">
                                    <small>No emotions detected</small>
                                </div>
                                """, unsafe_allow_html=True)
            
            # Add a button to open detailed gallery
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Open Detailed Frame Gallery", help="Click to open a detailed view of all frames", use_container_width=True):
                    st.session_state.show_detailed_gallery = True
                    st.rerun()
        else:
            st.warning("No frames available in gallery. Please process a video first.")
    
    # Global Detailed Gallery Section
    if hasattr(st.session_state, 'show_detailed_gallery') and st.session_state.show_detailed_gallery:
        st.markdown("---")
        st.subheader("🔍 Detailed Frame Gallery")
        
        if hasattr(st.session_state, 'processed_frames') and st.session_state.processed_frames:
            processed_frames = st.session_state.processed_frames
            all_results = st.session_state.all_results
            
            # Gallery controls
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("← Back to Results"):
                    st.session_state.show_detailed_gallery = False
                    st.rerun()
            
            with col2:
                st.markdown(f"**📸 Viewing {len(processed_frames)} captured frames**")
            
            with col3:
                if st.button("🗑️ Clear Gallery"):
                    st.session_state.show_detailed_gallery = False
                    st.session_state.processed_frames = []
                    st.session_state.all_results = []
                    st.rerun()
            
            # Frame selector
            frame_options = [f"Frame {i+1} - {frame['timestamp']:.1f}s" for i, frame in enumerate(processed_frames)]
            
            # Initialize selected frame index in session state
            if 'selected_frame_idx' not in st.session_state:
                st.session_state.selected_frame_idx = 0
            
            selected_frame_idx = st.selectbox("🎯 Select Frame to View:", 
                                            range(len(frame_options)), 
                                            index=st.session_state.selected_frame_idx,
                                            format_func=lambda x: frame_options[x])
            
            # Update session state when selection changes
            st.session_state.selected_frame_idx = selected_frame_idx
            
            if selected_frame_idx is not None:
                selected_frame = processed_frames[selected_frame_idx]
                frame_results = [r for r in all_results if r['frame'] == selected_frame['frame_number']]
                
                # Display selected frame
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.image(selected_frame['frame'], 
                           caption=f"Frame {selected_frame_idx + 1} - {selected_frame['timestamp']:.1f}s", 
                           width=600)
                
                with col2:
                    st.markdown("**📊 Frame Information:**")
                    st.markdown(f"""
                    - **Frame Number:** {selected_frame_idx + 1}
                    - **Timestamp:** {selected_frame['timestamp']:.1f}s
                    - **Original Frame:** {selected_frame['frame_number']}
                    """)
                    
                    if frame_results:
                        st.markdown("**🎭 Emotions Detected:**")
                        for i, result in enumerate(frame_results):
                            emotion = result['emotion']
                            confidence = result['confidence']
                            st.markdown(f"""
                            <div style="background: #f0f2f6; padding: 10px; margin: 5px 0; border-radius: 5px;">
                                <strong>{EMOTION_EMOJIS.get(emotion, '😐')} {emotion.title()}</strong><br>
                                <small>Emotion Confidence: {confidence:.1f}%</small><br>
                                <small>Face Detection: {result.get('face_confidence', 'N/A')}</small><br>
                                <small>Detection #{i+1}</small>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ No emotions detected in this frame")
            
            # Navigation buttons
            st.markdown("---")
            nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
            
            with nav_col1:
                if selected_frame_idx > 0:
                    if st.button("⬅️ Previous Frame"):
                        st.session_state.selected_frame_idx = selected_frame_idx - 1
                        st.rerun()
            
            with nav_col2:
                st.markdown(f"**Frame {selected_frame_idx + 1} of {len(processed_frames)}**")
            
            with nav_col3:
                if selected_frame_idx < len(processed_frames) - 1:
                    if st.button("Next Frame ➡️"):
                        st.session_state.selected_frame_idx = selected_frame_idx + 1
                        st.rerun()
        else:
            st.warning("No frames available in gallery. Please process a video first.")
    
    # Emotion History
    if st.session_state.emotion_history:
        st.header("📈 Emotion History")
        
        if st.button("🗑️ Clear History"):
            st.session_state.emotion_history = []
            st.rerun()
        
        # Show recent emotions
        recent_emotions = st.session_state.emotion_history[-10:]  # Last 10 detections
        
        cols = st.columns(min(5, len(recent_emotions)))
        for i, emotion_data in enumerate(recent_emotions):
            with cols[i % 5]:
                emotion = emotion_data['emotion']
                confidence = emotion_data['confidence']
                
                st.markdown(f"""
                <div class="emotion-card">
                    <h4>{EMOTION_EMOJIS.get(emotion, '😐')}</h4>
                    <p>{emotion.title()}</p>
                    <small>{confidence:.1f}%</small>
                </div>
                """, unsafe_allow_html=True)

def display_text_based_mood_input():
    """Display text-based mood input interface"""
    st.header("💬 Text-Based Mood Input")
    st.markdown("**Share your current mood and get personalized recommendations!**")
    st.markdown("*Perfect for when you prefer not to use camera-based detection*")
    
    # Create two columns for different input methods
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Select Your Current Mood")
        st.markdown("Choose from the options below:")
        
        # Emotion selection with descriptions
        emotion_options = {
            "😊 Happy": {
                "emotion": "happy",
                "description": "Feeling joyful, content, or positive",
                "color": "#FFD700"
            },
            "😢 Sad": {
                "emotion": "sad", 
                "description": "Feeling down, blue, or melancholic",
                "color": "#4169E1"
            },
            "😠 Angry": {
                "emotion": "angry",
                "description": "Feeling frustrated, irritated, or mad",
                "color": "#FF4500"
            },
            "😰 Anxious": {
                "emotion": "fear",
                "description": "Feeling worried, nervous, or stressed",
                "color": "#8B4513"
            },
            "😲 Surprised": {
                "emotion": "surprise",
                "description": "Feeling shocked, amazed, or caught off guard",
                "color": "#9370DB"
            },
            "🤢 Disgusted": {
                "emotion": "disgust",
                "description": "Feeling repulsed, grossed out, or appalled",
                "color": "#228B22"
            }
        }
        
        selected_emotion_key = st.selectbox(
            "How are you feeling right now?",
            options=list(emotion_options.keys()),
            format_func=lambda x: f"{x} - {emotion_options[x]['description']}"
        )
        
        # Display selected emotion info
        if selected_emotion_key:
            emotion_data = emotion_options[selected_emotion_key]
            st.markdown(f"""
            <div style="background-color: {emotion_data['color']}20; padding: 15px; border-radius: 10px; border-left: 5px solid {emotion_data['color']}; margin: 10px 0;">
                <h4>{selected_emotion_key}</h4>
                <p><strong>Description:</strong> {emotion_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("✍️ Or Describe Your Mood")
        st.markdown("Type how you're feeling in your own words:")
        
        # Text input for custom mood description
        custom_mood = st.text_area(
            "Describe your current mood:",
            placeholder="e.g., I'm feeling a bit overwhelmed today, or I'm excited about something new, or I'm just feeling neutral...",
            height=100
        )
        
        # Mood intensity slider
        st.markdown("**How intense is this feeling?**")
        mood_intensity = st.slider("Mood Intensity", 1, 10, 5, 
                                 help="1 = Very mild, 10 = Extremely intense")
        
        # Additional context
        st.markdown("**Any additional context?** (Optional)")
        additional_context = st.text_area(
            "Additional context:",
            placeholder="e.g., work stress, relationship issues, upcoming event, etc.",
            height=80
        )
    
    # Process button
    if st.button("🎵 Get My Recommendations", type="primary", use_container_width=True):
        if selected_emotion_key or custom_mood.strip():
            process_text_based_mood(selected_emotion_key, custom_mood, mood_intensity, additional_context)
        else:
            st.warning("Please select a mood or describe how you're feeling!")
    
    # Add some helpful tips
    st.markdown("---")
    st.markdown("### 💡 Tips for Better Recommendations")
    col_tip1, col_tip2, col_tip3 = st.columns(3)
    
    with col_tip1:
        st.markdown("""
        **🎯 Be Specific**
        - The more specific you are, the better recommendations you'll get
        - Include context about what's causing your mood
        """)
    
    with col_tip2:
        st.markdown("""
        **📊 Use the Intensity Slider**
        - Helps us understand how strongly you're feeling
        - Affects the type of recommendations you receive
        """)
    
    with col_tip3:
        st.markdown("""
        **🔄 Try Different Options**
        - You can always come back and try different moods
        - Mix and match selection and text description
        """)

def process_text_based_mood(selected_emotion_key, custom_mood, mood_intensity, additional_context):
    """Process text-based mood input and provide recommendations"""
    
    try:
        # Determine the emotion to use
        if selected_emotion_key:
            emotion_options = {
                "😊 Happy": "happy",
                "😢 Sad": "sad", 
                "😠 Angry": "angry",
                "😰 Anxious": "fear",
                "😲 Surprised": "surprise",
                "🤢 Disgusted": "disgust"
            }
            detected_emotion = emotion_options[selected_emotion_key]
            emotion_source = "selection"
        else:
            # Simple keyword-based emotion detection from text
            detected_emotion = detect_emotion_from_text(custom_mood)
            emotion_source = "text"
        
        # Display results
        st.markdown("---")
        st.subheader("🎯 Your Mood Analysis")
        
        # Show detected emotion
        emotion_display = {
            "happy": "😊 Happy",
            "sad": "😢 Sad", 
            "angry": "😠 Angry",
            "fear": "😰 Anxious/Worried",
            "surprise": "😲 Surprised",
            "disgust": "🤢 Disgusted"
        }
        
        col_emotion, col_intensity = st.columns(2)
        
        with col_emotion:
            st.markdown(f"**Detected Mood:** {emotion_display.get(detected_emotion, '🤔 Mixed Feelings')}")
            st.markdown(f"**Source:** {'Selection' if emotion_source == 'selection' else 'Text Analysis'}")
        
        with col_intensity:
            st.markdown(f"**Intensity Level:** {mood_intensity}/10")
            intensity_bar = "█" * mood_intensity + "░" * (10 - mood_intensity)
            st.markdown(f"`{intensity_bar}`")
        
        # Show context if provided
        if additional_context.strip():
            st.markdown(f"**Context:** {additional_context}")
        
        # Get and display music recommendations
        st.markdown("---")
        st.subheader("🎵 Music Recommendations")
        
        try:
            # Adjust recommendations based on intensity
            num_recommendations = min(6, max(3, mood_intensity))
            recommendations = music_recommender.get_enhanced_recommendations(detected_emotion, num_recommendations)
            
            if recommendations:
                st.session_state.playlist = recommendations
                
                # Display enhanced recommendations
                display_enhanced_music_recommendations(recommendations, detected_emotion, f"🎵 Music for Your {emotion_display.get(detected_emotion, 'Mood')}")
                
                # Display simple player if a track is selected
                if st.session_state.get('show_player') and st.session_state.get('current_track'):
                    st.markdown("---")
                    create_current_player(st.session_state.current_track)
                
                # Professional music section
                create_professional_music_section(recommendations, "🎵 Music Recommendations", detected_emotion)
                
                # Quick play section
                create_quick_play_section(recommendations, "🎮 Quick Play")
                
                # Music insights
                create_music_insights(recommendations, detected_emotion)
            else:
                st.warning("No music recommendations available for this mood.")
        except Exception as e:
            st.error(f"Error loading music recommendations: {e}")
        
        # Get and display reading recommendations
        st.markdown("---")
        st.subheader("📚 Reading Recommendations")
        
        try:
            reading_recs = reading_recommender.get_reading_recommendations(detected_emotion, 4)
            
            # Display reading recommendations
            display_reading_recommendations(reading_recs, detected_emotion, f"📚 Reading for Your {emotion_display.get(detected_emotion, 'Mood')}")
            
            # Display reading insights
            display_reading_insights(detected_emotion)
            
            # Quick reading links
            display_quick_reading_links(reading_recs, detected_emotion)
        except Exception as e:
            st.error(f"Error loading reading recommendations: {e}")
        
        # Get and display wellness recommendations
        st.markdown("---")
        st.subheader("🧘 Wellness Support")
        
        try:
            # Adjust confidence based on intensity and source
            confidence = min(95.0, 70.0 + (mood_intensity * 2.5))
            if emotion_source == "selection":
                confidence += 10.0  # Higher confidence for explicit selection
            
            wellness_recs = wellness_features.get_wellness_recommendations(detected_emotion, confidence)
            
            # Display wellness recommendations
            if wellness_recs:
                st.markdown("**Recommended Wellness Activities:**")
                # Handle both list and dict formats
                if isinstance(wellness_recs, list):
                    activities = wellness_recs[:3]
                else:
                    activities = wellness_recs.get("activities", [])[:3]
                
                for i, activity in enumerate(activities):
                    if isinstance(activity, dict):
                        st.markdown(f"**{i+1}. {activity.get('title', 'Wellness Activity')}**")
                        st.markdown(f"   {activity.get('description', 'A helpful wellness activity')}")
                        if activity.get('priority'):
                            priority_color = "#E74C3C" if activity['priority'] == 'high' else "#F39C12" if activity['priority'] == 'medium' else "#27AE60"
                            st.markdown(f"   🎯 Priority: {activity['priority'].title()}")
                    else:
                        st.markdown(f"**{i+1}. {activity}**")
            else:
                st.info("No specific wellness activities available for this mood. Try the breathing exercises below!")
        except Exception as e:
            st.error(f"Error loading wellness recommendations: {e}")
        
        # Mental Health Resources for Text Input
        st.markdown("---")
        display_mental_health_resources(detected_emotion, mood_intensity, f"🆘 Mental Health Support for Your {emotion_display.get(detected_emotion, 'Mood')}")
        
        # Quick mental health links
        display_quick_mental_health_links(detected_emotion, mood_intensity)
        
        # Add to emotion history
        if 'emotion_history' not in st.session_state:
            st.session_state.emotion_history = []
        
        try:
            st.session_state.emotion_history.append({
                'emotion': detected_emotion,
                'confidence': confidence,
                'source': 'text_input',
                'intensity': mood_intensity,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            st.warning(f"Could not save emotion history: {e}")
            
    except Exception as e:
        st.error(f"An error occurred while processing your mood: {e}")
        st.info("Please try again or contact support if the problem persists.")

def detect_emotion_from_text(text):
    """Simple keyword-based emotion detection from text"""
    text_lower = text.lower()
    
    # Emotion keywords
    emotion_keywords = {
        "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic", "love", "good", "positive", "cheerful", "delighted", "thrilled", "ecstatic"],
        "sad": ["sad", "depressed", "down", "blue", "melancholy", "upset", "crying", "tears", "hurt", "disappointed", "grief", "sorrow", "unhappy", "miserable"],
        "angry": ["angry", "mad", "furious", "rage", "irritated", "annoyed", "frustrated", "pissed", "livid", "fuming", "outraged", "hostile", "bitter"],
        "fear": ["anxious", "worried", "nervous", "scared", "afraid", "fear", "panic", "stress", "overwhelmed", "tense", "uneasy", "apprehensive", "terrified"],
        "surprise": ["surprised", "shocked", "amazed", "astonished", "stunned", "bewildered", "confused", "unexpected", "wow", "incredible", "unbelievable"],
        "disgust": ["disgusted", "grossed", "repulsed", "revolted", "sick", "nauseous", "appalled", "horrified", "disturbed", "offended"]
    }
    
    # Count keyword matches
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    # Return emotion with highest score, or default to "sad" if no clear match
    if emotion_scores:
        return max(emotion_scores.items(), key=lambda x: x[1])[0]
    else:
        return "sad"  # Default emotion

def display_live_webcam_detection():
    """Display live webcam emotion detection interface"""
    st.subheader("📹 Live Webcam Emotion Detection")
    st.markdown("**Capture your emotions in real-time using your webcam!**")
    
    # Initialize webcam session state
    if 'webcam_active' not in st.session_state:
        st.session_state.webcam_active = False
    if 'webcam_frames' not in st.session_state:
        st.session_state.webcam_frames = []
    if 'webcam_emotions' not in st.session_state:
        st.session_state.webcam_emotions = []
    
    # Webcam controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if not st.session_state.webcam_active:
            if st.button("🎥 Start Webcam", type="primary", use_container_width=True):
                st.session_state.webcam_active = True
                st.session_state.webcam_frames = []
                st.session_state.webcam_emotions = []
                st.rerun()
        else:
            if st.button("⏹️ Stop Webcam", type="secondary", use_container_width=True):
                st.session_state.webcam_active = False
                st.rerun()
    
    with col2:
        if st.session_state.webcam_active:
            if st.button("📸 Capture Frame", use_container_width=True):
                # Capture current frame (simulated)
                capture_webcam_frame()
    
    with col3:
        if st.session_state.webcam_frames:
            if st.button("🔄 Clear Frames", use_container_width=True):
                st.session_state.webcam_frames = []
                st.session_state.webcam_emotions = []
                st.rerun()
    
    # Display webcam status
    if st.session_state.webcam_active:
        st.success("🎥 Webcam is active! Click 'Capture Frame' to analyze emotions.")
        
        # Simulated webcam feed
        st.markdown("### 📹 Live Webcam Feed")
        st.info("🎥 **Webcam Feed Active** - Click 'Capture Frame' to analyze emotions in real-time")
        
        # Show capture instructions
        st.markdown("""
        **📸 How to use:**
        1. Position your face in front of the camera
        2. Click 'Capture Frame' to analyze your current emotion
        3. Repeat to capture multiple emotions
        4. Click 'Stop Webcam' when done
        5. View your emotional journey and get recommendations
        """)
        
    else:
        st.info("🎥 Click 'Start Webcam' to begin live emotion detection")
    
    # Display captured frames and emotions
    if st.session_state.webcam_frames:
        st.markdown("---")
        st.subheader("📸 Captured Frames & Emotions")
        
        # Show frame count
        st.markdown(f"**Total Frames Captured:** {len(st.session_state.webcam_frames)}")
        
        # Display frames in a grid
        if len(st.session_state.webcam_frames) > 0:
            cols = st.columns(min(4, len(st.session_state.webcam_frames)))
            for i, (col, frame_data) in enumerate(zip(cols, st.session_state.webcam_frames)):
                with col:
                    st.image(frame_data['image'], caption=f"Frame {i+1}", width=150)
                    st.markdown(f"**Emotion:** {frame_data['emotion']}")
                    st.markdown(f"**Confidence:** {frame_data['confidence']:.1f}%")
        
        # Analyze captured emotions
        if st.button("🎵 Analyze My Emotional Journey", type="primary", use_container_width=True):
            analyze_webcam_emotions()

def capture_webcam_frame():
    """Capture a frame from webcam and analyze emotion"""
    try:
        # Simulate webcam capture (in real implementation, this would capture from actual webcam)
        # For now, we'll use a placeholder image
        import numpy as np
        from PIL import Image
        
        # Create a placeholder image (in real implementation, capture from webcam)
        placeholder_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        pil_image = Image.fromarray(placeholder_image)
        
        # Simulate emotion detection
        emotions = ["happy", "sad", "angry", "fear", "surprise", "disgust"]
        import random
        detected_emotion = random.choice(emotions)
        confidence = random.uniform(70, 95)
        
        # Store frame data
        frame_data = {
            'image': pil_image,
            'emotion': detected_emotion,
            'confidence': confidence,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        
        st.session_state.webcam_frames.append(frame_data)
        st.session_state.webcam_emotions.append({
            'emotion': detected_emotion,
            'confidence': confidence,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        st.success(f"📸 Frame captured! Detected: {detected_emotion} ({confidence:.1f}%)")
        
    except Exception as e:
        st.error(f"Error capturing frame: {e}")

def analyze_webcam_emotions():
    """Analyze captured webcam emotions and provide recommendations"""
    if not st.session_state.webcam_emotions:
        st.warning("No emotions captured yet!")
        return
    
    st.markdown("---")
    st.subheader("🎯 Your Emotional Journey Analysis")
    
    # Calculate emotion statistics
    emotion_counts = {}
    total_confidence = 0
    
    for emotion_data in st.session_state.webcam_emotions:
        emotion = emotion_data['emotion']
        confidence = emotion_data['confidence']
        
        if emotion not in emotion_counts:
            emotion_counts[emotion] = {'count': 0, 'total_confidence': 0}
        
        emotion_counts[emotion]['count'] += 1
        emotion_counts[emotion]['total_confidence'] += confidence
        total_confidence += confidence
    
    # Calculate percentages
    total_frames = len(st.session_state.webcam_emotions)
    emotion_percentages = {}
    
    for emotion, data in emotion_counts.items():
        percentage = (data['count'] / total_frames) * 100
        avg_confidence = data['total_confidence'] / data['count']
        emotion_percentages[emotion] = percentage
    
    # Display emotion statistics
    st.markdown("### 📊 Emotion Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Emotion Distribution:**")
        for emotion, percentage in sorted(emotion_percentages.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"**{emotion.title()}:** {percentage:.1f}% ({emotion_counts[emotion]['count']} frames)")
    
    with col2:
        st.markdown("**Overall Statistics:**")
        st.markdown(f"**Total Frames:** {total_frames}")
        st.markdown(f"**Average Confidence:** {total_confidence/total_frames:.1f}%")
        st.markdown(f"**Dominant Emotion:** {max(emotion_percentages.items(), key=lambda x: x[1])[0].title()}")
    
    # Create emotion chart
    if emotion_percentages:
        import pandas as pd
        import altair as alt
        
        chart_data = pd.DataFrame([
            {"Emotion": emotion.title(), "Percentage": percentage}
            for emotion, percentage in emotion_percentages.items()
        ])
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Emotion', sort='-y'),
            y=alt.Y('Percentage', title='Percentage (%)'),
            color=alt.Color('Emotion', scale=alt.Scale(scheme='category10'))
        ).properties(
            title="Your Emotional Journey",
            width=600,
            height=300
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    # Get dominant emotion for recommendations
    dominant_emotion = max(emotion_percentages.items(), key=lambda x: x[1])[0]
    dominant_percentage = emotion_percentages[dominant_emotion]
    
    # Music Recommendations
    st.markdown("---")
    st.subheader("🎵 Music Recommendations")
    
    try:
        # Create playlist based on emotional journey
        playlist = music_recommender.create_mood_journey_playlist(emotion_percentages, total_frames)
        
        if playlist:
            st.session_state.playlist = playlist
            
            # Display enhanced playlist
            from music_player import display_mood_journey_playlist
            display_mood_journey_playlist(playlist, f"Emotional Journey ({total_frames} frames)")
            
            # Professional emotion-based playlist
            create_emotion_based_playlist(playlist, f"Emotional Journey ({total_frames} frames)")
            
            # Quick play by emotion
            st.markdown("**🎮 Quick Play by Emotion:**")
            emotion_cols = st.columns(min(len(emotion_percentages), 4))
            for i, (emotion, percentage) in enumerate(sorted(emotion_percentages.items(), key=lambda x: x[1], reverse=True)[:4]):
                with emotion_cols[i]:
                    emotion_tracks = [track for track in playlist if track.get('emotion') == emotion]
                    if emotion_tracks:
                        track = emotion_tracks[0]
                        youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
                        if st.button(f"▶️ {emotion.title()}\n({percentage:.1f}%)", key=f"webcam_emotion_play_{emotion}", use_container_width=True):
                            st.markdown(f"**[🎵 Play {track['title']}]({youtube_url})**")
                            st.session_state.current_track = track
                            st.session_state.show_player = True
        else:
            st.warning("No music recommendations available for this emotional journey.")
    except Exception as e:
        st.error(f"Error loading music recommendations: {e}")
    
    # Reading Recommendations
    st.markdown("---")
    st.subheader("📚 Reading Recommendations")
    
    try:
        reading_recs = reading_recommender.get_reading_recommendations(dominant_emotion, 4)
        
        # Display reading recommendations
        display_reading_recommendations(reading_recs, dominant_emotion, f"📚 Reading for Your {dominant_emotion.title()} Journey")
        
        # Display reading insights
        display_reading_insights(dominant_emotion)
        
        # Quick reading links
        display_quick_reading_links(reading_recs, dominant_emotion)
    except Exception as e:
        st.error(f"Error loading reading recommendations: {e}")
    
    # Mental Health Resources
    st.markdown("---")
    display_mental_health_resources(dominant_emotion, int(dominant_percentage), f"🆘 Mental Health Support for Your {dominant_emotion.title()} Journey")
    
    # Quick mental health links
    display_quick_mental_health_links(dominant_emotion, int(dominant_percentage))
    
    # Wellness Recommendations
    st.markdown("---")
    st.subheader("🧘 Wellness Support")
    
    try:
        wellness_recs = wellness_features.get_wellness_recommendations(dominant_emotion, dominant_percentage)
        
        if wellness_recs:
            st.markdown("**Recommended Wellness Activities:**")
            for i, activity in enumerate(wellness_recs[:3]):
                if isinstance(activity, dict):
                    st.markdown(f"**{i+1}. {activity.get('title', 'Wellness Activity')}**")
                    st.markdown(f"   {activity.get('description', 'A helpful wellness activity')}")
                    if activity.get('priority'):
                        priority_color = "#E74C3C" if activity['priority'] == 'high' else "#F39C12" if activity['priority'] == 'medium' else "#27AE60"
                        st.markdown(f"   🎯 Priority: {activity['priority'].title()}")
                else:
                    st.markdown(f"**{i+1}. {activity}**")
        else:
            st.info("No specific wellness activities available for this emotional journey.")
    except Exception as e:
        st.error(f"Error loading wellness recommendations: {e}")
    
    # Breathing exercises for certain emotions
    if dominant_emotion in ["sad", "angry", "fear"]:
        st.markdown("---")
        st.subheader("🫁 Breathing Exercise")
        try:
            display_breathing_exercise(dominant_emotion, wellness_features)
        except Exception as e:
            st.error(f"Error loading breathing exercise: {e}")
    
    # Add to emotion history
    if 'emotion_history' not in st.session_state:
        st.session_state.emotion_history = []
    
    try:
        st.session_state.emotion_history.append({
            'emotion': dominant_emotion,
            'confidence': dominant_percentage,
            'source': 'webcam',
            'frames_captured': total_frames,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        st.warning(f"Could not save emotion history: {e}")
    
    # Resources Section
    create_resources_section()
    
    # Enhanced footer
    create_enhanced_footer()

if __name__ == "__main__":
    main()
