"""
Video Analysis Dashboard
Provides advanced video processing with time-series analytics, emotion distribution,
and interactive visualizations for emotion tracking.
"""

import os
import time
import tempfile
import numpy as np
import cv2
import pandas as pd
import altair as alt
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image

from src.core.emotion_engine import detect_faces_and_emotions, fuse_emotions
from src.utils.constants import EMOTION_COLORS, EMOTION_EMOJIS

def render_video_analysis_dashboard():
    """Main entry point for the Video Analysis Dashboard UI."""
    st.markdown("""
        <style>
            .force-black-text {
                color: #000000 !important;
                -webkit-text-fill-color: #000000 !important;
                background-clip: unset !important;
                -webkit-background-clip: unset !important;
                background: none !important;
                text-shadow: none !important;
                opacity: 1 !important;
                visibility: visible !important;
                display: block !important;
            }
        </style>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2.5rem 2rem; border-radius: 20px; margin-bottom: 2rem;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); position: relative;">
            <div class="force-black-text" style="font-size: 2.8rem; font-weight: 800; line-height: 1.2;">
                📹 Advanced Video Analytics
            </div>
            <div class="force-black-text" style="margin-top: 0.8rem; font-size: 1.2rem; font-weight: 700;">
                Process video files to uncover deep emotional patterns over time.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar parameters
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Dashboard Settings")
    conf_thres = st.sidebar.slider("Detection Confidence", 0.1, 1.0, 0.5, 0.05, key="vid_dash_conf")
    iou_thres = st.sidebar.slider("IoU Threshold", 0.1, 1.0, 0.45, 0.05, key="vid_dash_iou")

    # Step 1: Upload
    st.markdown("### 📤 Upload a Video")
    uploaded_video = st.file_uploader(
        "Choose a video file...", 
        type=['mp4', 'mov', 'avi', 'mpeg4'],
        help="Recommended size: under 50MB for faster processing."
    )

    if uploaded_video:
        # Step 2: Processing Settings
        st.markdown("### ⏱️ Processing Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            process_seconds = st.number_input(
                "Process first N seconds", 
                min_value=1, max_value=300, value=10,
                help="Maximum duration of the video to analyze."
            )
        
        with col2:
            frame_skip = st.number_input(
                "Skip every N frames", 
                min_value=1, max_value=60, value=5,
                help="Higher values = faster processing but lower temporal resolution."
            )

        if st.button("🚀 Start Deep Analysis", type="primary", use_container_width=True):
            _handle_video_processing(uploaded_video, process_seconds, frame_skip, conf_thres, iou_thres)

    # Step 3: Render Results if they exist
    if st.session_state.get('video_analysis_results'):
        _render_dashboard_results()

def _handle_video_processing(uploaded_file, max_sec, skip, conf, iou):
    """Orchestrates the video processing pipeline."""
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.close()
    
    cap = cv2.VideoCapture(tfile.name)
    if not cap.isOpened():
        st.error("❌ Failed to open video file.")
        return

    # Metadata
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    actual_process_sec = min(max_sec, duration)
    frames_to_process = int(actual_process_sec * fps)

    # Display Info Box
    st.info(f"""
    📊 **Video Information**
    - **Total Duration:** {duration:.1f} seconds
    - **Resolution:** {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}
    - **FPS:** {fps:.1f}
    - **Target Clip:** {actual_process_sec:.1f} seconds ({frames_to_process} frames)
    """)

    progress_bar = st.progress(0)
    status_text = st.empty()
    frame_preview = st.empty()
    
    results = []
    
    try:
        start_time = time.time()
        processed_count = 0
        
        for i in range(0, frames_to_process):
            ret, frame = cap.read()
            if not ret:
                break
                
            if i % skip == 0:
                # Frame Analysis
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_results, _ = detect_faces_and_emotions(frame_rgb, conf, iou)
                
                timestamp = i / fps
                
                if frame_results:
                    # Get dominant emotion for this frame
                    dom_emo, dom_conf = fuse_emotions(frame_results)
                    results.append({
                        'time': timestamp,
                        'emotion': dom_emo,
                        'confidence': dom_conf,
                        'detections': len(frame_results)
                    })
                    
                    # Update Preview
                    from src.core.emotion_engine import draw_results
                    preview_img = draw_results(frame_rgb, frame_results)
                    frame_preview.image(preview_img, caption=f"Processing: {timestamp:.1f}s / {actual_process_sec:.1f}s", use_container_width=True)
                else:
                    results.append({
                        'time': timestamp,
                        'emotion': 'none',
                        'confidence': 0.0,
                        'detections': 0
                    })
                
                processed_count += 1
            
            # Progress Update
            progress = (i + 1) / frames_to_process
            progress_bar.progress(progress)
            status_text.markdown(f"**Processing frame {i+1}/{frames_to_process} ({timestamp:.1f}s/{actual_process_sec:.1f}s)**")

        total_time = time.time() - start_time
        st.success(f"✅ Deep analysis completed in {total_time:.1f} seconds! ({processed_count} samples)")
        
        # Save results to session state
        st.session_state.video_analysis_results = results
        st.session_state.video_metadata = {
            'processed_frames': processed_count,
            'duration': actual_process_sec,
            'total_time': total_time
        }
        
    finally:
        cap.release()
        try:
            os.unlink(tfile.name)
        except OSError:
            pass

def _render_dashboard_results():
    """Renders the analytics dashboard from stored results."""
    data = st.session_state.video_analysis_results
    meta = st.session_state.video_metadata
    
    if not data:
        st.warning("No data available to display.")
        return

    df = pd.DataFrame(data)
    # Filter out 'none' for charts
    df_filtered = df[df['emotion'] != 'none'].copy()

    st.markdown("---")
    st.header("📈 Processing Summary")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Samples Analyzed", meta['processed_frames'])
    col2.metric("Clip Duration", f"{meta['duration']:.1f}s")
    
    if not df_filtered.empty:
        top_emotion = df_filtered['emotion'].mode().iloc[0]
        col3.metric("Dominant Emotion", top_emotion.title(), f"{EMOTION_EMOJIS.get(top_emotion, '')}")
    else:
        col3.metric("Dominant Emotion", "N/A")

    # Dynamic Emotion Timeline
    st.subheader("📊 Dynamic Emotion Timeline")
    if not df_filtered.empty:
        chart = alt.Chart(df_filtered).mark_circle(size=60, opacity=0.7).encode(
            x=alt.X('time:Q', title='Time (seconds)'),
            y=alt.Y('confidence:Q', title='Confidence (%)', scale=alt.Scale(domain=[0, 100])),
            color=alt.Color('emotion:N', title='Emotion', scale=alt.Scale(
                domain=['anger', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'],
                range=['#ff4b4b', '#2ecc71', '#9b59b6', '#f1c40f', '#95a5a6', '#3498db', '#e67e22']
            )),
            tooltip=['time', 'emotion', 'confidence']
        ).properties(
            width='container',
            height=400
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No emotional data detected across the timeline.")

    # Distribution and Details
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("🍩 Emotion Distribution")
        if not df_filtered.empty:
            dist_df = df_filtered['emotion'].value_counts().reset_index()
            dist_df.columns = ['emotion', 'count']
            
            donut = alt.Chart(dist_df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="count", type="quantitative"),
                color=alt.Color(field="emotion", type="nominal", scale=alt.Scale(
                    domain=['anger', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'],
                    range=['#ff4b4b', '#2ecc71', '#9b59b6', '#f1c40f', '#95a5a6', '#3498db', '#e67e22']
                )),
                tooltip=['emotion', 'count']
            ).properties(height=300)
            
            st.altair_chart(donut, use_container_width=True)
        else:
            st.write("No distribution data available.")

    with col_right:
        st.subheader("📋 Detailed Statistics")
        if not df_filtered.empty:
            stats = df_filtered.groupby('emotion').agg({
                'confidence': ['mean', 'max'],
                'time': 'count'
            }).reset_index()
            stats.columns = ['Emotion', 'Avg Conf', 'Max Conf', 'Occurrences']
            stats['Emotion'] = stats['Emotion'].str.title()
            stats['Avg Conf'] = stats['Avg Conf'].map('{:.1f}%'.format)
            stats['Max Conf'] = stats['Max Conf'].map('{:.1f}%'.format)
            
            st.dataframe(stats, use_container_width=True, hide_index=True)
        else:
            st.write("No detection statistics available.")

    # Final Action
    if not df_filtered.empty:
        if st.button("Apply Final Analysis for Recommendations", type="primary", use_container_width=True):
            avg_emo, avg_conf = fuse_emotions(data) # Use all data for fusion
            st.session_state.final_emotion = avg_emo
            st.session_state.final_confidence = avg_conf
            st.success(f"Applied! You can now view recommendations based on **{avg_emo.title()}**.")
            
            # Switch to results if we were in a sub-tab
            # (In single mode, display_unified_recommendation_panel will be called)
            from src.ui.recommendation_panel import display_unified_recommendation_panel
            display_unified_recommendation_panel(avg_emo, avg_conf)
