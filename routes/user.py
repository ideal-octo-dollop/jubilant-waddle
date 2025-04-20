from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils import login_required
from models import get_user_progress, get_user_by_id, update_user_profile

# Change the blueprint definition to include a url_prefix
user_bp = Blueprint('user', __name__, url_prefix='')

@user_bp.route('/')
def home():
    return render_template('index.html')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    # Refresh progress data from database
    session['progress'] = get_user_progress(session['user_id'])
    return render_template('dashboard.html', username=session['username'], progress=session['progress'])

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_roll = request.form['rollno']
        new_college = request.form['college']
        new_state = request.form['state']
        new_phone = request.form['phone']

        update_user_profile(user_id, new_name, new_email, new_roll, new_college, new_state, new_phone)
        
        # Update session username if it changed
        if new_name != session.get('username'):
            session['username'] = new_name
            
        flash("Profile updated successfully!", "success")

    user = get_user_by_id(user_id)

    if not user:
        flash("User not found", "error")
        return redirect(url_for('user.home'))
        
    # Ensure profile_pic has a valid image, else load default
    profile_pic = user['profile_pic'] if user['profile_pic'] else 'default.jpg'
    profile_pic_url = url_for('static', filename=f'uploads/{profile_pic}')

    return render_template('profile.html',
        name=user['name'],
        email=user['email'],
        rollno=user['rollno'] or '',
        college=user['college'] or '',
        state=user['state'] or '',
        phone=user['phone'] or '',
        profile_pic=profile_pic_url
    )