from typing import List
from dataclasses import dataclass, field
import json
import datetime
import re
from collections import Counter

@dataclass
class QuizQuestion:
   question: str
   correctAnswer: str
   wrongAnswers: List[str]
   timeout: int = field(default=15)
   
   def __repr__(self):
      return self.question
     
     
asciiartstart="""
  ___                _            ___  ___                     __                        __
 / _ \     _   _    (_)    ____   |  \/  |     __ _     ___    | |_      ___     _ __    | |
| | | |   | | | |   | |   |_  /   | |\/| |    / _` |   / __|   | __|    / _ \   | '__|   | |
| |_| |   | |_| |   | |    / /    | |  | |   | (_| |   \__ \   | |_    |  __/   | |      |_|
 \__\_\    \__,_|   |_|   /___|   |_|  |_|    \__,_|   |___/    \__|    \___|   |_|      (_)
                                                                     
"""                     

asciiartend="""

 ____                         _ 
| __ )     _   _      ___    | |
|  _ \    | | | |    / _ \   | |
| |_) |   | |_| |   |  __/   |_|
|____/     \__, |    \___|   (_)
           |___/                

"""

def save_preferences(volume,music,background_colour,button_colour):
   with open(".Preferences.json", 'w') as file:
      try:
        savedData = {"Volume": volume , "Music": music , "colour" : background_colour , "buttoncolour": button_colour}
      except NameError:
        savedData = {"Volume": 0.3 , "Music": 'music/music1.ogg' , "colour" : background_colour , "buttoncolour": button_colour}

      json.dump(savedData, file, default = vars)  
     
def isItChristmasTimeNow():
  """
  Function return True, if current date is in range [1-25] December, False otherwise.
  """
  if datetime.datetime.now().month == 12 and datetime.datetime.now().day <= 25:
    return True
  return False

def isItHalloweenTimeNow():
  """
  Function return True, if current date is in range [1-31] October, False otherwise.
  """
  return datetime.datetime.now().month == 10

def isItValentinesTimeNow():
  """
  Function return True, if current date is Valentines.
  """
  if datetime.datetime.now().month == 2 and datetime.datetime.now().day == 14:
    return True
  return False
  
def isItStPatricksTimeNow():
  """
  Function return True, if current date is Valentines.
  """
  if datetime.datetime.now().month == 3 and datetime.datetime.now().day == 17:
    return True
  return False  
       
       
def is_silly(question, correct_answer, wrong_answers, question_list):

    if re.search(r'\d{10,}', question):
        return True, "Question contains a very long sequence of numbers."

    if len(set(wrong_answers)) != len(wrong_answers):
        return True, "Wrong answers are identical!"

    if correct_answer in wrong_answers:
        return True, "A wrong answer is the same as the correct answer!"

    question_counter = Counter((q.question, q.correctAnswer, tuple(q.wrongAnswers)) for q in question_list)
    if question_counter[(question, correct_answer, tuple(wrong_answers))] > 10:
        return True, "There are more than 10 identical questions."

    return False, ""
