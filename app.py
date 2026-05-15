"""
AI-Powered Smart Mental Wellness & Stress Prediction Platform
==============================================================
Main Flask Application

Routes:
    /               - Landing page
    /login          - User login
    /register       - User registration
    /logout         - User logout
    /dashboard      - Analytics dashboard
    /predict        - Stress prediction form
    /result         - Prediction results
    /emotion        - Emotion detection
    /history        - Stress history
    /api/stress-data - JSON API for Chart.js
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime

from database import db, User, StressHistory, init_db
from predict import predict_stress, get_suggestions
from trend_prediction import predict_trend, get_trend_data
from emotion_detection import detect_emotion

# ─────────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────────

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mental-wellness-secret-key-2024-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_wellness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
init_db(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login session management."""
    return db.session.get(User, int(user_id))


# ─────────────────────────────────────────────
# Allowed file extensions for image upload
# ─────────────────────────────────────────────

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ═══════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════


# ─────────────────────────────────────────────
# Landing Page
# ─────────────────────────────────────────────

@app.route('/')
def index():
    """Render the landing page."""
    return render_template('index.html')


# ─────────────────────────────────────────────
# Authentication Routes
# ─────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ─────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    """Render the analytics dashboard."""
    records = StressHistory.query.filter_by(user_id=current_user.id)\
        .order_by(StressHistory.created_at.desc()).all()
    
    # Calculate statistics
    total_predictions = len(records)
    
    if total_predictions > 0:
        avg_confidence = sum(r.confidence for r in records) / total_predictions
        
        # Stress distribution counts
        low_count = sum(1 for r in records if r.stress_level == 'Low Stress')
        mod_count = sum(1 for r in records if r.stress_level == 'Moderate Stress')
        high_count = sum(1 for r in records if r.stress_level == 'High Stress')
        
        # Most common stress level
        counts = {'Low Stress': low_count, 'Moderate Stress': mod_count, 'High Stress': high_count}
        dominant_stress = max(counts, key=counts.get)
    else:
        avg_confidence = 0
        low_count = mod_count = high_count = 0
        dominant_stress = 'N/A'
    
    # Trend prediction
    trend = predict_trend(records)
    
    # Chart data
    chart_data = get_trend_data(records)
    
    return render_template('dashboard.html',
        total_predictions=total_predictions,
        avg_confidence=round(avg_confidence, 1),
        low_count=low_count,
        mod_count=mod_count,
        high_count=high_count,
        dominant_stress=dominant_stress,
        trend=trend,
        chart_data=chart_data,
        recent_records=records[:5]
    )


# ─────────────────────────────────────────────
# Stress Prediction
# ─────────────────────────────────────────────

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Handle stress prediction form and results."""
    if request.method == 'POST':
        try:
            # Extract form data
            sleep_hours = float(request.form.get('sleep_hours', 7))
            screen_time = float(request.form.get('screen_time', 5))
            work_hours = float(request.form.get('work_hours', 8))
            exercise_hours = float(request.form.get('exercise_hours', 1))
            social_interaction = float(request.form.get('social_interaction', 5))
            lifestyle_score = float(request.form.get('lifestyle_score', 5))
            
            # Make prediction
            result = predict_stress(
                sleep_hours, screen_time, work_hours,
                exercise_hours, social_interaction, lifestyle_score
            )
            
            # Get AI suggestions
            suggestions = get_suggestions(result['stress_level'])
            
            # Save to database
            record = StressHistory(
                user_id=current_user.id,
                sleep_hours=sleep_hours,
                screen_time=screen_time,
                work_hours=work_hours,
                exercise_hours=exercise_hours,
                social_interaction=social_interaction,
                lifestyle_score=lifestyle_score,
                stress_level=result['stress_level'],
                confidence=result['confidence']
            )
            db.session.add(record)
            db.session.commit()
            
            # Store result in session for result page
            session['prediction_result'] = result
            session['prediction_suggestions'] = suggestions
            session['prediction_inputs'] = {
                'sleep_hours': sleep_hours,
                'screen_time': screen_time,
                'work_hours': work_hours,
                'exercise_hours': exercise_hours,
                'social_interaction': social_interaction,
                'lifestyle_score': lifestyle_score
            }
            
            return redirect(url_for('result'))
            
        except Exception as e:
            flash(f'Prediction error: {str(e)}', 'danger')
            return render_template('predict.html')
    
    return render_template('predict.html')


@app.route('/result')
@login_required
def result():
    """Display prediction results."""
    prediction_result = session.get('prediction_result')
    if not prediction_result:
        flash('No prediction result found. Please make a prediction first.', 'info')
        return redirect(url_for('predict'))
    
    suggestions = session.get('prediction_suggestions', [])
    inputs = session.get('prediction_inputs', {})
    
    return render_template('result.html',
        result=prediction_result,
        suggestions=suggestions,
        inputs=inputs
    )


# ─────────────────────────────────────────────
# Emotion Detection
# ─────────────────────────────────────────────

@app.route('/emotion', methods=['GET', 'POST'])
@login_required
def emotion():
    """Handle emotion detection from image upload."""
    emotion_result = None
    
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image file uploaded.', 'danger')
            return render_template('emotion.html')
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No image selected.', 'danger')
            return render_template('emotion.html')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Detect emotion
            emotion_result = detect_emotion(filepath)
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                pass
        else:
            flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF).', 'danger')
    
    return render_template('emotion.html', emotion_result=emotion_result)


# ─────────────────────────────────────────────
# Stress History
# ─────────────────────────────────────────────

@app.route('/history')
@login_required
def history():
    """Display user's stress prediction history."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = StressHistory.query.filter_by(user_id=current_user.id)\
        .order_by(StressHistory.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('history.html',
        records=pagination.items,
        pagination=pagination
    )


# ─────────────────────────────────────────────
# API Routes
# ─────────────────────────────────────────────

@app.route('/api/stress-data')
@login_required
def api_stress_data():
    """JSON API endpoint for Chart.js stress data."""
    records = StressHistory.query.filter_by(user_id=current_user.id)\
        .order_by(StressHistory.created_at.desc()).limit(30).all()
    
    chart_data = get_trend_data(records, limit=30)
    
    # Distribution data
    all_records = StressHistory.query.filter_by(user_id=current_user.id).all()
    distribution = {
        'Low Stress': sum(1 for r in all_records if r.stress_level == 'Low Stress'),
        'Moderate Stress': sum(1 for r in all_records if r.stress_level == 'Moderate Stress'),
        'High Stress': sum(1 for r in all_records if r.stress_level == 'High Stress')
    }
    
    return jsonify({
        'trend': chart_data,
        'distribution': distribution,
        'total': len(all_records)
    })


# ─────────────────────────────────────────────
# Error Handlers
# ─────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('base.html', error_code=404, error_message='Page not found'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('base.html', error_code=500, error_message='Internal server error'), 500


# ─────────────────────────────────────────────
# Run Application
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  🧠 Mental Wellness Platform Starting...")
    print("  📍 http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
