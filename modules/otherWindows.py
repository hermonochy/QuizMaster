import pygame
import webbrowser
import random

from modules.elements import *
from modules.persistence import openFile
from modules.extendedText import *
from modules.checker import isItHalloweenTimeNow
from modules.overlays import drawSpiderWebs


def countdown(titleofquiz, BACKGROUND_COLOUR, BLACK):
    for i in range(3,0,-1):
        screen.fill(BACKGROUND_COLOUR)
        display_message(titleofquiz, QUESTION_OFFSET, 70, BLACK)
        display_message((f"{i}!"), QUESTION_OFFSET + 200, 150, BLACK)
        pygame.display.update()
        pygame.time.delay(1000)
    screen.fill(BACKGROUND_COLOUR)
    display_message(("Go!"), QUESTION_OFFSET+200, 150, BLACK)
    pygame.display.update()
    pygame.time.delay(750)
    return

def about(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        button_license = Button("Licenses", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 250), 250, 40, BLACK)
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 300), 250, 40, BLACK)
        button_website = Button("For more information, please vist our website!", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 20), 600, 40, text_colour=LINK_COLOUR)
        button_tutorial = Button("There, you can also view our tutorials.", (SCREEN_WIDTH // 2 - 305, SCREEN_HEIGHT // 2 + 75), 600, 40, text_colour=LINK_COLOUR)
        display_message("About QuizMaster", SCREEN_HEIGHT // 8, 75, BLACK)
        display_message(about_p1, SCREEN_HEIGHT // 5, 30, BLACK)
        display_message(about_p2, SCREEN_HEIGHT // 3, 30, BLACK)
        display_message(about_p3, SCREEN_HEIGHT // 2.2, 30, BLACK)
        button_website.draw(screen, BACKGROUND_COLOUR, shadow_offset=0)
        button_tutorial.draw(screen, BACKGROUND_COLOUR, shadow_offset=0)
        button_license.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_go_back.is_clicked(pos):
                    return
                elif button_website.is_clicked(pos):
                    webbrowser.open("https://quizmaster-world.github.io/index.html")
                elif button_tutorial.is_clicked(pos):
                    webbrowser.open("https://quizmaster-world.github.io/Tutorials/QuizMaster.html")
                elif button_license.is_clicked(pos):
                    Licenses(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)

def Licenses(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    with open("LICENSE", 'r') as GPL:
        GPL_license = str(GPL.read())
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Licensing", SCREEN_HEIGHT // 8, 75, BLACK)
        display_message(licenses_text, SCREEN_HEIGHT // 5, 40, BLACK)
        button_GPL = Button("GPL v3", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50), 250, 40, text_colour=LINK_COLOUR)
        button_CC = Button("Creative Commons", (SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2), 300, 40, text_colour=LINK_COLOUR)
        button_go_back = Button("Go Back", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 300), 250, 40, BLACK)
        button_GPL.draw(screen, BACKGROUND_COLOUR, shadow_offset=0)
        button_CC.draw(screen, BACKGROUND_COLOUR, shadow_offset=0)
        button_go_back.draw(screen, BUTTON_COLOUR)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_GPL.is_clicked(pos):
                    openFile("./LICENSE")
                elif button_CC.is_clicked(pos):
                    try:
                        openFile("./Quizzes/LICENSE")
                    except FileNotFoundError:
                        print("Quizzes have not been downloaded!\n To load, run git submodule update --init")
                elif button_go_back.is_clicked(pos):
                    return

def show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    running = True
    total_items = len(incorrect_questions)
    items_per_page = 10
    scrollbar = Scrollbar((SCREEN_WIDTH - 40, 100), SCREEN_HEIGHT - 150, total_items, items_per_page)
    offset = 0

    while running:
        screen.fill(BACKGROUND_COLOUR)
        y_position = 100

        button_back = Button("Back to Results", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100), 300, 50)
        button_back.draw(screen, BUTTON_COLOUR)

        for idx in range(offset, min(offset + items_per_page, total_items)-1):
            question = incorrect_questions[idx]
            y_position = display_message(question.question, y_position, 30, BLACK)
            y_position = display_message(f"Correct Answer: {question.correctAnswer}", y_position, 30, BLACK)
            y_position += 20
        if total_items > items_per_page:
            scrollbar.draw(screen)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)

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


def standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions):
    good_praise_list = [f"Well Done! You know a lot about {titleofquiz.lower()}!",f"You are an expert on {titleofquiz.lower()}!", f" You have mastered {titleofquiz.lower()}!",f"You are amazing at {titleofquiz.lower()}!",f"You truly excel in {titleofquiz.lower()}!", f"Congratulations! You're a whiz on {titleofquiz.lower()}!",f"Bravo! You've nailed {titleofquiz.lower()}!"]
    good_praise = (random.choice(good_praise_list))
    medium_praise_list = ["Good enough...",f"You have a fair amount of knowledge on {titleofquiz.lower()}!", f"Not far of mastering {titleofquiz.lower()}!", f"Just a bit more practice on {titleofquiz.lower()}!",f"You’re making steady progress in {titleofquiz.lower()}!", f"You're on the right track with {titleofquiz.lower()}!",f"You've got a solid grasp of {titleofquiz.lower()}!",f"A commendable effort in {titleofquiz.lower()}!",f"You've got the basics of {titleofquiz.lower()} down!",f"Keep it up! You're building a good foundation in {titleofquiz.lower()}!"]
    medium_praise = (random.choice(medium_praise_list))
    bad_praise_list = [f"Your forte is definitely not {titleofquiz.lower()}!",f"You are terrible at {titleofquiz.lower()}!", f"You have alot to learn about {titleofquiz.lower()}!", f"You might want to consider revising another topic!", f"Sorry to say, but you're pretty terrible at {titleofquiz.lower()}!", f"You really struggle with {titleofquiz.lower()}!", f"You have a long way to go in mastering {titleofquiz.lower()}!", f"Not to be too hard, but it seems you're not great at {titleofquiz.lower()}!", f"Time to go back to the drawing board on {titleofquiz.lower()}!", f"You might want to consider taking another look at {titleofquiz.lower()}!", f"It's clear you're not an expert on  {titleofquiz.lower()}!", f"Unfortunately, you're not very good at {titleofquiz.lower()}!", f"You need to brush up on your {titleofquiz.lower()} skills!"]
    bad_praise = (random.choice(bad_praise_list))
    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2-200,40, BLACK)
        try:
            if correctAnswers/totalQuestions > 0.4 and correctAnswers/totalQuestions <= 0.8:
                display_message(medium_praise, y_position, 40, BLACK)
            if correctAnswers/totalQuestions > 0.8:
                display_message(good_praise, y_position, 40, BLACK)
            if correctAnswers/totalQuestions <= 0.4:
                display_message(bad_praise, y_position, 40, BLACK)
        except ZeroDivisionError:
                display_message("No questions attempted!", y_position, 40, BLACK)
    
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40, BLACK)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40, BLACK)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40, BLACK)
        if incorrect_questions:
          button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150 , SCREEN_HEIGHT // 2), 250, 40, BLACK)
          button_show_incorrect.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)

        if isItHalloweenTimeNow():
            drawSpiderWebs(screen)
        
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
                    return False
                if button_replay.is_clicked(pos):
                    return True
                if button_quit.is_clicked(pos):
                    quit()

def Instructions(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, **kwargs):
    while True:
        for _, value in kwargs.items():

            running = True

            screen.fill(BACKGROUND_COLOUR)
            display_message("Instructions:", 50, 75, BLACK)
            display_message(value, SCREEN_HEIGHT//4, 60, BLACK)
            button_continue = Button("Continue", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+200), 250, 40, BLACK)
            button_skip = Button("Skip", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+250), 250, 40, BLACK)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+300), 250, 40, BLACK)
            button_continue.draw(screen, BUTTON_COLOUR)
            button_skip.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)

            if isItHalloweenTimeNow():
                drawSpiderWebs(screen)

            pygame.display.update()
            pygame.time.wait(10)

            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if button_leave.is_clicked(pos):
                            quit()
                        elif button_skip.is_clicked(pos):
                            return
                        elif button_continue.is_clicked(pos):
                            running = False
                            break
        return