import random
import sqlite3

calculus_questions = {
    # Derivatives
    "question1": {
        "question": "What is the derivative of x^n?",
        "answer": "n * x^(n-1)"
    },
    "question2": {
        "question": "What is the derivative of e^x?",
        "answer": "e^x"
    },
    "question3": {
        "question": "What is the derivative of a^x, where a > 0?",
        "answer": "a^x * ln(a)"
    },
    "question4": {
        "question": "What is the derivative of ln(x)?",
        "answer": "1 / x"
    },
    "question5": {
        "question": "What is the derivative of sin(x)?",
        "answer": "cos(x)"
    },
    "question6": {
        "question": "What is the derivative of cos(x)?",
        "answer": "-sin(x)"
    },
    "question7": {
        "question": "What is the derivative of tan(x)?",
        "answer": "sec^2(x)"
    },
    "question8": {
        "question": "What is the derivative of sec(x)?",
        "answer": "sec(x) * tan(x)"
    },
    "question9": {
        "question": "What is the derivative of arcsin(x)?",
        "answer": "1 / sqrt(1 - x^2)"
    },
    "question10": {
        "question": "What is the derivative of arccos(x)?",
        "answer": "-1 / sqrt(1 - x^2)"
    },
    "question11": {
        "question": "What is the derivative of arctan(x)?",
        "answer": "1 / (1 + x^2)"
    },

    # Antiderivatives
    "question12": {
        "question": "What is the antiderivative of x^n, where n ≠ -1?",
        "answer": "x^(n+1) / (n+1) + C"
    },
    "question13": {
        "question": "What is the antiderivative of 1/x?",
        "answer": "ln|x| + C"
    },
    "question14": {
        "question": "What is the antiderivative of e^x?",
        "answer": "e^x + C"
    },
    "question15": {
        "question": "What is the antiderivative of e^(kx)?",
        "answer": "e^(kx) / k + C"
    },
    "question16": {
        "question": "What is the antiderivative of sin(x)?",
        "answer": "-cos(x) + C"
    },
    "question17": {
        "question": "What is the antiderivative of cos(x)?",
        "answer": "sin(x) + C"
    },
    "question18": {
        "question": "What is the antiderivative of sin(kx)?",
        "answer": "-cos(kx) / k + C"
    },
    "question19": {
        "question": "What is the antiderivative of cos(kx)?",
        "answer": "sin(kx) / k + C"
    },
    "question20": {
        "question": "What is the antiderivative of sec^2(x)?",
        "answer": "tan(x) + C"
    },
    "question21": {
        "question": "What is the antiderivative of sec(x)tan(x)?",
        "answer": "sec(x) + C"
    },
    "question22": {
        "question": "What is the antiderivative of 1 / (1 + x^2)?",
        "answer": "arctan(x) + C"
    },
    "question23": {
        "question": "What is the antiderivative of 1 / sqrt(1 - x^2)?",
        "answer": "arcsin(x) + C"
    },
    "question24": {
        "question": "What is the antiderivative of 1 / sqrt(k^2 - x^2)?",
        "answer": "arcsin(x / k) + C"
    },
    "question25": {
        "question": "What is the antiderivative of 1 / (kx + b)?",
        "answer": "ln|kx + b| / k + C"
    },
    "question26": {
        "question": "What is the antiderivative of k^x?",
        "answer": "k^x / ln(k) + C"
    },
    "question27": {
        "question": "What is the antiderivative of sec(x)?",
        "answer": "ln|sec(x) + tan(x)| + C"
    }
}


def random_questions(questions: dict):
    questions_keys = random.sample(list(questions), 3)
    return {keys: questions[keys] for keys in questions_keys}

ques = random_questions(calculus_questions)

#ans for the question testing
for key, value in ques.items():
      print(f'\nAns: {value['answer']}')


def check(questions: str):
    performance = {}

    for key, value in questions.items():
        print(f'\nQuestion: {value['question']}')

        is_correct = False
        attempts = 0 #if att 1:correct 3 pts, 2:one failed 1 pt, 2 failed:failed 0 pts

        while attempts < 2:

            try:
                user_input = input("Answer: ")
                attempts += 1

                if not user_input.strip():
                    attempts = 0
                    raise ValueError("Input cannot be empty")
            except ValueError as e:
                print("Error", e)
            
            if value['answer'].lower().strip().replace(' ', '') == user_input.lower().strip().replace(' ', ''):
                print("The answer is correct!")
                is_correct = True
                break
            else:
                print("Incorrect answer")

        points = 3 if attempts == 1 else 1 if attempts == 2 and is_correct == True else 0 

        performance[key] = {
            "correct":is_correct,
            "points": points
        }

        if not is_correct:
            print(f"The answer is: {value['answer']}")


    correct = sum(value['correct'] for value in performance.values())
    pts = sum(value['points'] for value in performance.values())

    print(f"\nSummary:\n\nCorrect answers: {correct}\nTotal points: {pts}")

    return performance.items()


###
### Database workflow

def init_db():
    conn = sqlite3.connect('performance.db')
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
    conn = sqlite3.connect("performance.db")
    cur = conn.cursor()

    for question_id, values in data:
        cur.execute("""
            INSERT INTO performance(question_id, correct, points)
            VALUES(?, ?, ?);
        """, (question_id, values['correct'], values['points']))

    conn.commit()
    conn.close()

def fetch_summary():
    conn = sqlite3.connect("performance.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM performance;")
    print(cur.fetchall())
    conn.close()


if __name__ == "__main__":
    init_db()  
    c = check(ques)
    store_performance(c)
    fetch_summary()
