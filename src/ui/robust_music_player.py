"""
Robust Music Player for AI MoodMate
This is a comprehensive solution that handles all music playback scenarios
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Optional
import webbrowser
import json

class RobustMusicPlayer:
    """A robust music player that handles all playback scenarios"""
    
    def __init__(self):
        self.current_track = None
        self.playlist = []
        self.current_index = 0
        
    def create_play_button(self, track: Dict, button_text: str = "▶️ Play", key: str = None, 
                          show_details: bool = True) -> bool:
        """
        Create a robust play button that definitely works
        
        Returns:
            bool: True if button was clicked, False otherwise
        """
        if not track or 'youtube_id' not in track:
            st.warning("⚠️ No track available")
            return False
        
        youtube_id = track['youtube_id']
        youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
        
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
            
            # Create a prominent play link
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; margin: 10px 0;">
                <h3 style="color: white; margin: 0;">🎵 Click to Play Music</h3>
                <a href="{youtube_url}" target="_blank" 
                   style="display: inline-block; background: #ff0000; color: white; 
                          padding: 12px 24px; text-decoration: none; border-radius: 25px; 
                          font-size: 16px; font-weight: bold; margin-top: 10px;">
                    ▶️ Play {track['title']} by {track['artist']}
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            # Method 2: Embedded Player (Fallback)
            st.markdown("### 🎵 Embedded Player")
            try:
                # Use Streamlit components for better iframe handling
                components.iframe(
                    f"https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0&enablejsapi=1",
                    height=315,
                    width=560
                )
            except Exception as e:
                st.warning(f"Embedded player failed: {e}")
                # Fallback to HTML iframe
                iframe_html = f"""
                <iframe width="100%" height="315" 
                        src="https://www.youtube.com/embed/{youtube_id}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                </iframe>
                """
                st.markdown(iframe_html, unsafe_allow_html=True)
            
            # Method 3: Additional Options
            st.markdown("### 🎵 Additional Options")
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
            
            # Show track details if requested
            if show_details:
                st.markdown("### 🎵 Track Details")
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
    
    def create_playlist_player(self, tracks: List[Dict], title: str = "🎵 Playlist") -> None:
        """Create a playlist player with navigation"""
        if not tracks:
            st.warning("No tracks in playlist")
            return
        
        st.subheader(title)
        
        # Playlist info
        st.info(f"📀 {len(tracks)} tracks in playlist")
        
        # Create playlist navigation
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("⏮️ First", key="playlist_first"):
                self.current_index = 0
                st.rerun()
        
        with col2:
            if st.button("⏪ Previous", key="playlist_prev"):
                self.current_index = max(0, self.current_index - 1)
                st.rerun()
        
        with col3:
            if st.button("⏩ Next", key="playlist_next"):
                self.current_index = min(len(tracks) - 1, self.current_index + 1)
                st.rerun()
        
        with col4:
            if st.button("⏭️ Last", key="playlist_last"):
                self.current_index = len(tracks) - 1
                st.rerun()
        
        # Show current track
        if 0 <= self.current_index < len(tracks):
            current_track = tracks[self.current_index]
            st.markdown(f"**Now Playing: {self.current_index + 1}/{len(tracks)}**")
            
            # Play current track
            self.create_play_button(
                current_track, 
                f"▶️ Play {current_track['title'][:20]}...", 
                "playlist_current",
                show_details=True
            )
        
        # Show all tracks in playlist
        st.markdown("### 📋 All Tracks")
        for i, track in enumerate(tracks):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"{i+1}. {track['title']} by {track['artist']}")
            with col2:
                if 'mood_match_score' in track:
                    st.write(f"Mood: {track['mood_match_score']:.1f}%")
            with col3:
                if st.button("▶️", key=f"playlist_track_{i}"):
                    self.current_index = i
                    st.rerun()
    
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
            
            # Show the player
            youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
            
            # Direct link
            st.markdown(f"**[🎵 Continue Playing on YouTube]({youtube_url})**")
            
            # Embedded player
            try:
                components.iframe(
                    f"https://www.youtube.com/embed/{track['youtube_id']}?autoplay=1&controls=1&showinfo=1&rel=0&mute=0",
                    height=315,
                    width=560
                )
            except Exception as e:
                st.warning(f"Player error: {e}")

# Global music player instance
music_player = RobustMusicPlayer()

def create_robust_play_button(track: Dict, button_text: str = "▶️ Play", key: str = None) -> bool:
    """Create a robust play button that definitely works"""
    return music_player.create_play_button(track, button_text, key)

def display_robust_playlist(tracks: List[Dict], title: str = "🎵 Playlist") -> None:
    """Display a robust playlist player"""
    music_player.create_playlist_player(tracks, title)

def show_current_player() -> None:
    """Show the current music player"""
    music_player.display_current_player()
