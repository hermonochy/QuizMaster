import pygame
import random
import sys

from pygame.locals import *
from modules.elements import *
from modules.extendedText import deathRain_p1, deathRain_p2, deathRain_p3
from modules.otherWindows import *

PLAYER_WIDTH = 75
PLAYER_HEIGHT = 75
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
POWERUP_WIDTH = 30
POWERUP_HEIGHT = 30
PLAYER_SPEED = 5
BASE_OBSTACLE_SPEED = 6
POWERUP_CHANCE = 0.15

BUTTON_COLOUR = (0,100,255)
WHITE = (255, 255, 255)
BACKGROUND_COLOUR = (0,181,226)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


player_image = pygame.image.load("images/hotAirBallon.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

obstacle_image = pygame.image.load("images/arrow.png")
obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

powerup_image = pygame.image.load("images/coin.png")
powerup_image = pygame.transform.scale(powerup_image, (POWERUP_WIDTH, POWERUP_HEIGHT))

class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.speed = PLAYER_SPEED
        self.speed_boost_time = 0

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self):
        if self.speed_boost_time > 0:
            self.speed_boost_time -= 1
        else:
            self.speed = PLAYER_SPEED

class Obstacle:
    def __init__(self, x, y, image, speed):
        self.rect = pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.image = image
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

class PowerUp:
    def __init__(self, x, y, image, speed):
        self.rect = pygame.Rect(x, y, POWERUP_WIDTH, POWERUP_HEIGHT)
        self.image = image
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

def deathRain(questionList, titleofquiz, doCountdown, v):

    if questionList is None or len(questionList) == 0:
        return

    clock = pygame.time.Clock()
    player = Player()
    objects = []
    score = 0
    totalQuestions = len(questionList)
    question_index = 0
    spawn_cooldown = 20 
    last_spawn = 0

    Instructions(BACKGROUND_COLOUR, BUTTON_COLOUR, WHITE, titleofquiz, p1=deathRain_p1, p2=deathRain_p2, p3=deathRain_p3)

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, WHITE)

    def get_current_speed():
        return min(BASE_OBSTACLE_SPEED + (score // 100) * (2/len(questionList)), 20)

    def get_spawn_chance():
        return max(20 - (score // 200), 5)

    def handle_question():
        nonlocal question_index
        if question_index >= totalQuestions:
            return False
        current_question = questionList[question_index]

        user_answer = None
        answerOptions = [current_question.correctAnswer] + current_question.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, WHITE)
            buttons.append(button)

        while user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question: {current_question.question}", QUESTION_OFFSET, 50, WHITE)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            
            button_go_back = Button("Cancel", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, WHITE)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, WHITE)
            display_message(f"Score: {score}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, WHITE)
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
        question_index += 1
        if user_answer == correct_index:
            return True
        return False

    frame_counter = 0
    while True:
        frame_counter += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)

        current_spawn_chance = get_spawn_chance()
        current_speed = get_current_speed()

        if frame_counter - last_spawn >= current_spawn_chance:
            x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            if random.random() < POWERUP_CHANCE:
                objects.append(PowerUp(x, -POWERUP_HEIGHT, powerup_image, current_speed))
            else:
                objects.append(Obstacle(x, -OBSTACLE_HEIGHT, obstacle_image, current_speed))
            last_spawn = frame_counter

        objects = [obj for obj in objects if obj.rect.top < SCREEN_HEIGHT]

        player.update()

        score += 1

        screen.fill(BACKGROUND_COLOUR)
        screen.blit(player_image, player.rect.topleft)
        for obj in objects:
            screen.blit(obj.image, obj.rect.topleft)

        display_message(f"Score: {score}", 20, 50, WHITE)

        for obj in objects:
            obj.move()
            if obj.rect.colliderect(player.rect):
                if isinstance(obj, Obstacle):
                    good_praise_list = [f"Well Done! You know a lot about {titleofquiz.lower()}!",f"You are an expert on {titleofquiz.lower()}!", f" You have mastered {titleofquiz.lower()}!"]
                    good_praise = (random.choice(good_praise_list))
                    medium_praise_list = ["Good enough...",f"You have a fair amount of knowledge on {titleofquiz.lower()}!", f"Not far of mastering {titleofquiz.lower()}!"]
                    medium_praise = (random.choice(medium_praise_list))
                    bad_praise_list = [f"Your forte is definitely not {titleofquiz.lower()}!",f"You are terrible at {titleofquiz.lower()}!", f"You have alot to learn about {titleofquiz.lower()}!"]
                    bad_praise = (random.choice(bad_praise_list))
                    display_message(f"Game Over! Final Score: {score}", SCREEN_HEIGHT // 3, 75, RED)
                    try:
                        if score/totalQuestions > 200 and score/totalQuestions <= 300:
                            display_message(medium_praise, SCREEN_HEIGHT//2, 50, YELLOW)
                        if score/totalQuestions > 300:
                            display_message(good_praise, SCREEN_HEIGHT//2, 50, GREEN)
                        if score/totalQuestions <= 200:
                            display_message(bad_praise, SCREEN_HEIGHT//2, 50, RED)
                    except ZeroDivisionError:
                            display_message("No questions attempted!", SCREEN_HEIGHT//2, 50, YELLOW)

                    pygame.display.update()

                    pygame.time.wait(3000)
                    return
                elif isinstance(obj, PowerUp):
                    if handle_question():
                        player.speed = PLAYER_SPEED * 2
                        player.speed_boost_time = 500
                        objects.remove(obj)
                    else:
                        break

        pygame.display.flip()
        clock.tick(60)