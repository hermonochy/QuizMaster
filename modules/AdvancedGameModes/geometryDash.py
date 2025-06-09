import pygame
import random
import time

from pygame.locals import *
from modules.elements import *
from modules.otherWindows import countdown, standard_end_window

def geometryDash(questionList, titleofquiz, doCountdown, doInstructions):
    if questionList is None or len(questionList) == 0:
        return

    running = True
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BUTTON_COLOUR = (25, 25, 25)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    GRAY = (128, 128, 128)
    
    player_size = 30
    player_x = 200
    player_y = SCREEN_HEIGHT - 150
    velocity_y = 0
    gravity = 0.5
    jump_power = -12
    is_jumping = False
    
    score = 0
    lives = 10
    game_speed = 4
    question_index = 0
    total_questions = len(questionList)
    
    PLATFORM_WIDTH = 100
    PLATFORM_HEIGHT = 20
    
    class GameObject:
        def __init__(self, x, y, width, height, color, type='platform'):
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color
            self.active = True
            self.type = type
    
    platforms = []
    dots = []
    obstacles = []
    
    def generate_platform_sequence(start_x, length):
        """Generate a sequence of connected platforms with proper spacing"""
        platforms = []
        current_x = start_x
        base_height = SCREEN_HEIGHT - 100
        
        for i in range(length):
            height_variation = random.randint(-25, 25)
            platform_y = base_height + height_variation
            
            platforms.append(GameObject(
                current_x, 
                platform_y,
                PLATFORM_WIDTH, 
                PLATFORM_HEIGHT, 
                GRAY
            ))
            
            if random.random() < 0.3 and question_index < total_questions:
                dot_x = current_x + PLATFORM_WIDTH/2
                dot_y = platform_y - 80  # Dot above platform
                dots.append(GameObject(
                    dot_x, dot_y, 20, 20, YELLOW, 'dot'
                ))
            
            if random.random() < 0.3:
                obstacle_height = random.randint(25, 50)
                obstacle_x = current_x + PLATFORM_WIDTH/2
                obstacle_y = platform_y - obstacle_height
                obstacles.append(GameObject(
                    obstacle_x, obstacle_y, 20, obstacle_height, BLUE, 'obstacle'
                ))
            
            # Move to next platform position with slight variation
            current_x += PLATFORM_WIDTH + random.randint(50, 100)
    
    def generate_level():
        # Generate initial ground
        ground = GameObject(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH * len(questionList), 100, WHITE, 'ground')
        platforms.append(ground)
        
        # Generate initial platform sequence
        generate_platform_sequence(SCREEN_WIDTH, 20)
    
    def handle_question():
        nonlocal question_index, score
        if question_index >= total_questions:
            return False
            
        current_question = questionList[question_index]
        question_index += 1
        
        user_answer = None
        answerOptions = [current_question.correctAnswer] + current_question.wrongAnswers
        random.shuffle(answerOptions)
        
        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", 
                          (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT),
                          400, 40, WHITE)
            buttons.append(button)
        
        while user_answer is None:
            screen.fill(BLACK)
            display_message(f"Question: {current_question.question}", 
                          QUESTION_OFFSET, 50, WHITE)
            
            for button in buttons:
                button.draw(screen, BUTTON_COLOUR)
            
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
        
        correct_index = answerOptions.index(current_question.correctAnswer)
        return user_answer == correct_index
    
    countdown(titleofquiz, BLACK, WHITE)
    generate_level()
    
    # Main game loop
    clock = pygame.time.Clock()
    last_platform_x = SCREEN_WIDTH
    
    while running and lives > 0:
        screen.fill(BLACK)
        
        # Display game info
        display_message(f"Lives: {lives}", 30, 30, WHITE)
        display_message(f"Score: {score}", 60, 30, WHITE)
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and not is_jumping:
            velocity_y = jump_power
            is_jumping = True
        
        # Apply gravity
        velocity_y += gravity
        player_y += velocity_y
        
        # Draw player
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, GREEN, player_rect)
        
        # Update and draw platforms
        for platform in platforms[:]:
            platform.rect.x -= game_speed
            pygame.draw.rect(screen, platform.color, platform.rect)
            
            # Check platform collision
            if player_rect.colliderect(platform.rect) and velocity_y > 0:
                player_y = platform.rect.top - player_size
                velocity_y = 0
                is_jumping = False
            
            # Remove off-screen platforms
            if platform.rect.right < 0:
                platforms.remove(platform)
        
        # Update and draw dots
        for dot in dots[:]:
            dot.rect.x -= game_speed
            if dot.active:
                pygame.draw.circle(screen, dot.color, 
                                 (dot.rect.centerx, dot.rect.centery), 10)
                
                if player_rect.colliderect(dot.rect):
                    dot.active = False
                    if handle_question():
                        score += 100
                    else:
                        lives -= 1
            
            if dot.rect.right < 0:
                dots.remove(dot)
        
        # Update and draw obstacles
        for obstacle in obstacles[:]:
            obstacle.rect.x -= game_speed
            pygame.draw.rect(screen, obstacle.color, obstacle.rect)
            
            if player_rect.colliderect(obstacle.rect):
                lives -= 1
                player_y = SCREEN_HEIGHT - 150
                velocity_y = 0
            
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
        
        # Generate new platforms when needed
        if last_platform_x - game_speed < SCREEN_WIDTH * 1.5:
            generate_platform_sequence(last_platform_x, 5)
            last_platform_x += (PLATFORM_WIDTH + 75) * 5
        
        # Check for falling off screen
        if player_y > SCREEN_HEIGHT:
            lives -= 1
            player_y = SCREEN_HEIGHT - 150
            velocity_y = 0
        
        # Check for game completion
        if question_index >= total_questions:
            display_message("You Win!", SCREEN_HEIGHT // 2, 100, GREEN)
            pygame.display.update()
            pygame.time.wait(3000)
            break
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
        
        pygame.display.update()
        clock.tick(60)
    
    if lives <= 0:
        display_message("Game Over!", SCREEN_HEIGHT // 2, 100, (255, 0, 0))
        pygame.display.update()
        pygame.time.wait(3000)