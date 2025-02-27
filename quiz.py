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
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button as button
from tkinter import *

from modules.persistence import *
from modules.checker import *
from modules.searchQuiz import search_str_in_file
from modules.pygameTextInput.pygame_textinput import TextInputVisualizer

pygame.init()
pygame.font.init()


textinput = TextInputVisualizer()
pygame.key.set_repeat(200, 25)

print(asciiartstart)

try:
  with open(".Preferences.json", "r") as file:
      try:
          prefDict = json.load(file)
          v = prefDict["Volume"]
          pygame.mixer.music.set_volume(v)
          if isItHalloweenTimeNow():
              colour_background = (250,100,0)
              buttons_colour =  (255,110,10)
              music = "music/music_halloween1.ogg"
          elif isItValentinesTimeNow():
              music = "music/music_valentines1.ogg"
              colour_background = (255,0,0)
              buttons_colour =  (255,10,10)
          elif isItStPatricksTimeNow():
              music = "music/music_stpatrick1.ogg"
              colour_background = (0,150,0)
              buttons_colour =  (10,175,10) 
          elif isItChristmasTimeNow():
              music = "music/music_christmas1.ogg"
              colour_background = prefDict["colour"]
              buttons_colour = prefDict["buttoncolour"]         
          else:
              music = prefDict["Music"]
              colour_background = prefDict["colour"]
              buttons_colour = prefDict["buttoncolour"] 
              celebration = False
          colour = colour_background
          button_colour = buttons_colour
      except json.JSONDecodeError:
          v = 0.5
          music_list = ['music/music1.ogg', 'music/music2.ogg', 'music/music3.ogg', 'music/music4.ogg', 'music/music5.ogg', 'music/music6.ogg']
          music = (random.choice(music_list))
          col_bg = random.uniform(0,1)
          colour_background = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,0.975))) 
          buttons_colour = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,1))) 
          colour = colour_background
          button_colour = buttons_colour
except FileNotFoundError:
    v = 0.5
    music_list = ['music/music1.ogg', 'music/music2.ogg', 'music/music3.ogg', 'music/music4.ogg', 'music/music5.ogg', 'music/music6.ogg']
    music = (random.choice(music_list))
    col_bg = random.uniform(0,1)
    colour_background = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,0.975))) 
    buttons_colour = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,1))) 
    colour = colour_background
    button_colour = buttons_colour
     

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 800
BACKGROUND_COLOUR = colour
BUTTON_COLOUR = button_colour
BLACK = (0, 0, 0)
FONT_SIZE = 40
QUESTION_OFFSET = 50
ANSWER_OFFSET = 200
OPTION_HEIGHT = 50

class GameMode(str, Enum):
    classic = 'classic'
    classicV2 = 'classicV2'
    speedRun = 'speedRun'
    survival = 'survival'

