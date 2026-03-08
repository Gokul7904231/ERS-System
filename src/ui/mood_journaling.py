import streamlit as st
from datetime import datetime
import json

from src.features.wellness_features import wellness_features


def display_mood_journal(emotion, wellness_features):
    """Display mood journaling interface based on detected emotion."""
    
    st.subheader("📝 Mood Journal")
    
    # Store journal entries in session state
    if "journal_entries" not in st.session_state:
        st.session_state.journal_entries = []
    
    # Get journaling prompts for the emotion
    prompts = wellness_features.get_mood_journal_prompts(emotion)
    
    # Display emotion-specific header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
        <p style="margin: 0; color: white;">Reflecting on your <strong>{emotion.title()}</strong> feelings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use form with clear_on_submit=True to prevent reruns while typing
    with st.form(f"mood_journal_form_{emotion}", clear_on_submit=True):
        
        # Journal prompts
        st.markdown("#### 💭 Reflection Prompts")
        
        journal_responses = {}
        for i, prompt in enumerate(prompts):
            journal_responses[f"prompt_{i}"] = st.text_area(
                prompt, 
                key=f"journal_prompt_{emotion}_{i}",
                height=80,
                placeholder="Share your thoughts here..."
            )
        
        # Additional free-form journaling
        st.markdown("#### ✍️ Additional Thoughts")
        additional_thoughts = st.text_area(
            "Is there anything else you'd like to write about?",
            key=f"additional_thoughts_{emotion}",
            height=100,
            placeholder="Write anything that comes to mind..."
        )
        
        # Mood tags
        st.markdown("#### 🏷️ Mood Tags")
        mood_tags = st.multiselect(
            "Select any additional mood tags:",
            ["Anxious", "Calm", "Energetic", "Tired", "Hopeful", "Frustrated", 
             "Grateful", "Lonely", "Excited", "Overwhelmed", "Peaceful", "Reflective"],
            key=f"mood_tags_{emotion}"
        )
        
        # Emotion intensity slider
        intensity = st.slider(
            "Emotion Intensity (1-10)", 
            min_value=1, 
            max_value=10, 
            value=5,
            key=f"intensity_slider_{emotion}",
            help="Rate how intense this emotion feels right now"
        )
        
        # Submit button
        submit = st.form_submit_button("💾 Save Journal Entry", use_container_width=True)
        
        if submit:
            # Check if there's any content to save
            has_content = any(journal_responses.values()) or additional_thoughts.strip() or mood_tags
            
            if has_content:
                # Create journal entry
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "emotion": emotion,
                    "intensity": intensity,
                    "responses": journal_responses,
                    "additional_thoughts": additional_thoughts,
                    "mood_tags": mood_tags
                }
                
                # Add to session state
                st.session_state.journal_entries.append(entry)
                
                st.success("✅ Journal entry saved! Great job taking time to reflect on your feelings.")
            else:
                st.warning("Please write something before saving.")
    
    # Display saved entries
    if st.session_state.journal_entries:
        
        st.markdown("---")
        st.markdown("### 📖 Previous Entries")
        
        # Show entries in reverse order (newest first)
        entries_to_show = list(reversed(st.session_state.journal_entries[-5:]))
        
        for idx, entry in enumerate(entries_to_show):
            entry_num = len(st.session_state.journal_entries) - idx if idx < len(st.session_state.journal_entries) else idx + 1
            
            with st.expander(f"📝 Entry {entry_num} - {entry['emotion'].title()} ({entry['intensity']}/10) | {datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')}"):
                st.markdown(f"**Date:** {datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**Emotion:** {entry['emotion'].title()}")
                st.markdown(f"**Intensity:** {entry['intensity']}/10")
                
                if entry['mood_tags']:
                    st.markdown(f"**Tags:** {', '.join(entry['mood_tags'])}")
                
                st.markdown("**Responses:**")
                for key, response in entry['responses'].items():
                    if response:
                        st.markdown(f"- {response}")
                
                if entry['additional_thoughts']:
                    st.markdown("**Additional Thoughts:**")
                    st.markdown(entry['additional_thoughts'])
        
        # Clear journal button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Clear All", key="clear_journal"):
                st.session_state.journal_entries = []
                st.rerun()
        with col2:
            # Export button
            if st.button("📥 Export Data", key="export_journal"):
                export_data = {
                    "export_date": datetime.now().isoformat(),
                    "total_entries": len(st.session_state.journal_entries),
                    "entries": st.session_state.journal_entries
                }
                json_data = json.dumps(export_data, indent=2)
                st.download_button(
                    label="💾 Download JSON",
                    data=json_data,
                    file_name=f"mood_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_journal"
                )


def display_mood_tracking():
    """Display mood tracking over time."""
    
    if not st.session_state.get('journal_entries', []):
        return
    
    st.markdown("---")
    st.subheader("📊 Mood Tracking")
    
    # Create mood tracking data
    mood_data = []
    for entry in st.session_state.journal_entries:
        mood_data.append({
            "date": datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d'),
            "emotion": entry['emotion'],
            "intensity": entry['intensity']
        })
    
    if mood_data:
        # Display mood trends
        st.markdown("#### Your Mood Trends")
        
        # Emotion frequency
        emotion_counts = {}
        for entry in mood_data:
            emotion = entry['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if emotion_counts:
            st.markdown("**Most Common Emotions:**")
            for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
                st.markdown(f"- {emotion.title()}: {count} times")
        
        # Average intensity
        avg_intensity = sum(entry['intensity'] for entry in mood_data) / len(mood_data)
        st.markdown(f"**Average Emotion Intensity:** {avg_intensity:.1f}/10")

