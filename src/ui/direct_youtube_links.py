"""
Direct YouTube Links - Show YouTube links directly without buttons
This is the absolute simplest solution
"""

import streamlit as st
from typing import Dict, List

def show_youtube_links_directly(tracks: List[Dict], title: str = "🎵 Music Recommendations"):
    """
    Show YouTube links directly without any buttons
    """
    if not tracks:
        st.warning("No music recommendations available")
        return
    
    st.subheader(title)
    
    for i, track in enumerate(tracks):
        if not track or 'youtube_id' not in track:
            continue
            
        youtube_id = track['youtube_id']
        youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
        
        st.markdown("---")
        
        # Show track info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{i+1}. {track['title']}** by {track['artist']}")
            if 'mood_match_score' in track:
                st.markdown(f"Mood Match: {track['mood_match_score']:.1f}%")
        with col2:
            st.markdown(f"**[🎵 Play on YouTube]({youtube_url})**")
        
        # Also show the URL for copying
        with st.expander(f"🔗 Copy URL for {track['title']}"):
            st.code(youtube_url)

def show_single_youtube_link(track: Dict, title: str = "🎵 Play Music"):
    """
    Show a single YouTube link
    """
    if not track or 'youtube_id' not in track:
        st.warning("No track available")
        return
    
    youtube_id = track['youtube_id']
    youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
    
    st.markdown(f"### {title}")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    st.markdown(f"**[🎵 Play on YouTube]({youtube_url})**")
    
    with st.expander("🔗 Copy URL"):
        st.code(youtube_url)
