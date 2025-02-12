from typing import List
from dataclasses import dataclass, field
import json


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
     
