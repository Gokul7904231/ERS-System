"""
Mental Health Resources for AI MoodMate
Provides professional mental health resources, crisis support, and counselor contact information
"""

import streamlit as st
from typing import Dict, List

class MentalHealthResources:
    def __init__(self):
        # Crisis resources (available 24/7)
        self.crisis_resources = {
            "suicide_prevention": {
                "name": "National Suicide Prevention Lifeline",
                "phone": "988",
                "text": "Text HOME to 741741",
                "website": "https://suicidepreventionlifeline.org/",
                "description": "Free, confidential support 24/7 for people in distress",
                "available": "24/7",
                "type": "crisis"
            },
            "crisis_text": {
                "name": "Crisis Text Line",
                "phone": "Text HOME to 741741",
                "website": "https://www.crisistextline.org/",
                "description": "Free, 24/7 crisis support via text message",
                "available": "24/7",
                "type": "crisis"
            },
            "samhsa": {
                "name": "SAMHSA National Helpline",
                "phone": "1-800-662-4357",
                "website": "https://www.samhsa.gov/find-help/national-helpline",
                "description": "Free, confidential treatment referral and information service",
                "available": "24/7",
                "type": "crisis"
            }
        }
        
        # Professional counseling resources
        self.counseling_resources = {
            "psychology_today": {
                "name": "Psychology Today Therapist Directory",
                "website": "https://www.psychologytoday.com/us/therapists",
                "description": "Find licensed therapists, psychiatrists, and counselors in your area",
                "features": ["Search by location", "Filter by specialty", "Read therapist profiles", "Contact directly"],
                "type": "professional"
            },
            "betterhelp": {
                "name": "BetterHelp Online Therapy",
                "website": "https://www.betterhelp.com/",
                "description": "Online therapy platform with licensed professional counselors",
                "features": ["Online sessions", "Messaging support", "Flexible scheduling", "Affordable options"],
                "type": "professional"
            },
            "talkspace": {
                "name": "Talkspace Online Therapy",
                "website": "https://www.talkspace.com/",
                "description": "Online therapy and psychiatry services",
                "features": ["Video sessions", "Text therapy", "Psychiatry services", "Insurance accepted"],
                "type": "professional"
            },
            "open_path": {
                "name": "Open Path Psychotherapy Collective",
                "website": "https://openpathcollective.org/",
                "description": "Affordable therapy for individuals and families",
                "features": ["Sliding scale fees", "In-person and online", "Licensed therapists", "No insurance required"],
                "type": "professional"
            }
        }
        
        # Emotion-specific resources
        self.emotion_resources = {
            "sad": {
                "depression_support": {
                    "name": "Depression and Bipolar Support Alliance",
                    "website": "https://www.dbsalliance.org/",
                    "description": "Support groups and resources for depression and bipolar disorder",
                    "type": "support"
                },
                "nami": {
                    "name": "NAMI (National Alliance on Mental Illness)",
                    "website": "https://www.nami.org/",
                    "description": "Mental health advocacy and support resources",
                    "type": "support"
                }
            },
            "angry": {
                "anger_management": {
                    "name": "Anger Management Resources",
                    "website": "https://www.apa.org/topics/anger",
                    "description": "Professional resources for anger management and emotional regulation",
                    "type": "educational"
                },
                "mindfulness": {
                    "name": "Mindfulness-Based Stress Reduction",
                    "website": "https://www.mindfulnesscds.com/",
                    "description": "Evidence-based mindfulness practices for emotional regulation",
                    "type": "educational"
                }
            },
            "fear": {
                "anxiety_disorders": {
                    "name": "Anxiety and Depression Association of America",
                    "website": "https://adaa.org/",
                    "description": "Resources and support for anxiety disorders",
                    "type": "support"
                },
                "anxiety_help": {
                    "name": "Anxiety.org",
                    "website": "https://www.anxiety.org/",
                    "description": "Comprehensive anxiety resources and treatment information",
                    "type": "educational"
                }
            },
            "happy": {
                "positive_psychology": {
                    "name": "Positive Psychology Center",
                    "website": "https://ppc.sas.upenn.edu/",
                    "description": "Research and resources on positive psychology and well-being",
                    "type": "educational"
                },
                "happiness_research": {
                    "name": "Greater Good Science Center",
                    "website": "https://greatergood.berkeley.edu/",
                    "description": "Science-based insights for a meaningful life",
                    "type": "educational"
                }
            }
        }
        
        # Self-help and educational resources
        self.self_help_resources = {
            "mindfulness": {
                "name": "Mindful.org",
                "website": "https://www.mindful.org/",
                "description": "Mindfulness meditation and stress reduction resources",
                "type": "self_help"
            },
            "cbt": {
                "name": "Cognitive Behavioral Therapy Resources",
                "website": "https://www.apa.org/ptsd-guideline/patients-and-families/cognitive-behavioral",
                "description": "Information about CBT and self-help techniques",
                "type": "self_help"
            },
            "meditation": {
                "name": "Headspace",
                "website": "https://www.headspace.com/",
                "description": "Meditation and mindfulness app with free resources",
                "type": "self_help"
            },
            "calm": {
                "name": "Calm",
                "website": "https://www.calm.com/",
                "description": "Meditation, sleep, and relaxation app",
                "type": "self_help"
            }
        }
    
    def get_crisis_resources(self) -> Dict:
        """Get immediate crisis support resources"""
        return self.crisis_resources
    
    def get_counseling_resources(self) -> Dict:
        """Get professional counseling and therapy resources"""
        return self.counseling_resources
    
    def get_emotion_specific_resources(self, emotion: str) -> Dict:
        """Get resources specific to the detected emotion"""
        return self.emotion_resources.get(emotion.lower(), {})
    
    def get_self_help_resources(self) -> Dict:
        """Get self-help and educational resources"""
        return self.self_help_resources
    
    def get_all_resources_for_emotion(self, emotion: str) -> Dict:
        """Get comprehensive resources for a specific emotion"""
        return {
            "crisis": self.get_crisis_resources(),
            "professional": self.get_counseling_resources(),
            "emotion_specific": self.get_emotion_specific_resources(emotion),
            "self_help": self.get_self_help_resources()
        }
    
    def get_priority_resources(self, emotion: str, intensity: int = 5) -> List[Dict]:
        """Get priority resources based on emotion and intensity"""
        priority_list = []
        
        # Always include crisis resources for high intensity negative emotions
        if intensity >= 7 and emotion.lower() in ["sad", "angry", "fear"]:
            priority_list.extend([
                {
                    "resource": self.crisis_resources["suicide_prevention"],
                    "priority": "urgent",
                    "reason": "High intensity negative emotion detected"
                },
                {
                    "resource": self.crisis_resources["crisis_text"],
                    "priority": "urgent",
                    "reason": "Immediate support available"
                }
            ])
        
        # Add professional counseling for moderate to high intensity
        if intensity >= 5:
            priority_list.extend([
                {
                    "resource": self.counseling_resources["psychology_today"],
                    "priority": "high",
                    "reason": "Find local professional help"
                },
                {
                    "resource": self.counseling_resources["betterhelp"],
                    "priority": "high",
                    "reason": "Convenient online therapy"
                }
            ])
        
        # Add emotion-specific resources
        emotion_specific = self.get_emotion_specific_resources(emotion)
        for key, resource in emotion_specific.items():
            priority_list.append({
                "resource": resource,
                "priority": "medium",
                "reason": f"Specific support for {emotion} feelings"
            })
        
        # Add self-help resources for all cases
        priority_list.extend([
            {
                "resource": self.self_help_resources["mindfulness"],
                "priority": "medium",
                "reason": "Evidence-based stress reduction"
            },
            {
                "resource": self.self_help_resources["cbt"],
                "priority": "low",
                "reason": "Self-help techniques"
            }
        ])
        
        return priority_list

# Create global instance
mental_health_resources = MentalHealthResources()
