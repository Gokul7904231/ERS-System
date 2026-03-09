"""
Centralized Session State Management
All session state defaults are defined here to prevent scattered initialization
and ensure consistent state across the application.
"""

import streamlit as st


def init_session_state():
    """Initialize all session state variables with safe defaults.
    
    Call this once at the top of app.py before any UI rendering.
    Uses setdefault pattern to avoid overwriting existing values.
    """
    defaults = {
        # Model state
        'models_loaded': False,
        'device': None,
        'face_model': None,
        'fer_detector': None,

        # Input mode
        'input_mode': 'single',

        # Emotion results
        'final_emotion': None,
        'final_confidence': None,
        'multimodal_results': [],
        'emotion_history': [],
        'all_results': [],
        'processed_frames': [],
        'show_multimodal_recommendations': False,

        # Music
        'playlist': [],
        'current_track': None,
        'current_track_index': 0,

        # Webcam
        'webcam_active': False,

        # Coloring game
        'coloring_progress': {},

        # Chat
        'chat_history': [],
        'chat_input_key': 0,
        'pending_message': None,

        # Journal
        'journal_entries': [],

        # Video Analysis Dashboard
        'video_analysis_results': None,
        'video_metadata': {},

        # Advanced emotion pipeline
        'advanced_detector': None,
        'emotion_smoother': None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
