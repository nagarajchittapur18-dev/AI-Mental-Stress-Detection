"""
Database Module for Mental Wellness Platform
=============================================
Handles SQLite database setup, user authentication models,
and stress history management using Flask-SQLAlchemy.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User model for authentication and profile management.
    
    Attributes:
        id: Primary key
        username: Unique username
        email: Unique email address
        password_hash: Hashed password (never store plain text)
        created_at: Account creation timestamp
        stress_records: Relationship to StressHistory
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to stress history
    stress_records = db.relationship(
        'StressHistory', backref='user', lazy=True,
        order_by='StressHistory.created_at.desc()'
    )
    
    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class StressHistory(db.Model):
    """
    Stress prediction history model.
    
    Stores each prediction's input features, results,
    and metadata for analytics and trend tracking.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        sleep_hours: Input feature
        screen_time: Input feature
        work_hours: Input feature
        exercise_hours: Input feature
        social_interaction: Input feature
        lifestyle_score: Input feature
        stress_level: Predicted stress level
        confidence: Model confidence score
        created_at: Prediction timestamp
    """
    __tablename__ = 'stress_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Input features
    sleep_hours = db.Column(db.Float, nullable=False)
    screen_time = db.Column(db.Float, nullable=False)
    work_hours = db.Column(db.Float, nullable=False)
    exercise_hours = db.Column(db.Float, nullable=False)
    social_interaction = db.Column(db.Float, nullable=False)
    lifestyle_score = db.Column(db.Float, nullable=False)
    
    # Prediction results
    stress_level = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert record to dictionary for API responses."""
        return {
            'id': self.id,
            'sleep_hours': self.sleep_hours,
            'screen_time': self.screen_time,
            'work_hours': self.work_hours,
            'exercise_hours': self.exercise_hours,
            'social_interaction': self.social_interaction,
            'lifestyle_score': self.lifestyle_score,
            'stress_level': self.stress_level,
            'confidence': round(self.confidence, 2),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }
    
    def __repr__(self):
        return f'<StressHistory {self.stress_level} ({self.confidence:.0%})>'


def init_db(app):
    """
    Initialize the database with the Flask app.
    Creates all tables if they don't exist.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully.")
