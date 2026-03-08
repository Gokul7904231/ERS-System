"""
Simple YouTube Links - The Most Basic Solution That Will Definitely Work
Just show YouTube links when users click play buttons
"""

import streamlit as st
from typing import Dict

def create_simple_youtube_link(track: Dict, button_text: str = "▶️ Play", key: str = None):
    """
    Create the simplest possible solution - just show YouTube links
    """
    if not track or 'youtube_id' not in track:
        st.warning("⚠️ No track available")
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    # Create a simple button
    if st.button(button_text, key=key, use_container_width=True):
        # Show the YouTube link immediately
        st.markdown("---")
        st.markdown("### 🎵 Click this link to play music:")
        st.markdown(f"**[🎵 {track['title']} - {track['artist']}]({youtube_url})**")
        
        # Also show it as a code block for copying
        st.markdown("**Or copy this URL:**")
        st.code(youtube_url)
        
        # Set session state
        st.session_state.current_track = track
        st.session_state.show_player = True

def show_simple_current_track():
    """Show the current track if one is playing"""
    if hasattr(st.session_state, 'current_track') and st.session_state.current_track:
        track = st.session_state.current_track
        youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
        
        st.markdown("---")
        st.markdown("### 🎵 Now Playing")
        st.markdown(f"**{track['title']}** by {track['artist']}")
        st.markdown(f"**[🎵 Continue Playing]({youtube_url})**")
        
        if st.button("⏹️ Stop", key="stop_simple"):
            st.session_state.current_track = None
            st.session_state.show_player = False
            st.rerun()
