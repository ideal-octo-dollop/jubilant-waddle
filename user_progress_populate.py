import sqlite3
from datetime import datetime

# Define the updated progress data (level 100 and xp 100)
progress_data = {
    'aptitude': {'level': 3, 'xp': 20},
    'coding': {'level': 5, 'xp': 40},
    'communication': {'level': 2, 'xp': 60}
}

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# User ID (we are assuming user ID = 1 for this example)
user_id = 1

# Get the current date and time
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Iterate over the progress data
for category, progress in progress_data.items():
    print(f"Checking category: {category} for user_id: {user_id}")

    # Check if the entry already exists
    cursor.execute('''
    SELECT * FROM user_progress WHERE user_id = ? AND category = ?
    ''', (user_id, category))
    existing_record = cursor.fetchone()

    if existing_record:
        print(f"Existing record found: {existing_record}")
        # If the record exists, update it
        cursor.execute('''
        UPDATE user_progress 
        SET current_level = ?, current_xp = ?, last_played = ?
        WHERE user_id = ? AND category = ?
        ''', (progress['level'], progress['xp'], current_time, user_id, category))

        print(f"Updated record for category: {category}")
    else:
        print(f"No existing record found for category: {category}, inserting new record.")
        # If no record exists, insert it
        cursor.execute('''
        INSERT INTO user_progress (user_id, category, current_level, current_xp, last_played)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category, progress['level'], progress['xp'], current_time))

        print(f"Inserted new record for category: {category}")

# Commit the changes and close the connection
conn.commit()

# Print success message
print("✅ Progress data updated successfully.")
conn.close()
