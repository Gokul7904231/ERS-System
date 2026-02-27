import streamlit as st
from datetime import datetime
import json

def display_mood_journal(emotion, wellness_data):
    """Display mood journaling interface based on detected emotion."""
    
    st.markdown("---")
    st.subheader("📝 Mood Journal")
    
    # Get journaling prompts for the emotion
    prompts = wellness_data.get_mood_journal_prompts(emotion)
    
    # Display emotion-specific header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">📝 Journaling for {emotion.title()} Feelings</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">Take a moment to reflect on your emotions and thoughts.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for journal entries
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
    
    # Journaling form
    with st.form("mood_journal_form"):
        st.markdown("### How are you feeling right now?")
        
        # Emotion intensity slider
        intensity = st.slider(
            "Emotion Intensity (1-10)", 
            min_value=1, 
            max_value=10, 
            value=5,
            help="Rate how intense this emotion feels right now"
        )
        
        # Journal prompts
        st.markdown("### Reflection Prompts")
        
        journal_responses = {}
        for i, prompt in enumerate(prompts):
            journal_responses[f"prompt_{i}"] = st.text_area(
                prompt, 
                key=f"journal_prompt_{i}",
                height=100,
                placeholder="Share your thoughts here..."
            )
        
        # Additional free-form journaling
        st.markdown("### Additional Thoughts")
        additional_thoughts = st.text_area(
            "Is there anything else you'd like to write about?",
            key="additional_thoughts",
            height=150,
            placeholder="Write anything that comes to mind..."
        )
        
        # Mood tags
        st.markdown("### Mood Tags")
        mood_tags = st.multiselect(
            "Select any additional mood tags that apply:",
            ["Anxious", "Calm", "Energetic", "Tired", "Hopeful", "Frustrated", "Grateful", "Lonely", "Excited", "Overwhelmed"],
            key="mood_tags"
        )
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Journal Entry", use_container_width=True)
        
        if submitted:
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
            st.rerun()
    
    # Display recent journal entries
    if st.session_state.journal_entries:
        st.markdown("---")
        st.subheader("📚 Recent Journal Entries")
        
        # Show last 3 entries
        recent_entries = st.session_state.journal_entries[-3:]
        
        for i, entry in enumerate(reversed(recent_entries)):
            with st.expander(f"Entry {len(st.session_state.journal_entries) - i} - {entry['emotion'].title()} ({entry['intensity']}/10)"):
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
        if st.button("🗑️ Clear All Journal Entries", key="clear_journal"):
            st.session_state.journal_entries = []
            st.success("Journal entries cleared.")
            st.rerun()

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
        st.markdown("### Your Mood Trends")
        
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
        
        # Recent trend
        if len(mood_data) >= 2:
            recent_avg = sum(entry['intensity'] for entry in mood_data[-3:]) / min(3, len(mood_data))
            older_avg = sum(entry['intensity'] for entry in mood_data[:-3]) / max(1, len(mood_data) - 3)
            
            if recent_avg > older_avg:
                trend = "increasing"
                trend_color = "#E74C3C"
            elif recent_avg < older_avg:
                trend = "decreasing"
                trend_color = "#27AE60"
            else:
                trend = "stable"
                trend_color = "#7F8C8D"
            
            st.markdown(f"**Recent Trend:** <span style='color: {trend_color};'>{trend.title()}</span>", unsafe_allow_html=True)

def export_journal_data():
    """Export journal data as JSON."""
    
    if not st.session_state.get('journal_entries', []):
        return
    
    st.markdown("---")
    st.subheader("📤 Export Journal Data")
    
    if st.button("📥 Download Journal Data", use_container_width=True):
        # Create JSON data
        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_entries": len(st.session_state.journal_entries),
            "entries": st.session_state.journal_entries
        }
        
        # Convert to JSON string
        json_data = json.dumps(export_data, indent=2)
        
        # Create download button
        st.download_button(
            label="💾 Download Journal Data",
            data=json_data,
            file_name=f"mood_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
