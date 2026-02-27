"""
YouTube Music Player Component for AI MoodMate
Provides embedded YouTube player for instant music playback
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import List, Dict
import random

def create_youtube_player(youtube_id: str, width: int = 560, height: int = 315, autoplay: bool = True) -> str:
    """
    Create HTML for YouTube embedded player
    
    Args:
        youtube_id: YouTube video ID
        width: Player width
        height: Player height
        autoplay: Whether to autoplay the video
        
    Returns:
        HTML string for YouTube player
    """
    autoplay_param = "1" if autoplay else "0"
    return f"""
    <iframe width="{width}" height="{height}" 
            src="https://www.youtube.com/embed/{youtube_id}?autoplay={autoplay_param}&controls=1&showinfo=1&rel=0&enablejsapi=1" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
    </iframe>
    """

def display_music_recommendations(recommendations: List[Dict], title: str = "🎵 Music Recommendations"):
    """
    Display music recommendations with YouTube players
    
    Args:
        recommendations: List of music recommendations
        title: Section title
    """
    st.subheader(title)
    
    if not recommendations:
        st.warning("No music recommendations available")
        return
    
    # Create tabs for each recommendation
    tabs = st.tabs([f"🎵 {i+1}" for i in range(len(recommendations))])
    
    for i, (tab, rec) in enumerate(zip(tabs, recommendations)):
        with tab:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Display track info
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
                    <h3 style="margin: 0; color: white;">{rec['title']}</h3>
                    <p style="margin: 5px 0; color: #f0f0f0;">by {rec['artist']}</p>
                    {f'<p style="margin: 5px 0; color: #e0e0e0;">Emotion: {rec.get("emotion", "N/A").title()} ({rec.get("percentage", 0):.1f}%)</p>' if "emotion" in rec else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # YouTube player
                youtube_html = create_youtube_player(rec['youtube_id'], width=500, height=300)
                st.markdown(youtube_html, unsafe_allow_html=True)
            
            with col2:
                # Additional info
                st.markdown("**📊 Track Details:**")
                st.markdown(f"**Title:** {rec['title']}")
                st.markdown(f"**Artist:** {rec['artist']}")
                
                if 'emotion' in rec:
                    st.markdown(f"**Emotion:** {rec['emotion'].title()}")
                    st.markdown(f"**Confidence:** {rec['percentage']:.1f}%")
                
                if 'spotify_url' in rec:
                    st.markdown(f"[🎧 Listen on Spotify]({rec['spotify_url']})")
                
                if 'album_cover' in rec and rec['album_cover']:
                    st.image(rec['album_cover'], width=150)

def display_playlist_summary(playlist: List[Dict], emotion_summary: str):
    """
    Display playlist summary with emotion analysis
    
    Args:
        playlist: List of music recommendations
        emotion_summary: Summary of detected emotions
    """
    st.markdown("---")
    st.subheader("🎭 Your Mood Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h3 style="margin: 0; color: white;">{emotion_summary}</h3>
            <p style="margin: 10px 0; color: #f0f0f0;">Based on your facial expressions, here are personalized music recommendations:</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Total Songs", len(playlist))
        st.metric("Emotions Detected", len(set(rec.get('emotion', 'unknown') for rec in playlist)))

def create_music_player_sidebar():
    """
    Create a sidebar music player for continuous playback
    """
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎵 Now Playing")
        
        if 'current_track' in st.session_state and st.session_state.current_track is not None:
            track = st.session_state.current_track
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #262730;">{track['title']}</h4>
                <p style="margin: 5px 0; color: #666;">by {track['artist']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Mini player
            youtube_html = create_youtube_player(track['youtube_id'], width=250, height=150)
            st.markdown(youtube_html, unsafe_allow_html=True)
            
            if st.button("🔄 Next Track"):
                if 'playlist' in st.session_state and st.session_state.playlist:
                    current_index = st.session_state.get('current_track_index', 0)
                    next_index = (current_index + 1) % len(st.session_state.playlist)
                    st.session_state.current_track = st.session_state.playlist[next_index]
                    st.session_state.current_track_index = next_index
                    st.rerun()
        else:
            st.info("No track selected. Choose a song from the recommendations below!")

def play_track(track: Dict):
    """
    Set a track as currently playing and display YouTube player
    
    Args:
        track: Track information
    """
    st.session_state.current_track = track
    st.session_state.show_player = True
    if 'playlist' in st.session_state:
        for i, t in enumerate(st.session_state.playlist):
            if t['title'] == track['title'] and t['artist'] == track['artist']:
                st.session_state.current_track_index = i
                break

def display_youtube_player(track: Dict):
    """Display YouTube player for the current track"""
    if not track or 'youtube_id' not in track:
        st.warning("No track selected or YouTube ID not available")
        return
    
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    
    # Create YouTube player with autoplay
    youtube_html = create_youtube_player(track['youtube_id'], width=560, height=315, autoplay=True)
    st.markdown(youtube_html, unsafe_allow_html=True)
    
    # Add player controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⏮️ Previous", use_container_width=True):
            play_previous_track()
    
    with col2:
        if st.button("⏸️ Stop", use_container_width=True):
            st.session_state.show_player = False
            st.session_state.current_track = None
            st.rerun()
    
    with col3:
        if st.button("⏭️ Next", use_container_width=True):
            play_next_track()

def play_next_track():
    """Play the next track in the playlist"""
    if 'playlist' in st.session_state and st.session_state.playlist:
        current_index = st.session_state.get('current_track_index', -1)
        next_index = (current_index + 1) % len(st.session_state.playlist)
        next_track = st.session_state.playlist[next_index]
        play_track(next_track)
        st.rerun()

def play_previous_track():
    """Play the previous track in the playlist"""
    if 'playlist' in st.session_state and st.session_state.playlist:
        current_index = st.session_state.get('current_track_index', -1)
        prev_index = (current_index - 1) % len(st.session_state.playlist)
        prev_track = st.session_state.playlist[prev_index]
        play_track(prev_track)
        st.rerun()

def display_enhanced_music_recommendations(recommendations: List[Dict], emotion: str, title: str = "🎵 Enhanced Music Recommendations"):
    """Display enhanced music recommendations with mood matching scores and visual indicators"""
    st.subheader(title)
    
    if not recommendations:
        st.warning("No music recommendations available")
        return
    
    # Display emotion insights
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {recommendations[0].get('emotion_color', '#667eea')} 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">🎭 {emotion.title()} Mood Music</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">Perfectly matched songs for your emotional state</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display recommendations with enhanced features
    for i, rec in enumerate(recommendations):
        with st.expander(f"🎵 {i+1}. {rec['title']} by {rec['artist']}", expanded=(i==0)):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Mood match score with visual indicator
                match_score = rec.get('mood_match_score', 85)
                score_color = "#4CAF50" if match_score >= 80 else "#FF9800" if match_score >= 60 else "#F44336"
                
                st.markdown(f"""
                <div style="background: {score_color}; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <strong>🎯 Mood Match: {match_score:.1f}%</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Music metadata
                if 'tempo_range' in rec:
                    st.markdown(f"**🎼 Tempo Range:** {rec['tempo_range'][0]}-{rec['tempo_range'][1]} BPM")
                if 'energy_level' in rec:
                    st.markdown(f"**⚡ Energy Level:** {rec['energy_level']}/10")
                if 'mood_keywords' in rec:
                    keywords = ", ".join(rec['mood_keywords'][:3])
                    st.markdown(f"**🏷️ Mood:** {keywords}")
            
            with col2:
                if st.button(f"▶️ Play", key=f"play_enhanced_{i}", use_container_width=True):
                    play_track(rec)
                    st.success(f"Now playing: {rec['title']}")
                    # Open YouTube directly in new tab
                    youtube_url = f"https://www.youtube.com/watch?v={rec['youtube_id']}"
                    st.markdown(f"""
                    <script>
                        window.open('{youtube_url}', '_blank');
                    </script>
                    """, unsafe_allow_html=True)
                    st.markdown(f"**🎵 [Click here to open in YouTube]({youtube_url})**")
                    st.rerun()
            
            with col3:
                if st.button(f"📊 Details", key=f"details_{i}", use_container_width=True):
                    st.session_state[f"show_details_{i}"] = True
            
            # Show detailed music analysis
            if st.session_state.get(f"show_details_{i}", False):
                st.markdown("---")
                st.markdown("### 🎵 Detailed Music Analysis")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("**Musical Characteristics:**")
                    if 'tempo_range' in rec:
                        st.markdown(f"• Tempo: {rec['tempo_range'][0]}-{rec['tempo_range'][1]} BPM")
                    if 'energy_level' in rec:
                        st.markdown(f"• Energy: {rec['energy_level']}/10")
                    if 'valence_score' in rec:
                        st.markdown(f"• Positivity: {rec['valence_score']}/10")
                
                with col_b:
                    st.markdown("**Mood Matching:**")
                    st.markdown(f"• Match Score: {match_score:.1f}%")
                    if 'visual_style' in rec:
                        styles = ", ".join(rec['visual_style'])
                        st.markdown(f"• Visual Style: {styles}")
                
                if st.button(f"❌ Close Details", key=f"close_details_{i}"):
                    st.session_state[f"show_details_{i}"] = False
                    st.rerun()

