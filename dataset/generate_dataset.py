"""
Dataset Generator for Mental Health Stress Prediction
=====================================================
Generates a synthetic mental health dataset with realistic correlations
between lifestyle factors and stress levels.
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)
N = 2000

print("=" * 60)
print("  Mental Health Dataset Generator")
print("=" * 60)
print(f"\nGenerating {N} samples...")

# Generate features with realistic distributions
sleep_hours = np.clip(np.random.normal(6.5, 1.5, N), 3, 10).round(1)
screen_time = np.clip(np.random.normal(7, 3, N), 1, 16).round(1)
work_hours = np.clip(np.random.normal(8, 2, N), 4, 14).round(1)
exercise_hours = np.clip(np.random.exponential(1.0, N), 0, 4).round(1)
social_interaction = np.clip(np.random.normal(5, 2, N), 1, 10).round(1)
lifestyle_score = np.clip(np.random.normal(5.5, 2, N), 1, 10).round(1)


def calculate_stress_score(sleep, screen, work, exercise, social, lifestyle):
    """Calculate raw stress score from features."""
    stress_score = (
        (10 - sleep) * 2.0 +
        screen * 1.5 +
        (work - 4) * 1.8 +
        (4 - exercise) * 2.0 +
        (10 - social) * 1.2 +
        (10 - lifestyle) * 1.5
    )
    stress_score += np.random.normal(0, 3)
    return stress_score


# Calculate all stress scores first
stress_scores = np.array([
    calculate_stress_score(sleep_hours[i], screen_time[i], work_hours[i],
                           exercise_hours[i], social_interaction[i], lifestyle_score[i])
    for i in range(N)
])

# Use percentiles for balanced distribution (~33% each class)
low_threshold = np.percentile(stress_scores, 33)
high_threshold = np.percentile(stress_scores, 66)

stress_levels = []
for s in stress_scores:
    if s < low_threshold:
        stress_levels.append("Low Stress")
    elif s < high_threshold:
        stress_levels.append("Moderate Stress")
    else:
        stress_levels.append("High Stress")

df = pd.DataFrame({
    'sleep_hours': sleep_hours,
    'screen_time': screen_time,
    'work_hours': work_hours,
    'exercise_hours': exercise_hours,
    'social_interaction': social_interaction,
    'lifestyle_score': lifestyle_score,
    'stress_level': stress_levels
})

os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mental_health_data.csv')
df.to_csv(output_path, index=False)

print(f"\nDataset saved to: {output_path}")
print(f"\nDataset Shape: {df.shape}")
print("\nStress Level Distribution:")
for level, count in df['stress_level'].value_counts().items():
    pct = count / len(df) * 100
    print(f"  {level:<20} {count:>4} ({pct:.1f}%)")

print(f"\n{'=' * 60}")
print("  Dataset generation complete!")
print(f"{'=' * 60}")