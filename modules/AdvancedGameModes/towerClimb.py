import pygame
import random
import time

from pygame.locals import *
from modules.elements import *
#from modules.extendedText import towerClimb_p1, towerClimb_p2, towerClimb_p3
from modules.otherWindows import countdown, standard_end_window, Instructions

TILE_SIZE = 60
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 55
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 160
FLOOR_GAP = 130
MAX_LIVES = 3
MAX_POWERUPS = 2
POWERUP_CHANCE = 0.18
PLATFORM_MOVE_CHANCE = 0.30

ASCEND_SPEED = 3
DESCEND_SPEED = 8
BG_COLOR = (28, 35, 57)
PLATFORM_COLOR = (200, 200, 220)
PLAYER_COLOR = (250, 221, 63)
FLOOR_COLOR = (80, 80, 120)
QUESTION_PLATFORM_COLOR = (255, 110, 80)
POWERUP_COLOR = (150, 255, 100)
TRAP_COLOR = (200, 70, 70)
BLACK = (255, 255, 255)

class Platform:
    def __init__(self, x, y, width, is_question=False, is_trap=False, is_powerup=False, moves=False):
        self.x = x
        self.y = y
        self.width = width
        self.is_question = is_question
        self.is_trap = is_trap
        self.is_powerup = is_powerup
        self.moves = moves
        self.move_dir = 1 if random.random() < 0.5 else -1
        self.move_dist = 0
        self.max_move_dist = random.randint(60, 150) if moves else 0
        self.speed = random.uniform(0.7, 2.1) if moves else 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, PLATFORM_HEIGHT)
    
    def update(self):
        if self.moves:
            self.x += self.move_dir * self.speed
            self.move_dist += abs(self.speed)
            if self.move_dist >= self.max_move_dist:
                self.move_dir *= -1
                self.move_dist = 0

    def draw(self, surface):
        color = PLATFORM_COLOR
        if self.is_question:
            color = QUESTION_PLATFORM_COLOR
        elif self.is_powerup:
            color = POWERUP_COLOR
        elif self.is_trap:
            color = TRAP_COLOR
        pygame.draw.rect(surface, color, self.rect(), border_radius=8)

class PowerUp:
    def __init__(self, typ, x, y):
        self.typ = typ
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 28, 28)
        self.color = (100, 245, 90) if typ == "life" else (120, 190, 255) if typ == "skip" else (240, 230, 60)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)
        font = pygame.font.Font(None, 22)
        txt = "L" if self.typ == "life" else "S" if self.typ == "skip" else "D"
        text = font.render(txt, True, (30, 30, 30))
        surface.blit(text, self.rect.move(7, 4))

class Trap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 18)
        self.color = TRAP_COLOR

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
        font = pygame.font.Font(None, 18)
        surface.blit(font.render("!", True, (250, 250, 250)), self.rect.move(10, -2))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vx = 0
        self.vy = 0
        self.lives = MAX_LIVES
        self.shield = 0
        self.score = 0
        self.skip_tokens = 0
        self.grounded = False
        self.last_platform = None

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx):
        self.vx = dx

    def jump(self):
        if self.grounded:
            self.vy = -30
            self.grounded = False

    def update(self, platforms, powerups, traps):
        self.vy += 0.7
        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width

        self.grounded = False
        for plat in platforms:
            if self.rect().colliderect(plat.rect()):
                if self.vy > 0 and self.y + self.height - self.vy <= plat.y + 3:
                    self.y = plat.y - self.height
                    self.vy = 0
                    self.grounded = True
                    self.last_platform = plat
        for pu in powerups[:]:
            if self.rect().colliderect(pu.rect):
                if pu.typ == "life":
                    self.lives = min(self.lives+1, MAX_LIVES)
                elif pu.typ == "skip":
                    self.skip_tokens += 1
                elif pu.typ == "shield":
                    self.shield += 1
                powerups.remove(pu)
        for trap in traps[:]:
            if self.rect().colliderect(trap.rect):
                if self.shield > 0:
                    self.shield -= 1
                else:
                    self.lives -= 1
                traps.remove(trap)
                self.y += 23

