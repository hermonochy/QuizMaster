import json
import os

def load_questions_from_json():
    try:
        with open('quiz_questions.json', 'r') as file:
            questions = json.load(file)
    except FileNotFoundError:
        return []
    return questions


def save_questions_json_file(quiz_name: str, quiz_data):
    try:
        with open(f'{quiz_name}.json', 'w') as file:
            json.dump(quiz_data, file)
        print(f"Saved quiz data to {quiz_name}.json")
    except Exception as e:
        print(f"Error saving quiz data: {e}")  
        
def save_questions_to_json(questions):
    with open('quiz_questions.json', 'w') as file:
        json.dump(questions, file)

