import streamlit as st
from datetime import datetime, timedelta

# Correctly use lowercase keys to match the application's normalized data
EMOTION_SCORE = {
    'anger': -3, 'contempt': -2, 'disgust': -2, 'fear': -2,
    'happy': 3, 'neutral': 0, 'sad': -1, 'surprise': 1
}

RECENT_PERIOD = timedelta(minutes=30)

def update_ers(current_emotion):
    """
    Update and return the Emotion Regulation Score (ERS) based on recent history.
    This function now correctly uses st.session_state for history.
    """
    if 'emotion_history' not in st.session_state:
        st.session_state.emotion_history = []

    now = datetime.now()
    # Filter for emotions within the recent period
    recent_emotions = [
        rec for rec in st.session_state.emotion_history 
        if now - rec['timestamp'] <= RECENT_PERIOD
    ]
    
    # If no recent history, the score is just the current emotion's score
    if not recent_emotions:
        return EMOTION_SCORE.get(current_emotion, 0)
        
    # Simple weighted average: more recent emotions have more weight
    total_score = 0
    total_weight = 0
    
    for i, record in enumerate(recent_emotions):
        weight = i + 1
        total_score += EMOTION_SCORE.get(record['emotion'], 0) * weight
        total_weight += weight
        
    # Add the current emotion with the highest weight for immediate impact
    current_weight = len(recent_emotions) + 1
    total_score += EMOTION_SCORE.get(current_emotion, 0) * current_weight
    total_weight += current_weight
    
    # Return the weighted average, or 0 if no weights
    return total_score / total_weight if total_weight > 0 else 0
