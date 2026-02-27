"""
Resources Section for AI MoodMate
A dedicated, scrollable section for all mental health and wellness resources
"""

import streamlit as st

def create_resources_section():
    """Create a dedicated resources section with all mental health and wellness resources"""
    
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 20px; margin: 2rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; margin: 0; color: #2c3e50; font-size: 2.5rem;">🆘 Mental Health & Wellness Resources</h2>
        <p style="text-align: center; margin: 1rem 0 0 0; color: #666; font-size: 1.2rem;">Comprehensive support and resources for your mental health journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different resource categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🆘 Crisis Support", "👩‍⚕️ Professional Help", "🧘 Self-Help", "📚 Reading & Learning", "💡 Wellness Tips"])
    
    with tab1:
        create_crisis_support_tab()
    
    with tab2:
        create_professional_help_tab()
    
    with tab3:
        create_self_help_tab()
    
    with tab4:
        create_reading_learning_tab()
    
    with tab5:
        create_wellness_tips_tab()

def create_crisis_support_tab():
    """Create crisis support resources tab"""
    st.markdown("""
    <div style="background: #ffebee; padding: 2rem; border-radius: 15px; border-left: 5px solid #f44336;">
        <h3 style="color: #c62828; margin: 0 0 1rem 0;">🚨 Immediate Crisis Support</h3>
        <p style="color: #666; margin: 0 0 1.5rem 0;">If you're in immediate danger or having thoughts of self-harm, please reach out for help right now.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #d32f2f; margin: 0 0 1rem 0;">🚨 Emergency Services</h4>
            <p style="margin: 0.5rem 0;"><strong>Emergency:</strong> Call 911</p>
            <p style="margin: 0.5rem 0;"><strong>Available:</strong> 24/7</p>
            <p style="margin: 0.5rem 0;">For immediate life-threatening emergencies</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #d32f2f; margin: 0 0 1rem 0;">🆘 Suicide Prevention Lifeline</h4>
            <p style="margin: 0.5rem 0;"><strong>Phone:</strong> 988</p>
            <p style="margin: 0.5rem 0;"><strong>Available:</strong> 24/7</p>
            <p style="margin: 0.5rem 0;">Free, confidential support for people in distress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #d32f2f; margin: 0 0 1rem 0;">💬 Crisis Text Line</h4>
            <p style="margin: 0.5rem 0;"><strong>Text:</strong> HOME to 741741</p>
            <p style="margin: 0.5rem 0;"><strong>Available:</strong> 24/7</p>
            <p style="margin: 0.5rem 0;">Free crisis support via text message</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #d32f2f; margin: 0 0 1rem 0;">📞 SAMHSA National Helpline</h4>
            <p style="margin: 0.5rem 0;"><strong>Phone:</strong> 1-800-662-4357</p>
            <p style="margin: 0.5rem 0;"><strong>Available:</strong> 24/7</p>
            <p style="margin: 0.5rem 0;">Free treatment referral and information service</p>
        </div>
        """, unsafe_allow_html=True)

def create_professional_help_tab():
    """Create professional help resources tab"""
    st.markdown("""
    <div style="background: #e3f2fd; padding: 2rem; border-radius: 15px; border-left: 5px solid #2196f3;">
        <h3 style="color: #1565c0; margin: 0 0 1rem 0;">👩‍⚕️ Professional Mental Health Support</h3>
        <p style="color: #666; margin: 0;">Find licensed mental health professionals and therapy options</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #1976d2; margin: 0 0 1rem 0;">🔍 Find Local Therapists</h4>
            <p style="margin: 0.5rem 0;"><strong>Psychology Today</strong></p>
            <p style="margin: 0.5rem 0;">Search by location, specialty, and insurance</p>
            <p style="margin: 0.5rem 0;">Read therapist profiles and contact directly</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #1976d2; margin: 0 0 1rem 0;">💻 Online Therapy</h4>
            <p style="margin: 0.5rem 0;"><strong>BetterHelp</strong></p>
            <p style="margin: 0.5rem 0;">Licensed professional counselors online</p>
            <p style="margin: 0.5rem 0;">Flexible scheduling and messaging support</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #1976d2; margin: 0 0 1rem 0;">📱 Talkspace</h4>
            <p style="margin: 0.5rem 0;">Online therapy and psychiatry services</p>
            <p style="margin: 0.5rem 0;">Video sessions and text therapy</p>
            <p style="margin: 0.5rem 0;">Insurance accepted</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #1976d2; margin: 0 0 1rem 0;">💰 Affordable Therapy</h4>
            <p style="margin: 0.5rem 0;"><strong>Open Path Psychotherapy</strong></p>
            <p style="margin: 0.5rem 0;">Sliding scale fees for individuals and families</p>
            <p style="margin: 0.5rem 0;">No insurance required</p>
        </div>
        """, unsafe_allow_html=True)

