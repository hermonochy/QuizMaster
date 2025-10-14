import pygame
import argparse

from enum import Enum
from pygame.locals import *

from modules.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from modules.persistence import getPreferences
from modules.extendedText import asciiartstart

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.init()

class GameMode(str, Enum):
    classic = 'classic'
    classicV2 = 'classicV2'
    speedRun = 'speedRun'
    survival = 'survival'
    practice = 'practice'
    midasMayhem = 'midasMayhem'
    mazeRun = 'mazeRun'
    spaceInvaders = 'spaceInvaders'
    strikeZone = 'strikeZone'
    deathRain = 'deathRain'
    farmFrenzy = 'farmFrenzy'
    quickClick = 'quickClick'

parser = argparse.ArgumentParser(
    prog='QuizMaster',
    description='Main program for QuizMaster. Features include: Playing quiz, preferences, description and starting QuizCreator.',
    )
parser.add_argument('-q', '--quizPath', nargs='?', const="")
parser.add_argument('-g', '--gameMode', nargs='?', const="", type=GameMode)
parser.add_argument('-v', '--volume', nargs='?', const="")
args = parser.parse_args()
    
clock = pygame.time.Clock()
print("\nQuizMaster Copyright (C) 2025 hermonochy")
print(asciiartstart)

volume, doCountdown, doInstructions, music, BACKGROUND_COLOUR, BUTTON_COLOUR = getPreferences()
pygame.display.set_caption('QuizMaster')
icon = pygame.image.load('images/Screenshots/logo1.png')
pygame.display.set_icon(icon)
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)
try:
    volume = float(args.volume)
except Exception:
    pass
pygame.mixer.music.set_volume(volume)