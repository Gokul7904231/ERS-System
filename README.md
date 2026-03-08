---
title: Mood Driven Personalized Recommendation System
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
---

# 🧠 Mood Driven Personalized Recommendation System

A comprehensive mental health and wellness companion that combines advanced emotion detection with personalized wellness support through AI-powered emotion recognition, music therapy, breathing exercises, mood journaling, and AI wellness coaching.

## 🌟 Features

### 🎭 Emotion Detection
- **Advanced AI Models**: YOLOv7 for face detection + FER2013 CNN for emotion classification
- **Multiple Input Sources**: Image upload, video upload, and live webcam support
- **Real-time Processing**: Instant emotion detection with confidence scores
- **8 Emotions**: happy, sad, anger, fear, surprise, disgust, contempt, neutral

### 🎵 Music Therapy
- **Personalized Playlists**: Curated music recommendations based on detected emotions
- **YouTube Integration**: In-app music playback
- **Emotion-Based Genres**: Music matched to specific emotional states

### 🧘 Wellness Support
- **Breathing Exercises**: Interactive animations with emotion-specific techniques
- **Mood Journaling**: Track emotional patterns over time
- **Coloring Game**: Therapeutic digital coloring experience
- **AI Wellness Chatbot**: Conversational AI for emotional support

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📋 Requirements

- Python 3.10+
- Streamlit
- PyTorch
- OpenCV

## 🔧 Configuration

The app uses Streamlit configuration in `.streamlit/config.toml` for optimal deployment on Hugging Face Spaces.

## 📁 Project Structure

```
ers-system/
├── app.py                  # Main entry point
├── requirements.txt        # Dependencies
├── runtime.txt            # Python runtime
├── .streamlit/            # Streamlit config
├── models/weights/        # AI models
└── src/                  # Source code
    ├── core/             # ML modules
    ├── features/         # Recommendations
    ├── ui/               # UI components
    └── ers/              # Emotion Response System
```

## ⚠️ Note

For the AI chatbot to work, set the `GEMINI_API_KEY` environment variable. Without it, the chatbot will use rule-based responses.

---
Built with ❤️ for mental wellness