class Button:
    def __init__(self, text, position, width=300, height=60):
        self.text = text
        self.position = position
        self.font = pygame.font.Font(None, FONT_SIZE)
        text_width, text_height = self.font.size(text)
        self.width = max(width, text_width + 20)
        self.height = max(height, text_height + 20) 
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, FONT_SIZE)
        label = font.render(self.text, True, BLACK)
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
class Scrollbar:
    def __init__(self, position, height, total_items, items_per_page):
        self.position = position
        self.height = height
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.rect = pygame.Rect(position[0], position[1], 20, height)
        self.handle_rect = pygame.Rect(position[0], position[1], 20, int(height * items_per_page // total_items))
        self.dragging = False
        self.offset_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.handle_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_y = event.pos[1] - self.handle_rect.y
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION:
            if self.dragging:
                new_y = event.pos[1] - self.offset_y
                new_y = max(self.rect.y, min(new_y, self.rect.y + self.rect.height - self.handle_rect.height))
                self.handle_rect.y = new_y

    def get_offset(self):
        return int((self.handle_rect.y - self.rect.y) * self.total_items // self.height)

def load_quiz(filename):
    with open(filename, 'r') as file:
        quizDicts = json.load(file)
        questionList = []
        for q in quizDicts["listOfQuestions"]:
            qq = QuizQuestion(**q)
            questionList.append(qq)
        titleofquiz = quizDicts["title"]
    return questionList, titleofquiz

def display_message(message, y_position, font_size, colour):
    font = pygame.font.Font(None, font_size)
    words = message.split()
    
    if len(message) > 60:
        text_lines = []
        line = ""
        
        for word in words:
            if font.size(line + word)[0] <= SCREEN_WIDTH:
                line += word + " "
            else:
                text_lines.append(line)
                line = word + " "
        
        if line:
            text_lines.append(line)

        for line in text_lines:
            text = font.render(line, True, colour)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 , y_position))
            screen.blit(text, text_rect)
            y_position += text.get_height()
    else:
        text = font.render(message, True, colour)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        
        y_position += text.get_height()

    return y_position
    
    
def quit():
    print(asciiartend)
    pygame.quit()
    sys.exit()
    
def screen_mode(BACKGROUND_COLOUR):
    R = BACKGROUND_COLOUR[0]
    G = BACKGROUND_COLOUR[1]
    B = BACKGROUND_COLOUR[2]
    global BLACK
    if R + G + B < 200 and max(R,G,B) < 100:
        BLACK = (255, 255, 255)
    else:
        BLACK = (0, 0, 0)



def preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v):
    running = True
    celebration = False
    numList = re.findall(r'\d+', music)     
    i = int(numList[0]) if numList else 1 
    screen.fill(BACKGROUND_COLOUR)
    volumeSlider = Slider(screen, SCREEN_WIDTH // 4, 150, 800, 40, min=0, max=1, step=0.05, initial=v, handleRadius=20)
    Rslider = Slider(screen, SCREEN_WIDTH // 4, 280, 800, 40, min=0, max=220, step=0.5, handleColour = (255,0,0), handleRadius=20, initial = BACKGROUND_COLOUR[0])
    Gslider = Slider(screen, SCREEN_WIDTH // 4, 330, 800, 40, min=0, max=248, step=0.5, handleColour = (20,255,50), handleRadius=20, initial = BACKGROUND_COLOUR[1])
    Bslider = Slider(screen, SCREEN_WIDTH // 4, 380, 800, 40, min=0, max=248, step=0.5, handleColour = (0,0,255), handleRadius=20, initial = BACKGROUND_COLOUR[2])
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
    display_message("Volume Control", 120, 40, BLACK)
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
        BUTTON_COLOUR = (R + 7, G + 7, B + 7)
        screen_mode(BACKGROUND_COLOUR)
        textinput.font_color = (BLACK)

        
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
                    return main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                if button_cancel.contains(*pos):
                    volumeSlider.hide()
                    Rslider.hide()
                    Gslider.hide()
                    Bslider.hide()
                    button_music.hide()
                    button_go_back.hide()
                    button_cancel.hide()
                    main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                    return

def choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR):
    searchTerm = ""
    user_answer = None
    initialized = False
    while True:
        if not initialized:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            initialized = True

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
        display_message("No Quiz Results found!", SCREEN_HEIGHT // 2, 75, (255,0,0))
        pygame.display.update()
        pygame.time.wait(250)
        choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR)
        return
        

    scrollbar = Scrollbar((SCREEN_WIDTH - 40, ANSWER_OFFSET), SCREEN_HEIGHT - ANSWER_OFFSET - 50, len(quizfileSearchResults), 10)
    buttons = []
    for idx, quizfile in enumerate(quizfileSearchResults):
        try:
            with open(quizfile, "r", errors="ignore") as file:
                quiztitle = json.load(file)["title"]
            button = Button(quiztitle, (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
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
                choose_game(BACKGROUND_COLOUR, BUTTON_COLOUR, questionList, titleofquiz)
            else:
                StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, questionList, titleofquiz)
            

def choose_game(BACKGROUND_COLOUR, BUTTON_COLOUR, questionList, titleofquiz):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Select Game Mode:", SCREEN_HEIGHT // 2 - 300, 75, BLACK)
        button_classic = Button("Classic", (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 200), 250, 60)
        button_classicV2 = Button("Classic V2.0", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200), 250, 60)
        button_speed = Button("Speed Run", (SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2 - 200), 250, 60)
        button_survival = Button("Survival", (SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 - 200), 250, 60)           
        button_classic.draw(screen, BUTTON_COLOUR)
        button_classicV2.draw(screen, BUTTON_COLOUR)
        button_speed.draw(screen, BUTTON_COLOUR)
        button_survival.draw(screen, BUTTON_COLOUR)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                event_time = pygame.time.get_ticks()
                if button_classic.is_clicked(pos):
                    classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                if button_classicV2.is_clicked(pos):
                    classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                if button_speed.is_clicked(pos):
                    speed(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                if button_survival.is_clicked(pos):
                    survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                            

def show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR):
    running = True
    total_items = len(incorrect_questions)
    items_per_page = 10
    scrollbar = Scrollbar((SCREEN_WIDTH - 40, 100), SCREEN_HEIGHT - 150, total_items, items_per_page)
    offset = 0
    button_back = button(screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100, 300, 50, text="Back to Results", textColour = BLACK, inactiveColour=BUTTON_COLOUR, shadowDistance = 2, radius=25)
    button_back.draw()

    while running:
        screen.fill(BACKGROUND_COLOUR)
        y_position = 50

        for idx in range(offset, min(offset + items_per_page, total_items)):
            question = incorrect_questions[idx]
            y_position = display_message(question.question, y_position, 30, BLACK)
            y_position = display_message(f"Correct Answer: {question.correctAnswer}", y_position, 30, BLACK)
            y_position += 20

        if total_items > items_per_page:
            scrollbar.draw(screen)
        pygame_widgets.update(pygame.event.get())
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_back.contains(*pos):
                    button_back.hide()
                    return
            if total_items > items_per_page:
                scrollbar.handle_event(event)

        offset = scrollbar.get_offset()
                            

def classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    good_praise_list = [f"Well Done! You know a lot about {titleofquiz}!",f"You are an expert on {titleofquiz}!", f" You have mastered {titleofquiz}!",f"You are amazing at {titleofquiz}!",f"You truly excel in {titleofquiz}!", f"Congratulations! You're a whiz on {titleofquiz}!",f"Bravo! You've nailed {titleofquiz}!"]
    good_praise = (random.choice(good_praise_list))
    medium_praise_list = ["Good enough...",f"You have a fair amount of knowledge on {titleofquiz}!", f"Not far of mastering {titleofquiz}", f"Just abit more practice on {titleofquiz}!",f"You’re making steady progress in {titleofquiz}.", f"You're on the right track with {titleofquiz}!",f"You've got a solid grasp of {titleofquiz}.",f"A commendable effort in {titleofquiz}!",f"You've got the basics of {titleofquiz} down!",f"Keep it up! You're building a good foundation in {titleofquiz}!"
]
    medium_praise = (random.choice(medium_praise_list))
    bad_praise_list = [f"Your forte is definitely not {titleofquiz}",f"You are terrible at {titleofquiz}!", f"You have alot to learn about {titleofquiz}!", f"You might want to consider revising another topic!", f"Sorry to say, but you're pretty terrible at {titleofquiz}", f"You really struggle with {titleofquiz}!", f"You have a long way to go in mastering {titleofquiz}!", f"Not to be too hard, but it seems you're not great at {titleofquiz}!", f"Time to go back to the drawing board on {titleofquiz}!", f"You might want to consider taking another look at {titleofquiz}!", f"It's clear you're not an expert on  {titleofquiz}!", f"Unfortunately, you're not very good at {titleofquiz}!", f"You need to brush up on your {titleofquiz} skills!"]
    bad_praise = (random.choice(bad_praise_list))
    for i in range(3,0,-1):
        screen.fill(BACKGROUND_COLOUR)
        display_message(titleofquiz, QUESTION_OFFSET,70, BLACK)
        display_message((f"{i}!"), QUESTION_OFFSET+200,150, BLACK)
        pygame.display.update()
        pygame.time.delay(1000)
    screen.fill(BACKGROUND_COLOUR)        
    display_message(("Go!"), QUESTION_OFFSET+200, 150, BLACK)
    pygame.display.update()
    pygame.time.delay(1000)        

    
    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        time_remaining = currentQuestion.timeout
        timeColour = BLACK
        
        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
            buttons.append(button)

        while running and time_remaining > 0 and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+200), 250, 40)  
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+300), 250, 40)
            display_message(f"Time remaining: {time_remaining}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, timeColour)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            pygame.time.wait(1000)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() 
                    if button_end.is_clicked(pos):
                       time_remaining = 0
                       totalQuestions = questionIndex       
                    if button_go_back.is_clicked(pos):
                       main(music,BACKGROUND_COLOUR,BUTTON_COLOUR, v)
                    if button_leave.is_clicked(pos):
                       quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx
 
                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                        user_answer = event.key - pygame.K_1

            time_remaining -= 1
            if time_remaining <= 5:
                timeColour = (255,0,0)


        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)

        questionIndex += 1

    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2-200,40, BLACK)
        try:
            if correctAnswers/totalQuestions > 0.8:
                display_message(good_praise, y_position,40, BLACK)
            if correctAnswers/totalQuestions > 0.4 and correctAnswers/totalQuestions < 0.8 or correctAnswers/totalQuestions == 0.8:
                display_message(medium_praise, y_position,40, BLACK)
            if correctAnswers/totalQuestions < 0.4 or correctAnswers/totalQuestions==0.4:
                display_message(bad_praise, y_position,40, BLACK)
        except ZeroDivisionError:
                display_message("No questions attempted!", y_position,40, BLACK)
    
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40)
        if incorrect_questions:
          button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150 , SCREEN_HEIGHT // 2), 250, 40)
          button_show_incorrect.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)        
        
        pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == QUIT:
               quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if incorrect_questions and questionIndex > 0:
                    if button_show_incorrect.is_clicked(pos):
                        show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                if button_go_back.is_clicked(pos):
                    main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                    return
                if button_replay.is_clicked(pos):
                    classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()
                    
def classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    
    total_time = sum(q.timeout-3 for q in questionList)+10
    start_time = time.time()

    good_praise_list = [f"Well Done! You know a lot about {titleofquiz}!", f"You are an expert on {titleofquiz}!", f" You have mastered {titleofquiz}!", f"You are amazing at {titleofquiz}!"]
    good_praise = (random.choice(good_praise_list))
    medium_praise_list = ["Good enough...", f"You have a fair amount of knowledge on {titleofquiz}!", f"Not far off mastering {titleofquiz}", f"Just a bit more practice on {titleofquiz}!", f"You’re making progress!"]
    medium_praise = (random.choice(medium_praise_list))
    bad_praise_list = [f"Your forte is definitely not {titleofquiz}", f"You are terrible at {titleofquiz}!", f"You have a lot to learn about {titleofquiz}!", f"You might want to consider revising another topic."]
    bad_praise = (random.choice(bad_praise_list))

    for i in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOUR)
        display_message(titleofquiz, QUESTION_OFFSET, 70, BLACK)
        display_message((f"{i}!"), QUESTION_OFFSET + 200, 150, BLACK)
        pygame.display.update()
        pygame.time.delay(1000)
    screen.fill(BACKGROUND_COLOUR)
    display_message(("Go!"), QUESTION_OFFSET + 200, 150, BLACK)
    pygame.display.update()
    pygame.time.delay(1000)

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
            buttons.append(button)

        while running and user_answer is None:
            elapsed_time = time.time() - start_time
            time_remaining = total_time - int(elapsed_time)
            
            if time_remaining < total_time/totalQuestions:
                timeColour = (255,0,0)
            else:
                timeColour = BLACK  

            if time_remaining <= 0:
                running = False
                break

            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40)
            display_message(f"Time remaining: {time_remaining}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, timeColour)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                        main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                    if button_leave.is_clicked(pos):
                        quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)

        questionIndex += 1

    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2 - 200, 40, BLACK)
        try:
            if correctAnswers / totalQuestions > 0.8:
                display_message(good_praise, y_position, 40, BLACK)
            if correctAnswers / totalQuestions > 0.4 and correctAnswers / totalQuestions <= 0.8 :
                display_message(medium_praise, y_position, 40, BLACK)
            if correctAnswers / totalQuestions < 0.4 or correctAnswers / totalQuestions == 0.4:
                display_message(bad_praise, y_position, 40, BLACK)
        except ZeroDivisionError:
            display_message("No questions attempted!", y_position, 40, BLACK)

        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40)
        if incorrect_questions:
            button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2), 250, 40)
            button_show_incorrect.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if incorrect_questions and questionIndex > 0:
                    if button_show_incorrect.is_clicked(pos):
                        show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                if button_go_back.is_clicked(pos):
                    main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                    return
                if button_replay.is_clicked(pos):
                    classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()


