"""
Module for the "basic" game modes: Classic, Classic V2, Speed Run, Survival and Practice. More complex game modes will be placed in seperate files due to length.
"""

import pygame
import random
import time

from pygame.locals import *
from modules.elements import *
from modules.extendedText import *
from modules.otherWindows import standard_end_window, countdown, Instructions

def classic(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)

    BLACK = screen_mode(BACKGROUND_COLOUR)

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=strikeZone_p1, p2=strikeZone_p2, p3=strikeZone_p3)

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, BLACK)

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        time_remaining = currentQuestion.timeout
        timeColour = BLACK
        
        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, BLACK)
            buttons.append(button)

        while running and time_remaining > 0 and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+200), 250, 40, BLACK)  
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+250), 250, 40, BLACK)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+300), 250, 40, BLACK)
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
                       return
                    if button_leave.is_clicked(pos):
                       quit()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx
 
                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                        user_answer = event.key - pygame.K_1

                    if event.key == pygame.K_y and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_SHIFT):
                        user_answer =  answerOptions.index(currentQuestion.correctAnswer)

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

    replay = standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions)
    if replay:
        classic(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
    else:       
        return

                    
def classicV2(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR):
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

    BLACK = screen_mode(BACKGROUND_COLOUR)

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=strikeZone_p1, p2=strikeZone_p2, p3=strikeZone_p3)

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, BLACK)

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, BLACK)
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
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40, BLACK)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, BLACK)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, BLACK)
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
                        return
                    if button_leave.is_clicked(pos):
                        quit()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1
                    if event.key == pygame.K_y and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_SHIFT):
                        user_answer =  answerOptions.index(currentQuestion.correctAnswer)

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)

        questionIndex += 1

    replay = standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions)
    if replay:
        classicV2(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
    else:       
        return


def speed(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    originalQuestions = questionList[:]
    incorrect_questions = []
    running = True
    correctAnswers = 0
    totalQuestions = len(originalQuestions)
    lives = int(len(questionList) // 3 + 1)

    BLACK = screen_mode(BACKGROUND_COLOUR)

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=strikeZone_p1, p2=strikeZone_p2, p3=strikeZone_p3)

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, BLACK)

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
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, BLACK)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question: {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, BLACK)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, BLACK)
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
                           return
                        if button_leave.is_clicked(pos):
                           quit()
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1
                    if event.key == pygame.K_y and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_SHIFT):
                        user_answer =  answerOptions.index(currentQuestion.correctAnswer)

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
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40, BLACK)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40, BLACK)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40, BLACK)
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
                    return
                if button_replay.is_clicked(pos):
                    speed(originalQuestions[:], titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()

def survival(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
        
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    lives = int(len(questionList) // 3+1)
    
    BLACK = screen_mode(BACKGROUND_COLOUR)

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=strikeZone_p1, p2=strikeZone_p2, p3=strikeZone_p3)

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, BLACK)

    while running and questionIndex < totalQuestions and lives > 0:
        currentQuestion = questionList[questionIndex]

        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, BLACK)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40, BLACK)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, BLACK)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, BLACK)
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
                        return
                    if button_leave.is_clicked(pos):
                        quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1
                    if event.key == pygame.K_y and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_SHIFT):
                        user_answer =  answerOptions.index(currentQuestion.correctAnswer)

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)
                lives -= 1

        questionIndex += 1

    replay = standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions)
    if replay:
        survival(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
    else:       
        return

def practice(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
        
    running = True
    questionIndex = 0
    totalQuestions = len(questionList)
    BLACK = screen_mode(BACKGROUND_COLOUR)
    if BUTTON_COLOUR[1] > 220:
        BUTTON_COLOUR = (BUTTON_COLOUR[0], 220, BUTTON_COLOUR[2]) # Improve visibility of answer reveal

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=strikeZone_p1, p2=strikeZone_p2, p3=strikeZone_p3)

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, BLACK)

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        reveal_answer = False 

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, BLACK)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for idx, button in enumerate(buttons):
                if reveal_answer and answerOptions[idx] == currentQuestion.correctAnswer:
                    button.draw(screen, (0, 255, 0))
                else:
                    button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            
            button_show = Button("Reveal Answer", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 300), 300, 50, BLACK)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, BLACK)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, BLACK)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 350), 250, 40, BLACK)
            button_show.draw(screen, BUTTON_COLOUR)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_show.is_clicked(pos):
                        reveal_answer = True
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                        return
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
                display_message("Correct!", SCREEN_HEIGHT // 2 + 200, 100, (0, 255, 0))
                pygame.display.update()
                pygame.time.wait(500)
            else:
                display_message("Incorrect!", SCREEN_HEIGHT // 2 + 200, 100, (255, 0, 0))
                pygame.display.update()
                pygame.time.wait(500)

        questionIndex += 1

    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed!", SCREEN_HEIGHT // 2 - 200, 40, BLACK)
        
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40, BLACK)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40, BLACK)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40, BLACK)
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
                    return
                if button_replay.is_clicked(pos):
                    practice(questionList, titleofquiz, doCountdown, doInstructions, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()
