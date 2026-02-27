"""
Basic Music Player - The Simplest Possible Solution
This will definitely work by just showing YouTube links
"""

import streamlit as st
from typing import Dict

def create_basic_play_button(track: Dict, button_text: str = "▶️ Play", key: str = None):
    """
    Create the simplest possible play button that just shows YouTube links
    """
    if not track or 'youtube_id' not in track:
        st.warning("⚠️ No track available")
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    # Just create a simple button that shows the link
    if st.button(button_text, key=key, use_container_width=True):
        st.success(f"🎵 {track['title']} by {track['artist']}")
        
        # Show the YouTube link in a prominent way
        st.markdown("---")
        st.markdown("### 🎵 Click this link to play:")
        st.markdown(f"**[🎵 {track['title']} - {track['artist']}]({youtube_url})**")
        
        # Also show the URL for copying
        st.markdown("**Or copy this URL:**")
        st.code(youtube_url)
        
        # Set session state
        st.session_state.current_track = track

def display_basic_player(track: Dict):
    """Display basic player info"""
    if not track or 'youtube_id' not in track:
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    st.markdown("---")
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    st.markdown(f"**[🎵 Continue Playing on YouTube]({youtube_url})**")
    
    # Stop button
    if st.button("⏹️ Stop", key="stop_basic"):
        st.session_state.current_track = None
        st.rerun()
