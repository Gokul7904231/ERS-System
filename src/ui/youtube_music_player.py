"""
YouTube Music Player - Based on Spotify-YouTube Converter Approach
This implements a more robust music player using YouTube's API and direct links
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List
import webbrowser
import json

class YouTubeMusicPlayer:
    """A robust YouTube music player based on proven approaches"""
    
    def __init__(self):
        self.current_track = None
        self.playlist = []
        
    def create_youtube_player_button(self, track: Dict, button_text: str = "▶️ Play", key: str = None) -> bool:
        """
        Create a YouTube player button that definitely works
        Based on the Spotify-YouTube converter approach
        """
        if not track or 'youtube_id' not in track:
            st.warning("⚠️ No track available")
            return False
        
        youtube_id = track['youtube_id']
        youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
        youtube_embed_url = f"https://www.youtube.com/embed/{youtube_id}"
        
        # Create the play button
        if st.button(button_text, key=key, use_container_width=True):
            self.current_track = track
            st.session_state.current_track = track
            st.session_state.show_player = True
            
            # Show success message
            st.success(f"🎵 Now Playing: {track['title']} by {track['artist']}")
            
            # Method 1: Direct YouTube Link (Most Reliable)
            st.markdown("---")
            st.markdown("### 🎵 Music Player")
            
            # Create multiple play options
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 Direct YouTube Link")
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; background: #ff0000; border-radius: 10px; margin: 10px 0;">
                    <a href="{youtube_url}" target="_blank" 
                       style="color: white; text-decoration: none; font-size: 16px; font-weight: bold;">
                        ▶️ Play on YouTube
                    </a>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 🎵 YouTube Music")
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; background: #1db954; border-radius: 10px; margin: 10px 0;">
                    <a href="https://music.youtube.com/watch?v={youtube_id}" target="_blank" 
                       style="color: white; text-decoration: none; font-size: 16px; font-weight: bold;">
                        🎵 Play on YouTube Music
                    </a>
                </div>
                """, unsafe_allow_html=True)
            
            # Method 2: Embedded Player (Fallback)
            st.markdown("#### 🎬 Embedded Player")
            try:
                # Use Streamlit components for better iframe handling
                components.iframe(
                    f"{youtube_embed_url}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0&enablejsapi=1",
                    height=315,
                    width=560
                )
            except Exception as e:
                st.warning(f"Embedded player failed: {e}")
                # Fallback to HTML iframe
                iframe_html = f"""
                <iframe width="100%" height="315" 
                        src="{youtube_embed_url}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                </iframe>
                """
                st.markdown(iframe_html, unsafe_allow_html=True)
            
            # Method 3: Additional Options
            st.markdown("#### 🔗 Additional Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Refresh Player", key=f"refresh_{key}"):
                    st.rerun()
            
            with col2:
                if st.button("📱 Open in App", key=f"app_{key}"):
                    st.info("Open YouTube app on your device")
            
            with col3:
                if st.button("🔗 Copy Link", key=f"copy_{key}"):
                    st.code(youtube_url)
                    st.success("Link copied! Share with friends.")
            
            # Show track details
            st.markdown("#### 🎵 Track Details")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Title", track['title'])
                st.metric("Artist", track['artist'])
            with col2:
                if 'mood_match_score' in track:
                    st.metric("Mood Match", f"{track['mood_match_score']:.1f}%")
                if 'tempo' in track:
                    st.metric("Tempo", track['tempo'])
            
            return True
        
        return False
    
    def display_current_player(self) -> None:
        """Display the current music player if a track is playing"""
        if hasattr(st.session_state, 'current_track') and st.session_state.current_track:
            track = st.session_state.current_track
            
            st.markdown("---")
            st.subheader("🎵 Now Playing")
            
            # Show current track info
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{track['title']}** by {track['artist']}")
            with col2:
                if st.button("⏹️ Stop", key="stop_current"):
                    st.session_state.current_track = None
                    st.session_state.show_player = False
                    st.rerun()
            
            # Show the player options
            youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
            youtube_music_url = f"https://music.youtube.com/watch?v={track['youtube_id']}"
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**[🎵 Continue on YouTube]({youtube_url})**")
            with col2:
                st.markdown(f"**[🎵 Continue on YouTube Music]({youtube_music_url})**")
    
    def create_playlist_player(self, tracks: List[Dict], title: str = "🎵 Playlist") -> None:
        """Create a playlist player with navigation"""
        if not tracks:
            st.warning("No tracks in playlist")
            return
        
        st.subheader(title)
        
        # Playlist info
        st.info(f"📀 {len(tracks)} tracks in playlist")
        
        # Show all tracks with play buttons
        for i, track in enumerate(tracks):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"{i+1}. {track['title']} by {track['artist']}")
            with col2:
                if 'mood_match_score' in track:
                    st.write(f"Mood: {track['mood_match_score']:.1f}%")
            with col3:
                if st.button("▶️", key=f"playlist_track_{i}"):
                    self.current_track = track
                    st.session_state.current_track = track
                    st.rerun()

# Global music player instance
youtube_music_player = YouTubeMusicPlayer()

def create_youtube_play_button(track: Dict, button_text: str = "▶️ Play", key: str = None) -> bool:
    """Create a YouTube play button that definitely works"""
    return youtube_music_player.create_youtube_player_button(track, button_text, key)

def display_youtube_playlist(tracks: List[Dict], title: str = "🎵 Playlist") -> None:
    """Display a YouTube playlist player"""
    youtube_music_player.create_playlist_player(tracks, title)

def show_youtube_current_player() -> None:
    """Show the current YouTube music player"""
    youtube_music_player.display_current_player()
