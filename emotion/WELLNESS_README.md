# 🧠 AI MoodMate - Mental Health & Wellness Companion

## 🌟 Overview

AI MoodMate is a comprehensive mental health and wellness companion that combines advanced emotion detection with personalized wellness support. It's designed to help students and individuals manage their mental health through AI-powered emotion recognition, music therapy, breathing exercises, mood journaling, and AI wellness coaching.

## 🚀 Key Features

### 🎭 Emotion Detection
- **Advanced AI Models**: YOLOv7 for face detection + RepVGG for emotion classification
- **Multiple Input Sources**: Image upload, video upload, and live webcam support
- **Real-time Processing**: Instant emotion detection with confidence scores
- **Comprehensive Emotions**: Detects 8 emotions (happy, sad, anger, fear, surprise, disgust, contempt, neutral)

### 🎵 Music Therapy
- **Personalized Playlists**: Curated music recommendations based on detected emotions
- **YouTube Integration**: In-app music playback with embedded players
- **Emotion-Based Genres**: Music matched to specific emotional states
- **Playlist Management**: Save and manage personalized playlists

### 🧘 Wellness Support

#### Breathing Exercises
- **Emotion-Specific Techniques**: Different breathing patterns for different emotions
- **Interactive Animations**: Visual breathing guides with real-time feedback
- **Stress Relief**: Specialized exercises for sad, angry, fearful, and disgusted emotions
- **Guided Sessions**: Step-by-step breathing instructions

#### Mood Journaling
- **Emotion-Triggered Prompts**: Personalized journaling questions based on detected emotions
- **Mood Tracking**: Track emotional patterns over time
- **Data Export**: Export journal entries for personal records
- **Progress Analytics**: Visualize mood trends and patterns

#### AI Wellness Chatbot
- **Emotional Support**: Conversational AI that responds to detected emotions
- **Crisis Resources**: Automatic crisis support for high-intensity negative emotions
- **Wellness Tips**: Daily tips and coping strategies
- **Personalized Responses**: Context-aware responses based on emotional state

### 📊 Wellness Dashboard
- **Real-time Stats**: Track journal entries and mood patterns
- **Quick Actions**: One-click access to wellness tools
- **Crisis Support**: Always-available emergency resources
- **Daily Tips**: Rotating wellness advice

## 🛠️ Technical Features

### Advanced Emotion Detection
- **Two-Stage Detection**: Face detection followed by emotion classification
- **Confidence Scoring**: Reliable emotion detection with confidence metrics
- **Batch Processing**: Efficient video processing with frame skipping
- **Real-time Analysis**: Live emotion detection capabilities

### Wellness Integration
- **Session State Management**: Persistent wellness data across app sessions
- **Modular Design**: Separate modules for different wellness features
- **Responsive UI**: Mobile-friendly interface with horizontal scrolling
- **Data Privacy**: Local data storage with export options

## 📱 User Experience

### For Students
- **Academic Stress Relief**: Specialized support for exam stress and academic pressure
- **Study Break Reminders**: Smart notifications based on stress levels
- **Focus Music**: Concentration-enhancing playlists
- **Peer Support**: Community features for student mental health

### For General Users
- **Daily Wellness**: Routine mental health check-ins
- **Crisis Support**: Emergency resources and hotlines
- **Personalized Care**: AI-driven wellness recommendations
- **Progress Tracking**: Long-term mental health monitoring

## 🎯 Wellness Features by Emotion

### 😢 Sadness
- **Breathing**: Gentle Calming Breath (4-4-4 pattern)
- **Music**: Indie, Alternative, Folk, Blues, Soul
- **Activities**: Light therapy, social connection
- **Journaling**: Gratitude prompts, self-care planning

### 😠 Anger
- **Breathing**: Cooling Breath (4-7-8 pattern)
- **Music**: Rock, Metal, Punk, Hardcore
- **Activities**: Physical exercise, mindfulness
- **Journaling**: Boundary setting, energy channeling

