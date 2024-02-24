import json
import os

def load_questions_from_json():
    try:
        with open('quiz_questions.json', 'r') as file:
            questions = json.load(file)
    except FileNotFoundError:
        return []
    return questions

def delete_questions_json_file():
    try:
        os.remove('quiz_questions.json')
        print("Deleted quiz_questions.json file")
    except FileNotFoundError:
        print("quiz_questions.json file not found")  
        
def save_questions_to_json(questions):
    with open('quiz_questions.json', 'w') as file:
        json.dump(questions, file)

