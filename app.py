from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import requests
import uuid
import os

app = Flask(__name__)
app.secret_key = 'your_top_secret_key'  # Needed for sessions and flash messages

# Configuration for uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Path for saving profile images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions for profile images

# Global Functions

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')

def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            # Check password validity
            if check_password_hash(user['password'], password):
                # Set session variables for user info
                session['user_id'] = user['id']
                session['username'] = user['name']
                session['logged_in'] = True

                # Fetch user progress for each category
                c = conn.cursor()
                c.execute('''
                    SELECT category, current_level, current_xp 
                    FROM user_progress 
                    WHERE user_id = ?
                ''', (user['id'],))
                progress_data = c.fetchall()

                # Store progress in session in a dictionary
                session['progress'] = {
                    row['category']: {
                        'level': row['current_level'],
                        'xp': row['current_xp']
                    } for row in progress_data
                }

                flash('You have been logged in, young padawan!', 'success')
                next_page = request.args.get('next', url_for('home'))  # Redirect to 'next' page or home
                return redirect(next_page)

            else:
                flash('Incorrect password.', 'danger')
        else:
            flash('No account found with that email.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if 'user_id' in session:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT category, current_level, current_xp 
            FROM user_progress 
            WHERE user_id = ?
        ''', (session['user_id'],))
        progress_data = c.fetchall()

        # Update session's progress for fresh data
        session['progress'] = {
            row['category']: {
                'level': row['current_level'],
                'xp': row['current_xp']
            } for row in progress_data
        }

        print("DEBUG - Progress data:", session['progress'])  # confirm it's working

        return render_template('dashboard.html', username=session['username'], progress=session['progress'])
    
    else:
        flash('You must log in first.', 'warning')
        return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        filename = None
        if profile_pic and allowed_file(profile_pic.filename):
            original = secure_filename(profile_pic.filename)
            unique_name = f"{uuid.uuid4().hex}_{original}"  # prevents name clashes
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
            profile_image_uniq_name = unique_name

            conn = get_db_connection()
            c = conn.cursor()

            # Insert user data into 'users' table
            c.execute("INSERT INTO users (name, email, phone, college, state, rollno, password, profile_pic) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (name, email, phone, college, state, rollno, hashed_password, profile_image_uniq_name))
            
            user_id = c.lastrowid  # Get the ID of the newly created user

            # Insert default progress into 'user_progress' table
            categories = ['aptitude', 'coding', 'communication']
            from datetime import datetime
            now = datetime.now()

            for category in categories:
                c.execute('''
                INSERT INTO user_progress (user_id, category, current_level, current_xp, last_played)
                VALUES (?, ?, ?, ?, ?)
                ''', (user_id, category, 1, 0, now))

            conn.commit()
            conn.close()

            flash("Registration successful! Progress initialized.", "success")
            return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/play_bef')
@login_required
def play_bef():
    return render_template('learning.html')


@app.route('/play/<category>')
@login_required
def play_category(category):
    print(f"User {session['user_id']} is attempting to play category: {category}")
    
    user_id = session['user_id']
    conn = get_db_connection()

    # Fetch the user's current progress in the given category
    try:
        progress = conn.execute(
            'SELECT current_level FROM user_progress WHERE user_id = ? AND category = ?',
            (user_id, category)
        ).fetchone()
        
        if progress is None:
            print(f"No progress found for user {user_id} in category '{category}'. Defaulting to level 1.")
            current_level = 1  # Default to level 1 if new
        else:
            current_level = progress['current_level']
            print(f"User {user_id} is at level {current_level} in category '{category}'.")
    except Exception as e:
        print(f"Error fetching user progress for {user_id} in category '{category}': {e}")
        flash("There was an error retrieving your progress.", "danger")
        conn.close()
        return redirect(url_for('home'))

    # Get the Level data for this category & level
    try:
        level = conn.execute(
            'SELECT * FROM Level WHERE category = ? AND id = ?',
            (category, current_level)
        ).fetchone()

        if not level:
            print(f"No level found for category '{category}' at level {current_level}.")
            flash(f"No level found for '{category}' at Level {current_level}.", "danger")
            conn.close()
            return redirect(url_for('home'))
        else:
            print(f"Level {current_level} data found for category '{category}'.")
    except Exception as e:
        print(f"Error fetching level data for category '{category}' at level {current_level}: {e}")
        flash("There was an error retrieving level data.", "danger")
        conn.close()
        return redirect(url_for('home'))

    # Get Questions for this level
    try:
        questions = conn.execute(
            'SELECT * FROM Questions WHERE level_id = ?',
            (level['level_id'],)
        ).fetchall()

        if not questions:
            print(f"No questions found for level {current_level} in category '{category}'.")
            flash("No questions available for this level.", "info")
    except Exception as e:
        print(f"Error fetching questions for level {current_level} in category '{category}': {e}")
        flash("There was an error retrieving questions.", "danger")
        conn.close()
        return redirect(url_for('home'))

    conn.close()
    
    print(f"Rendering learning page for category '{category}', level {current_level}.")
    return render_template(
        'learning.html', 
        category=category,
        level=level,
        questions=questions
    )




@app.route('/challenges')
@login_required
def challenges():
    return render_template('challenges.html')


@app.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('leaderboard.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    conn = get_db_connection()

    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_roll = request.form['rollno']
        new_college = request.form['college']
        new_state = request.form['state']
        new_phone = request.form['phone']

        conn.execute('''
            UPDATE users 
            SET name = ?, email = ?, rollno = ?, college = ?, state = ?, phone = ?
            WHERE id = ?
        ''', (new_name, new_email, new_roll, new_college, new_state, new_phone, user_id))
        conn.commit()

    user = conn.execute(
        'SELECT name, email, rollno, college, state, phone, profile_pic FROM users WHERE id = ?', 
        (user_id,)
    ).fetchone()
    conn.close()

    if user:
        # Ensure profile_pic has a valid image, else load default
        profile_pic = user['profile_pic'] if user['profile_pic'] else 'default.jpg'
        profile_pic_url = url_for('static', filename=f'uploads/{profile_pic}')  # Assuming your uploaded files are in static/uploads

        return render_template('profile.html',
            name=user['name'],
            email=user['email'],
            rollno=user['rollno'] or '',
            college=user['college'] or '',
            state=user['state'] or '',
            phone=user['phone'] or '',
            profile_pic=profile_pic_url
        )
    else:
        return "User not found", 404


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out. Farewell, warrior!', 'info')
    return redirect(url_for('login'))


@app.route("/chatbot")
@login_required
def chatbot_ui():
    return render_template("chatbot.html")


@app.route("/ask", methods=["POST"])
@login_required
def ask_phi():
    user_input = request.json.get("prompt", "")
    payload = {
        "model": "llama3",
        "prompt": user_input,
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload)

    if response.status_code == 200:
        data = response.json()
        return jsonify({"response": data.get("response", "")})
    else:
        return jsonify({"error": "Ollama API failed"}), 500


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # Ensure the upload folder exists
    app.run(debug=True)
