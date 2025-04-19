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

# Connect to your SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def fetch_levels():
    logging.info("📥 Fetching levels from Level table...")
    try:
        cursor.execute("SELECT level_id, category, title, description, difficulty FROM Level")
        levels = cursor.fetchall()
        logging.info(f"✅ Found {len(levels)} levels to process.\n")
        return levels
    except Exception as e:
        logging.error(f"❌ Failed to fetch levels: {e}")
        return []

def generate_questions(level):
    level_id, category, title, description, difficulty = level
    logging.info(f"⚡ Generating questions for Level ID: {level_id} ({title})...")

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
        logging.info("📡 Sending request to Ollama API...")
        response = requests.post("http://localhost:11434/api/generate", json=payload)

        if response.status_code == 200:
            raw_data = response.json().get("response", "").strip()
            logging.info(f"📋 Raw Ollama API response for Level {level_id}: {raw_data}")
            questions = json.loads(raw_data)

            if isinstance(questions, list) and all("question_text" in q for q in questions):
                logging.info(f"✅ {len(questions)} questions generated for Level {level_id}.\n")
                return questions
            else:
                logging.warning(f"⚠️ Invalid question format returned for Level {level_id}. Skipping.")
                return []
        else:
            logging.error(f"❌ Ollama API failed for Level {level_id}: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        logging.error(f"❌ Error generating questions for Level {level_id}: {e}")
        return []

def save_questions(level_id, questions):
    logging.info(f"💾 Saving {len(questions)} questions to database for Level {level_id}...")
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
    logging.info(f"✅ {success_count}/{len(questions)} questions saved for Level {level_id}.\n")

def main():
    logging.info("🚀 Starting question generation process...\n")
    levels = fetch_levels()

    if not levels:
        logging.warning("⚠️ No levels found. Exiting.")
        return

    for idx, level in enumerate(levels, start=1):
        logging.info(f"➡️ [{idx}/{len(levels)}] Processing Level {level[0]}...")
        questions = generate_questions(level)

        if questions:
            save_questions(level[0], questions)
        else:
            logging.warning(f"⚠️ No valid questions generated for Level {level[0]}. Skipping.\n")

        time.sleep(1)  # Avoid overloading Ollama server

    logging.info("🎉 All levels processed! Script completed.\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"💥 Unhandled exception: {e}")
    finally:
        conn.close()
        logging.info("🔒 Database connection closed.")
