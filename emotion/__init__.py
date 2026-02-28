# emotion package initializer

from emotion.emotion_detector import detect_emotion, init
from emotion.music_recommender import MusicRecommender

__all__ = [
    "detect_emotion",
    "init",
    "MusicRecommender",
]