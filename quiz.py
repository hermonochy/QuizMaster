#!/usr/bin/env python3

import pygame
import sys
import colorsys
import json
import random
import time
#import math
import re
import subprocess
from glob import glob

from pygame.locals import *

from modules.initialise import *
from modules.persistence import *
from modules.checker import *
from modules.elements import *
from modules.gameModes import classic, classicV2, speedRun, survival, practice
from modules.searchQuiz import search_str_in_file
from modules.otherWindows import about
from modules.math import returnQuiz
from modules.constants import *
from modules.overlays import drawSpiderWebs

from modules.AdvancedGameModes.spaceInvaders import spaceInvaders
from modules.AdvancedGameModes.strikeZone import strikeZone
from modules.AdvancedGameModes.farmFrenzy import farmFrenzy
from modules.AdvancedGameModes.blastField import blastField
from modules.AdvancedGameModes.MidasMayhem import midasMayhem
from modules.AdvancedGameModes.MazeRun import mazeRun
from modules.AdvancedGameModes.deathRain import deathRain
from modules.AdvancedGameModes.quickClick import quickClick

def preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, doInstructions, v):
    music_orig, BACKGROUND_COLOUR_orig, BUTTON_COLOUR_orig, doCountdown_orig, doInstructions_orig, v_orig = (
        music, BACKGROUND_COLOUR, BUTTON_COLOUR, doCountdown, doInstructions, v
    )
    running = True
    changes = False
    celebration = isItCelebrationNow()
    numList = re.findall(r'\d+', music)
    i = int(numList[0]) if numList else 1
    songPos = False # variable to alternate between celebration music, if more than one is avalible

    checkbox_countdown = Checkbox("Enable Countdown", (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 280), checked=doCountdown)
    checkbox_instructions = Checkbox("Enable Instructions", (SCREEN_WIDTH // 4, SCREEN_HEIGHT  - 230), checked=doInstructions)
    checkbox_mute = Checkbox("Mute", (SCREEN_WIDTH // 4, 165), checked=(v==0))

    volumeSlider = Slider((SCREEN_WIDTH // 4 + 150, 175), 550, min=0, max=1, step=0.05, handleColour=(0,0,0), handleRadius=18, initial=v)
    Rslider = Slider((SCREEN_WIDTH // 4, 280), 700, min=0, max=245, step=0.5, handleColour = (255,0,0), initial = BACKGROUND_COLOUR[0])
    Gslider = Slider((SCREEN_WIDTH // 4, 320), 700, min=0, max=245, step=0.5, handleColour = (0,240,0), initial = BACKGROUND_COLOUR[1])
    Bslider = Slider((SCREEN_WIDTH // 4, 360), 700, min=0, max=245, step=0.5, handleColour = (0,0,255), initial = BACKGROUND_COLOUR[2])

    session_music = music
    session_BG = BACKGROUND_COLOUR
    session_BTN = BUTTON_COLOUR
    session_v = v
    session_doCountdown = doCountdown
    session_doInstructions = doInstructions
    session_BLACK = BLACK

    while running:
        if not checkbox_mute.get():
            session_v = volumeSlider.get()
        else:
            session_v = 0
        R = Rslider.get()
        G = Gslider.get()
        B = Bslider.get()
        session_BG = (R, G, B)
        if all(i < 245 for i in (R, G, B)):
            session_BTN = (clamp(R + 10), clamp(G + 10), clamp(B + 10))
        else:
            session_BTN = (clamp(R - 10), clamp(G - 10), clamp(B - 10))

        session_BLACK = screen_mode(session_BG)
        pygame.mixer.music.set_volume(session_v)

        screen.fill(session_BG)
        display_message("Preferences", 50, 75, session_BLACK)
        display_message("_"*85, 50, 40, session_BLACK)
        display_message("Volume", 120, 40, session_BLACK)
        display_message("_"*90, 130, 25, session_BLACK)

        display_message("Colours", 220, 40, session_BLACK)
        display_message("_"*90, 230, 25, session_BLACK)

        display_message("Music", 420, 40, session_BLACK)
        display_message("_"*90, 430, 25, session_BLACK)

        display_message("General", 560, 40, session_BLACK)
        display_message("_"*90, 570, 25, session_BLACK)

        display_message("_"*85, 660, 40, session_BLACK)

        # Redefined every time to update background colour
        button_music = Button("Change Music", (SCREEN_WIDTH // 2.5, 460), 300, 50, session_BLACK)
        button_save = Button("Save", (SCREEN_WIDTH // 2.5, 720), 300, 50, session_BLACK)
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2.5, 780), 300, 50, session_BLACK)
        checkbox_mute.draw(screen, text_color=session_BLACK)
        checkbox_countdown.draw(screen, text_color=session_BLACK)
        checkbox_instructions.draw(screen, text_color=session_BLACK)
        button_music.draw(screen, session_BTN)
        button_go_back.draw(screen, session_BTN)
        button_save.draw(screen, session_BTN)

        volumeSlider.draw(screen)
        Rslider.draw(screen)
        Gslider.draw(screen)
        Bslider.draw(screen)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)

        pygame.display.flip()
        
        for event in pygame.event.get():

            songPos = not songPos

            volumeSlider.handle_event(event)
            Rslider.handle_event(event)
            Gslider.handle_event(event)
            Bslider.handle_event(event)
            checkbox_countdown.handle_event(event)
            checkbox_instructions.handle_event(event)
            checkbox_mute.handle_event(event)

            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_music.is_clicked(pos):
                    if i <= 6:
                        i += 1
                    else:
                        i = 1
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.unload()
                    session_music = f'sounds/music{i}.ogg'
                    if isItChristmasTimeNow():
                        session_music = ["sounds/music_christmas1.ogg", "sounds/music_christmas2.ogg"][int(songPos)]
                    elif isItHalloweenTimeNow():
                        session_music = ["sounds/music_halloween1.ogg", "sounds/music_halloween2.ogg"][int(songPos)]
                    elif isItStPatricksTimeNow():
                        session_music = "sounds/music_stpatricks1.ogg"
                    elif isItValentinesTimeNow():
                        session_music = "sounds/music_valentines1.ogg"
                    elif isItEasterTimeNow():
                        session_music = "sounds/music_easter1.ogg"
                    pygame.mixer.music.load(session_music)
                    pygame.mixer.music.play(-1)
                if button_save.is_clicked(pos):
                    session_doCountdown = checkbox_countdown.get()
                    session_doInstructions = checkbox_instructions.get()
                    session_BG = (Rslider.get(), Gslider.get(), Bslider.get())
                    if all(i < 245 for i in session_BG):
                        session_BTN = (clamp(session_BG[0] + 10), clamp(session_BG[1] + 10), clamp(session_BG[2] + 10))
                    else:
                        session_BTN = (clamp(session_BG[0] - 10), clamp(session_BG[1] - 10), clamp(session_BG[2] - 10))
                    save_music = session_music
                    if not celebration:
                        save_preferences(session_v, save_music, session_doCountdown, session_doInstructions, session_BG, session_BTN)
                        print("Saved...")
                    music_orig = save_music
                    BACKGROUND_COLOUR_orig = session_BG
                    BUTTON_COLOUR_orig = session_BTN
                    v_orig = session_v
                    doCountdown_orig = session_doCountdown
                    doInstructions_orig = session_doInstructions
                    session_BLACK = screen_mode(BACKGROUND_COLOUR_orig)
                    BLACK = session_BLACK
                if button_go_back.is_clicked(pos):
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(music_orig)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(v_orig)
                    BLACK = screen_mode(BACKGROUND_COLOUR_orig)
                    return BLACK, v_orig, doCountdown_orig, doInstructions_orig, music_orig, BACKGROUND_COLOUR_orig, BUTTON_COLOUR_orig


def choose_question_amount(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    """
    Function to choose amount of questions for an auto-generated quiz.
    """

    running = True
    button_go_back = Button("Go Back", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 1.2), 300, 40, BLACK)
    button_submit = Button("Choose", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 1.3), 300, 40, BLACK)
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
                    return numOfQuestions, False
                elif button_go_back.is_clicked(pos):
                    numOfQuestions = question_amount_slider.get()
                    return numOfQuestions, True

        screen.fill(BACKGROUND_COLOUR)
        question_amount_slider.draw(screen)
        display_message(str(question_amount_slider.get()), SCREEN_HEIGHT // 4, 50, BLACK)
        display_message("Settings", 50, 50, BLACK)
        display_message("Number of Questions:", 125, 40, BLACK)
        button_submit.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)

        pygame.display.update()

def quizDetails(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, doCountdown, doInstructions, questionList, title, difficulty):
    """
    Function to display the quiz details, including title, difficulty level,
    number of questions, a slider to reduce the number of questions, and the questions themselves.
    """
    running = True
    num_questions_total = len(questionList)
    visible_per_page = 10
    useSlider = True
    try:
        question_slider = Slider((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4), 450, min=1, max=num_questions_total, step=1, initial=num_questions_total)
    except ZeroDivisionError:
        useSlider = False

    button_confirm = Button("Choose", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 290), 350, 50, BLACK)
    button_go_back = Button("Go Back", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 350), 350, 50, BLACK)
    menuButton = menuButtons(BLACK)
    scrollbar = None
    offset = 0

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                quit()
            if useSlider:
                question_slider.handle_event(event)
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                menuButton.handle_click(pos)
                if button_confirm.is_clicked(pos):
                    choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList[:current_count], title)
                    return False
                elif button_go_back.is_clicked(pos):
                    if popup("Go Back?", "Are you sure you want to go back?", buttons=("Return", "Stay")) == "Return":
                        return True
                    else:
                        continue
            if scrollbar:
                scrollbar.handle_event(event)

        if useSlider:
            current_count = question_slider.get()
        else: 
            current_count = len(questionList)

        if current_count > visible_per_page:
            if not scrollbar or scrollbar.total_items != current_count:
                scrollbar = Scrollbar((SCREEN_WIDTH - 40, 300), 400, current_count, visible_per_page)
            offset = scrollbar.get_offset()
            offset = max(0, min(offset, current_count - visible_per_page))
            visible_questions = questionList[:current_count][offset:offset + visible_per_page]
        else:
            scrollbar = None
            offset = 0
            visible_questions = questionList[:current_count]

        screen.fill(BACKGROUND_COLOUR)
        if useSlider:
            question_slider.draw(screen)
        display_message(title, 50, 75, BLACK)
        display_message(f"Difficulty: {difficulty}", 120, 50, BLACK)
        display_message(f"Number of Questions: {current_count}", 175, 50, BLACK)
        display_message("Questions:", 275, 50, BLACK)

        for idx, question in enumerate(visible_questions):
            display_message(f"• {question}", 350 + idx * 40, 30, BLACK)

        if scrollbar:
            scrollbar.draw(screen)

        button_confirm.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        menuButton.draw(screen, BUTTON_COLOUR)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)

        pygame.display.update()

def choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v):
    searchTerm = ""
    user_answer = None
    searchBox = TextBox(SCREEN_WIDTH // 2 - 250, 120, 550, 54, text_color=(0,0,0), placeholder="Enter quiz keyword (e.g. history, science...)", border_radius=14)

    while True:
        button_random_quiz = Button("Random Quiz", (SCREEN_WIDTH // 2 - 150, 400), 300, 40, BLACK)
        button_general_knowledge = Button("General Knowledge Quiz", (SCREEN_WIDTH // 2 - 150, 475), 300, 40, BLACK)
        button_math = Button("Math Quiz", (SCREEN_WIDTH // 2 - 150, 550), 300, 40, BLACK)
        menuButton = menuButtons(BLACK)
        screen.fill(BACKGROUND_COLOUR)
        display_message("Search for a Quiz", 50, 50, BLACK)
        display_message("Or:", 350, 50, BLACK)
        searchBox.draw(screen)
        button_random_quiz.draw(screen, BUTTON_COLOUR)
        button_general_knowledge.draw(screen, BUTTON_COLOUR)
        button_math.draw(screen, BUTTON_COLOUR)
        menuButton.draw(screen, BUTTON_COLOUR)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)

        for event in pygame.event.get():
            searchBox.handle_event(event)
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menuButton.handle_click(pos):
                    return
                if button_random_quiz.is_clicked(pos):
                    quizfiles = glob('./Quizzes/**/*.json', recursive=True)
                    if quizfiles:
                        filename = random.choice(quizfiles)
                        try:
                            questionList, titleofquiz, difficulty, randomOrder = load_quiz(filename)
                            print(f"{titleofquiz} \nQuestions: {questionList}\n\n")
                        except Exception as ex:
                            print(f"Error in {filename}: {ex}")
                            break
                        if args.gameMode == None:
                            searchAgain = quizDetails(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, doCountdown, doInstructions, questionList, titleofquiz, difficulty)
                            if searchAgain:
                                break
                            else:
                                return
                        else:
                            StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz)
                        return
                elif button_general_knowledge.is_clicked(pos):
                    number_of_questions, goBack = choose_question_amount(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                    if goBack:
                        break
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
                            choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz)
                        else:
                            StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz)
                        return
                elif button_math.is_clicked(pos):
                    number_of_questions, goBack = choose_question_amount(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                    if goBack:
                        break
                    titleofquiz, questionList = returnQuiz(number_of_questions)
                    if args.gameMode == None:
                        choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz)
                    else:
                        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz)
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and searchBox.active:
                searchTerm = searchBox.get().strip()
                break

        pygame.display.update()

        if searchTerm != "":
            quizfiles = glob('./Quizzes/**/*.json', recursive=True)
            quizfileSearchResults = []
            for file in quizfiles:
                if search_str_in_file(file, searchTerm):
                    quizfileSearchResults.append(file)

            if not quizfileSearchResults:
                display_message("No Matching Quizzes found!", SCREEN_HEIGHT // 4, 80, (255,0,0))
                pygame.display.update()
                pygame.time.wait(800)
                searchTerm = ""
                continue

            scrollbar = Scrollbar((SCREEN_WIDTH - 75, ANSWER_OFFSET-15), SCREEN_HEIGHT - ANSWER_OFFSET - 100, len(quizfileSearchResults), 10)
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
            user_answer = None
            while running:
                screen.fill(BACKGROUND_COLOUR)
                for button in buttons:
                    button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
                if len(buttons) > 12:
                    scrollbar.draw(screen)
                menuButton.draw(screen, BUTTON_COLOUR)
                if isItHalloweenTimeNow():
                    drawSpiderWebs(screen)

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
                        scrollbar.handle_event(event)
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if menuButton.handle_click(pos):
                            return
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
                        searchAgain = quizDetails(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, doCountdown, doInstructions, questionList, titleofquiz, difficulty)
                        if searchAgain:
                            break
                        else:
                            return
                    else:
                        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz)
            searchTerm = ""

def choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Select Game Mode:", 50, 75, BLACK)
        display_message("Basic Games", 150, 50, BLACK)
        basic_modes = ButtonArray(["Classic", "Classic V2", "Speed Run", "Survival", "Practice"], (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 200), button_width=250, button_spacing=50, text_colour=BLACK)
        display_message("Advanced Games", SCREEN_HEIGHT // 2 + 50, 50, BLACK)
        advancedGamemodes = [
            "Spectre Swarm" if isItHalloweenTimeNow() else "Space Invaders", 
            "Strike Zone", 
            "Pumpkin Patch" if isItHalloweenTimeNow() else "Farm Frenzy",
            "Gift Fall" if isItChristmasTimeNow() else "Egg Storm" if isItEasterTimeNow() else "Death Rain", 
            "Blast Field",
            "Quick Click", 
            "Midas Mayhem", 
            "Maze Run (Alpha)"
        ]

        advanced_modes = ButtonArray(advancedGamemodes, (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 + 100), button_width=250, button_spacing=50, text_colour=BLACK)
        basic_modes.draw(screen, BUTTON_COLOUR)
        advanced_modes.draw(screen, BUTTON_COLOUR)
        menuButton = menuButtons(BLACK)
        menuButton.draw(screen, BUTTON_COLOUR)
        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menuButton.handle_click(pos):
                    return
                basic_btn_clicked, btn_basic = basic_modes.handle_click(pos)
                advanced_btn_clicked, btn_advanced = advanced_modes.handle_click(pos)
                btn_clicked = advanced_btn_clicked or basic_btn_clicked

                if btn_clicked:
                    if btn_basic == "Classic":
                        classic(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Classic V2":
                        classicV2(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Speed Run":
                        speedRun(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Survival":
                        survival(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_basic == "Practice":
                        practice(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_advanced == "Space Invaders" or btn_advanced == "Spectre Swarm":
                        spaceInvaders(questionList, titleofquiz, doCountdown, doInstructions, v)
                        return
                    elif btn_advanced == "Strike Zone":
                        strikeZone(questionList, titleofquiz, doCountdown, doInstructions, v)
                        return
                    elif btn_advanced == "Death Rain" or btn_advanced == "Gift Fall" or btn_advanced == "Egg Storm":
                        deathRain(questionList, titleofquiz, doCountdown, doInstructions, v)
                        return
                    elif btn_advanced == "Farm Frenzy" or btn_advanced == "Pumpkin Patch":
                        farmFrenzy(questionList, titleofquiz, doCountdown, doInstructions, v)
                        return
                    elif btn_advanced == "Blast Field":
                        blastField(questionList, titleofquiz, doCountdown, doInstructions, v)
                        return
                    elif btn_advanced == "Quick Click":
                        quickClick(questionList, titleofquiz, doCountdown, doInstructions)
                        return
                    elif btn_advanced == "Midas Mayhem":
                        midasMayhem(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return
                    elif btn_advanced == "Maze Run (Alpha)":
                        mazeRun(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                        return


def StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, doCountdown, doInstructions, questionList=None, titleofquiz=None):
    if args.quizPath != None:
        print("Loading quiz: ", args.quizPath)
        try:
            questionList, titleofquiz, difficulty, randomOrder = load_quiz(args.quizPath)
        except Exception as ex:
            print("Error:", ex)
            sys.exit()
    # With selected quiz, suppress quiz selection
    if args.quizPath != None and args.gameMode == None:
        choose_game_mode(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, v, questionList, titleofquiz)
    elif args.gameMode is not None:
        if args.gameMode == GameMode.classic:
            try:
                classic(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.classicV2:
            try:
                classicV2(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.speedRun:
            try:
                speedRun(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.survival:
            try:
                survival(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.practice:
            try:
                practice(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.midasMayhem:
            try:
                midasMayhem(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.mazeRun:
            try:
                mazeRun(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.spaceInvaders:
            try:
                spaceInvaders(questionList, titleofquiz, doCountdown, doInstructions, v)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.farmFrenzy:
            try:
                farmFrenzy(questionList, titleofquiz, doCountdown, doInstructions, v)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.strikeZone:
            try:
                strikeZone(questionList, titleofquiz, doCountdown, doInstructions, v)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.deathRain:
            try:
                deathRain(questionList, titleofquiz, doCountdown, doInstructions, v)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
        elif args.gameMode == GameMode.quickClick:
            try:
                quickClick(questionList, titleofquiz, doCountdown, doInstructions)
            except Exception as ex:
                print("Error: ", ex)
                choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
    # Start home page
    main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, doInstructions, volume)

def main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, doInstructions, v):
    running = True
    if isItCelebrationNow():
        if isItHalloweenTimeNow():
            welcome_image = pygame.transform.scale(pygame.image.load("images/pumpkin2.png"), (60, 60))
        elif isItChristmasTimeNow():
            welcome_image = pygame.transform.scale(pygame.image.load("images/santa.png"), (60,60))
        elif isItEasterTimeNow():
            welcome_image = pygame.transform.scale(pygame.image.load("images/easterEgg1.png"), (60,65))
    else:
        welcome_image = pygame.image.load("images/Screenshots/logo.png").convert()
    while running:
        refreshPage = False
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
        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)
        screen.blit(welcome_image, (SCREEN_WIDTH//4.8, SCREEN_HEIGHT//12))
        screen.blit(welcome_image, (SCREEN_WIDTH//1.325, SCREEN_HEIGHT//12))
        pygame.display.update()
        while not refreshPage:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_play.is_clicked(pos):
                        choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, v)
                        refreshPage = True
                    elif button_make.is_clicked(pos):
                        try:
                            subprocess.Popen(["python", "quizcreator"])
                        except:
                            subprocess.Popen(["python3", "quizcreator"])
                    elif button_preferences.is_clicked(pos):
                        BLACK, volume, doCountdown, doInstructions, music, BACKGROUND_COLOUR, BUTTON_COLOUR = preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, doCountdown, doInstructions, v)
                        refreshPage = True
                    elif button_about.is_clicked(pos):
                        about(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                        refreshPage = True
                    elif button_quit.is_clicked(pos):
                        quit()
                
if __name__ == '__main__':

    BLACK = screen_mode(BACKGROUND_COLOUR)
    try:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, volume, questionList, titleofquiz)
    except:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, volume, doCountdown, doInstructions)