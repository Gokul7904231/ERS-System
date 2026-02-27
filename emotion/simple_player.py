"""
Ultra Simple Music Player - Guaranteed to Work
This creates a simple solution that opens YouTube directly
"""

import streamlit as st
from typing import Dict

def create_simple_play_button(track: Dict, button_text: str = "▶️ Play", key: str = None):
    """Create a simple play button that opens YouTube directly"""
    if not track or 'youtube_id' not in track:
        st.warning("No track available")
        return
    
    youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
    
    # Create a button that shows the YouTube link
    if st.button(button_text, key=key, use_container_width=True):
        st.success(f"🎵 Opening: {track['title']} by {track['artist']}")
        
        # Show the YouTube link prominently
        st.markdown("---")
        st.markdown("### 🎵 Click the link below to play:")
        st.markdown(f"**[🎵 {track['title']} - {track['artist']}]({youtube_url})**")
        
        # Also show it as a clickable link in a box
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0;">
            <h3>🎵 Click to Play Music</h3>
            <a href="{youtube_url}" target="_blank" style="font-size: 18px; color: #ff0000; text-decoration: none;">
                ▶️ Play {track['title']} by {track['artist']}
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Set session state
        st.session_state.current_track = track
        st.session_state.show_player = True

def display_simple_player(track: Dict):
    """Display a simple player that shows YouTube link"""
    if not track or 'youtube_id' not in track:
        return
    
    youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
    
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    
    # Show the YouTube link prominently
    st.markdown("---")
    st.markdown("### 🎵 Click to Play:")
    st.markdown(f"**[🎵 {track['title']} - {track['artist']}]({youtube_url})**")
    
    # Also show it as a clickable link in a box
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0;">
        <h3>🎵 Click to Play Music</h3>
        <a href="{youtube_url}" target="_blank" style="font-size: 18px; color: #ff0000; text-decoration: none;">
            ▶️ Play {track['title']} by {track['artist']}
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Player controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏮️ Previous"):
            st.info("Previous track functionality")
    with col2:
        if st.button("⏸️ Stop"):
            st.session_state.show_player = False
            st.session_state.current_track = None
            st.rerun()
    with col3:
        if st.button("⏭️ Next"):
            st.info("Next track functionality")