### 😨 Fear
- **Breathing**: Grounding Breath (5-5-5 pattern)
- **Music**: Ambient, Dark Ambient, Experimental
- **Activities**: Grounding techniques, safety planning
- **Journaling**: Evidence-based reassurance, small steps

### 🤢 Disgust
- **Breathing**: Cleansing Breath (3-6-9 pattern)
- **Music**: Industrial, Noise, Experimental
- **Activities**: Value clarification, distance creation
- **Journaling**: Boundary setting, value alignment

### 😊 Happiness
- **Breathing**: Joyful Breath (natural with gratitude)
- **Music**: Pop, Dance-Pop, Electronic, Indie Pop
- **Activities**: Celebration, sharing joy
- **Journaling**: Memory creation, gratitude expansion

### 😲 Surprise
- **Breathing**: Centering Breath (4-4-4 with awareness)
- **Music**: Experimental, Indie, Alternative
- **Activities**: Opportunity exploration, processing
- **Journaling**: Surprise processing, opportunity identification

### 😐 Neutral
- **Breathing**: Balancing Breath (equal 4-4-4)
- **Music**: Ambient, Chill, Lounge, Instrumental
- **Activities**: Focus planning, balance maintenance
- **Journaling**: Overall assessment, improvement planning

## 🚀 Getting Started

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd YOLO/emotion

# Install dependencies
pip install -r requirements.txt
pip install -r wellness_requirements.txt

# Run the app
streamlit run streamlit_app.py
```

### First Use
1. **Load Models**: Click "🚀 Load Models" in the sidebar
2. **Upload Image/Video**: Choose your input source
3. **Get Wellness Support**: Receive personalized recommendations
4. **Start Journaling**: Begin tracking your mood
5. **Try Breathing Exercises**: Practice stress relief techniques

## 🧠 Mental Health Resources

### Crisis Support
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **National Alliance on Mental Illness**: 1-800-950-NAMI

### Online Resources
- **BetterHelp**: Online therapy platform
- **Talkspace**: Online therapy and psychiatry
- **Headspace**: Meditation and mindfulness app

## 🔬 Scientific Backing

### Evidence-Based Features
- **Breathing Techniques**: Scientifically proven stress reduction methods
- **Music Therapy**: Research-backed emotional regulation through music
- **Mood Tracking**: Clinical psychology principles for emotional monitoring
- **Crisis Intervention**: Evidence-based crisis support protocols

### Research Integration
- **FER2013 Dataset**: Trained on comprehensive facial expression data
- **YOLOv7 Architecture**: State-of-the-art object detection
- **RepVGG Classification**: Efficient emotion classification model
- **Wellness Psychology**: Evidence-based mental health interventions

## 🌟 Future Enhancements

### Planned Features
- **Community Support**: Peer-to-peer mental health support
- **Professional Integration**: Therapist dashboard and progress sharing
- **Advanced Analytics**: Predictive mood analysis and insights
- **Campus Integration**: University mental health service connections
- **Mobile App**: Native mobile application for iOS and Android

### Research Opportunities
- **Longitudinal Studies**: Long-term mental health impact assessment
- **Clinical Trials**: Evidence-based effectiveness studies
- **AI Improvement**: Enhanced emotion detection and wellness recommendations
- **Accessibility**: Inclusive design for diverse user needs

## 🤝 Contributing

We welcome contributions to improve AI MoodMate's mental health support capabilities:

1. **Wellness Features**: New breathing exercises, meditation techniques
2. **Music Therapy**: Expanded playlists and genre recommendations
3. **Crisis Support**: Additional resources and hotlines
4. **Accessibility**: Improved UI/UX for diverse users
5. **Research**: Evidence-based feature validation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Mental Health Professionals**: For guidance on evidence-based practices
- **Open Source Community**: For the amazing AI models and libraries
- **Users**: For feedback and suggestions to improve mental health support
- **Researchers**: For advancing emotion detection and wellness technology

---

**Remember**: AI MoodMate is a supportive tool, not a replacement for professional mental health care. If you're experiencing a mental health crisis, please reach out to qualified professionals immediately.

🧠 **Take care of your mental health - you're worth it!** ✨
