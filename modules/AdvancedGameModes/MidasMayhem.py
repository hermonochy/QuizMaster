import random
import pygame
from pygame.locals import *
from modules.elements import *
from modules.extendedText import midasMayhem_p1, midasMayhem_p2, midasMayhem_p3
from modules.otherWindows import *

def midasMayhem(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        return

    running = True
    questionIndex = 0
    totalQuestions = len(questionList)
    player_gold = 0
    BACKGROUND_COLOUR = (255,10,10)
    BUTTON_COLOUR = (212,175,55)
    BLACK = screen_mode(BACKGROUND_COLOUR)

    Instructions(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, p1=midasMayhem_p1, p2=midasMayhem_p2, p3=midasMayhem_p3)

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

        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+250), 250, 40, BLACK)
        button_leave = Button("Quit", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+300), 250, 40, BLACK)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Gold: {player_gold}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, BLACK)
            display_message(f"Question {questionIndex + 1}: {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_go_back.is_clicked(pos):
                        return
                    if button_leave.is_clicked(pos):
                        quit()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer == correct_answer_index:
            screen.fill((50,255,50))
            display_message("Correct!", SCREEN_HEIGHT//2-100, 100, (255,255,255))
            pygame.display.update()
            pygame.time.wait(1000)

            chest_outcomes = [
                {"label": "Gain Gold", "probability": 0.55, "operation": "add", "amount": random.randint(5, (questionIndex+1)*10)},
                {"label": "Lose Gold", "probability": 0.25, "operation": "subtract", "amount": random.randint(5, (questionIndex+1)*5)},
                {"label": "Double Gold", "probability": 0.1, "operation": "multiply", "factor": 2},
                {"label": "Triple Gold", "probability": 0.05, "operation": "multiply", "factor": 3},
                {"label": "Jackpot!", "probability": 0.002, "operation": "add", "amount": (questionIndex+1)*10},
                {"label": "Landmine", "probability": 0.048, "operation": "set", "value": 0},
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

            outcome = selected_chest
            if outcome["operation"] == "set":
                player_gold = outcome["value"]
                display_message("Landmine! You lost all your gold!", SCREEN_HEIGHT // 2, 40, BLACK)
            elif outcome["operation"] == "add":
                player_gold += outcome["amount"]
                display_message(f"{outcome['label']}! You gained {outcome['amount']} gold!", SCREEN_HEIGHT // 2, 40, BLACK)
            elif outcome["operation"] == "subtract":
                loss = min(player_gold, outcome["amount"])
                player_gold -= loss
                display_message(f"{outcome['label']}! You lost {loss} gold!", SCREEN_HEIGHT // 2, 40, BLACK)
            elif outcome["operation"] == "multiply":
                if outcome["factor"] > 1:
                    new_gold = player_gold * outcome["factor"]
                    gained = new_gold - player_gold
                    player_gold = new_gold
                    display_message(f"{outcome['label']}! Your gold increased by {gained}!", SCREEN_HEIGHT // 2, 40, BLACK)
                else:
                    player_gold = 0
                    display_message("You lost all your gold!", SCREEN_HEIGHT // 2, 40, BLACK)
            else:
                display_message("Unknown outcome.", SCREEN_HEIGHT // 2, 40, BLACK)

            pygame.display.update()
            pygame.time.wait(1500)
        else:
            screen.fill((255,10,10))
            display_message("Wrong!", SCREEN_HEIGHT//2-100, 100, (255,255,255))
            display_message(f"Correct Answer: \n{currentQuestion.correctAnswer}", SCREEN_HEIGHT // 2 + 100, 50, (255,255,255))
            pygame.display.update()
            pygame.time.wait(2000)
        if player_gold < 0:
            display_message("Game Over! You are in Debt!", SCREEN_HEIGHT//2, 75, (255,0,0))
            pygame.display.update()
            pygame.time.wait(2000)
            return

        questionIndex += 1

    good_praise_list = [f"Well Done! You know a lot about {titleofquiz.lower()}!",f"You are an expert on {titleofquiz.lower()}!", f" You have mastered {titleofquiz.lower()}!",f"You are amazing at {titleofquiz.lower()}!"]
    good_praise = (random.choice(good_praise_list))
    medium_praise_list = ["Good enough...",f"You have a fair amount of knowledge on {titleofquiz.lower()}!", f"Not far of mastering {titleofquiz.lower()}!", f"Just a bit more practice on {titleofquiz.lower()}!"]
    medium_praise = (random.choice(medium_praise_list))
    bad_praise_list = [f"Your forte is definitely not {titleofquiz.lower()}!",f"You are terrible at {titleofquiz.lower()}!", f"You have alot to learn about {titleofquiz.lower()}!", f"You might want to study {titleofquiz.lower()}!"]
    bad_praise = (random.choice(bad_praise_list))
    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed! You got {player_gold} gold.", SCREEN_HEIGHT // 2-200,40, BLACK)
    
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
                    midasMayhem(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()