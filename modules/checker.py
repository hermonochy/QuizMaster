import datetime
import re
from collections import Counter

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
       
       
def is_silly(question, correct_answer, wrong_answers, time_given, question_list):

    if re.search(r'\d{10,}', question):
        return True, "Question contains a very long sequence of numbers!"

    if len(set(wrong_answers)) != len(wrong_answers):
        return True, "Wrong answers are identical!"

    if correct_answer in wrong_answers:
        return True, "A wrong answer is the same as the correct answer!"

    question_counter = Counter((q.question, q.correctAnswer, tuple(q.wrongAnswers)) for q in question_list)
    if question_counter[(question, correct_answer, tuple(wrong_answers))] > 10:
        return True, "There are more than 10 identical questions!"
    
    if len(wrong_answers) > 9:
        return True, "Too many wrong answer options!"

    if time_given < 5:
      return True, f"{time_given} seconds is not enough!"

    return False, ""
