"""
Breathing Exercise UI
Displays breathing exercises with CSS-based animations instead of
server-side rerun loops. All animation happens in the browser.
"""

import streamlit as st
import streamlit.components.v1 as components


def display_breathing_exercise(emotion, wellness_data, key_prefix=""):
    """Display a breathing exercise based on the detected emotion.
    
    Uses a self-contained HTML/CSS/JS animation that runs entirely in the
    browser — no st.rerun() or time.sleep() needed.
    """
    st.markdown("---")
    st.subheader("🧘 Breathing Exercise")

    # Get breathing exercise details from the wellness_data instance
    exercise = wellness_data.get_breathing_exercise(emotion)

    # Display exercise info card
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

    # Parse breathing timing from technique string
    inhale_time, hold_time, exhale_time = _parse_technique(exercise['technique'])
    total_cycle = inhale_time + hold_time + exhale_time

    # Render the self-contained browser animation
    _render_breathing_animation(
        inhale_time, hold_time, exhale_time, total_cycle, key_prefix
    )


def _parse_technique(technique_str):
    """Extract inhale-hold-exhale timings from technique string like '4-7-8'."""
    timing_map = {
        "4-4-4": (4, 4, 4),
        "4-7-8": (4, 7, 8),
        "5-5-5": (5, 5, 5),
        "3-6-9": (3, 6, 9),
        "4-6-8": (4, 6, 8),
    }
    for pattern, timings in timing_map.items():
        if pattern in technique_str:
            return timings
    return (4, 4, 4)  # Default


def _render_breathing_animation(inhale, hold, exhale, total, key_prefix):
    """Render a fully self-contained breathing animation in HTML/CSS/JS.
    
    This runs entirely in the browser — no Streamlit reruns needed.
    """
    html_code = f"""
    <style>
        .breathe-btn {{
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin: 5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            outline: none;
        }}
        #start-btn-{key_prefix} {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
        }}
        #start-btn-{key_prefix}:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
        }}
        #stop-btn-{key_prefix} {{
            background: transparent;
            color: #ff4b4b;
            border: 2px solid #ff4b4b;
            position: absolute;
            top: 20px;
            right: 20px;
        }}
        #stop-btn-{key_prefix}:hover {{
            background: #ff4b4b;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255, 75, 75, 0.3);
        }}
    </style>
    <div id="breathing-app-{key_prefix}" style="text-align: center; padding: 20px; font-family: 'Segoe UI', sans-serif; position: relative;">
        <!-- Absolute position stop button -->
        <button id="stop-btn-{key_prefix}" class="breathe-btn" onclick="stopBreathing_{key_prefix.replace('-','_')}()" style="display: none;">
            ⏹️ Stop
        </button>
        
        <div id="circle-{key_prefix}" style="
            width: 180px; height: 180px; border-radius: 50%; margin: 0 auto 20px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-size: 22px; font-weight: bold;
            background: #4CAF50; transition: all 0.5s ease;
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.2);
        ">
            Press Start
        </div>
        <p id="phase-text-{key_prefix}" style="font-size: 18px; font-weight: bold; color: inherit; margin: 10px 0;">
            Ready to begin
        </p>
        <p id="stats-{key_prefix}" style="color: #888; font-size: 14px; margin: 5px 0;">
            Inhale {inhale}s · Hold {hold}s · Exhale {exhale}s
        </p>
        <div style="margin-top: 25px;">
            <button id="start-btn-{key_prefix}" class="breathe-btn" onclick="startBreathing_{key_prefix.replace('-','_')}()">
                🫁 Start
            </button>
        </div>
    </div>

    <script>
    (function() {{
        var timer_{key_prefix.replace('-','_')} = null;
        var startTime_{key_prefix.replace('-','_')} = 0;
        var inhale = {inhale};
        var hold = {hold};
        var exhale = {exhale};
        var total = inhale + hold + exhale;
        var prefix = "{key_prefix}";

        function getEl(id) {{ return document.getElementById(id + '-' + prefix); }}

        window.startBreathing_{key_prefix.replace('-','_')} = function() {{
            startTime_{key_prefix.replace('-','_')} = Date.now();
            getEl('start-btn').style.display = 'none';
            getEl('stop-btn').style.display = 'inline-block';
            tick_{key_prefix.replace('-','_')}();
        }};

        window.stopBreathing_{key_prefix.replace('-','_')} = function() {{
            if (timer_{key_prefix.replace('-','_')}) clearTimeout(timer_{key_prefix.replace('-','_')});
            getEl('start-btn').style.display = 'inline-block';
            getEl('stop-btn').style.display = 'none';
            var circle = getEl('circle');
            circle.style.background = '#4CAF50';
            circle.style.width = '180px';
            circle.style.height = '180px';
            circle.innerText = 'Press Start';
            getEl('phase-text').innerText = 'Exercise complete! Great job 🎉';
        }};

        function tick_{key_prefix.replace('-','_')}() {{
            var elapsed = (Date.now() - startTime_{key_prefix.replace('-','_')}) / 1000;
            var cyclePos = elapsed % total;
            var cycleNum = Math.floor(elapsed / total) + 1;
            var circle = getEl('circle');
            var phaseText = getEl('phase-text');
            var stats = getEl('stats');

            if (cyclePos < inhale) {{
                var progress = cyclePos / inhale;
                var size = 180 + progress * 80;
                circle.style.background = '#4CAF50';
                circle.style.width = size + 'px';
                circle.style.height = size + 'px';
                circle.innerText = 'Breathe In';
                phaseText.innerText = 'Breathe In · ' + Math.round(progress * 100) + '%';
                phaseText.style.color = '#4CAF50';
            }} else if (cyclePos < inhale + hold) {{
                var progress = (cyclePos - inhale) / hold;
                circle.style.background = '#FF9800';
                circle.style.width = '260px';
                circle.style.height = '260px';
                circle.innerText = 'Hold';
                phaseText.innerText = 'Hold · ' + Math.round(progress * 100) + '%';
                phaseText.style.color = '#FF9800';
            }} else {{
                var progress = (cyclePos - inhale - hold) / exhale;
                var size = 260 - progress * 80;
                circle.style.background = '#2196F3';
                circle.style.width = size + 'px';
                circle.style.height = size + 'px';
                circle.innerText = 'Breathe Out';
                phaseText.innerText = 'Breathe Out · ' + Math.round(progress * 100) + '%';
                phaseText.style.color = '#2196F3';
            }}

            stats.innerText = 'Elapsed: ' + Math.floor(elapsed) + 's · Cycle: ' + cycleNum;
            timer_{key_prefix.replace('-','_')} = setTimeout(tick_{key_prefix.replace('-','_')}, 50);
        }}
    }})();
    </script>
    """
    components.html(html_code, height=380)


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

    steps = [
        ("5", "things you can see", "Look around and name 5 things you can see"),
        ("4", "things you can touch", "Name 4 things you can touch or feel"),
        ("3", "things you can hear", "Listen and name 3 things you can hear"),
        ("2", "things you can smell", "Take a deep breath and name 2 things you can smell"),
        ("1", "thing you can taste", "Name 1 thing you can taste"),
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
        st.success("Excellent! You've completed the grounding exercise. How do you feel now? 🎉")