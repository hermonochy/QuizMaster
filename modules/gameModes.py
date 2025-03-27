"""
Module for the "basic" game modes: Classic, Classic V2, Speed Run and Survival. More complex game modes will be placed in seperate files due to length.
"""

import pygame
import random
import time

from pygame.locals import *
from modules.elements import *

def show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    running = True
    total_items = len(incorrect_questions)
    items_per_page = 10
    scrollbar = Scrollbar((SCREEN_WIDTH - 40, 100), SCREEN_HEIGHT - 150, total_items, items_per_page)
    offset = 0

    while running:
        screen.fill(BACKGROUND_COLOUR)
        y_position = 50
        button_back = Button("Back to Results", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100), 300, 50, BLACK)
        button_back.draw(screen, BUTTON_COLOUR)
        for idx in range(offset, min(offset + items_per_page, total_items)):
            question = incorrect_questions[idx]
            y_position = display_message(question.question, y_position, 30, BLACK)
            y_position = display_message(f"Correct Answer: {question.correctAnswer}", y_position, 30, BLACK)
            y_position += 20

        if total_items > items_per_page:
            scrollbar.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_back.is_clicked(pos):
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
    BLACK = screen_mode(BACKGROUND_COLOUR)

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
    
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40, BLACK)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40, BLACK)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40, BLACK)
        if incorrect_questions:
          button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150 , SCREEN_HEIGHT // 2), 250, 40, BLACK)
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
                        show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                if button_go_back.is_clicked(pos):
                    return
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
    BLACK = screen_mode(BACKGROUND_COLOUR)
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

        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40, BLACK)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40, BLACK)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40, BLACK)
        if incorrect_questions:
            button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2), 250, 40, BLACK)
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
                        show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                if button_go_back.is_clicked(pos):
                    return
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
    lives = int(len(questionList) // 3 + 1)

    BLACK = screen_mode(BACKGROUND_COLOUR)

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
    BLACK = screen_mode(BACKGROUND_COLOUR)
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
        
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40, BLACK)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40, BLACK)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40, BLACK)
        if incorrect_questions:
            button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2), 250, 40, BLACK)
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
                        show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                if button_go_back.is_clicked(pos):
                    return
                    return
                if button_replay.is_clicked(pos):
                    survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()

def practice(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
        
    running = True
    questionIndex = 0
    totalQuestions = len(questionList)
    BLACK = screen_mode(BACKGROUND_COLOUR)
    if BUTTON_COLOUR[1] > 200:
        BUTTON_COLOUR = (BUTTON_COLOUR[0], 200, BUTTON_COLOUR[2]) # Improve visibility of answer reveal
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
            
            button_show = Button("Reveal Answer", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40, BLACK)
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
                    practice(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()