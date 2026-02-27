import streamlit as st
import random
import base64
from PIL import Image, ImageDraw
import io

class ColoringGame:
    def __init__(self):
        # Emotion-based coloring page designs
        self.emotion_pages = {
            "sad": {
                "name": "Gentle Mandala",
                "description": "A calming circular pattern to help ease sadness",
                "design": "mandala",
                "complexity": "simple",
                "color_suggestion": "Soft blues and gentle purples"
            },
            "anger": {
                "name": "Energy Release Pattern",
                "description": "Bold geometric shapes to channel anger into creativity",
                "design": "geometric",
                "complexity": "medium",
                "color_suggestion": "Cool blues and peaceful greens"
            },
            "fear": {
                "name": "Safe Haven Garden",
                "description": "Simple, familiar shapes to feel secure and grounded",
                "design": "nature",
                "complexity": "simple",
                "color_suggestion": "Warm, comforting earth tones"
            },
            "disgust": {
                "name": "Cleansing Waves",
                "description": "Flowing patterns to help release negative feelings",
                "design": "waves",
                "complexity": "medium",
                "color_suggestion": "Fresh greens and clean whites"
            },
            "happy": {
                "name": "Joyful Sunshine",
                "description": "Bright, cheerful patterns to amplify happiness",
                "design": "sunshine",
                "complexity": "simple",
                "color_suggestion": "Bright yellows and warm oranges"
            },
            "surprise": {
                "name": "Wonder Spiral",
                "description": "Intriguing patterns to explore and discover",
                "design": "spiral",
                "complexity": "medium",
                "color_suggestion": "Vibrant purples and electric blues"
            },
            "contempt": {
                "name": "Release & Let Go",
                "description": "Open patterns to help release judgment and find peace",
                "design": "open",
                "complexity": "simple",
                "color_suggestion": "Soft grays and calming blues"
            },
            "neutral": {
                "name": "Balanced Harmony",
                "description": "Peaceful patterns to maintain emotional equilibrium",
                "design": "balanced",
                "complexity": "simple",
                "color_suggestion": "Natural greens and balanced tones"
            }
        }
        
        # Color palettes for each emotion
        self.color_palettes = {
            "sad": ["#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5", "#2196F3", "#1E88E5", "#1976D2"],
            "anger": ["#E8F5E8", "#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A", "#4CAF50", "#43A047", "#388E3C"],
            "fear": ["#FFF3E0", "#FFE0B2", "#FFCC80", "#FFB74D", "#FFA726", "#FF9800", "#FB8C00", "#F57C00"],
            "disgust": ["#F1F8E9", "#DCEDC8", "#C5E1A5", "#AED581", "#9CCC65", "#8BC34A", "#7CB342", "#689F38"],
            "happy": ["#FFFDE7", "#FFF9C4", "#FFF59D", "#FFF176", "#FFEE58", "#FFEB3B", "#FDD835", "#FBC02D"],
            "surprise": ["#F3E5F5", "#E1BEE7", "#CE93D8", "#BA68C8", "#AB47BC", "#9C27B0", "#8E24AA", "#7B1FA2"],
            "contempt": ["#FAFAFA", "#F5F5F5", "#EEEEEE", "#E0E0E0", "#BDBDBD", "#9E9E9E", "#757575", "#616161"],
            "neutral": ["#E8F5E8", "#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A", "#4CAF50", "#43A047", "#388E3C"]
        }
        
        # Initialize session state for coloring
        if 'coloring_page' not in st.session_state:
            st.session_state.coloring_page = None
        if 'coloring_progress' not in st.session_state:
            st.session_state.coloring_progress = {}
        if 'current_colors' not in st.session_state:
            st.session_state.current_colors = {}

    def get_coloring_page(self, emotion):
        """Get a coloring page design for the given emotion."""
        return self.emotion_pages.get(emotion, self.emotion_pages["neutral"])

    def get_color_palette(self, emotion):
        """Get color palette for the given emotion."""
        return self.color_palettes.get(emotion, self.color_palettes["neutral"])

    def create_svg_design(self, design_type, complexity):
        """Create SVG design based on type and complexity."""
        if design_type == "mandala":
            return self._create_mandala_svg(complexity)
        elif design_type == "geometric":
            return self._create_geometric_svg(complexity)
        elif design_type == "nature":
            return self._create_nature_svg(complexity)
        elif design_type == "waves":
            return self._create_waves_svg(complexity)
        elif design_type == "sunshine":
            return self._create_sunshine_svg(complexity)
        elif design_type == "spiral":
            return self._create_spiral_svg(complexity)
        elif design_type == "open":
            return self._create_open_svg(complexity)
        else:  # balanced
            return self._create_balanced_svg(complexity)

    def _create_mandala_svg(self, complexity):
        """Create a mandala SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="180" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="120" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="20" fill="none" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="20" x2="200" y2="380" stroke="#333" stroke-width="2"/>
                <line x1="20" y1="200" x2="380" y2="200" stroke="#333" stroke-width="2"/>
                <line x1="50" y1="50" x2="350" y2="350" stroke="#333" stroke-width="2"/>
                <line x1="350" y1="50" x2="50" y2="350" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="180" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="150" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="120" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="90" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="30" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="10" fill="none" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="20" x2="200" y2="380" stroke="#333" stroke-width="2"/>
                <line x1="20" y1="200" x2="380" y2="200" stroke="#333" stroke-width="2"/>
                <line x1="50" y1="50" x2="350" y2="350" stroke="#333" stroke-width="2"/>
                <line x1="350" y1="50" x2="50" y2="350" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="50" x2="200" y2="350" stroke="#333" stroke-width="1"/>
                <line x1="50" y1="200" x2="350" y2="200" stroke="#333" stroke-width="1"/>
            </svg>
            """

    def _create_geometric_svg(self, complexity):
        """Create a geometric SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <rect x="50" y="50" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="100" y="100" width="200" height="200" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="150" y="150" width="100" height="100" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="175" y="175" width="50" height="50" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <rect x="50" y="50" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="100" y="100" width="200" height="200" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="150" y="150" width="100" height="100" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="175" y="175" width="50" height="50" fill="none" stroke="#333" stroke-width="2"/>
                <polygon points="200,50 250,100 200,150 150,100" fill="none" stroke="#333" stroke-width="2"/>
                <polygon points="200,250 250,300 200,350 150,300" fill="none" stroke="#333" stroke-width="2"/>
                <polygon points="50,200 100,150 150,200 100,250" fill="none" stroke="#333" stroke-width="2"/>
                <polygon points="250,200 300,150 350,200 300,250" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """

    def _create_nature_svg(self, complexity):
        """Create a nature SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="80" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="40" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="20" fill="none" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="120" x2="200" y2="280" stroke="#333" stroke-width="2"/>
                <line x1="120" y1="200" x2="280" y2="200" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="80" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="40" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="20" fill="none" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="120" x2="200" y2="280" stroke="#333" stroke-width="2"/>
                <line x1="120" y1="200" x2="280" y2="200" stroke="#333" stroke-width="2"/>
                <path d="M 200 120 Q 150 100 200 80 Q 250 100 200 120" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 200 280 Q 150 300 200 320 Q 250 300 200 280" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """

    def _create_waves_svg(self, complexity):
        """Create a waves SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <path d="M 0 200 Q 100 150 200 200 T 400 200" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 0 250 Q 100 200 200 250 T 400 250" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 0 300 Q 100 250 200 300 T 400 300" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <path d="M 0 200 Q 100 150 200 200 T 400 200" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 0 250 Q 100 200 200 250 T 400 250" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 0 300 Q 100 250 200 300 T 400 300" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 0 150 Q 100 100 200 150 T 400 150" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 0 100 Q 100 50 200 100 T 400 100" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """

    def _create_sunshine_svg(self, complexity):
        """Create a sunshine SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="80" x2="200" y2="320" stroke="#333" stroke-width="2"/>
                <line x1="80" y1="200" x2="320" y2="200" stroke="#333" stroke-width="2"/>
                <line x1="120" y1="120" x2="280" y2="280" stroke="#333" stroke-width="2"/>
                <line x1="280" y1="120" x2="120" y2="280" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="80" x2="200" y2="320" stroke="#333" stroke-width="2"/>
                <line x1="80" y1="200" x2="320" y2="200" stroke="#333" stroke-width="2"/>
                <line x1="120" y1="120" x2="280" y2="280" stroke="#333" stroke-width="2"/>
                <line x1="280" y1="120" x2="120" y2="280" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="50" x2="200" y2="350" stroke="#333" stroke-width="1"/>
                <line x1="50" y1="200" x2="350" y2="200" stroke="#333" stroke-width="1"/>
            </svg>
            """

    def _create_spiral_svg(self, complexity):
        """Create a spiral SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <path d="M 200 200 A 50 50 0 0 1 250 200 A 50 50 0 0 1 200 250 A 50 50 0 0 1 150 200 A 50 50 0 0 1 200 150" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <path d="M 200 200 A 50 50 0 0 1 250 200 A 50 50 0 0 1 200 250 A 50 50 0 0 1 150 200 A 50 50 0 0 1 200 150" fill="none" stroke="#333" stroke-width="2"/>
                <path d="M 200 200 A 100 100 0 0 1 300 200 A 100 100 0 0 1 200 300 A 100 100 0 0 1 100 200 A 100 100 0 0 1 200 100" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """

    def _create_open_svg(self, complexity):
        """Create an open SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <rect x="100" y="100" width="200" height="200" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="150" y="150" width="100" height="100" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="175" y="175" width="50" height="50" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <rect x="100" y="100" width="200" height="200" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="150" y="150" width="100" height="100" fill="none" stroke="#333" stroke-width="2"/>
                <rect x="175" y="175" width="50" height="50" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="30" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """

    def _create_balanced_svg(self, complexity):
        """Create a balanced SVG design."""
        if complexity == "simple":
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="80" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="40" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="20" fill="none" stroke="#333" stroke-width="2"/>
            </svg>
            """
        else:  # medium
            return """
            <svg width="400" height="400" viewBox="0 0 400 400">
                <circle cx="200" cy="200" r="80" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="60" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="40" fill="none" stroke="#333" stroke-width="2"/>
                <circle cx="200" cy="200" r="20" fill="none" stroke="#333" stroke-width="2"/>
                <line x1="200" y1="120" x2="200" y2="280" stroke="#333" stroke-width="2"/>
                <line x1="120" y1="200" x2="280" y2="200" stroke="#333" stroke-width="2"/>
            </svg>
            """

coloring_game = ColoringGame()
