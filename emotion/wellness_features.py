import streamlit as st
import time
import random
from datetime import datetime, timedelta
import json

class WellnessFeatures:
    def __init__(self):
        self.emotion_to_wellness = {
            "sad": {
                "breathing_exercise": "Gentle Calming Breath",
                "technique": "4-4-4 breathing (inhale 4, hold 4, exhale 4)",
                "duration": 5,
                "description": "A gentle breathing pattern to help ease sadness and bring calmness.",
                "color": "#4A90E2",
                "reference": "Benson, H. (1975). The Relaxation Response. Harvard Medical School.",
                "research": "Proven effective for stress reduction and emotional regulation in clinical studies."
            },
            "anger": {
                "breathing_exercise": "Cooling Breath",
                "technique": "4-7-8 breathing (inhale 4, hold 7, exhale 8)",
                "duration": 7,
                "description": "A cooling breath technique to help manage anger and frustration.",
                "color": "#E74C3C",
                "reference": "Weil, A. (1999). Breathing: The Master Key to Self Healing. Based on ancient yogic pranayama.",
                "research": "Clinical studies show effectiveness for anxiety, insomnia, and emotional regulation."
            },
            "fear": {
                "breathing_exercise": "Grounding Breath",
                "technique": "5-5-5 breathing (inhale 5, hold 5, exhale 5)",
                "duration": 6,
                "description": "A grounding technique to help calm fear and anxiety.",
                "color": "#8E44AD",
                "reference": "Brown, R. & Gerbarg, P. (2012). The Healing Power of Breath. Columbia University research.",
                "research": "Used in Mindfulness-Based Stress Reduction (MBSR) programs worldwide."
            },
            "disgust": {
                "breathing_exercise": "Cleansing Breath",
                "technique": "3-6-9 breathing (inhale 3, hold 6, exhale 9)",
                "duration": 8,
                "description": "A cleansing breath pattern to help release negative feelings.",
                "color": "#27AE60",
                "reference": "Nestor, J. (2020). Breath: The New Science of a Lost Art. Stanford University studies.",
                "research": "Extended exhale activates vagal nerve, proven effective for panic disorders and PTSD."
            },
            "happy": {
                "breathing_exercise": "Joyful Breath",
                "technique": "Natural breathing with gratitude",
                "duration": 3,
                "description": "A light breathing pattern to enhance your happiness.",
                "color": "#F39C12",
                "reference": "Fredrickson, B. (2009). Positivity. University of North Carolina research on positive emotions.",
                "research": "Gratitude breathing enhances positive emotions and overall well-being."
            },
            "surprise": {
                "breathing_exercise": "Centering Breath",
                "technique": "4-4-4 breathing with awareness",
                "duration": 4,
                "description": "A centering breath to help process surprise and stay grounded.",
                "color": "#E67E22",
                "reference": "Kabat-Zinn, J. (1990). Full Catastrophe Living. MBSR program, University of Massachusetts.",
                "research": "Mindful breathing helps process unexpected emotions and maintain equilibrium."
            },
            "contempt": {
                "breathing_exercise": "Releasing Breath",
                "technique": "4-6-8 breathing (inhale 4, hold 6, exhale 8)",
                "duration": 6,
                "description": "A releasing breath to help let go of contempt and judgment.",
                "color": "#95A5A6",
                "reference": "Siegel, D. (2010). Mindsight: The New Science of Personal Transformation. UCLA research.",
                "research": "Extended exhale helps release judgmental thoughts and promotes compassion."
            },
            "neutral": {
                "breathing_exercise": "Balancing Breath",
                "technique": "Equal breathing (4-4-4)",
                "duration": 5,
                "description": "A balancing breath to maintain emotional equilibrium.",
                "color": "#7F8C8D",
                "reference": "Benson, H. (1975). The Relaxation Response. Harvard Medical School.",
                "research": "Equal breathing maintains autonomic nervous system balance and emotional stability."
            }
        }
        
        self.mood_journal_prompts = {
            "sad": [
                "What's making you feel sad today?",
                "What would help you feel better right now?",
                "What are you grateful for despite feeling sad?",
                "What self-care activity would you like to do?"
            ],
            "anger": [
                "What triggered your anger today?",
                "How can you channel this energy positively?",
                "What boundaries do you need to set?",
                "What would help you feel calmer?"
            ],
            "fear": [
                "What are you afraid of right now?",
                "What evidence do you have that you can handle this?",
                "What would you tell a friend in this situation?",
                "What small step can you take to feel safer?"
            ],
            "disgust": [
                "What's causing you to feel disgusted?",
                "How can you distance yourself from this?",
                "What values are important to you right now?",
                "What would help you feel cleaner or refreshed?"
            ],
            "happy": [
                "What's making you feel happy today?",
                "How can you share this joy with others?",
                "What would you like to do to celebrate?",
                "What memories are you creating right now?"
            ],
            "surprise": [
                "What surprised you today?",
                "How are you processing this surprise?",
                "What opportunities might this bring?",
                "What would you like to explore further?"
            ],
            "contempt": [
                "What's causing you to feel contempt?",
                "How can you practice compassion instead?",
                "What would help you feel more understanding?",
                "What boundaries do you need to maintain?"
            ],
            "neutral": [
                "How are you feeling overall today?",
                "What would you like to focus on?",
                "What's going well in your life?",
                "What would you like to improve?"
            ]
        }

    def get_breathing_exercise(self, emotion):
        """Returns breathing exercise details for a specific emotion."""
        if emotion in self.emotion_to_wellness:
            return self.emotion_to_wellness[emotion]
        return self.emotion_to_wellness["neutral"]

    def get_mood_journal_prompts(self, emotion):
        """Returns mood journaling prompts for a specific emotion."""
        if emotion in self.mood_journal_prompts:
            return self.mood_journal_prompts[emotion]
        return self.mood_journal_prompts["neutral"]

    def get_wellness_recommendations(self, emotion, confidence):
        """Returns comprehensive wellness recommendations based on emotion and confidence."""
        recommendations = []
        
        # Breathing exercises for stress-related emotions
        if emotion in ["sad", "anger", "angry", "fear", "disgust"]:
            recommendations.append({
                "type": "breathing",
                "title": "🧘 Breathing Exercise",
                "description": f"Try {self.emotion_to_wellness.get(emotion, self.emotion_to_wellness.get('anger', {}).get('breathing_exercise', 'Calming Breath'))} to help manage your {emotion} feelings.",
                "priority": "high" if confidence > 70 else "medium"
            })
        
        # Mood journaling for all emotions
        recommendations.append({
            "type": "journaling",
            "title": "📝 Mood Journaling",
            "description": f"Reflect on your {emotion} feelings with guided prompts.",
            "priority": "medium"
        })
        
        # Music therapy for all emotions
        recommendations.append({
            "type": "music",
            "title": "🎵 Music Therapy",
            "description": f"Listen to music that matches your {emotion} mood for emotional support.",
            "priority": "high"
        })
        
        # Additional recommendations based on emotion
        if emotion == "sad":
            recommendations.extend([
                {
                    "type": "activity",
                    "title": "🌅 Light Therapy",
                    "description": "Spend time in natural light or use a light therapy lamp.",
                    "priority": "medium"
                },
                {
                    "type": "social",
                    "title": "👥 Social Connection",
                    "description": "Reach out to a friend or family member for support.",
                    "priority": "high"
                }
            ])
        elif emotion == "anger" or emotion == "angry":
            recommendations.extend([
                {
                    "type": "physical",
                    "title": "🏃 Physical Activity",
                    "description": "Engage in physical exercise to release tension.",
                    "priority": "high"
                },
                {
                    "type": "mindfulness",
                    "title": "🧘 Mindfulness",
                    "description": "Practice mindfulness to stay present and calm.",
                    "priority": "medium"
                }
            ])
        elif emotion == "fear":
            recommendations.extend([
                {
                    "type": "grounding",
                    "title": "🌍 Grounding Techniques",
                    "description": "Use 5-4-3-2-1 grounding technique to feel more secure.",
                    "priority": "high"
                },
                {
                    "type": "safety",
                    "title": "🛡️ Safety Planning",
                    "description": "Create a safety plan for managing anxiety.",
                    "priority": "medium"
                }
            ])
        
        return recommendations

    def get_crisis_resources(self):
        """Returns crisis resources for users in distress."""
        return {
            "hotlines": [
                {"name": "National Suicide Prevention Lifeline", "number": "988", "available": "24/7"},
                {"name": "Crisis Text Line", "number": "Text HOME to 741741", "available": "24/7"},
                {"name": "National Alliance on Mental Illness", "number": "1-800-950-NAMI", "available": "Mon-Fri 10am-6pm"}
            ],
            "online_resources": [
                {"name": "BetterHelp", "url": "https://www.betterhelp.com", "description": "Online therapy platform"},
                {"name": "Talkspace", "url": "https://www.talkspace.com", "description": "Online therapy and psychiatry"},
                {"name": "Headspace", "url": "https://www.headspace.com", "description": "Meditation and mindfulness app"}
            ]
        }

wellness_features = WellnessFeatures()
