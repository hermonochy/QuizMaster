#!/usr/bin/env python3
import pygame
import pygame_widgets
import argparse
import sys
import colorsys
import json
import random
import time
import math
import re
import os
import subprocess
import datetime
import modules.PySimpleGUI as sg

from glob import glob
from enum import Enum
from pygame.locals import *
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button as button
from tkinter import *

from modules.persistence import *
from modules.checker import *
from modules.elements import *
from modules.gameModes import *
from modules.searchQuiz import search_str_in_file
from modules.otherWindows import about
from modules.pygameTextInput.pygame_textinput import TextInputVisualizer

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

class GameMode(str, Enum):
    classic = 'classic'
    classicV2 = 'classicV2'
    speedRun = 'speedRun'
    survival = 'survival'
    practice = 'practice'

def preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v):
    music_old, BACKGROUND_COLOUR_old, BUTTON_COLOUR_old, v_old = music, BACKGROUND_COLOUR, BUTTON_COLOUR, v
    running = True
    celebration = False
    numList = re.findall(r'\d+', music)     
    i = int(numList[0]) if numList else 1 
    screen.fill(BACKGROUND_COLOUR)
    volumeSlider = Slider(screen, SCREEN_WIDTH // 4, 150, 800, 40, min=0, max=1, step=0.005, initial=v, handleRadius=20)
    Rslider = Slider(screen, SCREEN_WIDTH // 4, 280, 800, 40, min=0, max=220, step=0.5, handleColour = (255,0,0), handleRadius=20, initial = BACKGROUND_COLOUR[0])
    Gslider = Slider(screen, SCREEN_WIDTH // 4, 330, 800, 40, min=0, max=245, step=0.5, handleColour = (20,255,50), handleRadius=20, initial = BACKGROUND_COLOUR[1])
    Bslider = Slider(screen, SCREEN_WIDTH // 4, 380, 800, 40, min=0, max=245, step=0.5, handleColour = (0,0,255), handleRadius=20, initial = BACKGROUND_COLOUR[2])
    button_music = button(screen, SCREEN_WIDTH // 2.5, 520, 300, 50, text="Change Music", textColour = BLACK, inactiveColour = BUTTON_COLOUR, shadowDistance = 2, radius = 25)
    button_go_back = button(screen, SCREEN_WIDTH // 2.5, 620, 300, 50, text="Main Menu", textColour = BLACK, inactiveColour = BUTTON_COLOUR, shadowDistance = 2, radius = 25)
    button_cancel = button(screen, SCREEN_WIDTH // 2.5, 680, 300, 50, text="Cancel", textColour = BLACK, inactiveColour = BUTTON_COLOUR, shadowDistance = 2, radius = 25)
    volumeSlider.draw()
    Rslider.draw()
    Gslider.draw()
    Bslider.draw()
    button_music.draw()
    button_go_back.draw()
    button_cancel.draw()
    screen.fill(BACKGROUND_COLOUR)
    display_message("Preferences", 50, 75, BLACK)
    display_message("_"*125, 50, 40, BLACK)
    display_message("Volume", 120, 40, BLACK)
    display_message("_"*100, 130, 25, BLACK)
    
    display_message("Colours", 230, 40, BLACK)
    display_message("_"*100, 240, 25, BLACK)

    display_message("Music", 485, 40, BLACK)
    display_message("_"*100, 495, 25, BLACK)
    display_message("_"*125, 550, 40, BLACK)

    while running:
        R = Rslider.getValue()
        G = Gslider.getValue()
        B = Bslider.getValue()
        BACKGROUND_COLOUR = (R, G, B)
        BUTTON_COLOUR = (R + 10, G + 10, B + 10)
        BLACK = screen_mode(BACKGROUND_COLOUR)

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()
        v = volumeSlider.getValue()
        pygame.mixer.music.set_volume(v)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_music.contains(*pos):
                    if i < 7:
                        i += 1
                    else:
                        i = 1
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.unload()
                    music = f'music/music{i}.ogg'
                    if isItChristmasTimeNow():
                        celebration = True
                        music = ["music/music_christmas1.ogg", "music/music_christmas2.ogg"][i % 2]
                    if isItHalloweenTimeNow():
                        celebration = True
                        music = ["music/music_halloween1.ogg", "music/music_halloween2.ogg"][i % 2]
                    if isItStPatricksTimeNow():
                        celebration = True
                        music = "music/music_stpatricks1.ogg"
                    if isItValentinesTimeNow():
                        celebration = True
                        music = "music/music_valentines1.ogg"
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)
                if button_go_back.contains(*pos):
                    volumeSlider.hide()
                    Rslider.hide()
                    Gslider.hide()
                    Bslider.hide()
                    button_music.hide()
                    button_go_back.hide()
                    button_cancel.hide()
                    if not celebration:
                        save_preferences(v, music, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v)
                if button_cancel.contains(*pos):
                    volumeSlider.hide()
                    Rslider.hide()
                    Gslider.hide()
                    Bslider.hide()
                    button_music.hide()
                    button_go_back.hide()
                    button_cancel.hide()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(music_old)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(v_old)
                    main(music_old, BACKGROUND_COLOUR_old, BUTTON_COLOUR_old, BLACK, v_old)
                    return

def choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    searchTerm = ""
    user_answer = None
    textinput.font_color = BLACK
    while True:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Enter Quiz Keyword:", 30, 50, BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                quit()
        textinput.update(events)

        screen.blit(textinput.surface, (500, 100))

        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            searchTerm = textinput.value
            break

        pygame.display.update()
        pygame.time.wait(30)

    quizfiles = glob('./quizzes/**/*.json', recursive=True)

    quizfileSearchResults = []
    for file in quizfiles:
        if search_str_in_file(file, searchTerm):
            quizfileSearchResults.append(file)

    if not quizfileSearchResults:
        display_message("No Matching Quizzes found!", SCREEN_HEIGHT // 2, 75, (255,0,0))
        pygame.display.update()
        pygame.time.wait(250)
        choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        return
        
    scrollbar = Scrollbar((SCREEN_WIDTH - 40, ANSWER_OFFSET), SCREEN_HEIGHT - ANSWER_OFFSET - 50, len(quizfileSearchResults), 10)
    buttons = []
    for idx, quizfile in enumerate(quizfileSearchResults):
        try:
            with open(quizfile, "r", errors="ignore") as file:
                quiztitle = json.load(file)["title"]
            button = Button(quiztitle, (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40, BLACK)
            buttons.append(button)
        except json.decoder.JSONDecodeError as ex:
            print(f"Error in quizfile {quizfile}! {ex}")
            continue

    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        for button in buttons:
            button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
        if len(buttons) > 12:    
           scrollbar.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
                scrollbar.handle_event(event)
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for idx, button in enumerate(buttons):
                    if button.is_clicked(pos):
                        user_answer = idx

        offset = scrollbar.get_offset()
        for idx, button in enumerate(buttons):
            button.position = (SCREEN_WIDTH // 2 - 150, 100 + (idx - offset) * OPTION_HEIGHT)
            button.rect.topleft = button.position

        if user_answer is not None:
            filename = quizfileSearchResults[user_answer]

            try:
                questionList, titleofquiz  = load_quiz(filename)
            except Exception as ex:
                print(f"Error in {filename}: {ex}")               
                break
                break
            print("Questions:", questionList)
            if args.gameMode == None:
                choose_game(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
                return
            else:
                StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
            
def choose_game(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Select Game Mode:", SCREEN_HEIGHT // 2 - 300, 75, BLACK)
        button_classic = Button("Classic", (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 200), 250, 60, BLACK)
        button_classicV2 = Button("Classic v2.0", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200), 250, 60, BLACK)
        button_speed = Button("Speed Run", (SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2 - 200), 250, 60, BLACK)
        button_survival = Button("Survival", (SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 - 200), 250, 60, BLACK)
        button_practice = Button("Practice", (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 100), 250, 60, BLACK)           
        button_classic.draw(screen, BUTTON_COLOUR)
        button_classicV2.draw(screen, BUTTON_COLOUR)
        button_speed.draw(screen, BUTTON_COLOUR)
        button_survival.draw(screen, BUTTON_COLOUR)
        button_practice.draw(screen, BUTTON_COLOUR)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                event_time = pygame.time.get_ticks()
                if button_classic.is_clicked(pos):
                    classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_classicV2.is_clicked(pos):
                    classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_speed.is_clicked(pos):
                    speed(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_survival.is_clicked(pos):
                    survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_practice.is_clicked(pos):
                    practice(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                

def StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList=None, titleofquiz=None):
    if args.gameMode == GameMode.classic:
        try:
            classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
    if args.gameMode == GameMode.classicV2:
        try:
            classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
    if args.gameMode == GameMode.speedRun:
        try:
            speed(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
    if args.gameMode == GameMode.survival:
        try:
            survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
    if args.gameMode == GameMode.practice:
        try:
            practice(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)

    if args.quizPath != None and args.gameMode == None:
        choose_game(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
    if args.gameMode == None:
        main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v)

                   
def main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v):
    running = True
    welcome_image = pygame.image.load("images/logo.png").convert()
    while running:
        screen.fill(BACKGROUND_COLOUR)
        button_play = Button("Play a Quiz", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 50), 250, 60, BLACK)
        button_make = Button("Make a Quiz", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50), 250, 60, BLACK)
        button_preferences = Button("Preferences", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 50), 250, 60, BLACK)
        button_about = Button("About", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 50), 250, 60, BLACK)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 150), 250, 60, BLACK)
        display_message("Welcome to QuizMaster!", SCREEN_HEIGHT // 8, 75, BLACK)
        button_make.draw(screen, BUTTON_COLOUR)
        button_play.draw(screen, BUTTON_COLOUR)
        button_preferences.draw(screen, BUTTON_COLOUR)
        button_about.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)
        screen.blit(welcome_image, (SCREEN_WIDTH//4.75, SCREEN_HEIGHT//12))
        screen.blit(welcome_image, (SCREEN_WIDTH//1.325, SCREEN_HEIGHT//12))
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_quit.is_clicked(pos):
                    quit()
                if button_make.is_clicked(pos):
                    try:
                        subprocess.Popen(["python3", "quizcreator"])
                    except:
                        subprocess.Popen(["python", "quizcreator"])
                if button_preferences.is_clicked(pos):
                    preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v)
                if button_about.is_clicked(pos):
                    about(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                if button_play.is_clicked(pos):
                    choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='QuizMaster',
        description='Main program for QuizMaster. Features include: Playing quiz, preferences, description and starting QuizCreator.',
        )
    parser.add_argument('-q', '--quizPath', nargs='?', const="")
    parser.add_argument('-g', '--gameMode', nargs='?', const="", type=GameMode)
    parser.add_argument('-v', '--volume', nargs='?', const="")
    args = parser.parse_args()

    if args.quizPath != None:
        print("Loading quiz: ", args.quizPath)
        try:
            questionList, titleofquiz = load_quiz(args.quizPath)
        except Exception as ex:
            print("Error:", ex)
            sys.exit()

    print(asciiartstart)

    try:
        with open(".Preferences.json", "r") as file:
            try:
                prefDict = json.load(file)
                v = prefDict["Volume"]
                pygame.mixer.music.set_volume(v)
                if isItHalloweenTimeNow():
                    colour = (250,100,0)
                    button_colour =  (255,110,10)
                    music = "music/music_halloween1.ogg"
                elif isItValentinesTimeNow():
                    music = "music/music_valentines1.ogg"
                    colour = (255,0,0)
                    button_colour =  (255,10,10)
                elif isItStPatricksTimeNow():
                    music = "music/music_stpatrick1.ogg"
                    colour = (0,225,0)
                    button_colour =  (0,200,0) 
                elif isItChristmasTimeNow():
                    music = "music/music_christmas1.ogg"
                    colour = (0,255,0)
                    button_colour = (255,0,0)         
                else:
                    music = prefDict["Music"]
                    colour = prefDict["colour"]
                    button_colour = prefDict["buttoncolour"] 
                    celebration = False
            except json.JSONDecodeError:
                v = 1.0
                music = 'music/music1.ogg'
                colour = (0,245,0)
                button_colour = (0,255,0)
    except FileNotFoundError:
        v = 1.0
        music = 'music/music1.ogg'
        colour = (0,245,0)
        button_colour = (0,255,0)
        
    textinput = TextInputVisualizer()
    pygame.key.set_repeat(200, 25)
         
    BACKGROUND_COLOUR = colour
    BUTTON_COLOUR = button_colour

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('QuizMaster')
    icon = pygame.image.load('images/logo1.png')
    pygame.display.set_icon(icon)
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    try:
        v = float(args.volume)
    except Exception:
        pass
    finally:
        pygame.mixer.music.set_volume(v)
    BLACK = screen_mode(BACKGROUND_COLOUR)
    
    try:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
    except:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
