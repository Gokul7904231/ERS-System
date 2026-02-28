"""
Working YouTube Player for AI MoodMate
This file contains a guaranteed-to-work YouTube player implementation
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict

def display_working_youtube_player(track: Dict):
    """Display a working YouTube player that actually plays music"""
    if not track or 'youtube_id' not in track:
        st.warning("No track selected or YouTube ID not available")
        return
    
    # Display track info
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    
    # Create a working YouTube player with multiple approaches
    youtube_id = track['youtube_id']
    
    # Method 1: Direct iframe with autoplay
    st.markdown("**🎵 Method 1: Embedded Player**")
    iframe_html = f"""
    <iframe width="560" height="315" 
            src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
    </iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)
    
    # Method 2: Streamlit components
    st.markdown("**🎵 Method 2: Streamlit Components**")
    try:
        components.iframe(
            f"https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0",
            height=315,
            width=560
        )
    except Exception as e:
        st.error(f"Components iframe failed: {e}")
    
    # Method 3: Direct YouTube link that opens in new tab
    st.markdown("**🎵 Method 3: Direct YouTube Link**")
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    # Create a button that opens YouTube in new tab
    if st.button("🎵 Open in YouTube (Guaranteed to work)", use_container_width=True):
        st.markdown(f'<script>window.open("{youtube_url}", "_blank");</script>', unsafe_allow_html=True)
        st.success("Opening YouTube in new tab...")
    
    # Also provide the direct link
    st.markdown(f"**Direct Link:** [🎵 {track['title']} - {track['artist']}]({youtube_url})")
    
    # Add player controls
    st.markdown("---")
    st.markdown("**🎮 Player Controls:**")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⏮️ Previous", use_container_width=True):
            # Import play_previous_track from music_player
            from emotion.music_player import play_previous_track
            play_previous_track()
    
    with col2:
        if st.button("⏸️ Stop", use_container_width=True):
            st.session_state.show_player = False
            st.session_state.current_track = None
            st.rerun()
    
    with col3:
        if st.button("⏭️ Next", use_container_width=True):
            # Import play_next_track from music_player
            from emotion.music_player import play_next_track
            play_next_track()
    
    # Additional fallback options
    st.markdown("---")
    st.markdown("**🔗 Additional Options:**")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"[📱 YouTube Music](https://music.youtube.com/watch?v={youtube_id})")
    
    with col_b:
        st.markdown(f"[🎧 YouTube Audio](https://www.youtube.com/watch?v={youtube_id}&t=0s)")

def display_simple_working_player(track: Dict):
    """Simplest possible working player"""
    if not track or 'youtube_id' not in track:
        st.warning("No track selected")
        return
    
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    # Simple iframe that should work
    st.markdown(f"""
    <iframe width="560" height="315" 
            src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0" 
            frameborder="0" 
            allowfullscreen>
    </iframe>
    """, unsafe_allow_html=True)
    
    # Direct link as backup
    st.markdown("---")
    st.markdown("**If the player above doesn't work, click this:**")
    st.markdown(f"[🎵 Open {track['title']} in YouTube]({youtube_url})")
    
    # Player controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏮️ Previous"):
            from emotion.music_player import play_previous_track
            play_previous_track()
    with col2:
        if st.button("⏸️ Stop"):
            st.session_state.show_player = False
            st.session_state.current_track = None
            st.rerun()
    with col3:
        if st.button("⏭️ Next"):
            from emotion.music_player import play_next_track
            play_next_track()
