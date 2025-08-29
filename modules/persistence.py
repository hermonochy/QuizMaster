import json
import platform
import subprocess
import os

from typing import List,Union
from dataclasses import dataclass, field

from modules.constants import *

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

def save_preferences(volume,music,do_countdown,do_instructions,background_colour,button_colour):
   with open(".Preferences.json", 'w') as file:
      try:
        savedData = {"Volume": volume , "Music": music , "Countdown" : do_countdown, "Instructions": do_instructions, "colour" : background_colour , "buttoncolour": button_colour}
      except NameError:
        print("Unable to save...")

      json.dump(savedData, file, default = vars)

def getPreferences():
    doCountdown = True
    doInstructions = True
    try:
        with open(".Preferences.json", "r") as file:
            try:
                prefDict = json.load(file)
                volume = prefDict["Volume"]
                doCountdown = prefDict["Countdown"]
                doInstructions = prefDict["Instructions"]
                pygame.mixer.music.set_volume(volume)
                if isItHalloweenTimeNow():
                    BACKGROUND_COLOUR = (250,100,0)
                    BUTTON_COLOUR =  (255,110,10)
                    music = "sounds/music_halloween1.ogg"
                elif isItValentinesTimeNow():
                    music = "sounds/music_valentines1.ogg"
                    BACKGROUND_COLOUR = (255,0,0)
                    BUTTON_COLOUR =  (255,10,10)
                elif isItStPatricksTimeNow():
                    music = "sounds/music_stpatrick1.ogg"
                    BACKGROUND_COLOUR = (0,225,0)
                    BUTTON_COLOUR =  (0,200,0) 
                elif isItEasterTimeNow():
                    music = "sounds/music_easter1.ogg"
                    BACKGROUND_COLOUR = (255,170,180)
                    BUTTON_COLOUR =  (250,250,100)
                elif isItChristmasTimeNow():
                    music = "sounds/music_christmas1.ogg"
                    BACKGROUND_COLOUR = (0,255,0)
                    BUTTON_COLOUR = (255,0,0)
                else:
                    music = prefDict["Music"]
                    BACKGROUND_COLOUR = prefDict["colour"]
                    BUTTON_COLOUR = prefDict["buttoncolour"]
                    celebration = False
            except:
                volume = DEFAULT_VOLUME
                doCountdown = DEFAULT_COUNTDOWN
                doInstructions = DEFAULT_INSTRUCTIONS
                music = DEFAULT_MUSIC
                BACKGROUND_COLOUR = DEFAULT_BACKGROUND_COLOUR
                BUTTON_COLOUR = DEFAULT_BUTTON_COLOUR
    except FileNotFoundError:
        volume = DEFAULT_VOLUME
        doCountdown = DEFAULT_COUNTDOWN
        doInstructions = DEFAULT_INSTRUCTIONS
        music = DEFAULT_MUSIC
        BACKGROUND_COLOUR = DEFAULT_BACKGROUND_COLOUR
        BUTTON_COLOUR = DEFAULT_BUTTON_COLOUR
    return volume, doCountdown, doInstructions, music, BACKGROUND_COLOUR, BUTTON_COLOUR

     
def openFile(file_path):
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", file_path])
    else:
        subprocess.run(["xdg-open", file_path])