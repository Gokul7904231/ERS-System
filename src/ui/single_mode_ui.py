"""
Single Mode UI
Handles photo, video, and webcam emotion detection in single-shot mode.
Extracted from app.py to separate UI from routing logic.
"""

import os
import time
import tempfile
import numpy as np
import cv2
import streamlit as st
from datetime import datetime
from PIL import Image

from src.core.emotion_engine import (
    detect_faces_and_emotions,
    draw_results,
    fuse_emotions,
    standardize_emotion_result,
    detect_emotion_from_text_simple,
)
from src.ui.enhanced_ui import create_soothing_section
from src.ui.recommendation_panel import display_unified_recommendation_panel
from src.ui.video_analysis_dashboard import render_video_analysis_dashboard


def _process_emotion_result(emotion, confidence, source):
    """Handle the final emotion result for single mode."""
    result = standardize_emotion_result(emotion, confidence, source)
    st.session_state.emotion_history.append({
        'timestamp': datetime.now(),
        'emotion': emotion,
        'confidence': confidence,
        'source': source,
    })
    display_unified_recommendation_panel(result["emotion"], result["confidence"])


def render_single_mode_ui():
    """Renders the UI for single-shot emotion detection and recommendation."""
    create_soothing_section(
        "Single-Mode Emotion Analysis",
        "Directly analyze an input and get immediate recommendations.",
        "pastel-blue",
    )

    method = st.radio(
        "Select Input Method:",
        ["📸 Photo", "🎬 Video", "📹 Webcam", "✍️ Text"],
        horizontal=True,
        key="single_mode_method",
    )

    conf_thres = st.sidebar.slider("Face Confidence Threshold", 0.1, 1.0, 0.5, 0.05)
    iou_thres = st.sidebar.slider("IoU Threshold", 0.1, 1.0, 0.45, 0.05)

    if method == "📸 Photo":
        _render_photo_mode(conf_thres, iou_thres)
    elif method == "🎬 Video":
        render_video_analysis_dashboard()
    elif method == "📹 Webcam":
        _render_webcam_mode(conf_thres, iou_thres)
    elif method == "✍️ Text":
        _render_text_mode()


def _render_photo_mode(conf_thres, iou_thres):
    """Handle photo upload and analysis."""
    uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        if st.button("Analyze Photo", type="primary", use_container_width=True):
            with st.spinner("Analyzing..."):
                image = Image.open(uploaded_file)
                results, error = detect_faces_and_emotions(image, conf_thres, iou_thres)
                if error:
                    st.error(f"Analysis failed: {error}")
                elif results:
                    st.image(
                        draw_results(np.array(image), results),
                        caption="Analysis Result",
                        width=600,
                    )
                    dom_emotion = max(results, key=lambda x: x['confidence'])
                    _process_emotion_result(
                        dom_emotion['emotion'], dom_emotion['confidence'], "photo"
                    )
                else:
                    st.warning("No faces were detected in the image.")


# Legacy video functions removed in favor of Video Analysis Dashboard


def _render_webcam_mode(conf_t, iou_t):
    """Handles live webcam detection for single mode."""
    st.info(
        "The webcam will capture a short burst of frames for analysis. "
        "Multiple faces will be considered for a comprehensive emotion assessment."
    )
    if st.button("Start Webcam Analysis", type="primary", use_container_width=True):
        st.session_state.webcam_active = True

    if st.session_state.webcam_active:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error(
                "Error: Could not access webcam. "
                "Please ensure it is connected and not in use by another application."
            )
            st.session_state.webcam_active = False
            return

        placeholder = st.empty()
        status_text = st.empty()
        all_webcam_results = []

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
                placeholder.image(
                    processed_frame,
                    caption=f"Processing frame {i+1}/{num_frames_to_capture} "
                            f"(Detected {len(results)} face(s))",
                )
                all_webcam_results.extend(results)
            else:
                placeholder.image(
                    frame_rgb,
                    caption=f"Processing frame {i+1}/{num_frames_to_capture} (No faces detected)",
                )

            status_text.info(f"Capturing frame {i+1}/{num_frames_to_capture}...")
            time.sleep(0.05)

        cap.release()
        st.session_state.webcam_active = False
        status_text.empty()

        if all_webcam_results:
            dom_emo, avg_conf = fuse_emotions(all_webcam_results)
            st.success(
                f"Webcam analysis complete. Dominant emotion: {dom_emo.title()} "
                f"(Avg Confidence: {avg_conf:.1f}%)"
            )
            _process_emotion_result(dom_emo, avg_conf, "webcam")
        else:
            st.warning(
                "No faces were detected during webcam analysis. "
                "Please ensure your face is clearly visible in the camera frame."
            )


def _render_text_mode():
    """Renders the high-fidelity text-based mood input form."""
    st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.05); padding: 1.5rem; border-radius: 15px; border-left: 5px solid #667eea; margin-bottom: 2rem;">
            <h4 style="margin: 0; color: #667eea;">✍️ Share Your Thoughts</h4>
            <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.95rem;">
                Tell us how you're feeling for a more personal recommendation.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✍️ Describe Your Mood")
    mood_desc = st.text_area(
        "Describe your current mood:",
        placeholder="e.g., I'm feeling a bit overwhelmed today, or I'm excited about something new...",
        height=100,
        help="Our AI will analyze your description to detect your emotion."
    )

    intensity = st.slider("Mood Intensity", 1, 10, 5, help="How strong is this feeling?")

    st.markdown("### 📝 Additional Context")
    extra_context = st.text_area(
        "Additional context:",
        placeholder="e.g., work stress, relationship issues, upcoming event, etc.",
        height=80
    )

    if st.button("🚀 Analyze Mood & Get Recommendations", type="primary", use_container_width=True):
        if not mood_desc.strip():
            st.warning("Please describe your mood before analyzing.")
        else:
            final_mood = detect_emotion_from_text_simple(mood_desc)
            if not final_mood or final_mood == "neutral":
                final_mood = "neutral"

            # Adjust confidence based on intensity
            confidence = 70.0 + (intensity * 2.0)
            confidence = min(100.0, confidence)

            _process_emotion_result(final_mood, confidence, "text_input")
            st.balloons()
