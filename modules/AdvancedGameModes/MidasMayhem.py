"""
Gold Miners: A game mode where players attempt to accumulate the most gold by answering questions correctly and choosing chests with varying outcomes.
"""

import random
import pygame
from pygame.locals import *
from modules.elements import *
from modules.otherWindows import *

def midasMayhem(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        return

    running = True
    questionIndex = 0
    totalQuestions = len(questionList)
    player_gold = 0

    BLACK = screen_mode(BACKGROUND_COLOUR)

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

        # Question Phase
        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Gold: {player_gold}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, BLACK)
            display_message(f"Question {questionIndex + 1}: {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer == correct_answer_index:
            display_message("Correct!", SCREEN_HEIGHT // 2, 40, (0,0,0))
            pygame.display.update()
            pygame.time.wait(1000)

            # Chest Phase
            chest_outcomes = [
                {"label": "Gain Gold", "probability": 0.4, "multiplier": 1.5},
                {"label": "Lose Gold", "probability": 0.3, "multiplier": -0.5},
                {"label": "Double Gold", "probability": 0.15, "multiplier": 2},
                {"label": "Triple Gold", "probability": 0.1, "multiplier": 3},
                {"label": "Jackpot", "probability": 0.002, "multiplier": 10},
                {"label": "Landmine", "probability": 0.048, "multiplier": 0},
            ]

            chests = [{"outcome": random.choices(chest_outcomes, weights=[o["probability"] for o in chest_outcomes])[0]}
                      for _ in range(3)]

            chest_buttons = [
                Button(f"Chest {i + 1}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + i * OPTION_HEIGHT), 400, 40, BLACK)
                for i in range(len(chests))
            ]

            selected_chest = None
            while selected_chest is None:
                screen.fill(BACKGROUND_COLOUR)
                display_message("Select a chest to open!", QUESTION_OFFSET, 50, BLACK)
                for button in chest_buttons:
                    button.draw(screen, BUTTON_COLOUR)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for i, button in enumerate(chest_buttons):
                            if button.is_clicked(pos):
                                selected_chest = chests[i]["outcome"]

            if selected_chest["multiplier"] == 0:
                player_gold = 0
                display_message("Landmine! You lost all your gold!", SCREEN_HEIGHT // 2, 40, (0,0,0))
            elif selected_chest["multiplier"] > 0:
                change = int((player_gold + 5) * selected_chest["multiplier"])
                player_gold += change
                display_message(f"{selected_chest['label']}! You gained {change} gold!", SCREEN_HEIGHT // 2, 40, (0,0,0))
            else:
                change = int(player_gold * abs(selected_chest["multiplier"]))
                player_gold -= change
                display_message(f"{selected_chest['label']}! You lost {change} gold!", SCREEN_HEIGHT // 2, 40, (0,0,0))

            pygame.display.update()
            pygame.time.wait(2000)
        else:
            display_message("Incorrect! No chest for this question.", SCREEN_HEIGHT // 2, 40, (0,0,0))
            pygame.display.update()
            pygame.time.wait(1000)

        questionIndex += 1

    good_praise_list = [f"Well Done! You know a lot about {titleofquiz.lower()}!",f"You are an expert on {titleofquiz.lower()}!", f" You have mastered {titleofquiz.lower()}!",f"You are amazing at {titleofquiz.lower()}!",f"You truly excel in {titleofquiz.lower()}!", f"Congratulations! You're a whiz on {titleofquiz.lower()}!",f"Bravo! You've nailed {titleofquiz.lower()}!"]
    good_praise = (random.choice(good_praise_list))
    medium_praise_list = ["Good enough...",f"You have a fair amount of knowledge on {titleofquiz.lower()}!", f"Not far of mastering {titleofquiz.lower()}!", f"Just a bit more practice on {titleofquiz.lower()}!",f"You’re making steady progress in {titleofquiz.lower()}!", f"You're on the right track with {titleofquiz.lower()}!",f"You've got a solid grasp of {titleofquiz.lower()}!",f"A commendable effort in {titleofquiz.lower()}!",f"You've got the basics of {titleofquiz.lower()} down!",f"Keep it up! You're building a good foundation in {titleofquiz.lower()}!"]
    medium_praise = (random.choice(medium_praise_list))
    bad_praise_list = [f"Your forte is definitely not {titleofquiz.lower()}!",f"You are terrible at {titleofquiz.lower()}!", f"You have alot to learn about {titleofquiz.lower()}!", f"You might want to consider revising another topic!", f"Sorry to say, but you're pretty terrible at {titleofquiz.lower()}!", f"You really struggle with {titleofquiz.lower()}!", f"You have a long way to go in mastering {titleofquiz.lower()}!", f"Not to be too hard, but it seems you're not great at {titleofquiz.lower()}!", f"Time to go back to the drawing board on {titleofquiz.lower()}!", f"You might want to consider taking another look at {titleofquiz.lower()}!", f"It's clear you're not an expert on  {titleofquiz.lower()}!", f"Unfortunately, you're not very good at {titleofquiz.lower()}!", f"You need to brush up on your {titleofquiz.lower()} skills!"]
    bad_praise = (random.choice(bad_praise_list))
    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed! You got {player_gold} gold.", SCREEN_HEIGHT // 2-200,40, BLACK)
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