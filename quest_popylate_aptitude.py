import sqlite3

# Connect to your DB
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Aptitude Quests Data (Adding quest_number)
aptitude_quests = [
    (1, "Aptitude", "Basic Arithmetic", "Solve simple addition, subtraction, multiplication, and division problems.", 50, 1),
    (2, "Aptitude", "Percentage Calculations", "Practice calculating percentages.", 75, 1),
    (3, "Aptitude", "Ratio and Proportions", "Learn the concepts of ratios and proportions.", 100, 2),
    (4, "Aptitude", "Time and Work Problems", "Solve problems related to time, work, and efficiency.", 100, 2),
    (5, "Aptitude", "Simple Interest", "Understand and calculate simple interest.", 125, 2),
    (6, "Aptitude", "Compound Interest", "Learn how compound interest works and solve related problems.", 150, 3),
    (7, "Aptitude", "Speed, Distance, and Time", "Solve problems related to speed, distance, and time.", 125, 3),
    (8, "Aptitude", "Averages", "Practice problems on averages and their applications.", 100, 3),
    (9, "Aptitude", "Profit and Loss", "Learn and solve problems related to profit and loss.", 150, 4),
    (10, "Aptitude", "Mixtures and Alligation", "Solve problems involving mixtures and alligation.", 175, 4),
    (11, "Aptitude", "Simple Algebra", "Solve basic algebraic equations and problems.", 150, 4),
    (12, "Aptitude", "Geometry Basics", "Understand basic geometric shapes and their properties.", 100, 4),
    (13, "Aptitude", "Mensuration", "Learn how to calculate area, volume, and surface area of different shapes.", 200, 5),
    (14, "Aptitude", "Linear Equations", "Practice solving linear equations in one variable.", 150, 5),
    (15, "Aptitude", "Probability", "Solve probability-related problems.", 175, 5),
    (16, "Aptitude", "Number Series", "Identify and complete number series.", 200, 6),
    (17, "Aptitude", "Permutations and Combinations", "Learn and solve problems on permutations and combinations.", 250, 6),
    (18, "Aptitude", "Pipes and Cisterns", "Solve problems related to pipes and cisterns.", 225, 6),
    (19, "Aptitude", "Work and Time", "Solve advanced work-time problems.", 300, 7),
    (20, "Aptitude", "Data Interpretation", "Interpret data from graphs, charts, and tables.", 300, 7)
]

# Insert Quests into Table
cursor.executemany('''
INSERT INTO quests (quest_number, category, title, description, xp_reward, level_required)
VALUES (?, ?, ?, ?, ?, ?)
''', aptitude_quests)

# Commit and close
conn.commit()
conn.close()

print("✅ 20 Aptitude Quests populated successfully!")
