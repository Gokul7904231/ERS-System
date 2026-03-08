from src.content.content.content_library import CONTENT_LIBRARY


def select_intervention(current_emotion, ers):
    """
    Adaptive Emotional Intervention Selection Algorithm (AEISA)

    Returns:
    - "breathing" → if guided breathing is required
    - dict (content library) → for music, books, videos
    """
    
    # Normalize current_emotion to lowercase for consistent lookup
    current_emotion_key = str(current_emotion).lower()

    # Safety fallback
    if current_emotion_key not in CONTENT_LIBRARY:
        current_emotion_key = "neutral"

    # Priority intervention: Breathing
    if current_emotion_key in ["anger", "fear"] and ers < 0:
        return "breathing"

    # Otherwise return content
    return CONTENT_LIBRARY[current_emotion_key]
