import pygame
import random
import time
import os

from pygame.locals import *
from modules.elements import *
from modules.checker import isItHalloweenTimeNow
from modules.extendedText import *
from modules.otherWindows import countdown, standard_end_window, Instructions

def spaceInvaders(questionList, titleofquiz, doCountdown, doInstructions, v):
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
    explosions = []
    player_width, player_height = 50, 50
    alien_width, alien_height = 40, 40
    alien_speed = 1
    projectile_speed = 1.5
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - 100
    question_index = 0
    total_questions = len(questionList)

    player_laser_img = pygame.image.load('images/Laser.png')
    alien_laser_img = pygame.image.load('images/Laser.png')
    explosion_sound = pygame.mixer.Sound('sounds/soundEffects/explosion.ogg')
    hit = pygame.mixer.Sound('sounds/soundEffects/hit.ogg')
    player_img = pygame.image.load('images/Spaceship.png')
    explosion_img = pygame.image.load('images/explosion.png')

    if isItHalloweenTimeNow():
        alien_img = pygame.image.load('images/pumpkin1.png')
        cannonFire = pygame.mixer.Sound('sounds/soundEffects/laserFire.ogg')
    else:
        alien_img = pygame.image.load('images/SpaceshipAlien1.png')
        cannonFire = pygame.mixer.Sound('sounds/soundEffects/cannonFire.ogg')

    cannonFire.set_volume(v)
    explosion_sound.set_volume(v)
    hit.set_volume(v)

    player_img = pygame.transform.scale(player_img, (player_width, player_height))
    alien_img = pygame.transform.scale(alien_img, (alien_width, alien_height))
    player_laser_img = pygame.transform.scale(player_laser_img, (15, 50))
    alien_laser_img = pygame.transform.scale(alien_laser_img, (20,60))
    explosion_img = pygame.transform.scale(explosion_img, (60, 60))

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=spaceInvaders_p1, p2=spaceInvaders_p2, p3=spaceInvaders_p3)
        
    if doCountdown:
        countdown(titleofquiz, BLACK, WHITE)

    def generate_aliens_bottom_up(rows, cols):
        aliens.clear()
        grid_height = rows * (alien_height + 10)
        bottom_y = 250 - alien_height
        for row in range(rows):
            for col in range(cols):
                aliens.append({
                    "x": col * (alien_width + 10) + 50,
                    "y": bottom_y - row * (alien_height + 10),
                    "alive": True
                })
    if total_questions < 40:
        rows = total_questions // 10 + 3
        cols = total_questions // 3 + 5
    else:
        cols = 20
        rows = total_questions*2
    generate_aliens_bottom_up(rows, cols)

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
                        user_answer = answerOptions.index(current_question.correctAnswer)

        correct_index = answerOptions.index(current_question.correctAnswer)
        if user_answer == correct_index:
            if not forSurvival:    
                ammo += total_questions // 10 + 10
            return True
        return False

    button_answer = Button("Answer Question", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 190), 300, 50, WHITE)
    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, WHITE)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, WHITE)

    can_shoot = True

    while running and lives > 0:
        screen.fill(BLACK)

        display_message(f"Lives: {lives}", 15, 50, WHITE)
        display_message(f"Ammo: {ammo}", 45, 50, WHITE)
        display_message(f"Question {question_index}/{total_questions}", 75, 50, WHITE)
        button_answer.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)

        screen.blit(player_img, (player_x, player_y))

        numAliens = 0
        max_alien_y = -float('inf')

        for alien in aliens:
            if alien["alive"]:
                numAliens += 1
                screen.blit(alien_img, (alien["x"], alien["y"]))
                alien["x"] += alien_speed
                if alien["x"] > SCREEN_WIDTH - alien_width or alien["x"] < 0:
                    alien_speed *= -1
                    for a in aliens:
                        a["y"] += 100/numAliens
                if random.random() < 0.015 * (1/numAliens):
                    cannonFire.play()
                    alien_projectiles.append({"x": alien["x"] + alien_width // 2, "y": alien["y"] + alien_height})

                if alien["y"] > max_alien_y:
                    max_alien_y = alien["y"]

        for projectile in projectiles[:]:
            screen.blit(player_laser_img, (projectile["x"], projectile["y"]))
            projectile["y"] -= projectile_speed
            if projectile["y"] < 0:
                projectiles.remove(projectile)

        for alien_projectile in alien_projectiles[:]:
            screen.blit(alien_laser_img, (alien_projectile["x"], alien_projectile["y"]))
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
            for projectile in projectiles[:]:
                if (alien["x"] < projectile["x"] < alien["x"] + alien_width and
                        alien["y"] < projectile["y"] < alien["y"] + alien_height):
                    alien["alive"] = False
                    explosion_sound.play()
                    if projectile in projectiles:
                        projectiles.remove(projectile)
                    explosions.append({
                        "x": alien["x"] + alien_width // 2,
                        "y": alien["y"] + alien_height // 2,
                        "size": 60,
                        "start_time": pygame.time.get_ticks(),
                        "duration": 750
                    })

        for explosion in explosions[:]:
            elapsed = pygame.time.get_ticks() - explosion["start_time"]
            if elapsed > explosion["duration"]:
                explosions.remove(explosion)
                continue

            shrink_ratio = 1.0 - (elapsed / explosion["duration"])
            size = int(explosion["size"] * shrink_ratio)
            if size < 5:
                size = 5
            exp_img_scaled = pygame.transform.scale(explosion_img, (size, size))
            screen.blit(exp_img_scaled, (explosion["x"] - size // 2, explosion["y"] - size // 2))

        if (all(not alien["alive"] for alien in aliens) and question_index >= total_questions) or all(not alien["alive"] for alien in aliens):
            display_message("You Win!", SCREEN_HEIGHT // 2, 100, (0,255,0))
            pygame.display.update()
            pygame.time.wait(3000)
            break

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += 5

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_answer.is_clicked(pos):
                    handle_question(False)
                elif button_go_back.is_clicked(pos):
                    if popup("Go Back?", "Are you sure you want to go back?", buttons=("Return", "Stay")) == "Return":
                        return
                    else:
                        continue
                elif button_leave.is_clicked(pos):
                    quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and can_shoot and ammo > 0:
                    cannonFire.play()
                    projectiles.append({"x": player_x + player_width // 2, "y": player_y})
                    ammo -= 1
                    can_shoot = False
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    can_shoot = True

        pygame.display.update()

    if lives == 0 or (question_index >= total_questions and all(alien["alive"] for alien in aliens)) or max_alien_y + alien_height >= player_y + player_height // 2:
        explosion_sound.play()
        display_message("You Lose!", SCREEN_HEIGHT // 2, 100, (255,0,0))
        pygame.display.update()
        pygame.time.wait(3000)