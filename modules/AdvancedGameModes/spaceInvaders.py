import pygame
import random
import time
import os

from pygame.locals import *
from modules.elements import *
from modules.checker import isItHalloweenTimeNow
from modules.extendedText import *
from modules.otherWindows import countdown, standard_end_window, Instructions

ALIEN_TYPES = [
    {
        "name": "normal",
        "img": "images/SpaceshipAlien1.png" if not isItHalloweenTimeNow() else "images/pumpkin1.png",
        "health": 1,
        "probability": 0.8,
        "gun": "normal",
        "kill_value": 1,
    },
    {
        "name": "shooter",
        "img": "images/SpaceshipAlien2.png" if not isItHalloweenTimeNow() else "images/ghost1.png",
        "health": 1,
        "probability": 0.08,
        "gun": "strong",
        "kill_value": 2,
    },
    {
        "name": "tough",
        "img": "images/SpaceshipAlien3.png" if not isItHalloweenTimeNow() else "images/pumpkin2.png",
        "health": 4,
        "probability": 0.1,
        "gun": "normal",
        "kill_value": 3,
    },
    {
        "name": "leader",
        "img": "images/SpaceshipAlienLeader.png" if not isItHalloweenTimeNow() else "images/ghost1.png",
        "health": 10,
        "probability": 0.02,
        "gun": "strong",
        "kill_value": 10,
    }
]

SHOP_ITEMS = [
    {"name": "Speed Boost", "desc": "Move faster for 15s", "cost": 10, "type": "speed"},
    {"name": "Laser Power", "desc": "Extra laser damage for 15s", "cost": 10, "type": "laser"},
    {"name": "Extra Life", "desc": "Gain +10 life", "cost": 16, "type": "life"},
    {"name": "Ammo Bonus", "desc": "+10 ammo per answer for 1 minute", "cost": 15, "type": "ammo"},
    {"name": "Shield", "desc": "Invulnerable for 15s", "cost": 20, "type": "shield"},
    {"name": "Auto-Fire", "desc": "Auto-shoot for 15s", "cost": 6, "type": "autofire"},
]

