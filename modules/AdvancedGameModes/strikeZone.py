import pygame
import random
import math
import time

from pygame.locals import *
from modules.elements import *
from modules.constants import *
from modules.extendedText import strikeZone_p1, strikeZone_p2, strikeZone_p3
from modules.otherWindows import countdown, Instructions

GUNS = [
    {
        "name": "Pistol",
        "desc": "Balanced: moderate damage, fast fire",
        "damage": 1,
        "ammo_cost": 1,
        "cooldown": 50,
        "projectile_speed": 22,
        "color": (255, 255, 0),
        "kills_cost": 0
    },
    {
        "name": "SMG",
        "desc": "Rapid fire, low damage, cheap ammo",
        "damage": 0.5,
        "ammo_cost": 1,
        "cooldown": 15,
        "projectile_speed": 19,
        "color": (180, 180, 180),
        "kills_cost": 5
    },
    {
        "name": "Shotgun",
        "desc": "Fires 3 spread shots, medium ammo use",
        "damage": 1,
        "ammo_cost": 3,
        "cooldown": 250,
        "projectile_speed": 13,
        "color": (255, 160, 40),
        "spread": 18,
        "pellets": 3,
        "kills_cost": 30
    },
    {
        "name": "Sniper",
        "desc": "High damage, slow fire, precise",
        "damage": 5,
        "ammo_cost": 2,
        "cooldown": 850,
        "projectile_speed": 40,
        "color": (80, 255, 255),
        "kills_cost": 35
    },
    {
      "name": "Burst Rifle",
      "desc": "Shoots a quick 5-round burst, balanced damage and speed",
      "damage": 1,
      "ammo_cost": 5,
      "cooldown": 500,
      "projectile_speed": 20,
      "color": (120, 200, 255),
      "pellets": 5,
      "spread": 8,
      "kills_cost": 45
    },
    {
        "name": "Laser",
        "desc": "Pierces through enemies, costly, fast",
        "damage": 2,
        "ammo_cost": 10,
        "cooldown": 10,
        "projectile_speed": 100,
        "color": (220, 40, 255),
        "piercing": True,
        "kills_cost": 59
    },
    {
        "name": "Mine",
        "desc": "Explosive, moderate damage",
        "damage": 7,
        "ammo_cost": 6,
        "cooldown": 500,
        "projectile_speed": 0,
        "color": (75,54,33),
        "explosive": True,
        "explosion_size": 200,
        "kills_cost": 60
    },
    {
        "name": "Rocket",
        "desc": "High damage, slow, expensive",
        "damage": 10,
        "ammo_cost": 10,
        "cooldown": 1000,
        "projectile_speed": 11,
        "color": (255, 60, 60),
        "explosive": True,
        "explosion_size": 250,
        "kills_cost": 150
    },
    {
        "name": "Missile",
        "desc": "Very high damage, slow, very expensive",
        "damage": 100,
        "ammo_cost": 25,
        "cooldown": 1500,
        "projectile_speed": 5,
        "color": (200, 0, 0),
        "explosive": True,
        "explosion_size": 1500,
        "kills_cost": 499
    }
]

