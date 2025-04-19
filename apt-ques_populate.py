import sqlite3
import requests
import logging
import json
import time

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

print("🔗 Connecting to database...")

# Connect to your database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def fetch_levels():
    print("📥 Fetching levels from Level table...")
    try:
        cursor.execute("SELECT level_id, category, title, description, difficulty FROM Level")
        levels = cursor.fetchall()
        print(f"✅ Found {len(levels)} levels to process.\n")
        return levels
    except Exception as e:
        logging.error(f"❌ Failed to fetch levels: {e}")
        return []

def generate_questions(level):
    level_id, category, title, description, difficulty = level
    print(f"\n⚡ Generating questions for Level ID: {level_id} ({title}) ...")

    prompt = f"""
You are an expert question setter for aptitude tests.

Generate 5 multiple-choice questions based on the following:
- Category: {category}
- Title: {title}
- Description: {description}
- Difficulty: {difficulty}

For each question, give:
1. Question text
2. Choices as a list of 4 options.
3. Correct answer (must match one of the choices).
4. Explanation.

Output JSON in this format:
[
    {{
        "question_text": "...",
        "choices": ["A", "B", "C", "D"],
        "correct_answer": "B",
        "explanation": "..."
    }}
]
"""
    try:
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
        print("📡 Sending request to Ollama API...")
        response = requests.post("http://localhost:11434/api/generate", json=payload)

        print("📋 Response from Ollama API:", response.text)  # Log the raw response text here

        if response.status_code == 200:
            data = response.json().get("response", "").strip()
            questions = json.loads(data)
            print(f"✅ {len(questions)} questions generated for Level {level_id}.\n")
            return questions
        else:
            logging.error(f"❌ Ollama API failed for Level {level_id}: {response.text}")
            return []

    except Exception as e:
        logging.error(f"❌ Error generating questions for Level {level_id}: {e}")
        return []

def save_questions(level_id, questions):
    print(f"💾 Saving {len(questions)} questions to database for Level {level_id}...")
    success_count = 0
    for q in questions:
        try:
            cursor.execute('''
                INSERT INTO Questions (level_id, question_text, correct_answer, choices, explaination)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                level_id,
                q["question_text"],
                q["correct_answer"],
                json.dumps(q["choices"]),
                q["explanation"]
            ))
            success_count += 1
        except Exception as e:
            logging.error(f"❌ Failed to save question for Level {level_id}: {e}")

    conn.commit()
    print(f"✅ {success_count} questions saved successfully for Level {level_id}.\n")

def main():
    print("🚀 Starting question generation process...\n")
    levels = fetch_levels()

    for idx, level in enumerate(levels, start=1):
        print(f"➡️ [{idx}/{len(levels)}] Processing Level {level[0]}...")
        questions = generate_questions(level)

        if questions:
            save_questions(level[0], questions)
        else:
            print(f"⚠️ No valid questions generated for {level[0]}. Skipping saving.\n")

        time.sleep(1)  # gentle delay to avoid hammering Ollama

    print("\n🎉 All levels processed! Script completed.\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"💥 Unhandled exception: {e}")
    finally:
        conn.close()
        print("🔒 Database connection closed.")