def display_mood_journey_playlist(playlist: List[Dict], emotion_summary: str):
    """Display a mood journey playlist with emotional flow visualization"""
    st.subheader("🎭 Your Emotional Music Journey")
    
    # Display journey summary
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">🎵 Mood Journey Playlist</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">{emotion_summary}</p>
        <p style="margin: 5px 0; color: #f0f0f0;">📊 {len(playlist)} songs • 🎯 Personalized emotional flow</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Group songs by emotion for visualization
    emotion_groups = {}
    for song in playlist:
        emotion = song.get('emotion', 'unknown')
        if emotion not in emotion_groups:
            emotion_groups[emotion] = []
        emotion_groups[emotion].append(song)
    
    # Display emotion flow visualization
    st.markdown("### 🌊 Emotional Flow")
    emotion_colors = {
        'happy': '#FFD700', 'sad': '#4169E1', 'anger': '#DC143C', 
        'fear': '#8B008B', 'surprise': '#FF6347', 'disgust': '#228B22',
        'contempt': '#696969', 'neutral': '#708090'
    }
    
    flow_html = '<div style="display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap;">'
    for emotion, songs in emotion_groups.items():
        color = emotion_colors.get(emotion, '#708090')
        percentage = songs[0].get('emotion_percentage', 0)
        flow_html += f'''
        <div style="background: {color}; color: white; padding: 10px 15px; border-radius: 20px; 
                    text-align: center; min-width: 100px;">
            <strong>{emotion.title()}</strong><br>
            <small>{len(songs)} songs ({percentage:.1f}%)</small>
        </div>
        '''
    flow_html += '</div>'
    st.markdown(flow_html, unsafe_allow_html=True)
    
    # Display playlist with enhanced features
    st.markdown("### 🎵 Playlist")
    
    for i, song in enumerate(playlist):
        emotion = song.get('emotion', 'unknown')
        color = emotion_colors.get(emotion, '#708090')
        
        with st.expander(f"🎵 {i+1}. {song['title']} by {song['artist']} ({emotion.title()})", expanded=(i==0)):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Emotion indicator
                st.markdown(f"""
                <div style="background: {color}; color: white; padding: 8px; border-radius: 5px; 
                            display: inline-block; margin-bottom: 10px;">
                    <strong>🎭 {emotion.title()}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Match score
                match_score = song.get('mood_match_score', 85)
                st.markdown(f"**🎯 Mood Match:** {match_score:.1f}%")
            
            with col2:
                if st.button(f"▶️ Play", key=f"play_journey_{i}", use_container_width=True):
                    play_track(song)
                    st.success(f"Now playing: {song['title']}")
                    # Open YouTube directly in new tab
                    youtube_url = f"https://www.youtube.com/watch?v={song['youtube_id']}"
                    st.markdown(f"""
                    <script>
                        window.open('{youtube_url}', '_blank');
                    </script>
                    """, unsafe_allow_html=True)
                    st.markdown(f"**🎵 [Click here to open in YouTube]({youtube_url})**")
                    st.rerun()
            
            with col3:
                if st.button(f"📊 Info", key=f"info_journey_{i}", use_container_width=True):
                    st.session_state[f"show_journey_info_{i}"] = True
            
            # Show song info
            if st.session_state.get(f"show_journey_info_{i}", False):
                st.markdown("---")
                st.markdown("**Song Details:**")
                st.markdown(f"• Emotion: {emotion.title()}")
                st.markdown(f"• Match Score: {match_score:.1f}%")
                if 'tempo_range' in song:
                    st.markdown(f"• Tempo: {song['tempo_range'][0]}-{song['tempo_range'][1]} BPM")
                if 'energy_level' in song:
                    st.markdown(f"• Energy: {song['energy_level']}/10")

def create_enhanced_youtube_player(track: Dict):
    """Create an enhanced YouTube player with better autoplay support"""
    if not track or 'youtube_id' not in track:
        return None
    
    youtube_id = track['youtube_id']
    title = track['title']
    artist = track['artist']
    
    # Create enhanced player HTML with JavaScript support
    player_html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin: 20px 0;">
        <h3 style="margin: 0; color: white;">🎵 Now Playing</h3>
        <p style="margin: 5px 0; color: #f0f0f0;"><strong>{title}</strong> by {artist}</p>
    </div>
    
    <div style="text-align: center; margin: 20px 0;">
        <iframe id="youtube-player" width="560" height="315" 
                src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0&enablejsapi=1&mute=0" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
    </div>
    
    <script>
        // Ensure autoplay works
        document.addEventListener('DOMContentLoaded', function() {{
            const iframe = document.getElementById('youtube-player');
            if (iframe) {{
                iframe.src = iframe.src + '&autoplay=1';
            }}
        }});
    </script>
    """
    
    return player_html

def display_enhanced_youtube_player(track: Dict):
    """Display enhanced YouTube player with better autoplay support"""
    if not track or 'youtube_id' not in track:
        st.warning("No track selected or YouTube ID not available")
        return
    
    # Display track info
    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    
    # Use Streamlit components for better YouTube integration
    youtube_url = f"https://www.youtube.com/embed/{track['youtube_id']}?autoplay=1&controls=1&showinfo=1&rel=0"
    
    # Display YouTube player using components
    components.iframe(youtube_url, height=315, width=560)
    
    # Add player controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⏮️ Previous", use_container_width=True):
            play_previous_track()
    
    with col2:
        if st.button("⏸️ Stop", use_container_width=True):
            st.session_state.show_player = False
            st.session_state.current_track = None
            st.rerun()
    
    with col3:
        if st.button("⏭️ Next", use_container_width=True):
            play_next_track()
    
    # Add direct YouTube link as fallback
    st.markdown("---")
    st.markdown("**🔗 Direct Links:**")
    youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
    st.markdown(f"[🎵 Open in YouTube]({youtube_url})")
    st.markdown(f"[📱 Open in YouTube Music](https://music.youtube.com/watch?v={track['youtube_id']})")
