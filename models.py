import sqlite3
from contextlib import contextmanager
from flask import g
from config import Config

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(Config.DATABASE)
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        if conn:
            conn.close()

def get_user_progress(user_id):
    """Fetch user progress for all categories"""
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            SELECT category, current_level, current_xp 
            FROM user_progress 
            WHERE user_id = ?
        ''', (user_id,))
        progress_data = c.fetchall()
        
        return {
            row['category']: {
                'level': row['current_level'],
                'xp': row['current_xp']
            } for row in progress_data
        }

def get_user_by_email(email):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def get_user_by_id(user_id):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

def update_user_profile(user_id, name, email, rollno, college, state, phone):
    with get_db_connection() as conn:
        conn.execute('''
            UPDATE users 
            SET name = ?, email = ?, rollno = ?, college = ?, state = ?, phone = ?
            WHERE id = ?
        ''', (name, email, rollno, college, state, phone, user_id))
        conn.commit()
        return True

def create_user(name, email, phone, college, state, rollno, hashed_password, profile_pic):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, phone, college, state, rollno, password, profile_pic) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (name, email, phone, college, state, rollno, hashed_password, profile_pic))
        user_id = c.lastrowid
        conn.commit()
        return user_id

def initialize_user_progress(user_id, categories, timestamp):
    with get_db_connection() as conn:
        c = conn.cursor()
        for category in categories:
            c.execute('''
            INSERT INTO user_progress (user_id, category, current_level, current_xp, last_played)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, category, 1, 0, timestamp))
        conn.commit()

def get_level_data(level_id):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM Level WHERE level_id = ?', (level_id,)).fetchone()

def get_questions(level_id):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM Questions WHERE level_id = ?', (level_id,)).fetchall()