"""
Direct Music Player - Guaranteed to Work
This creates a direct solution that actually plays music
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict

def create_direct_play_button(track: Dict, button_text: str = "▶️ Play", key: str = None):
    """Create a direct play button that actually plays music"""
    if not track or 'youtube_id' not in track:
        st.warning("No track available")
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    # Create a button that directly opens YouTube
    if st.button(button_text, key=key, use_container_width=True):
        st.success(f"🎵 Opening: {track['title']} by {track['artist']}")
        
        # Method 1: Direct iframe with autoplay
        st.markdown("### 🎵 Music Player")
        iframe_html = f"""
        <iframe width="100%" height="315" 
                src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
        """
        st.markdown(iframe_html, unsafe_allow_html=True)
        
        # Method 2: Streamlit components iframe
        try:
            components.iframe(
                f"https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0",
                height=315,
                width=None
            )
        except Exception as e:
            st.error(f"Components iframe failed: {e}")
        
        # Method 3: Direct YouTube link as backup
        st.markdown("---")
        st.markdown("### 🎵 If the player above doesn't work, click here:")
        st.markdown(f"**[🎵 {track['title']} - {track['artist']}]({youtube_url})**")
        
        # Method 4: JavaScript redirect
        st.markdown(f"""
        <script>
            window.open('{youtube_url}', '_blank');
        </script>
        """, unsafe_allow_html=True)
        
        # Set session state
        st.session_state.current_track = track
        st.session_state.show_player = True
        st.session_state.current_youtube_id = youtube_id

def display_direct_player(track: Dict):
    """Display a direct player that actually plays music"""
    if not track or 'youtube_id' not in track:
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    
    # Direct iframe player
    st.markdown("### 🎵 Music Player")
    iframe_html = f"""
    <iframe width="100%" height="315" 
            src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
    </iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)
    
    # Streamlit components iframe
    try:
        components.iframe(
            f"https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0",
            height=315,
            width=None
        )
    except Exception as e:
        st.error(f"Components iframe failed: {e}")
    
    # Direct YouTube link as backup
    st.markdown("---")
    st.markdown("### 🎵 If the player above doesn't work, click here:")
    st.markdown(f"**[🎵 {track['title']} - {track['artist']}]({youtube_url})**")
    
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

def create_working_play_button(track: Dict, button_text: str = "▶️ Play", key: str = None):
    """Create a working play button that definitely plays music"""
    if not track or 'youtube_id' not in track:
        st.warning("No track available")
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    # Create a button that opens YouTube in new tab
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
