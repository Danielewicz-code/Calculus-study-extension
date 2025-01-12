import random

def random_questions(questions: dict):
    questions_keys = random.sample(list(questions), 3)
    return {keys: questions[keys] for keys in questions_keys}

#ques = random_questions(calculus_questions)

#ans for the question testing
# for key, value in ques.items():
#       print(f'\nAns: {value['answer']}')


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

    return dict(performance)
