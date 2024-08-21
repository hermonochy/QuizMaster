import json
import os
from typing import List
from dataclasses import dataclass, field

@dataclass
class QuizQuestion:
   question: str
   correctAnswer: str
   wrongAnswers: List[str]
   timeout: int = field(default=10)
   
   #def __post_init__(self):
   #     if self.timeout is None:
   #         self.timeout = 10
   
   def __repr__(self):
      return self.question
     

def load_questions_from_json():
    try:
        with open('quiz_questions.json', 'r') as file:
            questions = json.load(file)
    except FileNotFoundError:
        return []
    return questions
    
class NoQuizTitleException(Exception):
   ...    
    
def load_quiz(jsonfilename):
    try:
        with open(jsonfilename , 'r') as file:
            quizdata = json.load(file)
            if not 'title' in quizdata.keys():
                raise NoQuizTitleException
    except FileNotFoundError:
        return None
    return quizdata
    


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

