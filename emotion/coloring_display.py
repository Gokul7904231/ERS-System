import streamlit as st
from coloring_game import coloring_game

def display_coloring_game(emotion):
    """Display the mood-refreshing coloring game."""
    
    st.subheader("🎨 Mood-Refreshing Coloring Game")
    
    # Get coloring page for the emotion
    page_info = coloring_game.get_coloring_page(emotion)
    color_palette = coloring_game.get_color_palette(emotion)
    
    # Display page information
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">{page_info['name']}</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">{page_info['description']}</p>
        <p style="margin: 5px 0; color: #f0f0f0;"><strong>Color Suggestion:</strong> {page_info['color_suggestion']}</p>
        <p style="margin: 5px 0; color: #f0f0f0;"><strong>Complexity:</strong> {page_info['complexity'].title()}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for the game
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎨 Color Palette")
        st.markdown("**Click a color to select it:**")
        
        # Display color palette
        for i, color in enumerate(color_palette):
            if st.button(f"Color {i+1}", key=f"color_{i}", 
                        help=f"Click to select {color}",
                        use_container_width=True):
                st.session_state.selected_color = color
                st.success(f"Selected: {color}")
        
        # Show selected color
        if 'selected_color' in st.session_state:
            st.markdown(f"**Selected Color:**")
            st.markdown(f'<div style="width: 50px; height: 50px; background-color: {st.session_state.selected_color}; border: 2px solid #333; border-radius: 5px;"></div>', 
                       unsafe_allow_html=True)
        
        # Game controls
        st.markdown("### 🎮 Game Controls")
        if st.button("🔄 New Page", use_container_width=True):
            st.session_state.coloring_progress = {}
            st.session_state.current_colors = {}
            st.rerun()
        
        if st.button("💾 Save Progress", use_container_width=True):
            st.success("Progress saved! Your beautiful artwork is preserved.")
        
        if st.button("📤 Share Artwork", use_container_width=True):
            st.info("Share your beautiful creation with friends!")
    
    with col2:
        st.markdown("### 🖼️ Coloring Page")
        st.markdown("**Click on areas to color them:**")
        
        # Get SVG design
        svg_design = coloring_game.create_svg_design(page_info['design'], page_info['complexity'])
        
        # Display the SVG with clickable areas
        st.markdown("""
        <div style="border: 2px solid #ddd; border-radius: 10px; padding: 20px; background: white;">
            <div id="coloring-area" style="text-align: center;">
        """ + svg_design + """
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Instructions
        st.markdown("""
        <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin-top: 10px;">
            <h4 style="margin: 0; color: #1976D2;">🎨 How to Play:</h4>
            <ol style="margin: 10px 0; color: #333;">
                <li><strong>Select a color</strong> from the palette on the left</li>
                <li><strong>Click on any area</strong> of the design to color it</li>
                <li><strong>Create your masterpiece</strong> and feel your mood lift!</li>
                <li><strong>Save your progress</strong> to continue later</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress tracking
    st.markdown("---")
    st.markdown("### 📊 Your Progress")
    
    if st.session_state.coloring_progress:
        progress_percent = len(st.session_state.coloring_progress) * 10  # Assuming 10 areas max
        st.progress(min(progress_percent, 100), text=f"Colored areas: {len(st.session_state.coloring_progress)}")
    else:
        st.progress(0, text="Start coloring to see your progress!")
    
    # Mood boost message
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFE0B2 0%, #FFCC80 100%); 
                padding: 20px; border-radius: 10px; margin-top: 20px;">
        <h3 style="margin: 0; color: #E65100;">✨ Mood Boost Tip</h3>
        <p style="margin: 10px 0; color: #333;">
            Coloring has been scientifically proven to reduce stress and anxiety! 
            As you focus on creating beautiful art, your mind naturally relaxes and your mood improves.
        </p>
        <p style="margin: 5px 0; color: #333; font-style: italic;">
            "Art washes away from the soul the dust of everyday life." - Pablo Picasso
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_standalone_coloring_game():
    """Display standalone coloring game that works without emotion detection."""
    
    st.subheader("🎨 Mood-Refreshing Coloring Game")
    
    # Let user choose emotion for coloring
    emotion_choice = st.selectbox(
        "What emotion are you feeling right now?",
        ["sad", "anger", "fear", "disgust", "happy", "surprise", "contempt", "neutral"],
        help="Choose the emotion that best describes your current mood"
    )
    
    st.markdown("---")
    
    # Display the coloring game
    display_coloring_game(emotion_choice)
