# 🧠 AI-Powered Smart Mental Wellness & Stress Prediction Platform

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10-orange?logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-yellow)

> An advanced deep learning-based web application for predicting mental stress levels, detecting emotions from facial images, and providing personalized wellness recommendations.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Model Architecture](#-model-architecture)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔮 **Stress Prediction** | ANN-based prediction using 6 lifestyle parameters |
| 😊 **Emotion Detection** | Real-time facial emotion recognition using DeepFace |
| 📊 **Analytics Dashboard** | Interactive charts with stress history and trends |
| 📈 **Trend Prediction** | Forecast future stress trajectory |
| 🔐 **User Authentication** | Secure login/register with password hashing |
| 💡 **AI Recommendations** | Personalized wellness suggestions |
| 📱 **Responsive Design** | Mobile-first glassmorphism UI |
| 🗄️ **Data Persistence** | SQLite database for user data and history |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10** — Core programming language
- **Flask 3.0** — Web framework
- **Flask-Login** — User session management
- **Flask-SQLAlchemy** — ORM for database
- **SQLite** — Lightweight database

### Machine Learning
- **TensorFlow 2.10** — Deep learning framework
- **Keras** — High-level neural network API
- **Scikit-learn** — Data preprocessing & evaluation
- **DeepFace** — Facial emotion recognition
- **OpenCV** — Image processing

### Frontend
- **Bootstrap 5.3** — Responsive UI framework
- **Chart.js 4** — Interactive data visualization
- **Font Awesome 6** — Icon library
- **Custom CSS** — Glassmorphism & animations

---

## 📁 Project Structure

```
AI-Mental-stress-detection-/
│
├── dataset/
│   ├── generate_dataset.py      # Synthetic dataset generator
│   └── mental_health_data.csv   # Generated training data
│
├── model/
│   ├── stress_model.keras       # Trained ANN model
│   ├── scaler.pkl               # Feature scaler
│   ├── encoder.pkl              # Label encoder
│   ├── confusion_matrix.png     # Model evaluation
│   ├── accuracy_graph.png       # Training accuracy plot
│   ├── loss_graph.png           # Training loss plot
│   └── stress_distribution.png  # Data distribution plot
│
├── static/
│   ├── css/
│   │   └── style.css            # Custom styles
│   └── js/
│       └── main.js              # Frontend logic
│
├── templates/
│   ├── base.html                # Base template
│   ├── index.html               # Landing page
│   ├── login.html               # Login page
│   ├── register.html            # Registration page
│   ├── dashboard.html           # Analytics dashboard
│   ├── predict.html             # Stress prediction form
│   ├── result.html              # Prediction results
│   ├── emotion.html             # Emotion detection
│   └── history.html             # Stress history
│
├── app.py                       # Flask application
├── predict.py                   # Prediction module
├── train_model.py               # Model training script
├── database.py                  # Database models & setup
├── trend_prediction.py          # Stress trend analysis
├── emotion_detection.py         # Emotion recognition
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
└── .gitignore                   # Git ignore rules
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step-by-Step Instructions

**1. Clone the Repository**
```bash
git clone https://github.com/yourusername/AI-Mental-stress-detection-.git
cd AI-Mental-stress-detection-
```

**2. Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Generate Dataset**
```bash
python dataset/generate_dataset.py
```

**5. Train the ANN Model**
```bash
python train_model.py
```
This will create the trained model and visualizations in the `model/` folder.

**6. Run the Application**
```bash
python app.py
```

**7. Open in Browser**
```
http://127.0.0.1:5000
```

---

## 📖 Usage

1. **Register** — Create a new account
2. **Login** — Access your dashboard
3. **Predict Stress** — Enter lifestyle parameters to get AI-powered stress prediction
4. **View Results** — See stress level, confidence score, and personalized recommendations
5. **Emotion Detection** — Upload a face image to detect emotions
6. **Dashboard** — View stress history, trends, and analytics
7. **History** — Browse all past predictions

---

## 🧬 Model Architecture

```
Input Layer (6 features)
    │
Dense(128, ReLU) + BatchNormalization + Dropout(0.3)
    │
Dense(64, ReLU) + BatchNormalization + Dropout(0.3)
    │
Dense(32, ReLU) + BatchNormalization + Dropout(0.2)
    │
Dense(3, Softmax) → Output (Low / Moderate / High Stress)
```

### Training Parameters
- **Optimizer**: Adam (lr=0.001)
- **Loss**: Categorical Crossentropy
- **Epochs**: 100
- **Batch Size**: 32
- **Validation Split**: 20%
- **Early Stopping**: patience=10

---

## 📸 Screenshots

> Screenshots will be added after running the application.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**MCA Final Year Project**

---

<p align="center">
  Made with ❤️ using Python, TensorFlow & Flask
</p>
