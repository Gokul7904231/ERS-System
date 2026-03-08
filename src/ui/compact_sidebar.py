"""
Compact Sidebar Component for SEntixcare
A single, scrollable container for all sidebar content
"""

import streamlit as st

def create_compact_sidebar():
    """Create a single, scrollable container for all sidebar content"""
    with st.sidebar:
        # App Branding
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-bottom: 2rem;">
            <h2 style="color: white; margin: 0; font-size: 2rem;">🧠 Sentixcare</h2>
            <p style="color: white; margin: 0; opacity: 0.9; font-size: 1.2rem;">Professional Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Scrollable Content Container
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%); 
            border-radius: 20px; 
            padding: 2rem; 
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
            max-height: 70vh;
            overflow-y: auto;
            border: 2px solid #e8f4fd;
            position: relative;
        ">
        """, unsafe_allow_html=True)
        
        # App Status
        st.markdown("### 📊 App Status")
        if st.session_state.get('models_loaded', False):
            st.success("✅ **Models Loaded & Ready**")
        else:
            st.warning("⚠️ **Models Not Loaded**")
            st.info("Click 'Load Models' button to start")
        
        st.markdown("---")
        
        # Quick Stats
        if st.session_state.get('emotion_history'):
            st.markdown("### 📈 Your Journey")
            total_detections = len(st.session_state.emotion_history)
            st.metric("Total Sessions", total_detections)
            
            # Most common emotion
            emotion_counts = {}
            for entry in st.session_state.emotion_history:
                emotion = entry['emotion']
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            if emotion_counts:
                most_common = max(emotion_counts, key=emotion_counts.get)
                st.metric("Most Common Mood", most_common.title())
            
            st.markdown("---")
        
        # Quick Help
        st.markdown("### 🆘 Quick Help")
        st.markdown("**🚨 Emergency: 911**")
        st.markdown("**🆘 Crisis Line: 988**")
        st.markdown("**💬 Crisis Text: 741741**")
        
        st.markdown("---")
        
        # Full Resources Link
        st.markdown("### 📚 Full Resources")
        st.info("Scroll down to find comprehensive mental health resources, professional help, self-help tools, and wellness tips.")
        
        st.markdown("---")
        
        # Now Playing
        st.markdown("### 🎵 Now Playing")
        if st.session_state.get('current_track'):
            track = st.session_state.current_track
            st.markdown(f"**{track['title']}**")
            st.markdown(f"by {track['artist']}")
            youtube_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
            st.markdown(f"[🎵 Play on YouTube]({youtube_url})")
        else:
            st.info("No track selected. Choose a song from the recommendations below!")
        
        st.markdown("---")
        
        # Reading Tips
        st.markdown("### 📚 Reading Tips")
        st.markdown("**💡 Quick Tips:**")
        st.markdown("• Set aside 10–15 minutes daily for reading")
        st.markdown("• Choose materials that match your current mood")
        st.markdown("• Keep a reading journal to track insights")
        st.markdown("• Join online book clubs for community")
        st.markdown("• Try audiobooks for busy schedules")
        
        st.markdown("**🔗 Popular Reading Platforms:**")
        st.markdown("• Goodreads")
        st.markdown("• Medium")
        st.markdown("• Project Gutenberg")
        st.markdown("• TED Talks")
        
        st.markdown("---")
        
        # Crisis Support
        st.markdown("### 🆘 Crisis Support")
        st.markdown("**🚨 Emergency: Call 911**")
        st.markdown("**🆘 Suicide Prevention: 988**")
        st.markdown("**💬 Crisis Text: Text HOME to 741741**")
        
        st.markdown("---")
        
        # Professional Help
        st.markdown("### 👩‍⚕️ Professional Help")
        st.markdown("• Find Therapists")
        st.markdown("• Online Therapy")
        st.markdown("• Affordable Therapy")
        
        st.markdown("---")
        
        # Self-Help
        st.markdown("### 🧘 Self-Help")
        st.markdown("• Mindfulness")
        st.markdown("• Meditation Apps")
        st.markdown("• CBT Resources")
        
        st.markdown("---")
        
        # Important Notice
        st.markdown("### ⚠️ Important")
        st.warning("This app is not a substitute for professional mental health care. If you're in crisis, please reach out for immediate help.")
        
        st.markdown("---")
        
        # Wellness Dashboard
        st.markdown("### 🧠 Wellness Dashboard")
        st.markdown("**💡 Daily Wellness Tip**")
        st.info("🎵 Listen to music that matches your current mood")
        
        st.markdown("---")
        
        # Scientific References
        st.markdown("### 📚 Scientific References")
        st.markdown("All breathing exercises are evidence-based and clinically validated.")
        st.markdown("See SCIENTIFIC_REFERENCES.md for detailed citations.")
        
        # Close the scrollable container
        st.markdown("</div>", unsafe_allow_html=True)
