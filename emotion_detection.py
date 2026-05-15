"""
Emotion Detection Module
=========================
Detects facial emotions from uploaded images using DeepFace and OpenCV.
"""

import os
import cv2
import numpy as np
from PIL import Image


def detect_emotion(image_path):
    """
    Detect dominant emotion from a face in the given image.
    
    Uses DeepFace for emotion analysis and OpenCV for face detection.
    
    Args:
        image_path (str): Path to the uploaded image file
    
    Returns:
        dict: {
            'success': bool,
            'dominant_emotion': str,       # e.g., 'happy', 'sad', 'neutral'
            'emotions': dict,              # All emotion scores
            'emoji': str,                  # Corresponding emoji
            'message': str,                # Human-readable message
            'face_detected': bool
        }
    """
    try:
        # Import DeepFace here to avoid slow startup
        from deepface import DeepFace
        
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            return {
                'success': False,
                'message': 'Could not read the image. Please upload a valid image file.',
                'face_detected': False
            }
        
        # Analyze emotion using DeepFace
        results = DeepFace.analyze(
            img_path=image_path,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv'
        )
        
        # DeepFace returns a list; take the first result
        if isinstance(results, list):
            result = results[0]
        else:
            result = results
        
        # Extract emotion data
        emotions = result.get('emotion', {})
        dominant = result.get('dominant_emotion', 'unknown')
        
        # Round emotion percentages
        emotions_rounded = {k: round(v, 1) for k, v in emotions.items()}
        
        # Map emotions to emojis
        emoji_map = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'surprise': '😲',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐'
        }
        
        # Map emotions to wellness messages
        message_map = {
            'happy': 'You appear to be in a positive emotional state. Keep spreading the joy!',
            'sad': 'You seem to be feeling down. Consider talking to someone you trust or taking a relaxing break.',
            'angry': 'Signs of frustration detected. Deep breathing exercises can help manage anger.',
            'surprise': 'You appear surprised! Embrace the unexpected moments in life.',
            'fear': 'Anxiety indicators detected. Grounding techniques (5-4-3-2-1) can help you feel calmer.',
            'disgust': 'Negative emotion detected. Try to shift your focus to something positive.',
            'neutral': 'Your expression appears neutral and calm. A balanced emotional state is healthy.'
        }
        
        return {
            'success': True,
            'dominant_emotion': dominant,
            'emotions': emotions_rounded,
            'emoji': emoji_map.get(dominant, '🤔'),
            'message': message_map.get(dominant, 'Emotion analysis complete.'),
            'face_detected': True
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Emotion detection failed: {str(e)}. Please ensure a clear face is visible in the image.',
            'face_detected': False
        }
