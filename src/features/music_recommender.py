"""
AI MoodMate - Music Recommendation System
Suggests music based on detected emotions using a YouTube-based recommendation system
"""

import random
from typing import List, Dict, Tuple

class MusicRecommender:
    def __init__(self):
        # Enhanced emotion to music mapping with detailed metadata
        self.emotion_music_mapping = {
            "happy": {
                "genres": ["pop", "dance", "electronic", "indie-pop", "funk"],
                "mood": "upbeat",
                "energy": "high",
                "valence": "positive",
                "keywords": ["happy", "joyful", "upbeat", "energetic", "celebratory"],
                "tempo_range": (120, 140),  # BPM
                "energy_level": 8,  # 1-10 scale
                "valence_score": 9,  # Musical positivity
                "danceability": 8,
                "color": "#FFD700",  # Gold
                "mood_keywords": ["uplifting", "energetic", "celebratory", "bright"],
                "visual_style": ["sunny", "bright", "vibrant"]
            },
            "sad": {
                "genres": ["indie", "alternative", "folk", "blues", "soul"],
                "mood": "melancholic",
                "energy": "low",
                "valence": "negative",
                "keywords": ["sad", "melancholic", "emotional", "heartfelt", "introspective"],
                "tempo_range": (60, 90),
                "energy_level": 3,
                "valence_score": 2,
                "danceability": 3,
                "color": "#4169E1",  # Royal Blue
                "mood_keywords": ["melancholic", "introspective", "emotional", "gentle"],
                "visual_style": ["soft", "blue", "gentle"]
            },
            "anger": {
                "genres": ["rock", "metal", "punk", "hardcore", "alternative"],
                "mood": "aggressive",
                "energy": "high",
                "valence": "negative",
                "keywords": ["angry", "aggressive", "intense", "powerful", "rebellious"],
                "tempo_range": (140, 180),
                "energy_level": 9,
                "valence_score": 3,
                "danceability": 6,
                "color": "#DC143C",  # Crimson
                "mood_keywords": ["intense", "aggressive", "powerful", "raw"],
                "visual_style": ["intense", "red", "powerful"]
            },
            "fear": {
                "genres": ["ambient", "dark-ambient", "experimental", "atmospheric"],
                "mood": "tense",
                "energy": "medium",
                "valence": "negative",
                "keywords": ["fearful", "tense", "anxious", "dark", "mysterious"],
                "tempo_range": (40, 80),
                "energy_level": 4,
                "valence_score": 2,
                "danceability": 2,
                "color": "#8B008B",  # Dark Magenta
                "mood_keywords": ["ominous", "tense", "atmospheric", "unsettling"],
                "visual_style": ["dark", "purple", "mysterious"]
            },
            "surprise": {
                "genres": ["experimental", "indie", "alternative", "electronic"],
                "mood": "unexpected",
                "energy": "variable",
                "valence": "neutral",
                "keywords": ["surprising", "unexpected", "quirky", "unique", "experimental"],
                "tempo_range": (100, 160),
                "energy_level": 7,
                "valence_score": 6,
                "danceability": 7,
                "color": "#FF6347",  # Tomato
                "mood_keywords": ["unexpected", "dynamic", "playful", "quirky"],
                "visual_style": ["dynamic", "orange", "playful"]
            },
            "disgust": {
                "genres": ["industrial", "noise", "experimental", "dark-ambient"],
                "mood": "repulsive",
                "energy": "medium",
                "valence": "negative",
                "keywords": ["disgusting", "repulsive", "dark", "experimental", "industrial"],
                "tempo_range": (60, 120),
                "energy_level": 5,
                "valence_score": 2,
                "danceability": 3,
                "color": "#228B22",  # Forest Green
                "mood_keywords": ["dark", "disturbing", "experimental", "unconventional"],
                "visual_style": ["dark", "green", "experimental"]
            },
            "contempt": {
                "genres": ["alternative", "indie", "post-punk", "experimental"],
                "mood": "dismissive",
                "energy": "medium",
                "valence": "negative",
                "keywords": ["contemptuous", "dismissive", "cynical", "sarcastic", "alternative"],
                "tempo_range": (80, 120),
                "energy_level": 5,
                "valence_score": 3,
                "danceability": 4,
                "color": "#696969",  # Dim Gray
                "mood_keywords": ["cynical", "sarcastic", "detached", "cool"],
                "visual_style": ["cool", "gray", "detached"]
            },
            "neutral": {
                "genres": ["ambient", "chill", "lounge", "instrumental", "classical"],
                "mood": "calm",
                "energy": "low",
                "valence": "neutral",
                "keywords": ["neutral", "calm", "peaceful", "relaxing", "ambient"],
                "tempo_range": (70, 110),
                "energy_level": 5,
                "valence_score": 5,
                "danceability": 5,
                "color": "#708090",  # Slate Gray
                "mood_keywords": ["balanced", "calm", "neutral", "peaceful"],
                "visual_style": ["calm", "gray", "balanced"]
            }
        }
        
        # YouTube-based playlists for each emotion
        self.curated_playlists = {
            "happy": [
                {"title": "Happy - Pharrell Williams", "artist": "Pharrell Williams", "youtube_id": "ZbZSe6N_BXs"},
                {"title": "Can't Stop the Feeling!", "artist": "Justin Timberlake", "youtube_id": "ru0K8uYEZWw"},
                {"title": "Good Vibrations", "artist": "The Beach Boys", "youtube_id": "Eab_beh07HU"},
                {"title": "Walking on Sunshine", "artist": "Katrina and the Waves", "youtube_id": "iPUmE-tne5U"},
                {"title": "Don't Stop Me Now", "artist": "Queen", "youtube_id": "HgzGwKwLmgM"}
            ],
            "sad": [
                {"title": "Someone You Loved", "artist": "Lewis Capaldi", "youtube_id": "zABLecsR5UE"},
                {"title": "All Too Well", "artist": "Taylor Swift", "youtube_id": "tollGa3l0k8"},
                {"title": "Hurt", "artist": "Johnny Cash", "youtube_id": "8AHCfZTRGiI"},
                {"title": "Mad World", "artist": "Gary Jules", "youtube_id": "4N3N1MlvVc4"},
                {"title": "The Sound of Silence", "artist": "Simon & Garfunkel", "youtube_id": "4fWyzwo1xg"}
            ],
            "anger": [
                {"title": "Break Stuff", "artist": "Limp Bizkit", "youtube_id": "XMwbj8kZ8J4"},
                {"title": "Killing in the Name", "artist": "Rage Against the Machine", "youtube_id": "bWXazVhlyxQ"},
                {"title": "Bodies", "artist": "Drowning Pool", "youtube_id": "04F4xlwsFj0"},
                {"title": "Down with the Sickness", "artist": "Disturbed", "youtube_id": "09LTT0xwdfw"},
                {"title": "Chop Suey!", "artist": "System of a Down", "youtube_id": "CSvFpBOe8eY"}
            ],
            "fear": [
                {"title": "Thriller", "artist": "Michael Jackson", "youtube_id": "sOnqjkJTMaA"},
                {"title": "Somebody's Watching Me", "artist": "Rockwell", "youtube_id": "7YvAYerbVc0"},
                {"title": "The Number of the Beast", "artist": "Iron Maiden", "youtube_id": "WxnN05vOuSM"},
                {"title": "Black Sabbath", "artist": "Black Sabbath", "youtube_id": "0qanF-91aJo"},
                {"title": "Enter Sandman", "artist": "Metallica", "youtube_id": "CD-E-LDc384"}
            ],
            "surprise": [
                {"title": "Bohemian Rhapsody", "artist": "Queen", "youtube_id": "fJ9rUzIMcZQ"},
                {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "youtube_id": "hTWKbfoikeg"},
                {"title": "Take On Me", "artist": "a-ha", "youtube_id": "dQw4w9WgXcQ"},
                {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses", "youtube_id": "1w7OgIMMRc4"},
                {"title": "Hotel California", "artist": "Eagles", "youtube_id": "BciS5krYL80"}
            ],
            "disgust": [
                {"title": "Closer", "artist": "Nine Inch Nails", "youtube_id": "PTFwQP86BRs"},
                {"title": "The Beautiful People", "artist": "Marilyn Manson", "youtube_id": "Ypkv0HeUvTc"},
                {"title": "Du Hast", "artist": "Rammstein", "youtube_id": "W3q8Od5qJio"},
                {"title": "Bleed", "artist": "Meshuggah", "youtube_id": "qc98u-eGzlc"},
                {"title": "The Dope Show", "artist": "Marilyn Manson", "youtube_id": "Ypkv0HeUvTc"}
            ],
            "contempt": [
                {"title": "Creep", "artist": "Radiohead", "youtube_id": "XFkzRNyygfk"},
                {"title": "Loser", "artist": "Beck", "youtube_id": "YgSPaXgAdzE"},
                {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "youtube_id": "hTWKbfoikeg"},
                {"title": "Bitter Sweet Symphony", "artist": "The Verve", "youtube_id": "1lyu1KKwC74"},
                {"title": "The Man Who Sold the World", "artist": "Nirvana", "youtube_id": "fregObNcHC8"}
            ],
            "neutral": [
                {"title": "Weightless", "artist": "Marconi Union", "youtube_id": "UfcAVejslrU"},
                {"title": "Clair de Lune", "artist": "Claude Debussy", "youtube_id": "CvFH_6DNRCY"},
                {"title": "River Flows in You", "artist": "Yiruma", "youtube_id": "7maZ6a9fJXc"},
                {"title": "Comptine d'un autre été", "artist": "Yann Tiersen", "youtube_id": "KvMY1uw05Sk"},
                {"title": "Spiegel im Spiegel", "artist": "Arvo Pärt", "youtube_id": "8kUyJz7wgwI"}
            ]
        }
    
    def get_music_recommendations(self, emotion: str, count: int = 5) -> List[Dict]:
        """
        Get music recommendations for a specific emotion (YouTube-based only)
        Args:
            emotion: The detected emotion
            count: Number of recommendations to return
        Returns:
            List of music recommendations with title, artist, and YouTube ID
        """
        # Normalize emotion name
        emotion = emotion.lower()
        if emotion == "angry":
            emotion = "anger"
        if emotion not in self.emotion_music_mapping:
            emotion = "neutral"
        return self._get_curated_recommendations(emotion, count)
    
    # Spotify-based recommendation method removed
    
    def _get_curated_recommendations(self, emotion: str, count: int) -> List[Dict]:
        """Get YouTube-based recommendations for the given emotion"""
        playlist = self.curated_playlists.get(emotion, self.curated_playlists["neutral"])
        return random.sample(playlist, min(count, len(playlist)))
    
    def _get_youtube_id(self, title: str, artist: str) -> str:
        """Get YouTube video ID for a track (not used in YouTube-only mode)"""
        # Not used in YouTube-only mode, kept for compatibility
        return "dQw4w9WgXcQ"
    
    def get_playlist_for_video_analysis(self, emotion_results: Dict[str, float], count_per_emotion: int = 3) -> List[Dict]:
        """
        Generate a playlist based on video emotion analysis results
        
        Args:
            emotion_results: Dictionary with emotion as key and percentage as value
            count_per_emotion: Number of songs per emotion
            
        Returns:
            List of music recommendations
        """
        playlist = []
        
        # Sort emotions by percentage (highest first)
        sorted_emotions = sorted(emotion_results.items(), key=lambda x: x[1], reverse=True)
        
        # Get recommendations for top emotions
        for emotion, percentage in sorted_emotions[:3]:  # Top 3 emotions
            if percentage > 10:  # Only include emotions with >10% presence
                recommendations = self.get_music_recommendations(emotion, count_per_emotion)
                for rec in recommendations:
                    rec['emotion'] = emotion
                    rec['percentage'] = percentage
                playlist.extend(recommendations)
        
        # Shuffle the playlist for variety
        random.shuffle(playlist)
        
        return playlist
    
    def get_emotion_summary(self, emotion_results: Dict[str, float]) -> str:
        """Generate a summary of detected emotions"""
        if not emotion_results:
            return "No emotions detected"
        
        sorted_emotions = sorted(emotion_results.items(), key=lambda x: x[1], reverse=True)
        top_emotion, top_percentage = sorted_emotions[0]
        
        if top_percentage > 50:
            return f"Your mood is predominantly {top_emotion.title()} ({top_percentage:.1f}%)"
        elif len(sorted_emotions) > 1:
            second_emotion, second_percentage = sorted_emotions[1]
            return f"Your mood is a mix of {top_emotion.title()} ({top_percentage:.1f}%) and {second_emotion.title()} ({second_percentage:.1f}%)"
        else:
            return f"Your mood is {top_emotion.title()} ({top_percentage:.1f}%)"
    
    def calculate_mood_match_score(self, emotion: str, track_data: Dict) -> float:
        """Calculate how well a track matches the detected emotion (0-100)"""
        # Normalize emotion name
        emotion = emotion.lower()
        if emotion == "angry":
            emotion = "anger"
        
        if emotion not in self.emotion_music_mapping:
            return 50.0  # Neutral score
        
        emotion_data = self.emotion_music_mapping[emotion]
        
        # Calculate match based on various factors
        match_score = 0.0
        
        # Genre matching (30% weight)
        track_genres = track_data.get('genres', [])
        emotion_genres = emotion_data['genres']
        genre_match = len(set(track_genres) & set(emotion_genres)) / len(emotion_genres)
        match_score += genre_match * 30
        
        # Energy level matching (25% weight)
        track_energy = track_data.get('energy', 5)  # Default to neutral
        emotion_energy = emotion_data['energy_level']
        energy_diff = abs(track_energy - emotion_energy) / 10
        energy_match = 1 - energy_diff
        match_score += energy_match * 25
        
        # Valence matching (25% weight)
        track_valence = track_data.get('valence', 5)  # Default to neutral
        emotion_valence = emotion_data['valence_score']
        valence_diff = abs(track_valence - emotion_valence) / 10
        valence_match = 1 - valence_diff
        match_score += valence_match * 25
        
        # Tempo matching (20% weight)
        track_tempo = track_data.get('tempo', 100)  # Default tempo
        emotion_tempo_range = emotion_data['tempo_range']
        if emotion_tempo_range[0] <= track_tempo <= emotion_tempo_range[1]:
            tempo_match = 1.0
        else:
            # Calculate distance from range
            if track_tempo < emotion_tempo_range[0]:
                tempo_diff = emotion_tempo_range[0] - track_tempo
            else:
                tempo_diff = track_tempo - emotion_tempo_range[1]
            tempo_match = max(0, 1 - (tempo_diff / 100))
        match_score += tempo_match * 20
        
        return min(100, max(0, match_score))
    
    def get_enhanced_recommendations(self, emotion: str, count: int = 5) -> List[Dict]:
        """Get enhanced music recommendations with mood matching scores"""
        # Normalize emotion name
        emotion = emotion.lower()
        if emotion == "angry":
            emotion = "anger"
        
        recommendations = self.get_music_recommendations(emotion, count)
        
        # Add mood matching scores and metadata
        for rec in recommendations:
            rec['mood_match_score'] = self.calculate_mood_match_score(emotion, rec)
            rec['emotion_color'] = self.emotion_music_mapping[emotion]['color']
            rec['tempo_range'] = self.emotion_music_mapping[emotion]['tempo_range']
            rec['energy_level'] = self.emotion_music_mapping[emotion]['energy_level']
            rec['mood_keywords'] = self.emotion_music_mapping[emotion]['mood_keywords']
            rec['visual_style'] = self.emotion_music_mapping[emotion]['visual_style']
        
        # Sort by mood match score
        recommendations.sort(key=lambda x: x['mood_match_score'], reverse=True)
        
        return recommendations
    
    def create_mood_journey_playlist(self, emotion_percentages: Dict[str, float], duration_minutes: int = 30) -> List[Dict]:
        """Create a playlist that follows the emotional journey detected in video"""
        playlist = []
        
        # Calculate songs per emotion based on percentages
        total_songs = max(10, duration_minutes * 2)  # ~2 songs per minute
        
        sorted_emotions = sorted(emotion_percentages.items(), key=lambda x: x[1], reverse=True)
        
        for emotion, percentage in sorted_emotions:
            if percentage > 5:  # Only include emotions with >5% presence
                songs_for_emotion = int((percentage / 100) * total_songs)
                songs_for_emotion = max(1, min(songs_for_emotion, 8))  # Between 1-8 songs
                
                recommendations = self.get_enhanced_recommendations(emotion, songs_for_emotion)
                for rec in recommendations:
                    rec['emotion'] = emotion
                    rec['emotion_percentage'] = percentage
                playlist.extend(recommendations)
        
        # Shuffle but maintain some emotional flow
        random.shuffle(playlist)
        
        return playlist[:total_songs]
    
    def get_music_insights(self, emotion: str) -> Dict:
        """Get detailed insights about music for a specific emotion"""
        # Normalize emotion name
        emotion = emotion.lower()
        if emotion == "angry":
            emotion = "anger"
        
        if emotion not in self.emotion_music_mapping:
            emotion = "neutral"
        
        emotion_data = self.emotion_music_mapping[emotion]
        
        return {
            "emotion": emotion,
            "color": emotion_data['color'],
            "tempo_range": emotion_data['tempo_range'],
            "energy_level": emotion_data['energy_level'],
            "valence_score": emotion_data['valence_score'],
            "danceability": emotion_data['danceability'],
            "mood_keywords": emotion_data['mood_keywords'],
            "visual_style": emotion_data['visual_style'],
            "genres": emotion_data['genres'],
            "description": f"Music for {emotion} mood typically features {emotion_data['tempo_range'][0]}-{emotion_data['tempo_range'][1]} BPM tempo with {emotion_data['energy_level']}/10 energy level."
        }

# Initialize the music recommender
music_recommender = MusicRecommender()
