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
    password TEXT NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ Database created and 'users' table initialized.")
