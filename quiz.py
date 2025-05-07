#!/usr/bin/env python3
import pygame
import argparse
import sys
import colorsys
import json
import random
import time
import math
import re
import subprocess
from glob import glob
from enum import Enum

from pygame.locals import *

from modules.persistence import *
from modules.checker import *
from modules.elements import *
from modules.gameModes import *
from modules.searchQuiz import search_str_in_file
from modules.otherWindows import about
from modules.pygameTextInput.pygame_textinput import TextInputVisualizer
from modules.constants import *

from modules.AdvancedGameModes.MidasMayhem import midasMayhem
from modules.AdvancedGameModes.MazeRun import mazeRun
from modules.AdvancedGameModes.spaceInvaders import spaceInvaders

class GameMode(str, Enum):
    classic = 'classic'
    classicV2 = 'classicV2'
    speedRun = 'speedRun'
    survival = 'survival'
    practice = 'practice'
    midasMayhem = 'midasMayhem'
    mazeRun = 'mazeRun'
    spaceInvaders = 'spaceInvaders'

def preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v):
    music_old, BACKGROUND_COLOUR_old, BUTTON_COLOUR_old, doCountdown_old, v_old = music, BACKGROUND_COLOUR, BUTTON_COLOUR, doCountdown, v
    running = True
    celebration = False
    numList = re.findall(r'\d+', music)
    i = int(numList[0]) if numList else 1 

    checkbox_countdown = Checkbox("Enable Countdown", (SCREEN_WIDTH // 4, 600), checked=doCountdown)

    volumeSlider = Slider((SCREEN_WIDTH // 4, 175), 800, min=0, max=1, step=0.01, handleColour=(0,0,0), handleRadius=18, initial=v)
    Rslider = Slider((SCREEN_WIDTH // 4, 280), 800, min=0, max=245, step=0.5, handleColour = (255,0,0), initial = BACKGROUND_COLOUR[0])
    Gslider = Slider((SCREEN_WIDTH // 4, 320), 800, min=0, max=245, step=0.5, handleColour = (20,255,50), initial = BACKGROUND_COLOUR[1])
    Bslider = Slider((SCREEN_WIDTH // 4, 360), 800, min=0, max=245, step=0.5, handleColour = (0,0,255), initial = BACKGROUND_COLOUR[2])

    while running:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Preferences", 50, 75, BLACK)
        display_message("_"*85, 50, 40, BLACK)
        display_message("Volume", 120, 40, BLACK)
        display_message("_"*90, 130, 25, BLACK)

        display_message("Colours", 220, 40, BLACK)
        display_message("_"*90, 230, 25, BLACK)

        display_message("Music", 420, 40, BLACK)
        display_message("_"*90, 430, 25, BLACK)

        display_message("General", 560, 40, BLACK)
        display_message("_"*90, 570, 25, BLACK)

        display_message("_"*85, 660, 40, BLACK)

        # Redefined every time to update background colour
        button_music = Button("Change Music", (SCREEN_WIDTH // 2.5, 460), 300, 50, BLACK)
        button_save = Button("Save", (SCREEN_WIDTH // 2.5, 720), 300, 50, BLACK)
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2.5, 780), 300, 50, BLACK)

        checkbox_countdown.draw(screen, text_color=BLACK)
        button_music.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_save.draw(screen, BUTTON_COLOUR)

        volumeSlider.draw(screen)
        Rslider.draw(screen)
        Gslider.draw(screen)
        Bslider.draw(screen)
        pygame.display.flip()
        v = volumeSlider.get()
        R = Rslider.get()
        G = Gslider.get()
        B = Bslider.get()
        BACKGROUND_COLOUR = (R, G, B)
        BUTTON_COLOUR = (R + 10, G + 10, B + 10)
        BLACK = screen_mode(BACKGROUND_COLOUR)
        pygame.mixer.music.set_volume(v)
        #pygame.display.update()
        
        for event in pygame.event.get():
            volumeSlider.handle_event(event)
            Rslider.handle_event(event)
            Gslider.handle_event(event)
            Bslider.handle_event(event)
            checkbox_countdown.handle_event(event)

            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
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
                if isItEasterTimeNow():
                    celebration = True
                    music = "music/music_easter1.ogg"
                if button_music.is_clicked(pos):
                    if i < 7:
                        i += 1
                    else:
                        i = 1
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.unload()
                    music = f'music/music{i}.ogg'
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)
                if button_save.is_clicked(pos):
                    R = Rslider.get()
                    G = Gslider.get()
                    B = Bslider.get()
                    doCountdown = checkbox_countdown.get()
                    BACKGROUND_COLOUR = (R, G, B)
                    BUTTON_COLOUR = (R + 10, G + 10, B + 10)
                    doCountdown_old, v_old = doCountdown, v
                    if not celebration:
                        save_preferences(v, music, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    music_old, BACKGROUND_COLOUR_old, BUTTON_COLOUR_old = music, BACKGROUND_COLOUR, BUTTON_COLOUR
                    print("Saved...")
                if button_go_back.is_clicked(pos):
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(music_old)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(v_old)
                    BLACK = screen_mode(BACKGROUND_COLOUR_old)
                    main(music_old, BACKGROUND_COLOUR_old, BUTTON_COLOUR_old, BLACK, doCountdown_old, v_old)
                    return

def choose_question_amount(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    """
    Function to choose amount of questions for an auto-generated quiz.
    """

    running = True
    button_submit = Button("Submit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 1.2), 300, 40, BLACK)
    question_amount_slider = Slider((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3), 800, min=1, max=250, step=1, initial=30)

    while running:
        events = pygame.event.get()
        for event in events:
            question_amount_slider.handle_event(event)
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_submit.is_clicked(pos):
                    numOfQuestions = question_amount_slider.get()
                    return numOfQuestions

        screen.fill(BACKGROUND_COLOUR)
        question_amount_slider.draw(screen)
        display_message(str(question_amount_slider.get()), SCREEN_HEIGHT // 4, 50, BLACK)
        display_message("Settings", 50, 50, BLACK)
        display_message("Number of Questions:", 125, 40, BLACK)
        button_submit.draw(screen, BUTTON_COLOUR)

        pygame.display.update()

def quizDetails(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, questionList, title, difficulty):
    """
    Function to display the quiz details, including title, difficulty level,
    number of questions, a slider to reduce the number of questions, and the questions themselves.
    """
    running = True
    num_questions = len(questionList)

    try:
        question_slider = Slider((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4), 450, min=1, max=num_questions, step=1, initial=num_questions)
        makeSlider = True
    except ZeroDivisionError:
        makeSlider = False

    scrollbar = None
    if num_questions > 10:
        scrollbar = Scrollbar((SCREEN_WIDTH - 40, 350), 400, num_questions, 10)
    
    button_confirm = Button("Confirm", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100), 300, 50, BLACK)

    offset = 0

    while running:
        events = pygame.event.get()
        for event in events:
            if makeSlider:
                question_slider.handle_event(event)
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_confirm.is_clicked(pos):
                    choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList[:num_questions], title)
                    return
            if scrollbar and (event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION):
                scrollbar.handle_event(event)

        if scrollbar:
            offset = scrollbar.get_offset()

        screen.fill(BACKGROUND_COLOUR)
        if makeSlider:
            question_slider.draw(screen)
            num_questions = question_slider.get()
        display_message(title, 50, 75, BLACK)
        display_message(f"Difficulty: {difficulty}", 120, 50, BLACK)
        display_message(f"Number of Questions: {num_questions}", 175, 50, BLACK)
        display_message("Questions:", 275, 50, BLACK)

        visible_questions = questionList[offset:offset + 10] if scrollbar else questionList
        for idx, question in enumerate(visible_questions):
            display_message(f"• {question}", 350 + idx * 40, 30, BLACK)
                
        if scrollbar:
            scrollbar.draw(screen)
        
        button_confirm.draw(screen, BUTTON_COLOUR)

        pygame.display.update()
                

def choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown):
    textinput = TextInputVisualizer()
    pygame.key.set_repeat(200, 25)

    searchTerm = ""
    user_answer = None
    textinput.font_color = BLACK
    
    button_random_quiz = Button("Random Quiz", (SCREEN_WIDTH // 2 - 150, 400), 300, 40, BLACK)
    button_general_knowledge = Button("General Knowledge Quiz", (SCREEN_WIDTH // 2 - 150, 475), 300, 40, BLACK)
    #button_math = Button("Math Quiz", (SCREEN_WIDTH // 2 - 150, 550), 300, 40, BLACK)

    while True:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Enter Quiz Keyword:", 50, 50, BLACK)
        display_message("Or:", 350, 50, BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                quit()
        textinput.update(events)

        screen.blit(textinput.surface, (500, 100))
        
        button_random_quiz.draw(screen, BUTTON_COLOUR)
        button_general_knowledge.draw(screen, BUTTON_COLOUR)
        #button_math.draw(screen, BUTTON_COLOUR)

        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            searchTerm = textinput.value
            break

        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_random_quiz.is_clicked(pos):
                    quizfiles = glob('./Quizzes/**/*.json', recursive=True)
                    if quizfiles:
                        filename = random.choice(quizfiles)
                        try:
                            questionList, titleofquiz, difficulty, randomOrder = load_quiz(filename)
                            print(f"{titleofquiz} \nQuestions: {questionList}")
                        except Exception as ex:
                            print(f"Error in {filename}: {ex}")
                            break
                        if args.gameMode == None:
                            quizDetails(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, questionList, titleofquiz, difficulty)
                        else:
                            StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, questionList, titleofquiz)
                        return
                elif button_general_knowledge.is_clicked(pos):
                    number_of_questions = choose_question_amount(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                    quizfiles = glob('./Quizzes/**/*.json', recursive=True)
                    if quizfiles:
                        questionList = []
                        for _ in range(number_of_questions):
                            filename = random.choice(quizfiles)
                            try:
                                questions, _, _, _ = load_quiz(filename)
                                question = random.choice(questions)
                                questionList.append(question)
                            except Exception as ex:
                                print(f"Error in {filename}: {ex}")
                                continue
                        titleofquiz = "General Knowledge Quiz"
                        if args.gameMode == None:
                            choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
                        else:
                            StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
                        return

        pygame.display.update()

    quizfiles = glob('./Quizzes/**/*.json', recursive=True)

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
            print(f"Error in quizfile {quizfile}: {ex}!")
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
                questionList, titleofquiz, difficulty, randomOrder = load_quiz(filename)
                if randomOrder:
                    random.shuffle(questionList)
            except Exception as ex:
                print(f"Error in {filename}: {ex}")
                break
            print("Questions:", questionList)
            if args.gameMode == None:
                quizDetails(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, questionList, titleofquiz, difficulty)
                return
            else:
                StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
            
def choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Select Game Mode:", 50, 75, BLACK)
        display_message("Basic Games", 150, 50, BLACK)
        basic_modes = ButtonArray(["Classic", "Classic V2", "Speed Run", "Survival", "Practice"], (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 200), button_width=250, button_spacing=50, text_colour=BLACK)
        display_message("Advanced Games", SCREEN_HEIGHT // 2 + 50, 50, BLACK)
        advanced_modes = ButtonArray(["Midas Mayhem", "Maze Run", "Space Invaders"], (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 + 100), button_width=250, button_spacing=50, text_colour=BLACK)
        basic_modes.draw(screen, BUTTON_COLOUR)
        advanced_modes.draw(screen, BUTTON_COLOUR)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                basic_btn_clicked, btn_basic = basic_modes.handle_click(pos)
                advanced_btn_clicked, btn_advanced = advanced_modes.handle_click(pos)
                btn_clicked = advanced_btn_clicked or basic_btn_clicked

                if btn_clicked:
                    if btn_basic == "Classic":
                        classic(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Classic V2":
                        classicV2(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Speed Run":
                        speed(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Survival":
                        survival(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Practice":
                        practice(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_advanced == "Midas Mayhem":
                        midasMayhem(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_advanced == "Maze Run":
                        mazeRun(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_advanced == "Maze Run":
                        mazeRun(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_advanced == "Space Invaders":
                        spaceInvaders(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                

def StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, questionList=None, titleofquiz=None):
    if args.quizPath != None:
        print("Loading quiz: ", args.quizPath)
        try:
            questionList, titleofquiz, difficulty, randomOrder = load_quiz(args.quizPath)
        except Exception as ex:
            print("Error:", ex)
            sys.exit()
    if args.gameMode is not None:
        if args.gameMode == GameMode.classic:
            try:
                classic(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        elif args.gameMode == GameMode.classicV2:
            try:
                classicV2(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        elif args.gameMode == GameMode.speedRun:
            try:
                speed(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        elif args.gameMode == GameMode.survival:
            try:
                survival(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        elif args.gameMode == GameMode.practice:
            try:
                practice(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        elif args.gameMode == GameMode.midasMayhem:
            try:
                midasMayhem(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        elif args.gameMode == GameMode.mazeRun:
            try:
                mazeRun(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
        elif args.gameMode == GameMode.spaceInvaders:
            try:
                spaceInvaders(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
    # With selected quiz, suppress quiz selection
    elif args.quizPath != None and args.gameMode == None:
        choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
    # Start home page
    elif args.gameMode == None and args.quizPath == None:
        main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, volume)

                   
def main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v):
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
                if button_play.is_clicked(pos):
                    choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown)
                elif button_make.is_clicked(pos):
                    try:
                        subprocess.Popen(["python", "quizcreator"])
                    except:
                        subprocess.Popen(["python3", "quizcreator"])
                elif button_preferences.is_clicked(pos):
                    preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
                elif button_about.is_clicked(pos):
                    about(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                elif button_quit.is_clicked(pos):
                    quit()
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='QuizMaster',
        description='Main program for QuizMaster. Features include: Playing quiz, preferences, description and starting QuizCreator.',
        )
    parser.add_argument('-q', '--quizPath', nargs='?', const="")
    parser.add_argument('-g', '--gameMode', nargs='?', const="", type=GameMode)
    parser.add_argument('-v', '--volume', nargs='?', const="")
    args = parser.parse_args()
        
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()

    print(asciiartstart)
    doCountdown = True
    try:
        with open(".Preferences.json", "r") as file:
            try:
                prefDict = json.load(file)
                volume = prefDict["Volume"]
                doCountdown = prefDict["Countdown"]
                pygame.mixer.music.set_volume(volume)
                if isItHalloweenTimeNow():
                    BACKGROUND_COLOUR = (250,100,0)
                    BUTTON_COLOUR =  (255,110,10)
                    music = "music/music_halloween1.ogg"
                elif isItValentinesTimeNow():
                    music = "music/music_valentines1.ogg"
                    BACKGROUND_COLOUR = (255,0,0)
                    BUTTON_COLOUR =  (255,10,10)
                elif isItStPatricksTimeNow():
                    music = "music/music_stpatrick1.ogg"
                    BACKGROUND_COLOUR = (0,225,0)
                    BUTTON_COLOUR =  (0,200,0) 
                elif isItEasterTimeNow():
                    music = "music/music_easter1.ogg"
                    BACKGROUND_COLOUR = (255,170,180)
                    BUTTON_COLOUR =  (250,250,100)
                elif isItChristmasTimeNow():
                    music = "music/music_christmas1.ogg"
                    BACKGROUND_COLOUR = (0,255,0)
                    BUTTON_COLOUR = (255,0,0)
                else:
                    music = prefDict["Music"]
                    BACKGROUND_COLOUR = prefDict["colour"]
                    BUTTON_COLOUR = prefDict["buttoncolour"]
                    celebration = False
            except:
                volume = DEFAULT_VOLUME
                doCountdown = True
                music = DEFAULT_MUSIC
                BACKGROUND_COLOUR = DEFAULT_BACKGROUND_COLOUR
                BUTTON_COLOUR = DEFAULT_BUTTON_COLOUR
    except FileNotFoundError:
        volume = DEFAULT_VOLUME
        music = DEFAULT_MUSIC
        BACKGROUND_COLOUR = DEFAULT_BACKGROUND_COLOUR
        BUTTON_COLOUR = DEFAULT_BUTTON_COLOUR

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('QuizMaster')
    icon = pygame.image.load('images/logo1.png')
    pygame.display.set_icon(icon)
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    try:
        volume = float(args.volume)
    except Exception:
        pass
    finally:
        pygame.mixer.music.set_volume(volume)
    BLACK = screen_mode(BACKGROUND_COLOUR)
    
    try:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, questionList, titleofquiz)
    except:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown)