def speed(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    originalQuestions = questionList[:]
    incorrect_questions = []
    running = True
    correctAnswers = 0
    totalQuestions = len(originalQuestions)
    lives = 3

    for i in range(3,0,-1):
        screen.fill(BACKGROUND_COLOUR)
        display_message(titleofquiz, QUESTION_OFFSET,70, BLACK)
        display_message((f"{i}!"), QUESTION_OFFSET+200,150, BLACK)
        pygame.display.update()
        pygame.time.delay(1000)
    screen.fill(BACKGROUND_COLOUR)        
    display_message(("Go!"), QUESTION_OFFSET+200,150, BLACK)
    pygame.display.update()
    pygame.time.delay(1000) 
    start_time = time.time()

    while running:
        if not questionList:
            break

        currentQuestion = questionList.pop(0)
        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question: {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40)
            elapsed_time = time.time() - start_time
            display_message(f"Time: {int(elapsed_time)}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, BLACK)
            display_message(f"Lives: {lives}", SCREEN_HEIGHT - (QUESTION_OFFSET + 40), 40, BLACK)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx, button in enumerate(buttons):
                        if button_go_back.is_clicked(pos):
                           main(music,BACKGROUND_COLOUR,BUTTON_COLOUR, v)
                        if button_leave.is_clicked(pos):
                           quit()
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
                continue
            else:
                questionList.append(currentQuestion)
                lives -= 1
                if lives < 0:
                    questionList = originalQuestions[:]
                    correctAnswers = 0
                    lives = 3

    end_time = time.time()
    total_time = int(end_time - start_time)

    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Speed Run completed! You answered all questions correctly in {total_time} seconds.", SCREEN_HEIGHT // 2 - 200, 40, BLACK)
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_go_back.is_clicked(pos):
                    main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                    return
                if button_replay.is_clicked(pos):
                    speed(originalQuestions[:], titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()

def survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
        
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    lives = int(len(questionList) // 3+1)
    good_praise_list = [f"Well Done! You know a lot about {titleofquiz}!", f"You are an expert on {titleofquiz}!", f" You have mastered {titleofquiz}!", f"You are amazing at {titleofquiz}!", f"You truly mastered {titleofquiz}!"]
    good_praise = (random.choice(good_praise_list))
    medium_praise_list = ["Good enough...", f"You have a fair amount of knowledge on {titleofquiz}!", f"Not far off mastering {titleofquiz}", f"Just a bit more practice on {titleofquiz}!", f"You're making progress on {titleofquiz}!"]
    medium_praise = (random.choice(medium_praise_list))
    bad_praise_list = [f"Your forte is definitely not {titleofquiz}", f"You are terrible at {titleofquiz}!", f"You have a lot to learn about {titleofquiz}!", f"You might want to consider revising another topic other than {titleofquiz}."]
    bad_praise = (random.choice(bad_praise_list))
    
    for i in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOUR)
        display_message(titleofquiz, QUESTION_OFFSET, 70, BLACK)
        display_message((f"{i}!"), QUESTION_OFFSET + 200, 150, BLACK)
        pygame.display.update()
        pygame.time.delay(1000)
    screen.fill(BACKGROUND_COLOUR)
    display_message(("Go!"), QUESTION_OFFSET + 200, 150, BLACK)
    pygame.display.update()
    pygame.time.delay(1000)
    
    while running and questionIndex < totalQuestions and lives > 0:
        currentQuestion = questionList[questionIndex]

        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40)
            display_message(f"Lives remaining: {lives}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, BLACK)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                        main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                    if button_leave.is_clicked(pos):
                        quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)
                lives -= 1

        questionIndex += 1

    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2 - 200, 40, BLACK)
        try:
            if correctAnswers / totalQuestions > 0.8:
                display_message(good_praise, y_position, 40, BLACK)
            if correctAnswers / totalQuestions > 0.4 and correctAnswers / totalQuestions <= 0.8:
                display_message(medium_praise, y_position, 40, BLACK)
            if correctAnswers / totalQuestions < 0.4 or correctAnswers / totalQuestions == 0.4:
                display_message(bad_praise, y_position, 40, BLACK)
        except ZeroDivisionError:
            display_message("No questions attempted!", y_position, 40, BLACK)
        
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40)
        if incorrect_questions:
            button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2), 250, 40)
            button_show_incorrect.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if incorrect_questions and questionIndex > 0:
                    if button_show_incorrect.is_clicked(pos):
                        show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                if button_go_back.is_clicked(pos):
                    main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                    return
                if button_replay.is_clicked(pos):
                    survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()

def StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, questionList=None, titleofquiz=None):
    if args.gameMode == GameMode.classic:
        try:
            classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR)
    if args.gameMode == GameMode.classicV2:
        try:
            classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR)
    if args.gameMode == GameMode.speedRun:
        try:
            speed(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR)
    if args.gameMode == GameMode.survival:
        try:
            survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
        except Exception as ex:
            print("Error: ", ex)
            choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR)
    if args.quizPath != None and args.gameMode == None:
        choose_game(BACKGROUND_COLOUR, BUTTON_COLOUR, questionList, titleofquiz)
    if args.gameMode == None:
        icon = pygame.image.load('images/logo1.png')
        pygame.display.set_icon(icon)
        main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)

                   
def main(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        button_play = Button("Play a Quiz", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2), 250, 60)
        button_make = Button("Make a Quiz", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2), 250, 60)
        button_preferences = Button("Preferences", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 100), 250, 60)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 100), 250, 60)
        display_message("Welcome to QuizMaster!", SCREEN_HEIGHT // 8, 75, BLACK)
        button_make.draw(screen, BUTTON_COLOUR)
        button_play.draw(screen, BUTTON_COLOUR)
        button_preferences.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)
        welcome_image = pygame.image.load("images/logo.png").convert()
        screen.blit(welcome_image, (SCREEN_WIDTH//4.75, SCREEN_HEIGHT//12))
        screen.blit(welcome_image, (SCREEN_WIDTH//1.325, SCREEN_HEIGHT//12))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_quit.is_clicked(pos):
                    quit()
                if button_make.is_clicked(pos):
                    subprocess.Popen(["python3", "quizcreator"])
                if button_preferences.is_clicked(pos):
                    preferences(music, BACKGROUND_COLOUR, BUTTON_COLOUR, v)
                if button_play.is_clicked(pos):
                    choose_quiz(BACKGROUND_COLOUR, BUTTON_COLOUR)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='quiz',
        description='Main program for QuizMaster. Features include: Playing quiz, preferences and starting QuizCreator.',
        )
    parser.add_argument('-q', '--quizPath', nargs='?', const="")
    parser.add_argument('-g', '--gameMode', nargs='?', const="", type=GameMode)
    args = parser.parse_args()

    if args.quizPath != None:
        print("Loading quiz: ", args.quizPath)
        try:
            questionList, titleofquiz = load_quiz(args.quizPath)
        except Exception as ex:
            print("Error:", ex)
            sys.exit()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('QuizMaster')
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    screen_mode(BACKGROUND_COLOUR)
    textinput.font_color = (BLACK)
    
    try:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR, questionList, titleofquiz)
    except:
        StartOption(BACKGROUND_COLOUR, BUTTON_COLOUR)
