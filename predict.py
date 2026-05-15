"""
Prediction Module for Stress Level
===================================
Loads the trained ANN model and preprocessing objects,
then provides prediction functionality.
"""

import os
import numpy as np
import pickle
from tensorflow.keras.models import load_model

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')

# Global variables for lazy loading
_model = None
_scaler = None
_encoder = None


def _load_artifacts():
    """Load model, scaler, and encoder (lazy loading pattern)."""
    global _model, _scaler, _encoder
    
    if _model is None:
        print("📦 Loading model artifacts...")
        _model = load_model(os.path.join(MODEL_DIR, 'stress_model.keras'))
        
        with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'rb') as f:
            _scaler = pickle.load(f)
        
        with open(os.path.join(MODEL_DIR, 'encoder.pkl'), 'rb') as f:
            _encoder = pickle.load(f)
        
        print("✅ Model artifacts loaded successfully.")


def predict_stress(sleep_hours, screen_time, work_hours,
                   exercise_hours, social_interaction, lifestyle_score):
    """
    Predict stress level from lifestyle parameters.
    
    Args:
        sleep_hours (float): Hours of sleep (3-10)
        screen_time (float): Screen time hours (1-16)
        work_hours (float): Work hours per day (4-14)
        exercise_hours (float): Exercise hours (0-4)
        social_interaction (float): Social score (1-10)
        lifestyle_score (float): Lifestyle score (1-10)
    
    Returns:
        dict: {
            'stress_level': str,        # 'Low Stress' / 'Moderate Stress' / 'High Stress'
            'confidence': float,         # 0.0 - 1.0
            'probabilities': dict,       # Probability for each class
            'risk_color': str            # CSS color class
        }
    """
    _load_artifacts()
    
    # Prepare input features
    features = np.array([[
        sleep_hours, screen_time, work_hours,
        exercise_hours, social_interaction, lifestyle_score
    ]])
    
    # Scale features using the saved scaler
    features_scaled = _scaler.transform(features)
    
    # Make prediction
    prediction = _model.predict(features_scaled, verbose=0)
    
    # Get predicted class and confidence
    predicted_index = np.argmax(prediction[0])
    confidence = float(prediction[0][predicted_index])
    stress_level = _encoder.inverse_transform([predicted_index])[0]
    
    # Build probability dictionary
    probabilities = {}
    for i, class_name in enumerate(_encoder.classes_):
        probabilities[class_name] = round(float(prediction[0][i]) * 100, 1)
    
    # Assign risk color for UI
    color_map = {
        'Low Stress': 'success',
        'Moderate Stress': 'warning',
        'High Stress': 'danger'
    }
    
    return {
        'stress_level': stress_level,
        'confidence': round(confidence * 100, 1),
        'probabilities': probabilities,
        'risk_color': color_map.get(stress_level, 'info')
    }


def get_suggestions(stress_level):
    """
    Generate AI-powered wellness suggestions based on stress level.
    
    Args:
        stress_level (str): Predicted stress level
    
    Returns:
        list: List of suggestion dictionaries with icon and text
    """
    suggestions = {
        'Low Stress': [
            {'icon': 'fa-smile-beam', 'text': 'Great job! Your stress levels are well-managed. Keep maintaining your healthy routine.'},
            {'icon': 'fa-running', 'text': 'Continue your exercise routine — it\'s clearly helping your mental wellness.'},
            {'icon': 'fa-users', 'text': 'Your social interactions are positive. Keep nurturing your relationships.'},
            {'icon': 'fa-book', 'text': 'Consider journaling to track what\'s working well in your lifestyle.'},
            {'icon': 'fa-music', 'text': 'Explore creative hobbies like music or art to maintain joy.'},
        ],
        'Moderate Stress': [
            {'icon': 'fa-bed', 'text': 'Try to improve your sleep schedule — aim for 7-9 hours of quality sleep.'},
            {'icon': 'fa-mobile-alt', 'text': 'Reduce screen time, especially before bed. Try the 20-20-20 rule.'},
            {'icon': 'fa-dumbbell', 'text': 'Increase physical activity — even 30 minutes of walking can reduce stress.'},
            {'icon': 'fa-brain', 'text': 'Practice mindfulness or meditation for 10-15 minutes daily.'},
            {'icon': 'fa-leaf', 'text': 'Take regular breaks during work. Try the Pomodoro technique (25 min work, 5 min break).'},
            {'icon': 'fa-heart', 'text': 'Connect with friends or family — social support is crucial for stress management.'},
        ],
        'High Stress': [
            {'icon': 'fa-exclamation-triangle', 'text': 'Your stress levels are concerning. Consider speaking with a mental health professional.'},
            {'icon': 'fa-bed', 'text': 'Prioritize sleep immediately — poor sleep significantly amplifies stress.'},
            {'icon': 'fa-ban', 'text': 'Drastically reduce screen time. Set device-free zones and times.'},
            {'icon': 'fa-clock', 'text': 'Review your work-life balance. Consider delegation or time management strategies.'},
            {'icon': 'fa-spa', 'text': 'Start deep breathing exercises (4-7-8 technique) multiple times daily.'},
            {'icon': 'fa-phone', 'text': 'Reach out to a trusted friend, family member, or counselor today.'},
            {'icon': 'fa-apple-alt', 'text': 'Improve nutrition — reduce caffeine, sugar, and processed foods.'},
            {'icon': 'fa-walking', 'text': 'Even light exercise like a 15-minute walk can provide immediate relief.'},
        ]
    }
    
    return suggestions.get(stress_level, suggestions['Moderate Stress'])
