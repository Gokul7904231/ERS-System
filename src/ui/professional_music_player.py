"""
Professional Music Player for AI MoodMate
Clean, modern, and user-friendly music interface
"""

import streamlit as st
from typing import Dict, List
import streamlit.components.v1 as components

def create_professional_music_section(tracks: List[Dict], title: str = "🎵 Music Recommendations", emotion: str = None):
    """Create a professional music recommendations section"""
    if not tracks:
        st.warning("No music recommendations available")
        return
    
    # Section header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);">
        <h2 style="color: white; margin: 0; text-align: center;">{title}</h2>
        <p style="color: white; margin: 0.5rem 0 0 0; text-align: center; opacity: 0.9;">Curated music to match your mood</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Music cards
    for i, track in enumerate(tracks):
        create_professional_music_card(track, i, emotion)

def create_professional_music_card(track: Dict, index: int, emotion: str = None):
    """Create a professional music card"""
    if not track or 'youtube_id' not in track:
        return
    
    youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
    emotion_text = f" for {emotion.title()}" if emotion else ""
    
    # Card container
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #f5576c;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="flex: 1;">
                <h3 style="margin: 0; color: #333; font-size: 1.3rem;">🎵 {track['title']}</h3>
                <p style="margin: 0.5rem 0; color: #666; font-size: 1.1rem;"><strong>by {track['artist']}</strong>{emotion_text}</p>
                {f"<p style='margin: 0; color: #888; font-size: 0.9rem;'>Mood Match: {track.get('mood_match_score', 0):.1f}%</p>" if 'mood_match_score' in track else ""}
            </div>
            <div style="margin-left: 1rem;">
                <a href="{youtube_url}" target="_blank" style="background: #ff0000; color: white; padding: 0.75rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: 600; display: inline-block; box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3); transition: all 0.3s ease;">
                    ▶️ Play
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional options
    with st.expander(f"🔗 More Options for {track['title'][:20]}..."):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**[🎵 YouTube]({youtube_url})**")
        with col2:
            st.markdown(f"**[🎵 YouTube Music](https://music.youtube.com/watch?v={track['youtube_id']})**")
        with col3:
            st.code(youtube_url)

def create_emotion_based_playlist(playlist: List[Dict], emotion_summary: str):
    """Create a professional emotion-based playlist"""
    if not playlist:
        st.warning("No playlist available")
        return
    
    # Playlist header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
        <h2 style="color: white; margin: 0; text-align: center;">🎵 Your Emotional Journey Playlist</h2>
        <p style="color: white; margin: 0.5rem 0 0 0; text-align: center; opacity: 0.9;">{emotion_summary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Playlist stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Songs", len(playlist))
    with col2:
        emotions = set(track.get('emotion', 'Unknown') for track in playlist)
        st.metric("Emotions", len(emotions))
    with col3:
        avg_confidence = sum(track.get('mood_match_score', 0) for track in playlist) / len(playlist)
        st.metric("Avg Match", f"{avg_confidence:.1f}%")
    
    # Playlist tracks
    for i, track in enumerate(playlist):
        emotion = track.get('emotion', 'Unknown')
        create_professional_music_card(track, i, emotion)

def create_current_player(track: Dict):
    """Create a professional current player"""
    if not track or 'youtube_id' not in track:
        return
    
    youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 1.5rem; border-radius: 15px; margin: 2rem 0; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);">
        <h3 style="color: white; margin: 0; text-align: center;">🎵 Now Playing</h3>
        <div style="text-align: center; margin: 1rem 0;">
            <h4 style="color: white; margin: 0.5rem 0;">{track['title']}</h4>
            <p style="color: white; margin: 0; opacity: 0.9;">by {track['artist']}</p>
        </div>
        <div style="text-align: center;">
            <a href="{youtube_url}" target="_blank" style="background: white; color: #4CAF50; padding: 0.75rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: 600; display: inline-block; margin: 0.5rem;">
                ▶️ Continue Playing
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stop button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⏹️ Stop", key="stop_current_player"):
            st.session_state.current_track = None
            st.session_state.show_player = False
            st.rerun()

def create_music_insights(tracks: List[Dict], emotion: str):
    """Create professional music insights"""
    if not tracks:
        return
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h3 style="color: #333; margin: 0 0 1rem 0;">📊 Music Insights for {emotion.title()}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Insights
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_match = sum(track.get('mood_match_score', 0) for track in tracks) / len(tracks)
        st.metric("Avg Mood Match", f"{avg_match:.1f}%")
    with col2:
        genres = set(track.get('genre', 'Unknown') for track in tracks)
        st.metric("Genres", len(genres))
    with col3:
        artists = set(track.get('artist', 'Unknown') for track in tracks)
        st.metric("Artists", len(artists))
    
    # Genre breakdown
    if tracks:
        st.markdown("### 🎭 Genre Breakdown")
        genre_counts = {}
        for track in tracks:
            genre = track.get('genre', 'Unknown')
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True):
            st.progress(count / len(tracks), text=f"{genre}: {count} songs")

def create_quick_play_section(tracks: List[Dict], title: str = "🎮 Quick Play"):
    """Create a quick play section with buttons"""
    if not tracks:
        return
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h4 style="color: #333; margin: 0 0 1rem 0;">{title}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick play buttons
    cols = st.columns(min(len(tracks), 4))
    for i, (col, track) in enumerate(zip(cols, tracks[:4])):
        with col:
            youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
            if st.button(f"▶️ {track['title'][:15]}...", key=f"quick_play_{i}", use_container_width=True):
                st.markdown(f"**[🎵 Play {track['title']}]({youtube_url})**")
                st.session_state.current_track = track
                st.session_state.show_player = True
