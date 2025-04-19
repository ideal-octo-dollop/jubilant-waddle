import sqlite3
import json

def fetch_questions():
    # Connect to your database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, level_id, question_text, correct_answer, choices, explaination FROM Questions")
        questions = cursor.fetchall()

        if not questions:
            print("⚠️ No questions found in the database.")
            return

        print(f"✅ Found {len(questions)} questions:\n")

        for q in questions:
            id, level_id, question_text, correct_answer, choices_json, explanation = q
            choices = json.loads(choices_json)

            print(f"🧾 Question ID: {id}")
            print(f"🔢 Level ID: {level_id}")
            print(f"❓ Question: {question_text}")
            print(f"💡 Choices:")
            for i, choice in enumerate(choices, start=1):
                print(f"   {chr(64+i)}. {choice}")
            print(f"✅ Correct Answer: {correct_answer}")
            print(f"🧠 Explanation: {explanation}\n")
            print("-" * 50)

    except Exception as e:
        print(f"❌ Error fetching questions: {e}")

    finally:
        conn.close()
        print("🔒 Database connection closed.")

if __name__ == "__main__":
    fetch_questions()
