import streamlit as st
import random
from datetime import datetime

class WellnessChatbot:
    def __init__(self):
        self.conversation_history = []
        self.emotion_responses = {
            "sad": [
                "I can see you're feeling sad. It's okay to feel this way. Would you like to talk about what's on your mind?",
                "Sadness is a natural emotion. Sometimes it helps to acknowledge what we're feeling. How can I support you right now?",
                "I'm here for you. Sometimes talking about our feelings can help us process them better. What would you like to share?",
                "It's brave to acknowledge when we're feeling down. Remember, this feeling won't last forever. What's one small thing that might help you feel a bit better?"
            ],
            "anger": [
                "I can sense you're feeling angry. Anger is a valid emotion, and it's important to express it healthily. What's making you feel this way?",
                "Anger often comes from feeling hurt or frustrated. It's okay to feel this way. How can we work through this together?",
                "I understand you're feeling angry. Sometimes anger is a signal that something needs to change. What would you like to do about it?",
                "Anger can be overwhelming. Let's take a moment to breathe together. What's the root of what you're feeling?"
            ],
            "fear": [
                "I can see you're feeling afraid. Fear is a natural response, and it's okay to feel scared. What's making you feel this way?",
                "Fear can be overwhelming, but you're safe here. What would help you feel more secure right now?",
                "It's normal to feel fear sometimes. You're not alone in this. What's one thing that might help you feel calmer?",
                "Fear is trying to protect you, but sometimes it can be too much. What would you like to do to feel safer?"
            ],
            "disgust": [
                "I can sense you're feeling disgusted. This emotion often comes from something that doesn't align with your values. What's bothering you?",
                "Disgust is a strong emotion that can help us set boundaries. What's making you feel this way?",
                "It's okay to feel disgusted. Sometimes this emotion helps us protect ourselves. What would help you feel better?",
                "Disgust can be a signal that something needs to change. What would you like to do about this feeling?"
            ],
            "happy": [
                "I can see you're feeling happy! That's wonderful. What's bringing you joy right now?",
                "Happiness is such a beautiful emotion. How can we celebrate this feeling together?",
                "I love seeing you happy! What's making you feel this way?",
                "Your happiness is contagious! What would you like to do to keep this positive energy going?"
            ],
            "surprise": [
                "I can see you're feeling surprised! Surprise can be exciting or overwhelming. How are you processing this?",
                "Surprise can bring new opportunities. What's your reaction to whatever surprised you?",
                "Sometimes surprise can be a good thing! How are you feeling about whatever happened?",
                "Surprise can be unexpected, but it can also be a chance for growth. What would you like to do with this feeling?"
            ],
            "contempt": [
                "I can sense you're feeling contempt. This emotion often comes from judgment or disappointment. What's making you feel this way?",
                "Contempt can be a strong emotion. It's okay to feel this way, but let's explore what's behind it. What's bothering you?",
                "I understand you're feeling contempt. Sometimes this emotion helps us set boundaries. What would help you feel better?",
                "Contempt can be a signal that something needs to change. What would you like to do about this feeling?"
            ],
            "neutral": [
                "I can see you're feeling neutral. Sometimes a calm, balanced state is exactly what we need. How are you doing overall?",
                "Neutral feelings can be peaceful. What's on your mind today?",
                "A neutral mood can be a good foundation. What would you like to focus on?",
                "Sometimes neutral is just right. How can I support you today?"
            ]
        }
        
        self.supportive_responses = [
            "I'm here for you. You're not alone in this.",
            "It takes courage to acknowledge your feelings. I'm proud of you.",
            "Your feelings are valid, and it's okay to feel this way.",
            "I believe in your strength to get through this.",
            "You're doing the best you can, and that's enough.",
            "It's okay to not be okay sometimes. I'm here to support you.",
            "You're stronger than you think, even when you don't feel it.",
            "Taking care of your mental health is important. You're doing great."
        ]
        
        self.coping_strategies = [
            "Take deep breaths and focus on your breathing",
            "Try the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
            "Practice self-compassion - treat yourself like you would a good friend",
            "Engage in a calming activity like reading, drawing, or listening to music",
            "Reach out to someone you trust for support",
            "Write down your thoughts and feelings in a journal",
            "Take a walk or get some fresh air",
            "Practice mindfulness or meditation"
        ]

    def get_initial_response(self, emotion, confidence):
        """Get the initial response based on detected emotion."""
        if emotion in self.emotion_responses:
            responses = self.emotion_responses[emotion]
            return random.choice(responses)
        return "I can see you're feeling something. How can I help you today?"

    def get_supportive_response(self):
        """Get a supportive response."""
        return random.choice(self.supportive_responses)

    def get_coping_strategy(self):
        """Get a random coping strategy."""
        return random.choice(self.coping_strategies)

    def get_crisis_response(self):
        """Get a crisis response with resources."""
        return {
            "message": "I'm concerned about you. If you're having thoughts of self-harm, please reach out for help immediately.",
            "resources": [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "Emergency Services: 911"
            ]
        }

    def get_wellness_tip(self, emotion):
        """Get a wellness tip based on emotion."""
        tips = {
            "sad": "Remember that sadness is temporary. Try to engage in activities that bring you comfort and joy.",
            "anger": "Anger is energy. Try channeling it into physical activity or creative expression.",
            "fear": "Fear is trying to protect you. Take small steps to face what you're afraid of.",
            "disgust": "Disgust can help you set healthy boundaries. Use it to protect your values.",
            "happy": "Share your happiness with others! Joy multiplies when shared.",
            "surprise": "Embrace the unexpected. Sometimes the best things come from surprises.",
            "contempt": "Try to understand what's behind your contempt. It might be protecting you from something.",
            "neutral": "Neutral feelings can be a good foundation for making decisions."
        }
        return tips.get(emotion, "Take care of yourself today. You're doing great.")

    def add_to_conversation(self, user_message, bot_response):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "user": user_message,
            "bot": bot_response
        })

    def get_conversation_summary(self):
        """Get a summary of the conversation."""
        if not self.conversation_history:
            return "No conversation yet."
        
        return f"You've had {len(self.conversation_history)} exchanges with your wellness companion today."

wellness_chatbot = WellnessChatbot()
