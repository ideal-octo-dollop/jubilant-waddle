import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    college TEXT NOT NULL,
    rollno INT NOT NULL,
    state TEXT NOT NULL,
    password TEXT NOT NULL,
    profile_pic TEXT NOT NULL
)
''')

# Create the user_progress table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    current_level INTEGER DEFAULT 1,
    current_xp INTEGER DEFAULT 0,
    last_played DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ Database created and both 'users' and 'user_progress' tables initialized.")
