import sqlite3
from questions import random_questions, check
from settings import calculus_questions

def init_db():
    try:
        conn = sqlite3.connect('performance.db')
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS performance(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT,
                correct BOOLEAN,
                points INTEGER,
                timestamp Datetime DEFAULT CURRENT_TIMESTAMP);
    """)

    conn.commit()
    conn.close()

def store_performance(data):
    try:
        conn = sqlite3.connect('performance.db')
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")

    cur = conn.cursor()

    for question_id, values in data.items():
        cur.execute("""
            INSERT INTO performance(question_id, correct, points)
            VALUES(?, ?, ?);
        """, (question_id, values['correct'], values['points']))

    conn.commit()
    conn.close()

#fetch all attempts
def fetch_summary():
    try:
        conn = sqlite3.connect('performance.db')
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
    cur = conn.cursor()
    cur.execute("SELECT * FROM performance;")
    print(f'fetch: {cur.fetchall()}')
    conn.close()

#fetch lower band answers
def fetch_attempts_and_avg():
    try:
        conn = sqlite3.connect('performance.db')
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")

    cur = conn.cursor()

    cur.execute(
        """
        SELECT question_id, COUNT(*) AS attempts, 
        AVG(points) as avg_points FROM performance GROUP BY question_id ORDER BY avg_points ASC;
    """)

    results = cur.fetchall()
    print("\nPerformance summary (Aggregated)")
    for row in results:
        print(f"Question id: {row[0]}, Attempts: {row[1]}, AVG points: {row[2]:.2f}")

    conn.close()


if __name__ == "__main__":
    init_db() 
    ques = random_questions(calculus_questions)
    c = check(ques)
    store_performance(c)
    fetch_summary()
    fetch_attempts_and_avg()


# modify random questions and calc_questions 