def create_self_help_tab():
    """Create self-help resources tab"""
    st.markdown("""
    <div style="background: #f3e5f5; padding: 2rem; border-radius: 15px; border-left: 5px solid #9c27b0;">
        <h3 style="color: #7b1fa2; margin: 0 0 1rem 0;">🧘 Self-Help & Wellness Resources</h3>
        <p style="color: #666; margin: 0;">Tools and techniques you can use on your own</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #7b1fa2; margin: 0 0 1rem 0;">🧘 Mindfulness & Meditation</h4>
            <p style="margin: 0.5rem 0;"><strong>Headspace</strong></p>
            <p style="margin: 0.5rem 0;">Meditation and mindfulness app</p>
            <p style="margin: 0.5rem 0;">Free resources and guided sessions</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #7b1fa2; margin: 0 0 1rem 0;">🌊 Calm</h4>
            <p style="margin: 0.5rem 0;">Meditation, sleep, and relaxation app</p>
            <p style="margin: 0.5rem 0;">Sleep stories and breathing exercises</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #7b1fa2; margin: 0 0 1rem 0;">🧠 CBT Resources</h4>
            <p style="margin: 0.5rem 0;"><strong>Cognitive Behavioral Therapy</strong></p>
            <p style="margin: 0.5rem 0;">Self-help techniques and resources</p>
            <p style="margin: 0.5rem 0;">Evidence-based approaches</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #7b1fa2; margin: 0 0 1rem 0;">📚 Mindful.org</h4>
            <p style="margin: 0.5rem 0;">Mindfulness meditation resources</p>
            <p style="margin: 0.5rem 0;">Articles and guided practices</p>
        </div>
        """, unsafe_allow_html=True)

def create_reading_learning_tab():
    """Create reading and learning resources tab"""
    st.markdown("""
    <div style="background: #e8f5e8; padding: 2rem; border-radius: 15px; border-left: 5px solid #4caf50;">
        <h3 style="color: #2e7d32; margin: 0 0 1rem 0;">📚 Reading & Learning Resources</h3>
        <p style="color: #666; margin: 0;">Expand your knowledge and find inspiration through reading</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
        <h4 style="color: #2e7d32; margin: 0 0 1rem 0;">💡 Reading Tips for Mental Wellness</h4>
        <ul style="font-size: 1.1rem; line-height: 1.8; color: #333;">
            <li><strong>Set aside 10-15 minutes daily</strong> for reading</li>
            <li><strong>Choose materials that match your current mood</strong> for better engagement</li>
            <li><strong>Keep a reading journal</strong> to track insights and reflections</li>
            <li><strong>Join online book clubs</strong> for community and discussion</li>
            <li><strong>Try audiobooks</strong> for busy schedules or when you need a break from screens</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #2e7d32; margin: 0 0 1rem 0;">📖 Goodreads</h4>
            <p style="margin: 0.5rem 0;">Discover and track books</p>
            <p style="margin: 0.5rem 0;">Join reading communities</p>
            <p style="margin: 0.5rem 0;">Get personalized recommendations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #2e7d32; margin: 0 0 1rem 0;">📚 Project Gutenberg</h4>
            <p style="margin: 0.5rem 0;">Free ebooks and classic literature</p>
            <p style="margin: 0.5rem 0;">No registration required</p>
            <p style="margin: 0.5rem 0;">Thousands of free books</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #2e7d32; margin: 0 0 1rem 0;">✍️ Medium</h4>
            <p style="margin: 0.5rem 0;">Articles on mental health and wellness</p>
            <p style="margin: 0.5rem 0;">Personal stories and insights</p>
            <p style="margin: 0.5rem 0;">Expert advice and tips</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #2e7d32; margin: 0 0 1rem 0;">🎤 TED Talks</h4>
            <p style="margin: 0.5rem 0;">Inspiring talks on mental health</p>
            <p style="margin: 0.5rem 0;">Expert insights and research</p>
            <p style="margin: 0.5rem 0;">Free video content</p>
        </div>
        """, unsafe_allow_html=True)

def create_wellness_tips_tab():
    """Create wellness tips tab"""
    st.markdown("""
    <div style="background: #fff3e0; padding: 2rem; border-radius: 15px; border-left: 5px solid #ff9800;">
        <h3 style="color: #e65100; margin: 0 0 1rem 0;">💡 Daily Wellness Tips</h3>
        <p style="color: #666; margin: 0;">Simple, practical tips for better mental health and wellness</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #e65100; margin: 0 0 1rem 0;">🏃‍♀️ Physical Activity</h4>
            <p style="margin: 0.5rem 0;">Even a short walk can help improve your mood</p>
            <p style="margin: 0.5rem 0;">Try 10 minutes of gentle exercise daily</p>
            <p style="margin: 0.5rem 0;">Dance to your favorite music</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #e65100; margin: 0 0 1rem 0;">😴 Sleep & Rest</h4>
            <p style="margin: 0.5rem 0;">Aim for 7-9 hours of sleep nightly</p>
            <p style="margin: 0.5rem 0;">Create a relaxing bedtime routine</p>
            <p style="margin: 0.5rem 0;">Limit screen time before bed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #e65100; margin: 0 0 1rem 0;">🍎 Nutrition & Hydration</h4>
            <p style="margin: 0.5rem 0;">Stay hydrated throughout the day</p>
            <p style="margin: 0.5rem 0;">Eat regular, balanced meals</p>
            <p style="margin: 0.5rem 0;">Limit caffeine and sugar</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
            <h4 style="color: #e65100; margin: 0 0 1rem 0;">🤝 Social Connection</h4>
            <p style="margin: 0.5rem 0;">Reach out to friends and family</p>
            <p style="margin: 0.5rem 0;">Join community groups or activities</p>
            <p style="margin: 0.5rem 0;">Practice active listening</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Important disclaimer
    st.markdown("""
    <div style="background: #ffebee; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #f44336; margin: 2rem 0;">
        <h4 style="color: #c62828; margin: 0 0 1rem 0;">⚠️ Important Disclaimer</h4>
        <p style="color: #666; margin: 0; font-size: 1rem; line-height: 1.6;">
            This app is not a substitute for professional mental health care. If you're in crisis, 
            please reach out for immediate help using the crisis resources above. Always seek the 
            advice of qualified health providers with questions about your mental health.
        </p>
    </div>
    """, unsafe_allow_html=True)
