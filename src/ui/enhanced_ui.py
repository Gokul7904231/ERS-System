"""
Enhanced UI Components for AI MoodMate
Clear, engaging design with soothing pastel colors and interactive elements
"""

import streamlit as st
from typing import Dict, List
import streamlit.components.v1 as components

def apply_enhanced_styling():
    """Apply enhanced, clear styling with soothing pastel colors"""
    st.markdown("""
    <style>
    /* Enhanced App Styling */
    .main {
        padding-top: 1rem;
        padding-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 50%, #f0f8ff 100%);
        min-height: 100vh;
    }
    
    /* Clear, Crisp Header Styling */
    .enhanced-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .enhanced-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .enhanced-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.1);
        z-index: 1;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .enhanced-header h1 {
        font-size: 5rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        text-shadow: 5px 5px 10px rgba(0,0,0,0.8);
        position: relative;
        z-index: 3;
        letter-spacing: -2px;
        color: #ffffff !important;
        text-stroke: 2px rgba(0,0,0,0.6);
        -webkit-text-stroke: 2px rgba(0,0,0,0.6);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .enhanced-header p {
        font-size: 1.6rem;
        opacity: 1;
        margin-bottom: 0.8rem;
        font-weight: 700;
        position: relative;
        z-index: 3;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        color: #ffffff;
        text-stroke: 0.5px rgba(0,0,0,0.3);
        -webkit-text-stroke: 0.5px rgba(0,0,0,0.3);
    }
    
    /* Soothing Pastel Colors */
    .pastel-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .pastel-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 50%, #7fcdcd 100%);
    }
    
    .pastel-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.2);
    }
    
    /* Interactive Cursor Effects */
    .interactive-button {
        background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 50%, #7fcdcd 100%);
        color: #2c3e50;
        border: none;
        border-radius: 50px;
        padding: 1.2rem 3rem;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(168, 230, 207, 0.4);
        min-height: 60px;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .interactive-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .interactive-button:hover::before {
        left: 100%;
    }
    
    .interactive-button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 40px rgba(168, 230, 207, 0.6);
        background: linear-gradient(135deg, #b8f6df 0%, #98e8d0 50%, #8fdddd 100%);
    }
    
    /* Soothing Radio Buttons */
    .soothing-radio {
        background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.1);
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .soothing-radio:hover {
        border-color: #a8e6cf;
        box-shadow: 0 15px 35px rgba(168, 230, 207, 0.2);
    }
    
    .soothing-radio label {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 100%);
        border: 2px solid transparent;
    }
    
    .soothing-radio label:hover {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
        border-color: #a8e6cf;
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 20px rgba(168, 230, 207, 0.3);
    }
    
    /* Pastel Color Palette */
    .pastel-blue { background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); }
    .pastel-green { background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); }
    .pastel-purple { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); }
    .pastel-pink { background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%); }
    .pastel-orange { background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%); }
    
    /* Enhanced Typography */
    .stMarkdown {
        font-size: 17px;
        line-height: 1.7;
        color: #2c3e50;
    }
    
    .stMarkdown h1 {
        font-size: 3rem;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stMarkdown h2 {
        font-size: 2.4rem;
        color: #34495e;
        margin-bottom: 1.2rem;
        font-weight: 600;
    }
    
    .stMarkdown h3 {
        font-size: 1.9rem;
        color: #34495e;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Soothing Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9ff 100%);
        font-size: 16px;
        border-right: 2px solid #e8f4fd;
    }
    
    .css-1d391kg .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Enhanced Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #a8e6cf;
        border-radius: 20px;
        padding: 1.2rem;
        color: #155724;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(168, 230, 207, 0.3);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffd93d;
        border-radius: 20px;
        padding: 1.2rem;
        color: #856404;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(255, 217, 61, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 2px solid #7fcdcd;
        border-radius: 20px;
        padding: 1.2rem;
        color: #0c5460;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(127, 205, 205, 0.3);
    }
    
    /* Custom Cursor */
    body {
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="%23a8e6cf" opacity="0.3"/><circle cx="12" cy="12" r="6" fill="%23667eea" opacity="0.6"/><circle cx="12" cy="12" r="2" fill="%23667eea"/></svg>'), auto;
    }
    
    /* Hover Effects */
    .hover-lift {
        transition: all 0.3s ease;
    }
    
    .hover-lift:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.2);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .enhanced-header h1 {
            font-size: 3rem;
        }
        
        .pastel-card {
            padding: 2rem;
        }
        
        .interactive-button {
            padding: 1rem 2.5rem;
            font-size: 1.1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_enhanced_header():
    """Create a clear, crisp header with enhanced styling"""
    st.markdown("""
    <div class="enhanced-header">
        <h1>🧠 Sentixcare</h1>
        <p>Your Intelligent Mental Health & Wellness Companion</p>
        <p>Emotion Detection • Music Therapy • Wellness Support</p>
    </div>
    """, unsafe_allow_html=True)

def create_soothing_navigation():
    """Create soothing navigation with pastel colors"""
    st.markdown("""
    <div class="pastel-card">
        <h2 style="text-align: center; margin: 0; color: #667eea; font-size: 2.8rem; font-weight: 700;">🎯 How would you like to start?</h2>
        <p style="text-align: center; margin: 1.5rem 0 0 0; color: #666; font-size: 1.3rem; font-weight: 400;">Select your preferred method to begin your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

def create_soothing_section(title: str, description: str = "", color_class: str = "pastel-blue"):
    """Create a soothing section with pastel colors"""
    if description:
        st.markdown(f"""
        <div class="pastel-card {color_class}">
            <h2 style="color: #667eea; margin: 0 0 1.5rem 0; font-size: 2.4rem; font-weight: 700;">{title}</h2>
            <p style="color: #666; margin: 0; font-size: 1.2rem; font-weight: 400; line-height: 1.6;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="pastel-card {color_class}">
            <h2 style="color: #667eea; margin: 0; font-size: 2.4rem; font-weight: 700;">{title}</h2>
        </div>
        """, unsafe_allow_html=True)

def create_enhanced_footer():
    """Create an enhanced, soothing footer"""
    st.markdown("""
    <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 30px; margin-top: 4rem; box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%); animation: shimmer 4s ease-in-out infinite;"></div>
        <h3 style="color: white; margin: 0 0 1.5rem 0; font-size: 2.2rem; font-weight: 700; position: relative; z-index: 2;">🧠 Sentixcare - Professional Edition</h3>
        <p style="color: white; margin: 0 0 1rem 0; opacity: 0.95; font-size: 1.3rem; font-weight: 400; position: relative; z-index: 2;">Powered by Advanced AI • Built for Mental Health & Wellness</p>
        <p style="color: white; margin: 0; opacity: 0.8; font-size: 1rem; position: relative; z-index: 2;">© 2026 Sentixcare. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def apply_chat_styling():
    """Apply modern chat UI styling with chat bubbles and enhanced components"""
    st.markdown("""
    <style>
    /* Chat Container Styling - Dark Theme */
    .chat-container {
        max-width: 100%;
        margin: 0 auto;
    }
    
    /* Chat Header */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 16px 16px 0 0;
        color: white;
        margin-bottom: 0;
    }
    
    .chat-header h4 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .chat-header p {
        margin: 5px 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Chat Messages Area - Dark Theme */
    .chat-messages {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px;
        min-height: 150px;
        max-height: 400px;
        overflow-y: auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Modern Chat Bubbles */
    .chat-message {
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message.user {
        justify-content: flex-end;
    }
    
    .chat-message.bot {
        justify-content: flex-start;
    }
    
    .message-bubble {
        max-width: 75%;
        padding: 14px 18px;
        border-radius: 16px;
        font-size: 15px;
        line-height: 1.5;
        word-wrap: break-word;
        position: relative;
    }
    
    /* User Message Bubble (Right aligned) - Gradient with shadow */
    .chat-message.user .message-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Bot/Companion Message Bubble (Left aligned) - Dark neutral */
    .chat-message.bot .message-bubble {
        background: #1e293b;
        color: #e2e8f0;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .message-label {
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 4px;
        display: block;
    }
    
    .chat-message.user .message-label {
        color: rgba(255, 255, 255, 0.8);
        text-align: right;
    }
    
    .chat-message.bot .message-label {
        color: #94a3b8;
    }
    
    .message-content {
        display: block;
    }
    
    /* Chat Input Area - Dark Theme */
    .chat-input-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 16px;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    .chat-input {
        flex: 1;
        padding: 14px 18px;
        border: 2px solid #334155;
        border-radius: 25px;
        font-size: 15px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: all 0.3s ease;
        outline: none;
        background: #0f172a;
        color: #e2e8f0;
    }
    
    .chat-input:focus {
        border-color: #667eea;
        background: #1e293b;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
    }
    
    .chat-input::placeholder {
        color: #64748b;
    }
    
    /* Chat Buttons */
    .chat-button {
        padding: 12px 24px;
        border: none;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .chat-button.send {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .chat-button.send:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .chat-button.send:active {
        transform: scale(0.98);
    }
    
    .chat-button.clear {
        background: #334155;
        color: #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .chat-button.clear:hover {
        background: #475569;
        transform: scale(1.02);
    }
    
    /* Wellness Tip Section */
    .wellness-tip {
        background: #1e293b;
        padding: 16px;
        border-radius: 12px;
        margin-top: 16px;
        border-left: 4px solid #10b981;
    }
    
    .wellness-tip h5 {
        margin: 0 0 8px 0;
        color: #34d399;
        font-size: 14px;
    }
    
    .wellness-tip p {
        margin: 0;
        color: #94a3b8;
        font-size: 13px;
    }
    
    /* Coping Strategies */
    .coping-strategies {
        background: #1e293b;
        padding: 16px;
        border-radius: 12px;
        margin-top: 12px;
    }
    
    .coping-strategies h5 {
        margin: 0 0 12px 0;
        color: #94a3b8;
        font-size: 14px;
    }
    
    .coping-strategies ol {
        margin: 0;
        padding-left: 20px;
    }
    
    .coping-strategies li {
        margin: 8px 0;
        color: #cbd5e1;
        font-size: 13px;
    }
    
    /* Welcome Message - Dark Theme */
    .welcome-message {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        color: #e2e8f0;
        margin-bottom: 20px;
        border: 1px solid #334155;
    }
    
    .welcome-message h4 {
        margin: 0 0 8px 0;
        font-size: 1.2rem;
        color: #f1f5f9;
    }
    
    .welcome-message p {
        margin: 0;
        font-size: 14px;
        opacity: 0.95;
        color: #94a3b8;
    }
    
    /* Scrollbar Styling - Dark Theme */
    .chat-messages::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .message-bubble {
            max-width: 90%;
            padding: 12px 14px;
            font-size: 14px;
        }
        
        .chat-input-container {
            padding: 12px;
        }
        
        .chat-button {
            padding: 10px 18px;
            font-size: 13px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
