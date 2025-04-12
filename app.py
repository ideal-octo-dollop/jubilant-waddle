from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  # Include check_password_hash
import requests 

app = Flask(__name__)
app.secret_key = 'your_top_secret_key'  # Needed for sessions and flash messages

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

@app.route('/')
@login_required
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
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['name']
                flash('You have been logged in, young padawan!', 'success')
                session['logged_in'] = True
                session['user_id'] = user['id']
                return redirect(url_for('home'))
            else:
                flash('Incorrect password.', 'danger')
        else:
            flash('No account found with that email.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
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

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (name, email, phone, college, state, rollno, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (name, email, phone, college, state, rollno, hashed_password))
            conn.commit()
            
            flash("Registration successful!", "success")
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "error")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/learning')
@login_required
def learning():
    return render_template('learning.html')

@app.route('/challenges')
@login_required
def challenges():
    return render_template('challenges.html')

@app.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
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

    user = conn.execute('SELECT name, email, rollno, college, state, phone FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if user:
        return render_template('profile.html',
            name=user['name'],
            email=user['email'],
            rollno=user['rollno'] or '',
            college=user['college'] or '',
            state=user['state'] or '',
            phone=user['phone'] or ''
        )
    else:
        return "User not found", 404


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. Farewell, warrior!', 'info')
    return redirect(url_for('login'))


@app.route("/chatbot")
def chatbot_ui():
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
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
    app.run(debug=True)
