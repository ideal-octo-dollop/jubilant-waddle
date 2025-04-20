from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from models import get_user_by_email, create_user, initialize_user_progress, get_user_progress
from utils import allowed_file
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            # Set session variables for user info
            session['user_id'] = user['id']
            session['username'] = user['name']
            session['logged_in'] = True
            
            # Get user progress and store in session
            session['progress'] = get_user_progress(user['id'])

            flash('You have been logged in, young padawan!', 'success')
            next_page = request.args.get('next', url_for('user.dashboard'))
            return redirect(next_page)
        else:
            flash('Invalid email or password.', 'danger')
            
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        college = request.form['college']
        state = request.form['state']
        rollno = request.form['rollno']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        profile_pic = request.files['profile_pic']

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        profile_image_uniq_name = None
        
        if profile_pic and allowed_file(profile_pic.filename):
            original = secure_filename(profile_pic.filename)
            profile_image_uniq_name = f"{uuid.uuid4().hex}_{original}"
            
            # Ensure upload folder exists
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            profile_pic.save(os.path.join(Config.UPLOAD_FOLDER, profile_image_uniq_name))

        # Create user and initialize progress
        user_id = create_user(name, email, phone, college, state, rollno, hashed_password, profile_image_uniq_name)
        
        # Initialize user progress
        categories = ['aptitude', 'coding', 'communication']
        now = datetime.now()
        initialize_user_progress(user_id, categories, now)

        flash("Registration successful! Progress initialized.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. Farewell, warrior!', 'info')
    return redirect(url_for('auth.login'))