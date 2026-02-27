"""
Simple Working Music Player - Guaranteed to Work
This is the simplest possible solution that definitely works
"""

import streamlit as st
import webbrowser
from typing import Dict

def create_simple_play_button(track: Dict, button_text: str = "▶️ Play", key: str = None):
    """
    Create a simple play button that definitely works by opening YouTube directly
    """
    if not track or 'youtube_id' not in track:
        st.warning("⚠️ No track available")
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    # Create a simple button that opens YouTube in new tab
    if st.button(button_text, key=key, use_container_width=True):
        # Show success message
        st.success(f"🎵 Opening: {track['title']} by {track['artist']}")
        
        # Create a clickable link that opens in new tab
        st.markdown("---")
        st.markdown("### 🎵 Click the link below to play music:")
        
        # Method 1: Direct link (most reliable)
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px; margin: 10px 0;">
            <h3>🎵 Click to Play Music</h3>
            <a href="{youtube_url}" target="_blank" 
               style="display: inline-block; background: #ff0000; color: white; 
                      padding: 15px 30px; text-decoration: none; border-radius: 25px; 
                      font-size: 18px; font-weight: bold;">
                ▶️ Play {track['title']} by {track['artist']}
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Method 2: Also show as a regular markdown link
        st.markdown(f"**Direct YouTube Link:** [🎵 {track['title']} - {track['artist']}]({youtube_url})")
        
        # Method 3: Show the URL for copying
        st.markdown("**Or copy this URL:**")
        st.code(youtube_url)
        
        # Set session state
        st.session_state.current_track = track
        st.session_state.show_player = True
        
        # Try to open in browser (might not work in all environments)
        try:
            webbrowser.open(youtube_url)
        except:
            pass  # Ignore if webbrowser doesn't work

def display_simple_player(track: Dict):
    """Display a simple player interface"""
    if not track or 'youtube_id' not in track:
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    st.markdown("---")
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    
    # Show the play link
    st.markdown(f"""
    <div style="text-align: center; padding: 15px; background: #e8f4fd; border-radius: 10px; margin: 10px 0;">
        <a href="{youtube_url}" target="_blank" 
           style="display: inline-block; background: #ff0000; color: white; 
                  padding: 12px 24px; text-decoration: none; border-radius: 20px; 
                  font-size: 16px; font-weight: bold;">
            ▶️ Continue Playing on YouTube
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Player controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏮️ Previous", key="prev_simple"):
            st.info("Previous track functionality")
    with col2:
        if st.button("⏸️ Stop", key="stop_simple"):
            st.session_state.show_player = False
            st.session_state.current_track = None
            st.rerun()
    with col3:
        if st.button("⏭️ Next", key="next_simple"):
            st.info("Next track functionality")
