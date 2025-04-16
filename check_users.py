import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Fetch and display all users
print("🧑‍💼 Users Table Data:")
cursor.execute('''
SELECT id, name, email, phone, college, rollno, state, password, profile_pic FROM users
''')
users = cursor.fetchall()

for user in users:
    print(f"User ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Phone: {user[3]}, College: {user[4]}, Roll No: {user[5]}, State: {user[6]}, Password: {user[7]}, Profile Pic: {user[8]}")
print("---------------------------------------------------")

# Fetch and display user progress data
print("📊 User Progress Table Data:")
cursor.execute('''
SELECT user_id, category, current_level, current_xp, last_played FROM user_progress
''')
user_progress = cursor.fetchall()

for progress in user_progress:
    print(f"User ID: {progress[0]}, Category: {progress[1]}, Level: {progress[2]}, XP: {progress[3]}, Last Played: {progress[4]}")
print("---------------------------------------------------")

# Close the connection
conn.close()
