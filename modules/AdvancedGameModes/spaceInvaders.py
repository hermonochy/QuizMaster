import pygame
import random
import time

from pygame.locals import *
from modules.elements import *
from modules.otherWindows import countdown, standard_end_window

def spaceInvaders(questionList, titleofquiz, doCountdown):
    if questionList is None or len(questionList) == 0:
        return

    running = True
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    BUTTON_COLOUR = (25,25,25)
    lives = int(len(questionList) // 3 + 1)
    ammo = 0
    aliens = []
    projectiles = []
    alien_projectiles = []
    player_width, player_height = 50, 50
    alien_width, alien_height = 40, 40
    alien_speed = 1
    projectile_speed = 1.5
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - 100
    question_index = 0
    total_questions = len(questionList)
    cannonFire = pygame.mixer.Sound('soundEffects/spaceInvaders/cannonFire.ogg')
    explosion = pygame.mixer.Sound('soundEffects/spaceInvaders/explosion.ogg')
    hit = pygame.mixer.Sound('soundEffects/spaceInvaders/hit.ogg')


    countdown(titleofquiz, BLACK, WHITE)

    def generate_aliens(rows, cols):
        for row in range(rows):
            for col in range(cols):
                aliens.append({
                    "x": col * (alien_width + 10) + 50,
                    "y": row * (alien_height + 10) + 50,
                    "alive": True
                })

    generate_aliens(total_questions // 5 + 1, total_questions // 2 + 1)

    def handle_question(forSurvival):
        nonlocal ammo, question_index
        if question_index >= total_questions:
            return False
        current_question = questionList[question_index]
        question_index += 1

        user_answer = None
        answerOptions = [current_question.correctAnswer] + current_question.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, WHITE)
            buttons.append(button)


        while user_answer is None:
            screen.fill((0,0,0))
            display_message(f"Question: {current_question.question}", QUESTION_OFFSET, 50, WHITE)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BLACK)
            
            button_go_back = Button("Cancel", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, WHITE)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, WHITE)
            display_message(f"Lives remaining: {lives}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, WHITE)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
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
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1
                    if event.key == pygame.K_y and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_SHIFT):
                        user_answer =  answerOptions.index(currentQuestion.correctAnswer)

        correct_index = answerOptions.index(current_question.correctAnswer)
        if user_answer == correct_index:
            if not forSurvival:    
                ammo += 10
            return True
        return False

    button_answer = Button("Answer Question", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 190), 300, 50, WHITE)
    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, WHITE)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, WHITE)

    while running and lives > 0:

        screen.fill(BLACK)

        display_message(f"Lives: {lives}", 10, 50, WHITE)
        display_message(f"Ammo: {ammo}", 40, 50, WHITE)
        display_message(f"Question {question_index}/{total_questions}", 70, 50, WHITE)
        button_answer.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)

        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_width, player_height))

        for alien in aliens:
            if alien["alive"]:
                pygame.draw.rect(screen, (255, 0, 0), (alien["x"], alien["y"], alien_width, alien_height))
                alien["x"] += alien_speed
                if alien["x"] > SCREEN_WIDTH - alien_width or alien["x"] < 0:
                    alien_speed *= -1
                    for a in aliens:
                        a["y"] += 10
                if random.random() < 0.001:
                    cannonFire.play()
                    alien_projectiles.append({"x": alien["x"] + alien_width // 2, "y": alien["y"] + alien_height})

        for projectile in projectiles:
            pygame.draw.rect(screen, (0, 0, 255), (projectile["x"], projectile["y"], 5, 10))
            projectile["y"] -= projectile_speed
            if projectile["y"] < 0:
                projectiles.remove(projectile)

        for alien_projectile in alien_projectiles:
            pygame.draw.rect(screen, (255, 255, 0), (alien_projectile["x"], alien_projectile["y"], 5, 10))
            alien_projectile["y"] += projectile_speed
            if alien_projectile["y"] > SCREEN_HEIGHT:
                alien_projectiles.remove(alien_projectile)
            elif (player_x < alien_projectile["x"] < player_x + player_width and
                  player_y < alien_projectile["y"] < player_y + player_height):
                alien_projectiles.remove(alien_projectile)
                hit.play()
                if not handle_question(True):
                    lives -= 1

        for alien in aliens:
            if not alien["alive"]:
                continue
            for projectile in projectiles:
                if (alien["x"] < projectile["x"] < alien["x"] + alien_width and
                        alien["y"] < projectile["y"] < alien["y"] + alien_height):
                    alien["alive"] = False
                    explosion.play()
                    if projectile in projectiles:
                        projectiles.remove(projectile)

        if (all(not alien["alive"] for alien in aliens) and question_index >= total_questions) or all(not alien["alive"] for alien in aliens):
            display_message("You Win!", SCREEN_HEIGHT // 2, 50, WHITE)
            pygame.display.update()
            pygame.time.wait(3000)
            break

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += 5
        if keys[K_SPACE] and ammo > 0:
            cannonFire.play()
            projectiles.append({"x": player_x + player_width // 2, "y": player_y})
            ammo -= 1
            # ensure the player does not shoot too many projectiles at once
            pygame.time.wait(50)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_answer.is_clicked(pos):
                    handle_question(False)
                elif button_go_back.is_clicked(pos):
                    return
                elif button_leave.is_clicked(pos):
                    quit()

        pygame.display.update()

    if lives == 0 or (question_index >= total_questions and all(alien["alive"] for alien in aliens)):
        explosion.play()
        display_message("You Lose!", SCREEN_HEIGHT // 2, 50, WHITE)
        pygame.display.update()
        pygame.time.wait(3000)