def spaceInvaders(questionList, titleofquiz, doCountdown, doInstructions, v):
    if questionList is None or len(questionList) == 0:
        return

    running = True
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BUTTON_COLOUR = (25, 25, 25)
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
    kill_currency = 0

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=spaceInvaders_p1, p2=spaceInvaders_p2)

    if doCountdown:
        countdown(titleofquiz, BLACK, WHITE)

    timed_effects = {}

    shop_bg_color = (45, 40, 80)
    shop_border_color = (160, 80, 255)
    shop_title_color = (255, 255, 140)
    shop_item_bg = (60, 50, 120)
    shop_highlight = (100, 255, 160)
    shop_text_color = (220, 220, 255)
    shop_desc_color = (130, 230, 255)
    shop_unavailable_color = (90, 90, 90)

    ALIEN_IMAGES = {}
    for atype in ALIEN_TYPES:
        img = pygame.image.load(atype["img"])
        img = pygame.transform.scale(img, (alien_width, alien_height))
        ALIEN_IMAGES[atype["name"]] = img

    player_laser_img = pygame.image.load('images/Laser.png')
    alien_laser_img = pygame.image.load('images/Laser.png')
    explosion_sound = pygame.mixer.Sound('sounds/soundEffects/explosion.ogg')
    hit = pygame.mixer.Sound('sounds/soundEffects/hit.ogg')
    player_img = pygame.image.load('images/Spaceship.png')
    explosion_img = pygame.image.load('images/explosion.png')

    if isItHalloweenTimeNow():
        cannonFire = pygame.mixer.Sound('sounds/soundEffects/laserFire.ogg')
        strongCannonFire = pygame.mixer.Sound('sounds/soundEffects/laserFire.ogg')
    else:
        cannonFire = pygame.mixer.Sound('sounds/soundEffects/cannonFire.ogg')
        strongCannonFire = pygame.mixer.Sound('sounds/soundEffects/cannonFire.ogg')

    cannonFire.set_volume(v)
    explosion_sound.set_volume(v)
    hit.set_volume(v)
    strongCannonFire.set_volume(min(v+0.3, 1))

    player_img = pygame.transform.scale(player_img, (player_width, player_height))
    player_laser_img = pygame.transform.scale(player_laser_img, (15, 50))
    alien_laser_img = pygame.transform.scale(alien_laser_img, (20, 60))
    explosion_img = pygame.transform.scale(explosion_img, (60, 60))

    def choose_alien_type():
        rnd = random.random()
        cumulative = 0.0
        for atype in ALIEN_TYPES:
            cumulative += atype["probability"]
            if rnd < cumulative:
                return atype
        return ALIEN_TYPES[0]

    def generate_aliens(rows, cols):
        aliens.clear()
        bottom_y = 250 - alien_height
        for row in range(rows):
            for col in range(cols):
                atype = choose_alien_type()
                aliens.append({
                    "x": col * (alien_width + 10) + 50,
                    "y": bottom_y - row * (alien_height + 10),
                    "alive": True,
                    "type": atype["name"],
                    "health": atype["health"],
                    "max_health": atype["health"],
                    "gun": atype["gun"]
                })

    if total_questions < 40:
        rows = total_questions // 8 + 2
        cols = total_questions // 2 + 4
    else:
        cols = 20
        rows = total_questions - 32
    generate_aliens(rows, cols)

    def get_effect(name, default=0):
        now = pygame.time.get_ticks()
        if name in timed_effects:
            exp, val = timed_effects[name]
            if exp > now:
                return val
            else:
                del timed_effects[name]
        return default

    def set_effect(name, value, duration_ms):
        timed_effects[name] = [pygame.time.get_ticks() + duration_ms, value]

    def handle_shop():
        nonlocal kill_currency, lives, ammo, timed_effects
        shop_width = 600
        shop_height = 700
        shop_rect = pygame.Rect((SCREEN_WIDTH - shop_width)//2, (SCREEN_HEIGHT - shop_height)//2, shop_width, shop_height)
        font = pygame.font.Font(None, 52)
        item_font = pygame.font.Font(None, 38)
        desc_font = pygame.font.Font(None, 30)
        selected = 0
        clock = pygame.time.Clock()
        running_shop = True

        # Fade in effect
        for alpha in range(0, 180, 15):
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((20, 20, 20, alpha))
            screen.blit(dim, (0, 0))
            pygame.display.update()
            pygame.time.wait(10)

        while running_shop:
            screen.fill((0,0,0))
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((30, 30, 30, 160))
            screen.blit(dim, (0, 0))
            pygame.draw.rect(screen, shop_bg_color, shop_rect, border_radius=26)
            pygame.draw.rect(screen, shop_border_color, shop_rect, 7, border_radius=26)
            title = font.render("Space Shop", True, shop_title_color)
            screen.blit(title, (shop_rect.centerx - title.get_width()//2, shop_rect.y+24))

            coins_txt = desc_font.render(f"Kills: {kill_currency}", True, (255,240,160))
            screen.blit(coins_txt, (shop_rect.right-180, shop_rect.y+10))

            btn_w, btn_h = 340, 68
            btn_x = shop_rect.centerx - btn_w//2
            btn_y = shop_rect.y + 100

            for idx, item in enumerate(SHOP_ITEMS):
                is_selected = (selected == idx)
                color = shop_highlight if is_selected else shop_item_bg
                pygame.draw.rect(screen, color, (btn_x, btn_y+idx*80, btn_w, btn_h), border_radius=15)
                enough = kill_currency >= item["cost"]
                txt_col = shop_text_color if enough else shop_unavailable_color
                item_name = item_font.render(f"{item['name']} [ {item['cost']} ]", True, txt_col)
                screen.blit(item_name, (btn_x+24, btn_y+idx*80+12))
                desc = desc_font.render(item["desc"], True, shop_desc_color)
                screen.blit(desc, (btn_x+32, btn_y+idx*80+42))

            info = desc_font.render("Arrows: Select   Enter: Buy   Esc: Close", True, (210,210,255))
            screen.blit(info, (shop_rect.centerx-info.get_width()//2, shop_rect.bottom-48))

            pygame.display.update()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key in [K_DOWN, K_s]:
                        selected = (selected+1)%len(SHOP_ITEMS)
                    if event.key in [K_UP, K_w]:
                        selected = (selected-1)%len(SHOP_ITEMS)
                    if event.key in [K_RETURN, K_KP_ENTER]:
                        item = SHOP_ITEMS[selected]
                        if kill_currency >= item["cost"]:
                            kill_currency -= item["cost"]
                            now = pygame.time.get_ticks()
                            if item["type"] == "speed":
                                set_effect("speed", 11, 15000)
                            elif item["type"] == "laser":
                                set_effect("laser_power", 2.5, 15000)
                            elif item["type"] == "life":
                                lives += 10
                            elif item["type"] == "ammo":
                                set_effect("ammo_per_answer", 18, 60000)
                            elif item["type"] == "shield":
                                set_effect("shield", True, 15000)
                            elif item["type"] == "autofire":
                                set_effect("autofire", True, 15000)
                            running_shop = False
                            break
                    if event.key == K_ESCAPE:
                        running_shop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for idx in range(len(SHOP_ITEMS)):
                        if pygame.Rect(btn_x, btn_y+idx*80, btn_w, btn_h).collidepoint(mx, my):
                            item = SHOP_ITEMS[idx]
                            if kill_currency >= item["cost"]:
                                kill_currency -= item["cost"]
                                if item["type"] == "speed":
                                    set_effect("speed", 11, 15000)
                                elif item["type"] == "laser":
                                    set_effect("laser_power", 2.5, 15000)
                                elif item["type"] == "life":
                                    lives += 10
                                elif item["type"] == "ammo":
                                    set_effect("ammo_per_answer", 18, 60000)
                                elif item["type"] == "shield":
                                    set_effect("shield", True, 15000)
                                elif item["type"] == "autofire":
                                    set_effect("autofire", True, 15000)
                                running_shop = False
                                break

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
            screen.fill((0, 0, 0))
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
                ammo += get_effect("ammo_per_answer", total_questions // 10 + 10)
            return True
        return False

    button_answer = Button("Answer Question", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 190), 300, 50, WHITE)
    button_shop = Button("Shop", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 250), 300, 50, WHITE)
    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 310), 250, 40, WHITE)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 360), 250, 40, WHITE)

    can_shoot = True
    auto_fire_timer = 0

    while running and lives > 0:
        screen.fill(BLACK)

        display_message(f"Money: ${kill_currency}", 45, 45, (255,255,150), x_position=120)
        display_message(f"Lives: {lives}", 45, 50, WHITE)
        display_message(f"Ammo: {ammo}", 75, 50, WHITE)
        display_message(f"Question {question_index}/{total_questions}", 105, 50, WHITE)

        xfx = SCREEN_WIDTH-200
        yfx = 15
        for fx in timed_effects:
            exp, _ = timed_effects[fx]
            remain = max(0, (exp-pygame.time.get_ticks())//1000)
            color = (130,255,200) if remain > 0 else (200,200,200)
            display_message(f"{fx} ({remain}s)", yfx, 36, color, x_position=xfx)
            yfx += 28

        button_answer.draw(screen, BUTTON_COLOUR)
        button_shop.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)

        if get_effect("shield", False):
            pygame.draw.ellipse(screen, (240,255,255,120), (player_x-10, player_y-10, player_width+20, player_height+20), 5)

        screen.blit(player_img, (player_x, player_y))

        numAliens = 0
        max_alien_y = -float('inf')

        for alien in aliens:
            if alien["alive"]:
                numAliens += 1
                screen.blit(ALIEN_IMAGES[alien["type"]], (alien["x"], alien["y"]))
                if alien["max_health"] > 1:
                    health_ratio = alien["health"] / alien["max_health"]
                    bar_width = int(alien_width * health_ratio)
                    pygame.draw.rect(screen, (255, 0, 0), (alien["x"], alien["y"] - 8, alien_width, 5))
                    pygame.draw.rect(screen, (0, 255, 0), (alien["x"], alien["y"] - 8, bar_width, 5))
                    if health_ratio <= 1:
                        alien["health"] += 0.00025
                alien["x"] += alien_speed
                if alien["x"] > SCREEN_WIDTH - alien_width or alien["x"] < 0:
                    alien_speed *= -1
                    for a in aliens:
                        a["y"] += 25 / numAliens

                shoot_chance = 0.015 if alien["gun"] == "normal" else 0.05
                if random.random() < shoot_chance * (1 / numAliens):
                    if alien["gun"] == "strong":
                        strongCannonFire.play()
                        alien_projectiles.append({
                            "x": alien["x"] + alien_width // 2,
                            "y": alien["y"] + alien_height,
                            "speed": projectile_speed * 1.7,
                            "color": (255, 0, 0, 0.2)
                        })
                    else:
                        cannonFire.play()
                        alien_projectiles.append({
                            "x": alien["x"] + alien_width // 2,
                            "y": alien["y"] + alien_height,
                            "speed": projectile_speed,
                            "color": (0, 255, 0, 0.2)
                        })

                if alien["y"] > max_alien_y:
                    max_alien_y = alien["y"]

        for projectile in projectiles[:]:
            screen.blit(player_laser_img, (projectile["x"], projectile["y"]))
            projectile["y"] -= projectile_speed
            if projectile["y"] < 0:
                projectiles.remove(projectile)

        for alien_projectile in alien_projectiles[:]:
            color = alien_projectile.get("color", (255, 255, 255))
            pygame.draw.rect(screen, color, (alien_projectile["x"], alien_projectile["y"], 5, 10), border_radius=5)
            alien_projectile["y"] += alien_projectile.get("speed", projectile_speed)
            if alien_projectile["y"] > SCREEN_HEIGHT:
                alien_projectiles.remove(alien_projectile)
            elif (player_x < alien_projectile["x"] < player_x + player_width and
                  player_y < alien_projectile["y"] < player_y + player_height):
                if not get_effect("shield", False):
                    alien_projectiles.remove(alien_projectile)
                    hit.play()
                    if not handle_question(True):
                        lives -= 1
                else:
                    alien_projectiles.remove(alien_projectile)

        for alien in aliens:
            if not alien["alive"]:
                continue
            for projectile in projectiles[:]:
                if (alien["x"] < projectile["x"] < alien["x"] + alien_width and
                        alien["y"] < projectile["y"] < alien["y"] + alien_height):
                    laser_power = get_effect("laser_power", 1.5)
                    alien["health"] -= laser_power
                    if alien["health"] <= 0:
                        alien["alive"] = False
                        explosion_sound.play()
                        explosions.append({
                            "x": alien["x"] + alien_width // 2,
                            "y": alien["y"] + alien_height // 2,
                            "size": 60,
                            "start_time": pygame.time.get_ticks(),
                            "duration": 1000
                        })
                        for t in ALIEN_TYPES:
                            if alien["type"] == t["name"]:
                                kill_currency += t["kill_value"]
                                break
                    else:
                        hit.play()
                    if projectile in projectiles:
                        projectiles.remove(projectile)

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

        if all(not alien["alive"] for alien in aliens):
            display_message("You Win!", SCREEN_HEIGHT // 2, 100, (0,255,0))
            pygame.display.update()
            pygame.time.wait(3000)
            break

        keys = pygame.key.get_pressed()
        move_speed = get_effect("speed", 5)
        if keys[K_LEFT] and player_x > 0:
            player_x -= move_speed
        if keys[K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += move_speed

        if get_effect("autofire", False) and ammo > 0:
            auto_fire_timer += 1
            if auto_fire_timer > 10:
                cannonFire.play()
                projectiles.append({"x": player_x + player_width // 2, "y": player_y})
                ammo -= 1
                auto_fire_timer = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_answer.is_clicked(pos):
                    handle_question(False)
                elif button_shop.is_clicked(pos):
                    handle_shop()
                elif button_go_back.is_clicked(pos):
                    if popup("Go Back?", "Are you sure you want to go back?", buttons=("Return", "Stay")) == "Return":
                        return
                    else:
                        continue
                elif button_leave.is_clicked(pos):
                    quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and can_shoot and ammo > 0 and not get_effect("autofire", False):
                    cannonFire.play()
                    projectiles.append({"x": player_x + player_width // 2, "y": player_y})
                    ammo -= 1
                    can_shoot = False
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    can_shoot = True

        pygame.display.update()

    if lives < 0 or (question_index >= total_questions and all(alien["alive"] for alien in aliens)) or max_alien_y + alien_height >= player_y + player_height // 2:
        explosion_sound.play()
        display_message("You Lose!", SCREEN_HEIGHT // 2, 100, (255, 0, 0))
        pygame.display.update()
        pygame.time.wait(3000)