def towerClimb(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if not questionList or len(questionList) == 0:
        return

    clock = pygame.time.Clock()

    Instructions(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, 
        p1=towerClimb_p1 if "towerClimb_p1" in globals() else "Climb the tower floor by floor! Each question is a floor. Watch out for traps and collect powerups.",
        p2=towerClimb_p2 if "towerClimb_p2" in globals() else "Move with arrow keys, jump with space, and reach the top! Correct answers let you skip floors.",
        p3=towerClimb_p3 if "towerClimb_p3" in globals() else "Some platforms are dangerous, and there are multiple ways to boost your climb!"
    )

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, BLACK)

    n_questions = len(questionList)
    n_floors = n_questions + 5
    platforms = []
    powerups = []
    traps = []

    floor_spacing = FLOOR_GAP
    platform_positions = []
    for i in range(n_floors):
        y = SCREEN_HEIGHT - (i+1)*floor_spacing
        is_question = (i < n_questions)
        is_trap = (random.random() < 0.17) and not is_question and i > 2
        is_powerup = (random.random() < POWERUP_CHANCE) and not is_question
        moves = (random.random() < PLATFORM_MOVE_CHANCE) and not is_question
        width = random.randint(110, PLATFORM_WIDTH)
        x = random.randint(50, SCREEN_WIDTH-width-50)
        platforms.append(Platform(x, y, width, is_question, is_trap, is_powerup, moves))
        if is_powerup:
            typ = random.choice(["life", "skip", "shield"])
            powerups.append(PowerUp(typ, x+width//2-14, y-35))
        if is_trap:
            traps.append(Trap(x+width//2-16, y-18))
        platform_positions.append((x, y))
    goal_platform = Platform(SCREEN_WIDTH//2-100, 60, 200, False, False, False, False)
    platforms.append(goal_platform)
    platform_positions.append((goal_platform.x, goal_platform.y))

    player = Player(platforms[0].x + platforms[0].width//2 - PLAYER_WIDTH//2, platforms[0].y - PLAYER_HEIGHT)
    player.lives = MAX_LIVES

    current_floor = 0
    question_index = 0
    answered_questions = set()
    question_answered_this_floor = False
    shield_flash = 0
    game_over = False
    win = False
    floor_labels = [f"Floor {i+1}" for i in range(n_floors-1)] + ["Rooftop"]
    font = pygame.font.Font(None, 30)
    big_font = pygame.font.Font(None, 60)

    # --- Main Loop ---
    while not game_over and not win:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); return
            if event.type == KEYDOWN:
                if event.key in (K_w, K_UP, K_SPACE):
                    player.jump()
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[K_LEFT] or keys[K_a]:
            dx = -6
        elif keys[K_RIGHT] or keys[K_d]:
            dx = 6
        player.move(dx)
        # Update moving platforms
        for plat in platforms:
            plat.update()
        # Update player
        player.update(platforms, powerups, traps)

        # Ascend camera if player is moving up
        cam_offset = min(0, SCREEN_HEIGHT//2 - player.y - player.height//2)
        # Draw BG
        screen.fill(BACKGROUND_COLOUR)
        # Draw platforms, powerups, traps
        for plat in platforms:
            draw_y = plat.y + cam_offset
            plat_draw = Platform(plat.x, draw_y, plat.width, plat.is_question, plat.is_trap, plat.is_powerup, plat.moves)
            plat_draw.draw(screen)
            # Label floors
            label = font.render(floor_labels[platforms.index(plat)] if platforms.index(plat) < len(floor_labels) else "", True, FLOOR_COLOR)
            screen.blit(label, (plat.x+plat.width//2-label.get_width()//2, draw_y-23))
        for pu in powerups:
            pu_draw = PowerUp(pu.typ, pu.x, pu.y + cam_offset)
            pu_draw.draw(screen)
        for trap in traps:
            tr_draw = Trap(trap.x, trap.y + cam_offset)
            tr_draw.draw(screen)
        # Draw goal
        pygame.draw.rect(screen, (180, 210, 255), goal_platform.rect().move(0, cam_offset), border_radius=8)
        screen.blit(font.render("Goal", True, (0, 0, 80)), (goal_platform.x+70, goal_platform.y+cam_offset-18))

        # Draw player (with shield effect)
        ply_rect = player.rect().move(0, cam_offset)
        color = PLAYER_COLOR if player.shield == 0 or shield_flash % 8 < 4 else (255, 255, 180)
        pygame.draw.ellipse(screen, color, ply_rect)
        # Player stats
        lives_txt = "♥ " * player.lives + "♡ " * (MAX_LIVES-player.lives)
        stats = f"Lives: {lives_txt}  •  Shield: {player.shield}  •  Skips: {player.skip_tokens}  •  Floor: {current_floor+1}/{n_floors}"
        screen.blit(font.render(stats, True, BLACK), (40, 18))
        # Question trigger
        current_plat = None
        for plat in platforms:
            if player.rect().colliderect(plat.rect()):
                current_plat = plat
                break
        if current_plat and current_plat.is_question and platforms.index(current_plat) not in answered_questions:
            # Pause player
            player.vx = 0
            player.vy = 0
            # Ask quiz question
            this_q = questionList[question_index]
            user_answer = None
            answerOptions = [this_q.correctAnswer] + this_q.wrongAnswers
            random.shuffle(answerOptions)
            buttons = []
            for idx, answer in enumerate(answerOptions):
                button = Button(f"{idx+1}. {answer}", (SCREEN_WIDTH//2-200, 220+idx*60), 400, 40, BLACK)
                buttons.append(button)
            btn_skip = Button("Skip (press K)", (SCREEN_WIDTH//2-200, 220+len(answerOptions)*60+30), 400, 40, BLACK)
            while user_answer is None:
                for ev in pygame.event.get():
                    if ev.type == QUIT:
                        pygame.quit(); return
                    if ev.type == KEYDOWN:
                        if ev.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            user_answer = ev.key - pygame.K_1
                        if ev.key == pygame.K_k and player.skip_tokens > 0:
                            user_answer = "skip"
                    if ev.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for idx, button in enumerate(buttons):
                            if button.is_clicked(pos):
                                user_answer = idx
                        if btn_skip.is_clicked(pos) and player.skip_tokens > 0:
                            user_answer = "skip"
                screen.fill(BACKGROUND_COLOUR)
                for plat in platforms:
                    plat_draw = Platform(plat.x, plat.y + cam_offset, plat.width, plat.is_question, plat.is_trap, plat.is_powerup, plat.moves)
                    plat_draw.draw(screen)
                for pu in powerups:
                    pu_draw = PowerUp(pu.typ, pu.x, pu.y + cam_offset)
                    pu_draw.draw(screen)
                for trap in traps:
                    tr_draw = Trap(trap.x, trap.y + cam_offset)
                    tr_draw.draw(screen)
                pygame.draw.ellipse(screen, color, ply_rect)
                # Question prompt
                qtxt = this_q.question
                y = 90
                for line in qtxt.split("\n"):
                    question_line = font.render(line, True, BLACK)
                    screen.blit(question_line, (SCREEN_WIDTH//2-question_line.get_width()//2, y))
                    y += 28
                for button in buttons:
                    button.draw(screen, BUTTON_COLOUR)
                if player.skip_tokens > 0:
                    btn_skip.draw(screen, (210, 210, 30))
                screen.blit(font.render(f"Lives: {player.lives}   Shield: {player.shield}   Skips: {player.skip_tokens}", True, BLACK), (60, SCREEN_HEIGHT-50))
                pygame.display.update()
            # Handle skip
            if user_answer == "skip":
                player.skip_tokens -= 1
                display_message("Skipped!", SCREEN_HEIGHT//2, 60, (255, 255, 80))
                pygame.display.update()
                pygame.time.wait(800)
            else:
                if answerOptions[user_answer] == this_q.correctAnswer:
                    player.score += 150
                    display_message("Correct!", SCREEN_HEIGHT//2, 80, (70, 255, 80))
                    pygame.display.update()
                    pygame.time.wait(800)
                    # 20% to get a bonus powerup
                    if random.random() < 0.20 and len(powerups) < MAX_POWERUPS+n_floors//5:
                        typ = random.choice(["life", "skip", "shield"])
                        pwr = PowerUp(typ, current_plat.x+current_plat.width//2-14, current_plat.y-65)
                        powerups.append(pwr)
                else:
                    if player.shield > 0:
                        player.shield -= 1
                        shield_flash = 0
                        display_message("Shield saved you!", SCREEN_HEIGHT//2, 50, (255, 230, 100))
                        pygame.display.update()
                        pygame.time.wait(1000)
                    else:
                        player.lives -= 1
                        display_message(f"Wrong! Correct: {this_q.correctAnswer}", SCREEN_HEIGHT//2, 60, (255, 90, 90))
                        pygame.display.update()
                        pygame.time.wait(1600)
                        if player.lives <= 0:
                            game_over = True
                            break
            answered_questions.add(platforms.index(current_plat))
            question_index += 1
            if question_index >= len(questionList):
                current_floor = n_floors-1
        # Win condition: reach the goal (top platform)
        if player.rect().colliderect(goal_platform.rect()):
            win = True
            break
        # Floor tracking
        for idx, plat in enumerate(platforms):
            if player.rect().colliderect(plat.rect()):
                current_floor = idx
                break
        # Game over if fell below screen
        if player.y > SCREEN_HEIGHT + 80:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True
            else:
                # Respawn at last platform
                if player.last_platform:
                    player.x = player.last_platform.x + player.last_platform.width//2 - PLAYER_WIDTH//2
                    player.y = player.last_platform.y - PLAYER_HEIGHT - 6
                    player.vx = 0
                    player.vy = 0
        shield_flash += 1
        # Draw
        pygame.display.update()

    # --- End Window ---
    if win:
        praise = [
            f"Incredible! You conquered the tower of {titleofquiz}!",
            f"QuizMaster Champion! Floor reached: {n_floors}",
            f"Your quiz climbing skills are legendary!"
        ]
        msg = random.choice(praise)
        while True:
            screen.fill(BACKGROUND_COLOUR)
            y = display_message(msg, SCREEN_HEIGHT//2-180, 50, (100, 255, 120))
            y = display_message(f"Final Score: {player.score}", y+40, 40, (250, 250, 250))
            y = display_message(f"Skips Left: {player.skip_tokens}  •  Shield: {player.shield}  •  Lives: {player.lives}", y+30, 35, (255, 255, 200))
            btn_menu = Button("Main Menu", (SCREEN_WIDTH//2-150, y+60), 250, 40, BLACK)
            btn_replay = Button("Replay", (SCREEN_WIDTH//2-150, y+110), 250, 40, BLACK)
            btn_quit = Button("Quit", (SCREEN_WIDTH//2-150, y+160), 250, 40, BLACK)
            btn_menu.draw(screen, BUTTON_COLOUR)
            btn_replay.draw(screen, BUTTON_COLOUR)
            btn_quit.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); return
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn_menu.is_clicked(pos):
                        return
                    if btn_replay.is_clicked(pos):
                        towerClimb(questionList, titleofquiz, doCountdown)
                        return
                    if btn_quit.is_clicked(pos):
                        pygame.quit(); return
    else:
        msg = "Game Over! The tower defeated you."
        while True:
            screen.fill(BACKGROUND_COLOUR)
            y = display_message(msg, SCREEN_HEIGHT//2-120, 50, (255, 80, 80))
            y = display_message(f"Final Score: {player.score}", y+20, 40, BLACK)
            btn_menu = Button("Main Menu", (SCREEN_WIDTH//2-150, y+60), 250, 40, BLACK)
            btn_replay = Button("Replay", (SCREEN_WIDTH//2-150, y+110), 250, 40, BLACK)
            btn_quit = Button("Quit", (SCREEN_WIDTH//2-150, y+160), 250, 40, BLACK)
            btn_menu.draw(screen, BUTTON_COLOUR)
            btn_replay.draw(screen, BUTTON_COLOUR)
            btn_quit.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); return
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn_menu.is_clicked(pos):
                        return
                    if btn_replay.is_clicked(pos):
                        towerClimb(questionList, titleofquiz, doCountdown)
                        return
                    if btn_quit.is_clicked(pos):
                        pygame.quit(); return

# --- Display Message Helper ---
def display_message(msg, y, size, color):
    font = pygame.font.Font(None, size)
    lines = msg.split("\n")
    for i, line in enumerate(lines):
        text = font.render(line, True, color)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y + i*size))
    return y + len(lines)*size