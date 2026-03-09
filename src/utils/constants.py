"""
Shared constants used across the application.
"""

EMOTIONS = (
    "anger", "contempt", "disgust", "fear",
    "happy", "neutral", "sad", "surprise"
)

EMOTION_COLORS = {
    "anger": (0, 0, 255),
    "contempt": (128, 0, 128),
    "disgust": (0, 128, 0),
    "fear": (255, 255, 0),
    "happy": (0, 255, 0),
    "neutral": (128, 128, 128),
    "sad": (255, 0, 0),
    "surprise": (0, 255, 255),
}

EMOTION_EMOJIS = {
    "anger": "😠",
    "contempt": "😏",
    "disgust": "🤢",
    "fear": "😨",
    "happy": "😊",
    "neutral": "😐",
    "sad": "😢",
    "surprise": "😲",
}

MOOD_GOAL_MAPPING = {
    "sad": "Hopeful & Energetic",
    "anger": "Calm & Relaxed",
    "fear": "Safe & Grounded",
    "neutral": "Motivated & Focused",
    "happy": "Joyful & Energetic",
    "disgust": "Cleansed & Refreshed",
    "surprise": "Curious & Engaged",
    "contempt": "Open & Empathetic",
}
