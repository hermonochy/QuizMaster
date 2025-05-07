from typing import List,Union
from dataclasses import dataclass, field
import json


@dataclass
class QuizQuestion:
   question: str
   correctAnswer: Union[str,int,float,bool]
   wrongAnswers: List[Union[str,int,float,bool]]
   timeout: int = field(default=15)
   
   def __repr__(self):
      return self.question

def load_quiz(filename):
    with open(filename, 'r') as file:
        quizDicts = json.load(file)
        questionList = []
        for q in quizDicts["listOfQuestions"]:
            qq = QuizQuestion(**q)
            questionList.append(qq)
        titleofquiz = quizDicts["title"]
        difficulty = quizDicts.get("difficulty", 3)
        randomOrder = quizDicts.get("randomOrder", False)
    return questionList, titleofquiz, difficulty, randomOrder

def save_preferences(volume,music,do_countdown,background_colour,button_colour):
   with open(".Preferences.json", 'w') as file:
      try:
        savedData = {"Volume": volume , "Music": music , "Countdown" : do_countdown, "colour" : background_colour , "buttoncolour": button_colour}
      except NameError:
        print("Unable to save...")

      json.dump(savedData, file, default = vars)
     
