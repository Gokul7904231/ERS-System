import streamlit as st
import time
import random

def display_breathing_exercise(emotion, wellness_data):
    """Display a breathing exercise based on the detected emotion."""
    
    st.markdown("---")
    st.subheader("🧘 Breathing Exercise")
    
    # Get breathing exercise details
    exercise = wellness_data.get_breathing_exercise(emotion)
    
    # Display exercise info
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {exercise['color']} 0%, #667eea 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">{exercise['breathing_exercise']}</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">{exercise['description']}</p>
        <p style="margin: 5px 0; color: #f0f0f0;"><strong>Technique:</strong> {exercise['technique']}</p>
        <p style="margin: 5px 0; color: #f0f0f0;"><strong>Duration:</strong> {exercise['duration']} minutes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display scientific reference
    st.markdown("### 📚 Scientific Reference")
    st.info(f"""
    **Reference:** {exercise['reference']}
    
    **Research:** {exercise['research']}
    """)
    
    # Breathing exercise controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🫁 Start Breathing Exercise", use_container_width=True, key="start_breathing"):
            st.session_state.breathing_active = True
            st.session_state.breathing_start_time = time.time()
            st.rerun()
    
    # Display breathing exercise if active
    if st.session_state.get('breathing_active', False):
        display_breathing_animation(exercise)
        
        # Stop button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⏹️ Stop Exercise", use_container_width=True, key="stop_breathing"):
                st.session_state.breathing_active = False
                st.session_state.breathing_start_time = None
                st.success("Great job completing your breathing exercise! 🎉")
                st.rerun()

def display_breathing_animation(exercise):
    """Display the breathing animation."""
    
    # Create a placeholder for the animation
    animation_placeholder = st.empty()
    
    # Breathing cycle timing based on technique
    if "4-4-4" in exercise['technique']:
        inhale_time = 4
        hold_time = 4
        exhale_time = 4
    elif "4-7-8" in exercise['technique']:
        inhale_time = 4
        hold_time = 7
        exhale_time = 8
    elif "5-5-5" in exercise['technique']:
        inhale_time = 5
        hold_time = 5
        exhale_time = 5
    elif "3-6-9" in exercise['technique']:
        inhale_time = 3
        hold_time = 6
        exhale_time = 9
    elif "4-6-8" in exercise['technique']:
        inhale_time = 4
        hold_time = 6
        exhale_time = 8
    else:
        inhale_time = 4
        hold_time = 4
        exhale_time = 4
    
    cycle_time = inhale_time + hold_time + exhale_time
    
    # Calculate elapsed time
    start_time = st.session_state.get('breathing_start_time', time.time())
    elapsed_time = time.time() - start_time
    
    # Calculate current cycle position
    cycle_position = elapsed_time % cycle_time
    
    # Determine current phase
    if cycle_position < inhale_time:
        phase = "inhale"
        phase_text = "Breathe In"
        phase_color = "#4CAF50"
        progress = cycle_position / inhale_time
    elif cycle_position < inhale_time + hold_time:
        phase = "hold"
        phase_text = "Hold"
        phase_color = "#FF9800"
        progress = (cycle_position - inhale_time) / hold_time
    else:
        phase = "exhale"
        phase_text = "Breathe Out"
        phase_color = "#2196F3"
        progress = (cycle_position - inhale_time - hold_time) / exhale_time
    
    # Display the animation
    animation_placeholder.markdown(f"""
    <div style="text-align: center; padding: 40px;">
        <div style="background: {phase_color}; 
                    width: {int(200 + progress * 100)}px; 
                    height: {int(200 + progress * 100)}px; 
                    border-radius: 50%; 
                    margin: 0 auto 20px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    color: white; 
                    font-size: 24px; 
                    font-weight: bold;
                    transition: all 0.5s ease;">
            {phase_text}
        </div>
        <p style="font-size: 18px; color: {phase_color}; font-weight: bold;">
            {phase_text} • {int(progress * 100)}%
        </p>
        <p style="color: #666; font-size: 14px;">
            Elapsed: {int(elapsed_time)}s • Cycle: {int(elapsed_time // cycle_time) + 1}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh for animation
    time.sleep(0.1)
    st.rerun()

def display_grounding_exercise():
    """Display a 5-4-3-2-1 grounding exercise."""
    
    st.markdown("---")
    st.subheader("🌍 Grounding Exercise: 5-4-3-2-1")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #8E44AD 0%, #667eea 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">5-4-3-2-1 Grounding Technique</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">This technique helps you stay present and calm by focusing on your senses.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌍 Start Grounding Exercise", use_container_width=True, key="start_grounding"):
        st.session_state.grounding_active = True
        st.rerun()
    
    if st.session_state.get('grounding_active', False):
        display_grounding_steps()

def display_grounding_steps():
    """Display the grounding exercise steps."""
    
    steps = [
        ("5", "things you can see", "Look around and name 5 things you can see"),
        ("4", "things you can touch", "Name 4 things you can touch or feel"),
        ("3", "things you can hear", "Listen and name 3 things you can hear"),
        ("2", "things you can smell", "Take a deep breath and name 2 things you can smell"),
        ("1", "thing you can taste", "Name 1 thing you can taste")
    ]
    
    for i, (number, sense, instruction) in enumerate(steps):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #8E44AD;">
            <h4 style="margin: 0; color: #8E44AD;">{number}. {sense.title()}</h4>
            <p style="margin: 5px 0; color: #666;">{instruction}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"✅ Completed {number}", key=f"grounding_{i}"):
            st.success(f"Great! You've completed step {number}.")
    
    if st.button("🏁 Finish Grounding Exercise", use_container_width=True, key="finish_grounding"):
        st.session_state.grounding_active = False
        st.success("Excellent! You've completed the grounding exercise. How do you feel now? 🎉")
        st.rerun()
