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
);
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
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, category)
);
''')

# Create the user_streak_days table (for GitHub-style streak calendar)
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_streak_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    activity_count INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, date)
);
''')

# Create the user_badges table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    badge_name TEXT NOT NULL,
    earned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, badge_name)
);
''')

# Create the leaderboard_snapshots table
cursor.execute('''
CREATE TABLE IF NOT EXISTS leaderboard_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_xp INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    snapshot_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Level (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    level_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    difficulty TEXT,
    xp INTEGER NOT NULL
)
''')

# Create Questions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level_id TEXT NOT NULL,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    choices TEXT NOT NULL,
    explaination TEXT,
    FOREIGN KEY (level_id) REFERENCES Level(level_id)
)
''')



# Commit and close connection
conn.commit()
conn.close()

print("✅ Database created — all tables initialized: Users, Progress, Streaks, Badges, Leaderboard, Quests & Quest Completion!")
