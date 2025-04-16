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
    return questionList, titleofquiz

def save_preferences(volume,music,background_colour,button_colour):
   with open(".Preferences.json", 'w') as file:
      try:
        savedData = {"Volume": volume , "Music": music , "colour" : background_colour , "buttoncolour": button_colour}
      except NameError:
        savedData = {"Volume": 0.3 , "Music": 'music/music1.ogg' , "colour" : background_colour , "buttoncolour": button_colour}

      json.dump(savedData, file, default = vars)  
     
