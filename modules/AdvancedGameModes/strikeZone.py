import pygame
import random
import math
import time

from pygame.locals import *
from modules.elements import *
from modules.constants import *
from modules.otherWindows import countdown

def strikeZone(questionList, titleofquiz, doCountdown):

    questionLength = len(questionList)

    if questionList is None or questionLength == 0:
        return

    running = True
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BUTTON_COLOUR = (25, 25, 25)

    PLAYER_SPEED = 10
    PROJECTILE_SPEED = 20
    ENEMY_SPEED = 2
    ENEMY_SPAWN_RATE = 30
    POWER_UP_DURATION = 5000

    player = {"image": pygame.Surface((50, 50)), "rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 50), "health": 100, "level": 1, "experience": 0}
    projectiles = []
    enemies = []
    powerups = []
    enemy_spawn_counter = 0
    ammo = questionLength * 50
    score = 0
    question_index = 0
    total_questions = questionLength
    cannonFire = pygame.mixer.Sound('soundEffects/cannonFire.ogg')
    explosion = pygame.mixer.Sound('soundEffects/explosion.ogg')
    hit = pygame.mixer.Sound('soundEffects/hit.ogg')


    player["image"].fill(BLUE)

    def handle_question(forPowerup=False):
        nonlocal question_index, ammo
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
            screen.fill(BLACK)
            display_message(f"Question: {current_question.question}", QUESTION_OFFSET, 50, WHITE)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BLACK)
            
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
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_index = answerOptions.index(current_question.correctAnswer)
        if user_answer == correct_index:
            if forPowerup:
                ammo += 250
                player["health"] += 10
            else:
                ammo += 100
            return True
        return False

    countdown(titleofquiz, BLACK, WHITE)

    button_answer = Button("Answer Question", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 190), 300, 50, WHITE)
    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, WHITE)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, WHITE)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if ammo > 0:
                        cannonFire.play()
                        angle = math.atan2(pygame.mouse.get_pos()[1] - player["rect"].centery, 
                                        pygame.mouse.get_pos()[0] - player["rect"].centerx)
                        projectile_surface = pygame.Surface((10, 10))
                        projectile_surface.fill((255, 255, 0))
                        projectiles.append({
                            "image": projectile_surface,
                            "rect": pygame.Rect(player["rect"].centerx, player["rect"].centery, 10, 10),
                            "angle": angle
                        })
                        ammo -= 1
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_answer.is_clicked(pos):
                    handle_question(forPowerup=False)
                elif button_go_back.is_clicked(pos):
                    return
                elif button_leave.is_clicked(pos):
                    quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player["rect"].x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player["rect"].x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            player["rect"].y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player["rect"].y += PLAYER_SPEED

        player["rect"].clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        for projectile in projectiles[:]:
            projectile["rect"].x += PROJECTILE_SPEED * math.cos(projectile["angle"])
            projectile["rect"].y += PROJECTILE_SPEED * math.sin(projectile["angle"])
            if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).contains(projectile["rect"]):
                projectiles.remove(projectile)

        enemy_spawn_counter += 1
        if enemy_spawn_counter >= ENEMY_SPAWN_RATE:
            enemy_spawn_counter = 0
            enemies.append({"image": pygame.Surface((50, 50)), "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50)})
            enemies[-1]["image"].fill(RED)

        for enemy in enemies[:]:
            dx = player["rect"].x - enemy["rect"].x
            dy = player["rect"].y - enemy["rect"].y
            distance = math.hypot(dx, dy)
            if distance > 0:
                dx /= distance
                dy /= distance
            enemy["rect"].x += dx * ENEMY_SPEED
            enemy["rect"].y += dy * ENEMY_SPEED

            if player["rect"].colliderect(enemy["rect"]):
                hit.play()
                player["health"] -= 1
                enemies.remove(enemy)

        for projectile in projectiles[:]:
            for enemy in enemies[:]:
                if projectile["rect"].colliderect(enemy["rect"]):
                    explosion.play()
                    enemies.remove(enemy)
                    projectiles.remove(projectile)
                    score += 1
                    break

        if random.random() < 0.001 and len(powerups) < 10:
            powerups.append({"image": pygame.Surface((30, 30)), "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT - 30), 30, 30)})
            powerups[-1]["image"].fill(GREEN)

        for powerup in powerups[:]:
            if player["rect"].colliderect(powerup["rect"]):
                handle_question(forPowerup=True)
                powerups.remove(powerup)

        screen.fill(BLACK)
        button_answer.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)

        screen.blit(player["image"], player["rect"])
        for projectile in projectiles:
            screen.blit(projectile["image"], projectile["rect"])
        for enemy in enemies:
            screen.blit(enemy["image"], enemy["rect"])
        for powerup in powerups:
            screen.blit(powerup["image"], powerup["rect"])

        if player["health"] <= 0:
            explosion.play()
            display_message("You Lose!", 300, 100, RED)
            pygame.display.flip()
            pygame.time.wait(3000)
            return
    
        if question_index == questionLength and score > questionLength*5:
            display_message("You Win!", 300, 100, GREEN)
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        display_message(f'Health: {player["health"]}', 10, 24, WHITE)
        display_message(f'Ammo: {ammo}', 40, 24, WHITE)
        display_message(f'Score: {score}', 70, 24, WHITE)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
