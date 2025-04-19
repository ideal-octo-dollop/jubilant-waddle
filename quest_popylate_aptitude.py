import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

levels = [
    ("Aptitude", "APT-001", "Percentage Basics", "Solve simple percentage problems.", 100, "Easy"),
    ("Aptitude", "APT-002", "Percentage Increase/Decrease", "Understand percentage change scenarios.", 120, "Easy"),
    ("Aptitude", "APT-003", "Successive Percentage Changes", "Multiple percentage changes in sequence.", 150, "Medium"),
    ("Aptitude", "APT-004", "Real-World Percentage Applications", "Apply percentage concepts in real-life problems.", 180, "Medium"),
    ("Aptitude", "APT-005", "Advanced Percentage Word Problems", "Challenging percentage-based numerical problems.", 200, "Hard"),

    ("Aptitude", "APT-006", "Time and Work Basics", "Understand basic work-time relationship.", 100, "Easy"),
    ("Aptitude", "APT-007", "Combined Work Problems", "Multiple people completing tasks together.", 120, "Easy"),
    ("Aptitude", "APT-008", "Efficiency and Work", "Compare work efficiency of individuals.", 150, "Medium"),
    ("Aptitude", "APT-009", "Pipes and Cisterns", "Work-related problems involving pipes and tanks.", 180, "Medium"),
    ("Aptitude", "APT-010", "Advanced Time and Work", "Challenging and multi-step time-work problems.", 220, "Hard"),

    ("Aptitude", "APT-011", "Probability Basics", "Basic understanding of chance and outcomes.", 100, "Easy"),
    ("Aptitude", "APT-012", "Single Event Probability", "Probability of simple, single events.", 120, "Easy"),
    ("Aptitude", "APT-013", "Multiple Events", "Handle compound probability scenarios.", 150, "Medium"),
    ("Aptitude", "APT-014", "Probability in Real-life Scenarios", "Games and case-based probability applications.", 180, "Medium"),
    ("Aptitude", "APT-015", "Advanced Probability", "Tough problems with layered logic.", 220, "Hard"),

    ("Aptitude", "APT-016", "Ratio Basics", "Understand ratios and their usage.", 100, "Easy"),
    ("Aptitude", "APT-017", "Solving Proportions", "Equating and solving proportions.", 120, "Easy"),
    ("Aptitude", "APT-018", "Mixtures and Alligation", "Mixing components using ratio logic.", 150, "Medium"),
    ("Aptitude", "APT-019", "Advanced Ratio Problems", "Tough ratio-based problem solving.", 180, "Hard"),
    ("Aptitude", "APT-020", "Partnership Problems", "Profit sharing in business scenarios.", 200, "Expert")
]

cursor.executemany('''
INSERT INTO Level (category, level_id, title, description, xp, difficulty)
VALUES (?, ?, ?, ?, ?, ?)
''', levels)

conn.commit()
conn.close()

print("20 aptitude levels inserted with fixed APT-### IDs and difficulty levels.")
