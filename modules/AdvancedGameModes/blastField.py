import pygame
import random
import math
from pygame.locals import *
from modules.elements import *
from modules.extendedText import *
from modules.otherWindows import countdown, Instructions

EXPLOSION_IMG = pygame.image.load("images/explosion.png")
QUESTION_IMG = pygame.image.load("images/coin.png")
PLAYER_IMG = pygame.image.load("images/figure.png")

POWERUP_COLOURS = {
    "bomb": (90,180,255),
    "radius": (255,190,60),
    "instant": (130,240,120)
}
POWERUP_LABELS = {"bomb":"B", "radius":"R", "instant":"A"}

def compute_grid_size(total_questions):
    N = max(total_questions, 9)
    cols = math.ceil(math.sqrt(N * 16/9))
    rows = math.ceil(N / cols)
    return int(cols), int(rows)

def tile_color(x, y):
    color1 = (210, 235, 255)
    color2 = (210, 255, 235)
    return color1 if (x + y) % 2 == 0 else color2

def get_explosion_tiles(cx, cy, grid_cols, grid_rows):
    tiles = [(cx, cy)]
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy == 0: continue
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < grid_cols and 0 <= ny < grid_rows:
                tiles.append((nx, ny))
    return tiles

def blastField(questionList, titleofquiz, doCountdown, doInstructions, v):
    if not questionList or len(questionList) == 0:
        return

    class Player:
        def __init__(self):
            self.x = grid_cols // 2
            self.y = grid_rows // 2
            self.lives = 3
            self.bomb_count = max(3, total_questions // 6)
            self.max_bomb_count = max(3, total_questions // 4)
            self.blast_radius = 1
            self.score = 0
            self.instant_answer = False

    total_questions = len(questionList)
    grid_cols, grid_rows = compute_grid_size(total_questions)
    TILE_W = SCREEN_WIDTH // grid_cols
    TILE_H = SCREEN_HEIGHT // grid_rows

    player = Player()
    bombs = []  
    explosions = []  
    questions = {}  
    powerups = {}
    popup_question = None
    popup_tile = None
    
    all_tiles = [(x, y) for x in range(grid_cols) for y in range(grid_rows) if (x, y) != (player.x, player.y)]
    random.shuffle(all_tiles)
    for i in range(min(len(questionList), len(all_tiles))):
        x, y = all_tiles[i]
        questions[(x, y)] = {"question": questionList[i], "revealed": False, "answered": False}

    if total_questions <= 10: countdown_time = 10
    elif total_questions <= 25: countdown_time = 15
    elif total_questions <= 50: countdown_time = 25
    else: countdown_time = 45

    if doInstructions:
        Instructions(
            (210, 235, 255), (60, 130, 130), (20,30,80), titleofquiz,
            p1="Move with arrow keys. Press SPACE to place a bomb! Bombs explode, revealing questions in their blast radius.",
            p2="Click a revealed question to answer it. Correct clears tiles and awards points, wrong costs a life. Power-ups may appear: extra bombs, or instant answer.",
            p3="Game ends if you run out of lives or questions. Maximize your score!"
        )
    if doCountdown:
        countdown(titleofquiz, (210,235,255), (20,30,80))

    clock = pygame.time.Clock()
    running = True

    def get_tile_rect(x, y):
        return pygame.Rect(x * TILE_W, y * TILE_H, TILE_W, TILE_H)

    def spawn_powerup(pos):
        r = random.random()
        if r < 0.5:
            powerups[pos] = {"type": "bomb"}
        else:
            powerups[pos] = {"type": "instant"}

    while running:
        t_now = pygame.time.get_ticks()
        
        if popup_question is None:
            screen.fill((210, 235, 255))
            
            for x in range(grid_cols):
                for y in range(grid_rows):
                    rect = get_tile_rect(x, y)
                    color = tile_color(x, y)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (110,180,220), rect, 2)

            
            for (qx, qy), qdata in questions.items():
                if qdata["revealed"] and not qdata["answered"]:
                    qrect = get_tile_rect(qx, qy)
                    img = pygame.transform.smoothscale(QUESTION_IMG, (min(TILE_W, TILE_H)-14, min(TILE_W, TILE_H)-14))
                    screen.blit(img, (qrect.centerx-img.get_width()//2, qrect.centery-img.get_height()//2))

            
            for (px, py), pdata in powerups.items():
                rect = get_tile_rect(px, py)
                color = POWERUP_COLOURS.get(pdata["type"], (255,255,255))
                pygame.draw.circle(screen, color, rect.center, min(TILE_W, TILE_H)//3)
                label = POWERUP_LABELS.get(pdata["type"], "?")
                font = pygame.font.Font(None, min(TILE_W, TILE_H)//2)
                txt = font.render(label, True, (40,40,40))
                txt_rect = txt.get_rect(center=rect.center)
                screen.blit(txt, txt_rect)

            
            prect = get_tile_rect(player.x, player.y)
            img = pygame.transform.smoothscale(PLAYER_IMG, (min(TILE_W, TILE_H)-8, min(TILE_W, TILE_H)-8))
            screen.blit(img, (prect.centerx-img.get_width()//2, prect.centery-img.get_height()//2))

            
            for bomb in bombs:
                if not bomb.get("exploded", False):
                    brect = get_tile_rect(bomb["x"], bomb["y"])
                    pygame.draw.circle(screen, (255,100,100), brect.center, min(TILE_W, TILE_H)//4)
                    pygame.draw.circle(screen, (255,255,255), brect.center, min(TILE_W, TILE_H)//4, 2)

            
            to_remove = []
            for exp in explosions:
                elapsed = t_now - exp["start"]
                grow_time = 250
                shrink_time = 250
                total_time = grow_time + shrink_time
                if elapsed > total_time:
                    to_remove.append(exp)
                    continue
                
                if elapsed <= grow_time:
                    scale = 0.5 + 0.5*(elapsed/grow_time)
                else:
                    scale = 1.0 - 0.5*((elapsed-grow_time)/shrink_time)
                for (ex, ey) in exp["tiles"]:
                    rect = get_tile_rect(ex, ey)
                    size = int(max(TILE_W, TILE_H) * scale) + 24
                    img = pygame.transform.smoothscale(EXPLOSION_IMG, (size, size))
                    screen.blit(img, (rect.centerx-img.get_width()//2, rect.centery-img.get_height()//2))
            
            for exp in to_remove:
                explosions.remove(exp)

            display_message(f"Lives: {player.lives}   Score: {player.score}", 16, 32, (20,60,130))

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif popup_question is None and event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player.x > 0:
                    player.x -= 1
                elif keys[pygame.K_RIGHT] and player.x < grid_cols-1:
                    player.x += 1
                elif keys[pygame.K_UP] and player.y > 0:
                    player.y -= 1
                elif keys[pygame.K_DOWN] and player.y < grid_rows-1:
                    player.y += 1
                elif keys[pygame.K_SPACE]:
                    
                    if player.bomb_count > 0 and not any(b["x"]==player.x and b["y"]==player.y for b in bombs):
                        bombs.append({"x": player.x, "y": player.y, "placed_time": pygame.time.get_ticks(), "exploded": False})
                        player.bomb_count -= 1
            elif popup_question is None and event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                for (qx, qy), qdata in questions.items():
                    if qdata["revealed"] and not qdata["answered"]:
                        rect = get_tile_rect(qx, qy)
                        if rect.collidepoint(mx, my):
                            if player.instant_answer:
                                qdata["answered"] = True
                                player.instant_answer = False
                                player.score += 25
                                if random.random() < 0.5:
                                    spawn_powerup((qx, qy))
                                break
                            popup_question = qdata
                            popup_tile = (qx, qy)
                            break

        
        now = pygame.time.get_ticks()
        for bomb in bombs[:]:
            if not bomb.get("exploded", False) and now - bomb["placed_time"] >= 900:
                
                x0, y0 = bomb["x"], bomb["y"]
                affected = get_explosion_tiles(x0, y0, grid_cols, grid_rows)
                
                for pos in affected:
                    if pos in questions and not questions[pos]["answered"]:
                        questions[pos]["revealed"] = True
                
                explosions.append({"tiles": affected, "center": (x0, y0), "start": now})
                bomb["exploded"] = True
                bombs.remove(bomb)

        
        px, py = player.x, player.y
        if (px, py) in powerups:
            pu = powerups[(px, py)]["type"]
            if pu == "bomb":
                player.bomb_count = min(player.max_bomb_count, player.bomb_count+1)
            elif pu == "instant":
                player.instant_answer = True
            del powerups[(px, py)]

        
        if popup_question is not None:
            screen.fill((230,248,255))
            current_question = popup_question["question"]
            user_answer = None
            answerOptions = [current_question.correctAnswer] + current_question.wrongAnswers
            random.shuffle(answerOptions)
            buttons = []
            for idx, answer in enumerate(answerOptions):
                button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, 180 + idx * 60), 400, 40, (30,30,30), use_outline=True, outline_color=(60,130,190))
                buttons.append(button)
            display_message(f"Question:", 100, 38, (20,90,160), x_position=SCREEN_WIDTH//2)
            display_message(f"{current_question.question}", 140, 28, (20,40,90), x_position=SCREEN_WIDTH//2)
            for button in buttons:
                button.draw(screen, (255,255,255), border_radius=14)
            pygame.display.update()
            answered = False
            while not answered:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for idx, button in enumerate(buttons):
                            if button.is_clicked(pos):
                                user_answer = idx
                                answered = True
                                break
                    if event.type == KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            idx = event.key - pygame.K_1
                            if idx < len(answerOptions):
                                user_answer = idx
                                answered = True
                                break
            correct_index = answerOptions.index(current_question.correctAnswer)
            gx, gy = popup_tile
            if user_answer == correct_index:
                popup_question["answered"] = True
                player.score += 25
            else:
                player.lives -= 1
            popup_question = None
            popup_tile = None

        
        if player.lives <= 0 or all(q["answered"] for q in questions.values()):
            screen.fill((210,235,255))
            display_message("Game Over!" if player.lives <= 0 else "You Win!", SCREEN_HEIGHT//2-50, 80, (60,130,190), x_position=SCREEN_WIDTH//2)
            display_message(f"Final Score: {player.score}", SCREEN_HEIGHT//2+60, 50, (130,100,180), x_position=SCREEN_WIDTH//2)
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        pygame.display.flip()
        clock.tick(60)