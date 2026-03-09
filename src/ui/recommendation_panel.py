"""
Recommendation Panel UI
Displays the unified recommendation tabs after emotion detection.
Extracted from app.py to separate UI from routing logic.
"""

import streamlit as st

from src.utils.constants import EMOTION_EMOJIS, MOOD_GOAL_MAPPING
from src.features.music_recommender import music_recommender
from src.ui.music_player import display_enhanced_music_recommendations
from src.features.reading_recommender import reading_recommender
from src.ui.reading_display import (
    display_reading_recommendations,
    display_reading_insights,
)
from src.features.wellness_features import wellness_features
from src.ui.breathing_exercises import display_breathing_exercise
from src.ui.coloring_display import display_coloring_game
from src.ui.mood_journaling import display_mood_journal
from src.ui.mental_health_display import (
    show_chatbot,
    display_mental_health_resources,
    display_quick_mental_health_links,
)
from src.ers.ers_engine import update_ers
from src.ers.aeisa import select_intervention


def display_final_emotion_card(emotion, confidence):
    """Polished card for the final emotion result."""
    emoji = EMOTION_EMOJIS.get(emotion.lower(), "😐")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; color: white; margin-bottom: 25px; 
                text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <div style="font-size: 60px; margin-bottom: 10px;">{emoji}</div>
        <h2 style="margin: 0; color: white; text-transform: capitalize; font-size: 32px;">{emotion}</h2>
        <p style="margin: 5px 0; font-size: 20px; opacity: 0.9;">Confidence: {confidence:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)


def display_unified_recommendation_panel(emotion, confidence):
    """Unified panel for all recommendations — music, reading, wellness, etc."""
    # Sanitize the emotion string
    clean_emotion = str(emotion).split('(')[0].strip().lower()

    display_final_emotion_card(clean_emotion, confidence)

    ers_value = update_ers(clean_emotion)
    intervention_data = select_intervention(clean_emotion, ers_value)

    # Robustly determine the intervention name
    if isinstance(intervention_data, dict):
        intervention_name = intervention_data.get(
            'intervention', intervention_data.get('name', 'general support')
        )
    else:
        intervention_name = str(intervention_data)

    st.markdown(f"### 🛡️ ERS Primary Intervention: **{intervention_name.title()}**")

    tabs = st.tabs([
        "🎵 Music",
        "📚 Reading",
        "🧘 Wellness",
        "🎨 Coloring Game",
        "💬 AI Chatbot",
        "📝 Mood Journal",
        "🆘 Support",
    ])

    target_mood = MOOD_GOAL_MAPPING.get(clean_emotion, "Balanced")

    with tabs[0]:  # Music
        st.subheader(f"🎵 {clean_emotion.title()} → Mood Lift: {target_mood}")
        music_recs = music_recommender.get_enhanced_recommendations(clean_emotion, count=5)
        if music_recs:
            st.session_state.playlist = music_recs
            display_enhanced_music_recommendations(
                music_recs, clean_emotion, f"Music for a {target_mood} Mood"
            )
        else:
            st.info("No music recommendations available.")

    with tabs[1]:  # Reading
        st.subheader("📚 Reading Suggestions")
        reading_recs = reading_recommender.get_reading_recommendations(clean_emotion, 4)
        display_reading_recommendations(
            reading_recs, clean_emotion, f"Reading for {clean_emotion.title()}"
        )
        display_reading_insights(clean_emotion)

    with tabs[2]:  # Wellness
        st.subheader("🧘 Wellness & Mindfulness")
        wellness_recs = wellness_features.get_wellness_recommendations(clean_emotion, confidence)
        if wellness_recs:
            for rec in wellness_recs:
                priority_color = (
                    "#E74C3C" if rec.get('priority') == 'high'
                    else "#F39C12" if rec.get('priority') == 'medium'
                    else "#27AE60"
                )
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid {priority_color};">
                    <h4 style="margin: 0; color: {priority_color};">{rec.get('title', 'Activity')}</h4>
                    <p style="margin: 5px 0; color: #666;">{rec.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)

        display_breathing_exercise(clean_emotion, wellness_features, key_prefix="rec_panel")

    with tabs[3]:  # Coloring Game
        display_coloring_game(clean_emotion, key_prefix="rec_panel")

    with tabs[4]:  # AI Chatbot
        st.subheader("💬 AI Wellness Companion")
        show_chatbot(clean_emotion)
        st.info("Talk with your AI wellness assistant about how you feel.")

    with tabs[5]:  # Mood Journal
        display_mood_journal(clean_emotion, wellness_features)

    with tabs[6]:  # Support
        st.subheader("🆘 Mental Health Resources")
        display_mental_health_resources(
            clean_emotion, int(confidence), f"Support for {clean_emotion.title()}"
        )
        display_quick_mental_health_links(clean_emotion, int(confidence))
