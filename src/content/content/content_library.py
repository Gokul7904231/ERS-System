"""
Content Library for Emotion-Based Interventions
Maps emotions to recommended intervention types
"""

# Content library mapping emotions to intervention types
# Each emotion maps to a dict with 'type' (intervention type) and optionally 'metadata'
CONTENT_LIBRARY = {
    "happy": {
        "type": "music",
        "description": "Maintain your positive mood with uplifting music"
    },
    "sad": {
        "type": "music",
        "description": "Comforting music to help with sadness"
    },
    "anger": {
        "type": "breathing",  # High priority: breathing for anger
        "description": "Calm your anger with breathing exercises"
    },
    "fear": {
        "type": "breathing",  # High priority: breathing for fear
        "description": "Reduce your anxiety with breathing exercises"
    },
    "surprise": {
        "type": "music",
        "description": "Music to help process unexpected emotions"
    },
    "disgust": {
        "type": "music",
        "description": "Music to help shift your mood"
    },
    "contempt": {
        "type": "journaling",
        "description": "Reflect on your feelings through journaling"
    },
    "neutral": {
        "type": "music",
        "description": "Relaxing music for your calm state"
    },
    # Additional mappings for variations
    "Angry": {
        "type": "breathing",
        "description": "Calm your anger with breathing exercises"
    },
    "Fear": {
        "type": "breathing",
        "description": "Reduce your anxiety with breathing exercises"
    },
    "Neutral": {
        "type": "music",
        "description": "Relaxing music for your calm state"
    }
}

def get_content_for_emotion(emotion: str) -> dict:
    """
    Get content/intervention type for a given emotion
    
    Args:
        emotion: The emotion to get content for
        
    Returns:
        dict with 'type' and 'description' keys
    """
    # Try direct lookup first
    if emotion in CONTENT_LIBRARY:
        return CONTENT_LIBRARY[emotion]
    
    # Try lowercase version
    emotion_lower = emotion.lower()
    if emotion_lower in CONTENT_LIBRARY:
        return CONTENT_LIBRARY[emotion_lower]
    
    # Try title case version
    emotion_title = emotion.title()
    if emotion_title in CONTENT_LIBRARY:
        return CONTENT_LIBRARY[emotion_title]
    
    # Default fallback
    return CONTENT_LIBRARY["neutral"]
