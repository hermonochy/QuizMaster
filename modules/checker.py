import re
import math
from datetime import datetime
from collections import Counter
 
 
def isItCelebrationNow():
  if isItChristmasTimeNow():
    return True
  elif isItHalloweenTimeNow():
    return True
  elif isItEasterTimeNow():
    return True
  elif isItValentinesTimeNow():
    return True
  elif isItStPatricksTimeNow():
    return True
  return False

def isItChristmasTimeNow():
  """
  Function return True, if current date is in range [1-25] December, False otherwise.
  """
  if datetime.now().month == 12 and datetime.now().day <= 25:
    return True
  return False

def isItHalloweenTimeNow():
  """
  Function return True, if current date is in range [1-31] October, False otherwise.
  """
  return datetime.now().month == 10

def isItValentinesTimeNow():
  """
  Function return True, if current date is Valentines.
  """
  if datetime.now().month == 2 and datetime.now().day == 14:
    return True
  return False
  
def isItStPatricksTimeNow():
  """
  Function return True, if current date is Valentines.
  """
  if datetime.now().month == 3 and datetime.now().day == 17:
    return True
  return False  

def isItEasterTimeNow():
  """
  Function return True, if current date is Easter.
  """
  Y = datetime.now().year
  A = Y % 19
  B = Y % 4
  C = Y % 7
  P = math.floor(Y / 100)
  Q = math.floor((13 + 8 * P) / 25)
  M = (15 - Q + P - P // 4) % 30
  N = (4 + P - P // 4) % 7
  D = (19 * A + M) % 30
  E = (2 * B + 4 * C + 6 * D + N) % 7
  days = (22 + D + E)

  if ((D == 29) and (E == 6)):
      easter_date = datetime(Y, 4, 19)
  elif ((D == 28) and (E == 6)):
      easter_date = datetime(Y, 4, 18)
  else:
      if (days > 31):
          easter_date = datetime(Y, 4, days - 31)
      else:
          easter_date = datetime(Y, 3, days)

  today = datetime.now()
  return easter_date.date() == today.date()
       
def is_silly(question, correct_answer, wrong_answers, time_given, question_list):

    if re.search(r'\d{50,}', question) or re.search(r'\d{50,}', correct_answer):
        return True, "Question contains a very long sequence of numbers!"
    
    if re.search(r'^[a-zA-Z0-9]{20,}$', question):
      return True, "Question appears to be a string of random characters!"

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
