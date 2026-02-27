"""
Professional UI Components for AI MoodMate
Modern, clean, and professional interface design
"""

import streamlit as st
from typing import Dict, List
import streamlit.components.v1 as components

def apply_professional_styling():
    """Apply professional CSS styling to the app"""
    st.markdown("""
    <style>
    /* Main App Styling */
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
        font-size: 18px;
        line-height: 1.6;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.5rem;
        opacity: 0.95;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }
    
    /* Increase font sizes throughout */
    .stMarkdown {
        font-size: 18px;
        line-height: 1.6;
    }
    
    .stMarkdown h1 {
        font-size: 3rem;
        color: #2c3e50;
        margin-bottom: 1.5rem;
    }
    
    .stMarkdown h2 {
        font-size: 2.5rem;
        color: #34495e;
        margin-bottom: 1.2rem;
    }
    
    .stMarkdown h3 {
        font-size: 2rem;
        color: #34495e;
        margin-bottom: 1rem;
    }
    
    .stMarkdown h4 {
        font-size: 1.5rem;
        color: #34495e;
        margin-bottom: 0.8rem;
    }
    
    .stMarkdown p {
        font-size: 18px;
        line-height: 1.6;
        color: #2c3e50;
    }
    
    .stMarkdown li {
        font-size: 18px;
        line-height: 1.6;
        color: #2c3e50;
    }
    
    /* Card Styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        min-height: 50px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Radio Button Styling */
    .stRadio > div {
        font-size: 1.3rem;
        line-height: 1.8;
    }
    
    .stRadio > div > label {
        font-size: 1.3rem;
        font-weight: 500;
        color: #2c3e50;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        font-size: 16px;
    }
    
    .css-1d391kg .stMarkdown {
        font-size: 16px;
        line-height: 1.5;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        font-size: 1.4rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .css-1d391kg p {
        font-size: 16px;
        line-height: 1.5;
        color: #495057;
    }
    
    .css-1d391kg li {
        font-size: 16px;
        line-height: 1.5;
        color: #495057;
    }
    
    /* Scrollable sidebar content */
    .sidebar-content {
        max-height: 70vh;
        overflow-y: auto;
        padding-right: 10px;
    }
    
    .sidebar-content::-webkit-scrollbar {
        width: 6px;
    }
    
    .sidebar-content::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .sidebar-content::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 3px;
    }
    
    .sidebar-content::-webkit-scrollbar-thumb:hover {
        background: #5a6fd8;
    }
    
    /* Success Messages */
    .success-message {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    /* Music Player Styling */
    .music-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    .music-card h3 {
        margin-top: 0;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Emotion Cards */
    .emotion-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 0.5rem;
        text-align: center;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .emotion-card:hover {
        border-color: #667eea;
        transform: scale(1.05);
    }
    
    /* Progress Bar */
    .progress-container {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
    
    /* YouTube Link Styling */
    .youtube-link {
        background: #ff0000;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
    }
    
    .youtube-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 0, 0, 0.4);
        color: white;
        text-decoration: none;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .feature-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_professional_header():
    """Create a professional header for the app"""
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AI MoodMate</h1>
        <p>Your Intelligent Mental Health & Wellness Companion</p>
        <p>Emotion Detection • Music Therapy • Wellness Support</p>
    </div>
    """, unsafe_allow_html=True)

def create_feature_card(title: str, description: str, icon: str, key: str = None):
    """Create a professional feature card"""
    st.markdown(f"""
    <div class="feature-card">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def create_emotion_card(emotion: str, percentage: float, color: str):
    """Create a professional emotion card"""
    st.markdown(f"""
    <div class="emotion-card" style="border-color: {color};">
        <h4>{emotion.title()}</h4>
        <p><strong>{percentage:.1f}%</strong></p>
    </div>
    """, unsafe_allow_html=True)

def create_music_card(track: Dict, emotion: str = None):
    """Create a professional music card"""
    emotion_text = f" for {emotion.title()}" if emotion else ""
    st.markdown(f"""
    <div class="music-card">
        <h3>🎵 {track['title']}</h3>
        <p><strong>by {track['artist']}</strong>{emotion_text}</p>
        <p><a href="https://www.youtube.com/watch?v={track['youtube_id']}" target="_blank" class="youtube-link">▶️ Play on YouTube</a></p>
    </div>
    """, unsafe_allow_html=True)

def create_progress_indicator(message: str):
    """Create a professional progress indicator"""
    st.markdown(f"""
    <div class="progress-container">
        <div class="loading-spinner"></div>
        <strong>{message}</strong>
    </div>
    """, unsafe_allow_html=True)

def create_success_message(message: str):
    """Create a professional success message"""
    st.markdown(f"""
    <div class="success-message">
        ✅ {message}
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, icon: str):
    """Create a professional metric card"""
    st.markdown(f"""
    <div class="metric-card">
        <h4>{icon} {title}</h4>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)

def create_professional_sidebar():
    """Create a clean, professional sidebar"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-bottom: 2rem;">
            <h2 style="color: white; margin: 0; font-size: 2rem;">🧠 AI MoodMate</h2>
            <p style="color: white; margin: 0; opacity: 0.9; font-size: 1.2rem;">Professional Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        # App Status
        st.markdown("### 📊 App Status")
        if st.session_state.get('models_loaded', False):
            st.success("✅ **Models Loaded & Ready**")
        else:
            st.warning("⚠️ **Models Not Loaded**")
            st.info("Click 'Load Models' button to start")
        
        # Quick Stats
        if st.session_state.get('emotion_history'):
            st.markdown("### 📈 Your Journey")
            total_detections = len(st.session_state.emotion_history)
            st.metric("Total Sessions", total_detections)
            
            # Most common emotion
            emotion_counts = {}
            for entry in st.session_state.emotion_history:
                emotion = entry['emotion']
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            if emotion_counts:
                most_common = max(emotion_counts, key=emotion_counts.get)
                st.metric("Most Common Mood", most_common.title())
        
        # Quick Access to Resources
        st.markdown("### 🆘 Quick Help")
        st.markdown("**🚨 Emergency: 911**")
        st.markdown("**🆘 Crisis Line: 988**")
        st.markdown("**💬 Crisis Text: 741741**")
        
        # Link to full resources
        st.markdown("---")
        st.markdown("### 📚 Full Resources")
        st.info("Scroll down to find comprehensive mental health resources, professional help, self-help tools, and wellness tips.")

def create_professional_navigation():
    """Create professional navigation"""
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 3rem;">
        <h2 style="text-align: center; margin: 0; color: #667eea; font-size: 2.5rem;">🎯 How would you like to start?</h2>
        <p style="text-align: center; margin: 1rem 0 0 0; color: #666; font-size: 1.2rem;">Select your preferred method to begin your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

def create_professional_footer():
    """Create a professional footer"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-top: 3rem;">
        <h4 style="color: white; margin: 0;">🧠 AI MoodMate - Professional Edition</h4>
        <p style="color: white; margin: 0; opacity: 0.9;">Powered by Advanced AI • Built for Mental Health & Wellness</p>
        <p style="color: white; margin: 0; opacity: 0.7; font-size: 0.9rem;">© 2024 AI MoodMate. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