def strikeZone(questionList, titleofquiz, doCountdown, doInstructions, v):
    questionLength = len(questionList)

    if questionList is None or questionLength == 0:
        return

    running = True
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)
    BUTTON_COLOUR = (25, 25, 25)

    PLAYER_SPEED = 10
    PROJECTILE_SPEED = 20
    ENEMY_SPEED = 2
    ENEMY_SPAWN_RATE = 30
    POWER_UP_DURATION = 5000

    health = questionLength
    player = {"image": pygame.Surface((50, 50)), "rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 50), "health": health, "level": 1, "experience": 0}
    projectiles = []
    enemies = []
    powerups = []
    enemy_spawn_counter = 0
    ammo = questionLength * 5
    score = 0
    question_index = 0
    total_questions = questionLength
    shield_active = False
    shield_timer = 0
    all_out_shot_active = False
    all_out_shot_radius = 0
    all_out_shot_center = None
    gun_powerup_active = False
    owned_guns = [0]
    current_gun_index = 0
    last_fire_time = 0

    cannonFire = pygame.mixer.Sound('sounds/soundEffects/cannonFire.ogg')
    explosion = pygame.mixer.Sound('sounds/soundEffects/explosion.ogg')
    hit = pygame.mixer.Sound('sounds/soundEffects/hit.ogg')
    cannonFire.set_volume(v)
    explosion.set_volume(v)
    hit.set_volume(v)
    player["image"].fill(BLUE)

    def handle_question(forPowerup=False, powerup_type=None):
        nonlocal question_index, ammo, shield_active, shield_timer, all_out_shot_active, all_out_shot_radius, all_out_shot_center, gun_powerup_active
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
            if powerup_type == "white":
                all_out_shot_active = True
                all_out_shot_radius = 0
                all_out_shot_center = player["rect"].center
            elif powerup_type == "orange":
                shield_active = True
                shield_timer = pygame.time.get_ticks() + 9000
            elif powerup_type == "green":
                player["health"] += 2
            elif powerup_type == "yellow":
                ammo += 100
            else:
                ammo += 10
            return True
        return False

    def handle_shop():
        nonlocal score, owned_guns, current_gun_index
        shop_width = 600
        shop_height = 750
        shop_rect = pygame.Rect((SCREEN_WIDTH - shop_width)//2, (SCREEN_HEIGHT - shop_height)//2, shop_width, shop_height)
        font = pygame.font.Font(None, 52)
        item_font = pygame.font.Font(None, 38)
        desc_font = pygame.font.Font(None, 30)
        selected = 0
        running_shop = True

        for alpha in range(0, 170, 15):
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((10, 10, 20, alpha))
            screen.blit(dim, (0, 0))
            pygame.display.update()
            pygame.time.wait(10)

        buyable_guns = [i for i in range(len(GUNS)) if i not in owned_guns]
        if not buyable_guns:
            shop_items = []
        else:
            shop_items = [GUNS[i] for i in buyable_guns]

        while running_shop:
            screen.fill((0,0,0))
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((20, 20, 30, 140))
            screen.blit(dim, (0, 0))
            pygame.draw.rect(screen, (40, 40, 100), shop_rect, border_radius=24)
            pygame.draw.rect(screen, (110, 110, 220), shop_rect, 7, border_radius=24)
            title = font.render("Gun Shop", True, (255, 255, 140))
            screen.blit(title, (shop_rect.centerx - title.get_width()//2, shop_rect.y+24))

            coins_txt = desc_font.render(f"Kills: {score}", True, (255,240,160))
            screen.blit(coins_txt, (shop_rect.right-180, shop_rect.y+10))

            btn_w, btn_h = 340, 58
            btn_x = shop_rect.centerx - btn_w//2
            btn_y = shop_rect.y + 100

            for idx, gun in enumerate(shop_items):
                is_selected = (selected == idx)
                color = (100,255,160) if is_selected else (60,50,120)
                pygame.draw.rect(screen, color, (btn_x, btn_y+idx*70, btn_w, btn_h), border_radius=12)
                enough = score >= gun["kills_cost"]
                txt_col = (240,240,255) if enough else (100,100,100)
                gun_name = item_font.render(f"{gun['name']} [ {gun['kills_cost']} ]", True, txt_col)
                screen.blit(gun_name, (btn_x+16, btn_y+idx*70+8))
                desc = desc_font.render(gun["desc"], True, (130,230,255))
                screen.blit(desc, (btn_x+18, btn_y+idx*70+34))

            info = desc_font.render("Arrows: Select   Enter: Buy   Esc: Close", True, (210,210,255))
            screen.blit(info, (shop_rect.centerx-info.get_width()//2, shop_rect.bottom-48))

            pygame.display.update()
            pygame.time.wait(16)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key in [K_DOWN, K_s]:
                        selected = (selected+1)%max(1, len(shop_items))
                    if event.key in [K_UP, K_w]:
                        selected = (selected-1)%max(1, len(shop_items))
                    if event.key in [K_RETURN, K_KP_ENTER]:
                        if shop_items:
                            gun = shop_items[selected]
                            if score >= gun["kills_cost"]:
                                owned_guns.append(GUNS.index(gun))
                                score -= gun["kills_cost"]
                                running_shop = False
                    if event.key == K_ESCAPE:
                        running_shop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for idx in range(len(shop_items)):
                        if pygame.Rect(btn_x, btn_y+idx*70, btn_w, btn_h).collidepoint(mx, my):
                            gun = shop_items[idx]
                            if score >= gun["kills_cost"]:
                                owned_guns.append(GUNS.index(gun))
                                running_shop = False

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=strikeZone_p1, p2=strikeZone_p2, p3=strikeZone_p3)

    if doCountdown:
        countdown(titleofquiz, BLACK, WHITE)

    button_answer = Button("Answer Question", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 190), 300, 50, WHITE)
    button_shop = Button("Shop", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 250), 300, 50, WHITE)
    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 310), 250, 40, WHITE)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 360), 250, 40, WHITE)

    can_shoot = True
    fire_cooldown = 0

    while running:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()
        if shield_active and current_time > shield_timer:
            shield_active = False

        button_answer.draw(screen, BUTTON_COLOUR)
        button_shop.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)

        display_message(f'Health: {player["health"]}', 10, 24, WHITE)
        display_message(f'Ammo: {ammo}', 40, 24, WHITE)
        display_message(f'Score: {score}', 70, 24, WHITE)
        gun_strs = []
        for idx in owned_guns:
            if idx == current_gun_index:
                gun_strs.append(f"[{GUNS[idx]['name']}]")
            else:
                gun_strs.append(GUNS[idx]['name'])
        display_message("Guns: " + "  ".join(gun_strs), 100, 20, WHITE)

        screen.blit(player["image"], player["rect"])

        for projectile in projectiles:
            pygame.draw.circle(screen, projectile["color"], projectile["rect"].center, 8)

        for enemy in enemies:
            screen.blit(enemy["image"], enemy["rect"])

        for powerup in powerups:
            screen.blit(powerup["image"], powerup["rect"])

        if shield_active:
            pygame.draw.rect(screen, ORANGE, player["rect"], 5)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    idx = event.key - pygame.K_1
                    if idx in owned_guns:
                        current_gun_index = idx
                if event.key == pygame.K_SPACE and can_shoot and fire_cooldown <= 0:
                    gun = GUNS[current_gun_index]
                    if ammo >= gun["ammo_cost"]:
                        cannonFire.play()
                        if gun.get("pellets", 0) > 1:
                            for i in range(gun["pellets"]):
                                spread = random.uniform(-gun["spread"], gun["spread"])
                                base_angle = math.atan2(pygame.mouse.get_pos()[1] - player["rect"].centery, pygame.mouse.get_pos()[0] - player["rect"].centerx)
                                angle = base_angle + math.radians(spread)
                                proj_rect = pygame.Rect(player["rect"].centerx, player["rect"].centery, 10, 10)
                                projectiles.append({
                                    "color": gun["color"],
                                    "rect": proj_rect,
                                    "angle": angle,
                                    "projectile_speed": gun.get("projectile_speed", PROJECTILE_SPEED),
                                    "damage": gun["damage"],
                                    "piercing": gun.get("piercing", False),
                                    "explosive": gun.get("explosive", False),
                                    "explosion_size": gun.get("explosion_size", 200)
                                })
                        else:
                            angle = math.atan2(pygame.mouse.get_pos()[1] - player["rect"].centery, pygame.mouse.get_pos()[0] - player["rect"].centerx)
                            proj_rect = pygame.Rect(player["rect"].centerx, player["rect"].centery, 10, 10)
                            projectiles.append({
                                "color": gun["color"],
                                "rect": proj_rect,
                                "angle": angle,
                                "projectile_speed": gun.get("projectile_speed", PROJECTILE_SPEED),
                                "damage": gun["damage"],
                                "piercing": gun.get("piercing", False),
                                "explosive": gun.get("explosive", False),
                                "explosion_size": gun.get("explosion_size", 200)
                            })
                        ammo -= gun["ammo_cost"]
                        fire_cooldown = gun["cooldown"]
                        can_shoot = False
                if event.key == pygame.K_ESCAPE:
                    quit()
            elif event.type == KEYUP:
                if event.key == pygame.K_SPACE:
                    can_shoot = True
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_answer.is_clicked(pos):
                    handle_question(forPowerup=False)
                elif button_shop.is_clicked(pos):
                    handle_shop()
                elif button_go_back.is_clicked(pos):
                    if popup("Go Back?", "Are you sure you want to go back?", buttons=("Return", "Stay")) == "Return":
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
            speed = projectile.get("projectile_speed", PROJECTILE_SPEED)
            projectile["rect"].x += speed * math.cos(projectile["angle"])
            projectile["rect"].y += speed * math.sin(projectile["angle"])
            if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).contains(projectile["rect"]):
                projectiles.remove(projectile)

        enemy_spawn_counter += 1
        if enemy_spawn_counter >= ENEMY_SPAWN_RATE:
            enemy_spawn_counter = 0
            max_attempts = 20
            safe_distance = 500
            spawn_x, spawn_y = None, None
            for _ in range(max_attempts):
                candidate_x = random.randint(0, SCREEN_WIDTH - 50)
                candidate_y = random.randint(0, SCREEN_HEIGHT - 50)
                candidate_rect = pygame.Rect(candidate_x, candidate_y, 50, 50)
                dx = candidate_rect.centerx - player["rect"].centerx
                dy = candidate_rect.centery - player["rect"].centery
                distance = math.hypot(dx, dy)
                if not candidate_rect.colliderect(player["rect"]) and distance > safe_distance:
                    spawn_x, spawn_y = candidate_x, candidate_y
                    break
            if spawn_x is None or spawn_y is None:
                spawn_x = random.randint(0, SCREEN_WIDTH - 50)
                spawn_y = random.randint(0, SCREEN_HEIGHT - 50)
            enemies.append({
                "image": pygame.Surface((50, 50)),
                "rect": pygame.Rect(spawn_x, spawn_y, 50, 50)
            })
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
                if not shield_active:
                    hit.play()
                    player["health"] -= 1
                enemies.remove(enemy)

        if random.random() < 0.002 and len(powerups) < 12:
            types = ["yellow", "green", "white", "orange"]
            weights = [50, 30, 5, 15]
            powerup_type = random.choices(types, weights=weights)[0]
            powerup_color = {
                "yellow": YELLOW,
                "green": GREEN,
                "white": WHITE,
                "orange": ORANGE,
            }[powerup_type]
            powerups.append({
                "image": pygame.Surface((30, 30)),
                "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT - 30), 30, 30),
                "type": powerup_type
            })
            powerups[-1]["image"].fill(powerup_color)

        for powerup in powerups[:]:
            if player["rect"].colliderect(powerup["rect"]):
                handle_question(forPowerup=True, powerup_type=powerup["type"])
                powerups.remove(powerup)

        if all_out_shot_active:
            all_out_shot_radius += 10
            pygame.draw.circle(screen, (255, 255, 255), all_out_shot_center, all_out_shot_radius, 5)

            for enemy in enemies[:]:
                enemy_center = enemy["rect"].center
                distance_to_circle = math.hypot(enemy_center[0] - all_out_shot_center[0], enemy_center[1] - all_out_shot_center[1])
                if distance_to_circle <= all_out_shot_radius:
                    enemies.remove(enemy)
                    score += 1

            if all_out_shot_radius > max(SCREEN_WIDTH, SCREEN_HEIGHT) + 500:
                all_out_shot_active = False

        for projectile in projectiles[:]:
            hit_enemy = False
            for enemy in enemies[:]:
                if projectile["rect"].colliderect(enemy["rect"]):
                    hit_enemy = True
                    score += 1
                    if projectile.get("explosive"):
                        explosion.play()
                        for near_enemy in enemies[:]:
                            size = projectile.get("explosion_size")
                            if pygame.Rect.colliderect(projectile["rect"].inflate(size,size), near_enemy["rect"]):
                                enemies.remove(near_enemy)
                                score += 1
                    elif projectile.get("piercing"):
                        explosion.play()
                        enemies.remove(enemy)
                        continue
                    else:
                        explosion.play()
                        enemies.remove(enemy)
                    break
            if hit_enemy and not projectile.get("piercing"):
                if projectile in projectiles:
                    projectiles.remove(projectile)

        if player["health"] <= 0 or (question_index == questionLength and ammo <= 0 and score < questionLength*5):
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

        fire_cooldown = max(0, fire_cooldown-16)

        #ENEMY_SPAWN_RATE += 1
        pygame.display.flip()
        pygame.time.Clock().tick(60)
