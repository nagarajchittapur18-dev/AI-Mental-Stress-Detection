"""
ANN Model Training Script for Mental Stress Prediction
=======================================================
Trains a deep neural network and generates evaluation visualizations.
"""

import os, numpy as np, pandas as pd, pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'mental_health_data.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 60)
print("  ANN Model Training — Stress Prediction")
print("=" * 60)

# 1. Load Dataset
print("\n📂 Loading dataset...")
df = pd.read_csv(DATASET_PATH)
print(f"   Shape: {df.shape}")

FEATURES = ['sleep_hours', 'screen_time', 'work_hours',
            'exercise_hours', 'social_interaction', 'lifestyle_score']
X = df[FEATURES].values
y = df['stress_level'].values

# 2. Preprocessing
print("\n⚙️  Preprocessing...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_onehot = to_categorical(y_encoded)
print(f"   Classes: {list(encoder.classes_)}")

# Save preprocessing objects
with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)
with open(os.path.join(MODEL_DIR, 'encoder.pkl'), 'wb') as f:
    pickle.dump(encoder, f)

# 3. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_onehot, test_size=0.2, random_state=42, stratify=y_encoded)
print(f"\n📊 Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

# 4. Build ANN
print("\n🧠 Building ANN...")
model = Sequential([
    Dense(128, activation='relu', input_shape=(6,), kernel_initializer='he_normal', name='dense_1'),
    BatchNormalization(name='bn_1'),
    Dropout(0.3, name='dropout_1'),
    Dense(64, activation='relu', kernel_initializer='he_normal', name='dense_2'),
    BatchNormalization(name='bn_2'),
    Dropout(0.3, name='dropout_2'),
    Dense(32, activation='relu', kernel_initializer='he_normal', name='dense_3'),
    BatchNormalization(name='bn_3'),
    Dropout(0.2, name='dropout_3'),
    Dense(3, activation='softmax', name='output')
], name='StressPredictionANN')

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# 5. Train
callbacks = [
    EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)
]

print("\n🏋️ Training...")
history = model.fit(X_train, y_train, epochs=100, batch_size=32,
                    validation_split=0.2, callbacks=callbacks, verbose=1)

# 6. Evaluate
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\n   Test Accuracy: {test_acc*100:.1f}% | Test Loss: {test_loss:.4f}")

y_pred_classes = np.argmax(model.predict(X_test, verbose=0), axis=1)
y_true_classes = np.argmax(y_test, axis=1)
print(classification_report(y_true_classes, y_pred_classes, target_names=encoder.classes_))

# 7. Save Model
model.save(os.path.join(MODEL_DIR, 'stress_model.keras'))
print("✅ Model saved.")

# 8. Generate Visualizations
print("\n🎨 Generating visualizations...")
plt.style.use('seaborn-v0_8-darkgrid')

# Confusion Matrix
fig, ax = plt.subplots(figsize=(8, 6))
cm = confusion_matrix(y_true_classes, y_pred_classes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=encoder.classes_,
            yticklabels=encoder.classes_, ax=ax, linewidths=0.5, annot_kws={'size': 14})
ax.set_xlabel('Predicted', fontsize=12, fontweight='bold')
ax.set_ylabel('True', fontsize=12, fontweight='bold')
ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, 'confusion_matrix.png'), dpi=150)
plt.close()

# Accuracy Graph
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(history.history['accuracy'], label='Train Accuracy', linewidth=2, color='#667eea')
ax.plot(history.history['val_accuracy'], label='Val Accuracy', linewidth=2, color='#f093fb', linestyle='--')
ax.set_xlabel('Epoch', fontsize=12); ax.set_ylabel('Accuracy', fontsize=12)
ax.set_title('Model Accuracy', fontsize=14, fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, 'accuracy_graph.png'), dpi=150)
plt.close()

# Loss Graph
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(history.history['loss'], label='Train Loss', linewidth=2, color='#f5576c')
ax.plot(history.history['val_loss'], label='Val Loss', linewidth=2, color='#4facfe', linestyle='--')
ax.set_xlabel('Epoch', fontsize=12); ax.set_ylabel('Loss', fontsize=12)
ax.set_title('Model Loss', fontsize=14, fontweight='bold')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, 'loss_graph.png'), dpi=150)
plt.close()

# Stress Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
colors = ['#43e97b', '#f9d423', '#f5576c']
counts = df['stress_level'].value_counts()
axes[0].pie(counts.values, labels=counts.index, autopct='%1.1f%%', colors=colors,
            startangle=90, explode=(0.05, 0.05, 0.05), shadow=True)
axes[0].set_title('Stress Distribution', fontsize=13, fontweight='bold')
sns.countplot(data=df, x='stress_level', ax=axes[1],
              order=['Low Stress', 'Moderate Stress', 'High Stress'],
              palette=colors, edgecolor='black')
axes[1].set_title('Stress Counts', fontsize=13, fontweight='bold')
for p in axes[1].patches:
    axes[1].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2., p.get_height()),
                     ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, 'stress_distribution.png'), dpi=150)
plt.close()

print("\n✅ All visualizations saved to model/ folder.")
print(f"{'=' * 60}")
print(f"  Training Complete! Accuracy: {test_acc*100:.1f}%")
print(f"{'=' * 60}")
