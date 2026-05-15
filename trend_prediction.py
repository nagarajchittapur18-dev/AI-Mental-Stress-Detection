"""
Stress Trend Prediction Module
===============================
Analyzes user's stress history to predict future stress trajectory.
"""


def predict_trend(stress_records):
    """
    Analyze recent stress history and predict future trend.
    
    Uses a weighted moving average of recent predictions to determine
    whether the user's stress is improving, stable, or worsening.
    
    Args:
        stress_records: List of StressHistory objects (most recent first)
    
    Returns:
        dict: {
            'trend': str,           # 'Improving' / 'Stable' / 'Worsening'
            'trend_icon': str,      # Font Awesome icon class
            'trend_color': str,     # CSS color class
            'message': str,         # Human-readable trend message
            'data_points': int      # Number of records analyzed
        }
    """
    if len(stress_records) < 2:
        return {
            'trend': 'Insufficient Data',
            'trend_icon': 'fa-question-circle',
            'trend_color': 'secondary',
            'message': 'Need at least 2 predictions to analyze trends. Keep using the platform!',
            'data_points': len(stress_records)
        }
    
    # Map stress levels to numeric scores
    stress_map = {
        'Low Stress': 1,
        'Moderate Stress': 2,
        'High Stress': 3
    }
    
    # Get numeric scores (most recent first)
    scores = [stress_map.get(r.stress_level, 2) for r in stress_records[:10]]
    
    # Calculate weighted averages for recent vs older periods
    # Recent = first half, Older = second half
    mid = len(scores) // 2
    if mid == 0:
        mid = 1
    
    recent_avg = sum(scores[:mid]) / mid
    older_avg = sum(scores[mid:]) / (len(scores) - mid)
    
    # Determine trend based on difference
    diff = recent_avg - older_avg
    
    if diff < -0.3:
        return {
            'trend': 'Improving',
            'trend_icon': 'fa-arrow-down',
            'trend_color': 'success',
            'message': 'Your stress levels are decreasing. Great progress! Keep up your healthy habits.',
            'data_points': len(scores)
        }
    elif diff > 0.3:
        return {
            'trend': 'Worsening',
            'trend_icon': 'fa-arrow-up',
            'trend_color': 'danger',
            'message': 'Your stress levels are increasing. Consider reviewing your lifestyle habits and seeking support.',
            'data_points': len(scores)
        }
    else:
        return {
            'trend': 'Stable',
            'trend_icon': 'fa-minus',
            'trend_color': 'info',
            'message': 'Your stress levels are relatively stable. Continue monitoring and maintaining balance.',
            'data_points': len(scores)
        }


def get_trend_data(stress_records, limit=20):
    """
    Prepare stress history data for Chart.js visualization.
    
    Args:
        stress_records: List of StressHistory objects (most recent first)
        limit: Maximum number of data points
    
    Returns:
        dict: Chart.js compatible data structure
    """
    records = list(reversed(stress_records[:limit]))
    
    stress_map = {'Low Stress': 1, 'Moderate Stress': 2, 'High Stress': 3}
    
    labels = [r.created_at.strftime('%b %d') for r in records]
    values = [stress_map.get(r.stress_level, 2) for r in records]
    confidences = [round(r.confidence, 1) for r in records]
    
    return {
        'labels': labels,
        'stress_values': values,
        'confidences': confidences
    }
