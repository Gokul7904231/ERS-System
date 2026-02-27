"""
Modern UI Components for AI MoodMate
Enhanced professional design with modern UI patterns
"""

import streamlit as st
from typing import Dict, List
import streamlit.components.v1 as components

def apply_modern_styling():
    """Apply modern, professional CSS styling to the app"""
    st.markdown("""
    <style>
    /* Modern App Styling */
    .main {
        padding-top: 1rem;
        padding-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Modern Header Styling */
    .modern-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .modern-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.1;
    }
    
    .modern-header h1 {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .modern-header p {
        font-size: 1.4rem;
        opacity: 0.95;
        margin-bottom: 0.5rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* Modern Typography */
    .stMarkdown {
        font-size: 16px;
        line-height: 1.7;
        color: #2c3e50;
    }
    
    .stMarkdown h1 {
        font-size: 2.8rem;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stMarkdown h2 {
        font-size: 2.2rem;
        color: #34495e;
        margin-bottom: 1.2rem;
        font-weight: 600;
    }
    
    .stMarkdown h3 {
        font-size: 1.8rem;
        color: #34495e;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .stMarkdown h4 {
        font-size: 1.4rem;
        color: #34495e;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }
    
    .stMarkdown p {
        font-size: 16px;
        line-height: 1.7;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    /* Modern Card Styling */
    .modern-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Modern Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        min-height: 55px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Modern Radio Button Styling */
    .stRadio > div {
        font-size: 1.2rem;
        line-height: 1.8;
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stRadio > div > label {
        font-size: 1.2rem;
        font-weight: 500;
        color: #2c3e50;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio > div > label:hover {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        transform: translateX(5px);
    }
    
    /* Modern Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        font-size: 16px;
        border-right: 1px solid #e0e0e0;
    }
    
    .css-1d391kg .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        font-size: 1.3rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .css-1d391kg p {
        font-size: 16px;
        line-height: 1.6;
        color: #495057;
    }
    
    /* Modern Success/Warning/Info Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        border-radius: 15px;
        padding: 1rem;
        color: #155724;
        font-weight: 500;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 1px solid #ffeaa7;
        border-radius: 15px;
        padding: 1rem;
        color: #856404;
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 1px solid #bee5eb;
        border-radius: 15px;
        padding: 1rem;
        color: #0c5460;
        font-weight: 500;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        border-radius: 15px;
        padding: 1rem;
        color: #721c24;
        font-weight: 500;
    }
    
    /* Modern Metric Cards */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Modern File Uploader */
    .stFileUploader > div {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        border: 2px dashed #667eea;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Modern Expander */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #2c3e50;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Modern Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .modern-header h1 {
            font-size: 2.5rem;
        }
        
        .modern-card {
            padding: 1.5rem;
        }
        
        .stButton > button {
            padding: 0.8rem 2rem;
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_modern_header():
    """Create a modern, professional header"""
    st.markdown("""
    <div class="modern-header">
        <h1>🧠 AI MoodMate</h1>
        <p>Your Intelligent Mental Health & Wellness Companion</p>
        <p>Emotion Detection • Music Therapy • Wellness Support</p>
    </div>
    """, unsafe_allow_html=True)

def create_modern_navigation():
    """Create modern navigation with enhanced styling"""
    st.markdown("""
    <div class="modern-card">
        <h2 style="text-align: center; margin: 0; color: #667eea; font-size: 2.5rem;">🎯 How would you like to start?</h2>
        <p style="text-align: center; margin: 1rem 0 0 0; color: #666; font-size: 1.2rem;">Select your preferred method to begin your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

def create_modern_section(title: str, description: str = ""):
    """Create a modern section container"""
    if description:
        st.markdown(f"""
        <div class="modern-card">
            <h2 style="color: #667eea; margin: 0 0 1rem 0;">{title}</h2>
            <p style="color: #666; margin: 0; font-size: 1.1rem;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="modern-card">
            <h2 style="color: #667eea; margin: 0;">{title}</h2>
        </div>
        """, unsafe_allow_html=True)

def create_modern_footer():
    """Create a modern, professional footer"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 25px; margin-top: 4rem; box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);">
        <h3 style="color: white; margin: 0 0 1rem 0; font-size: 2rem;">🧠 AI MoodMate - Professional Edition</h3>
        <p style="color: white; margin: 0 0 1rem 0; opacity: 0.9; font-size: 1.2rem;">Powered by Advanced AI • Built for Mental Health & Wellness</p>
        <p style="color: white; margin: 0; opacity: 0.7; font-size: 1rem;">© 2024 AI MoodMate. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
