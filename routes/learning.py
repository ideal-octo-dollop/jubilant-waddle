from flask import Blueprint, render_template, session, redirect, url_for, flash
from utils import login_required
from models import get_db_connection, get_level_data, get_questions

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/challenges')
@login_required
def challenges():
    return render_template('challenges.html')

@learning_bp.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('leaderboard.html')

@learning_bp.route('/play_bef')
@login_required
def play_bef():
    return render_template('learning.html')

@learning_bp.route('/play/<category>')
@login_required
def play_category(category):
    user_id = session['user_id']
    
    try:
        with get_db_connection() as conn:
            # Fetch the user's current progress in the given category
            progress = conn.execute(
                'SELECT current_level FROM user_progress WHERE user_id = ? AND category = ?',
                (user_id, category)
            ).fetchone()
            
            current_level = progress['current_level'] if progress else 1
            
            # Convert to format like APT-001
            level_id = f"APT-{current_level:03d}"

            # Get the Level data
            level = get_level_data(level_id)

            if not level:
                flash(f"No level found for '{category}' at Level {current_level}.", "danger")
                return redirect(url_for('user.home'))

            # Get Questions for this level
            questions = get_questions(level_id)

            if not questions:
                flash("No questions available for this level.", "info")
                
            level = dict(level)
            questions = [dict(q) for q in questions]
    
    except Exception as e:
        flash(f"Error loading level: {str(e)}", "danger")
        return redirect(url_for('user.home'))
    
    return render_template(
        'question1.html', 
        category=category,
        level=level,
        questions=questions
    )