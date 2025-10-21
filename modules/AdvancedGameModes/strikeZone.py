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
        "color": (255, 179, 71),  
        "kills_cost": 0
    },
    {
        "name": "SMG",
        "desc": "Rapid fire, low damage, cheap ammo",
        "damage": 0.5,
        "ammo_cost": 1,
        "cooldown": 15,
        "projectile_speed": 20,
        "color": (170, 170, 180),  
        "kills_cost": 5
    },
    {
        "name": "Shotgun",
        "desc": "Fires 3 spread shots, medium ammo use",
        "damage": 1,
        "ammo_cost": 3,
        "cooldown": 150,
        "projectile_speed": 13,
        "color": (255, 160, 80),  
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
        "color": (0, 212, 255),  
        "kills_cost": 35
    },
    {
      "name": "Burst Rifle",
      "desc": "Quick 5-round bursts, balanced damage and speed",
      "damage": 1,
      "ammo_cost": 5,
      "cooldown": 450,
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
        "color": (200, 80, 255),  
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
        "color": (150, 100, 60),  
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
        "color": (255, 90, 90),  
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
        "color": (200, 40, 40),  
        "explosive": True,
        "explosion_size": 1500,
        "kills_cost": 299
    }
]

def strikeZone(questionList, titleofquiz, doCountdown, doInstructions, v):
    questionLength = len(questionList)

    if questionList is None or questionLength == 0:
        return

    running = True
    
    BG_TOP = (12, 18, 36)         
    BG_BOTTOM = (18, 28, 48)      
    UI_TEXT = (230, 236, 241)     
    DANGER = (255, 99, 71)        
    SUCCESS = (102, 255, 178)     
    ACCENT = (0, 212, 255)        
    GOLD = (255, 179, 71)         
    PLAYER_COLOR = (0, 200, 180)  
    ENEMY_COLOR = (255, 80, 90)   
    POWERUP_GLOW = (255, 200, 110) 
    BUTTON_COLOUR = (28, 36, 54)  

    PLAYER_SPEED = 10
    PROJECTILE_SPEED = 20
    ENEMY_SPEED = 2
    ENEMY_SPAWN_RATE = 30
    POWER_UP_DURATION = 5000

    leaveGame = False
    health = questionLength
    player = {"image": pygame.Surface((50, 50), pygame.SRCALPHA), "rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 50), "health": health, "level": 1, "experience": 0}
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
    
    player["image"].fill(PLAYER_COLOR)
    inner = pygame.Surface((44,44), pygame.SRCALPHA)
    inner.fill((255,255,255,18))
    player["image"].blit(inner, (3,3))

    def endGameScreen(message, textColour):
        screen.fill(BG_TOP)
        display_message(message, 300, 100, textColour)
        pygame.display.flip()
        pygame.time.wait(3000)
        return

    def draw_background(surface):
        h = SCREEN_HEIGHT
        step = 12  
        for i in range(0, h, step):
            t = i / h
            r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
            g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
            b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
            pygame.draw.rect(surface, (r, g, b), (0, i, SCREEN_WIDTH, step))
        
        rng = random.Random(999)
        star_count = 80
        for i in range(star_count):
            x = rng.randint(0, SCREEN_WIDTH - 1)
            y = rng.randint(0, SCREEN_HEIGHT - 1)
            
            brightness = rng.randint(120, 255)
            size = rng.choice([1, 2, 3])
            col = (brightness, brightness, brightness)
            if size == 1:
                surface.set_at((x, y), col)
            else:
                pygame.draw.circle(surface, col, (x, y), 1)

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
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, UI_TEXT)
            buttons.append(button)

        while user_answer is None:
            draw_background(screen)
            display_message(f"Question: {current_question.question}", QUESTION_OFFSET, 50, GOLD)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BUTTON_COLOUR)
            
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
                player["health"] += 5
            elif powerup_type == "yellow":
                ammo += 100
            else:
                ammo += 10
            return True
        return False

    def handle_shop():
        nonlocal score, owned_guns, current_gun_index
        shop_width = 620
        shop_height = 760
        shop_rect = pygame.Rect((SCREEN_WIDTH - shop_width)//2, (SCREEN_HEIGHT - shop_height)//2, shop_width, shop_height)
        font = pygame.font.Font(None, 52)
        item_font = pygame.font.Font(None, 38)
        desc_font = pygame.font.Font(None, 30)
        selected = 0
        running_shop = True

        for alpha in range(0, 190, 15):
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((8, 10, 18, alpha))
            screen.blit(dim, (0, 0))
            pygame.display.update()
            pygame.time.wait(8)

        buyable_guns = [i for i in range(len(GUNS)) if i not in owned_guns]
        if not buyable_guns:
            shop_items = []
        else:
            shop_items = [GUNS[i] for i in buyable_guns]

        while running_shop:
            draw_background(screen)
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((10, 12, 20, 160))
            screen.blit(dim, (0, 0))
            pygame.draw.rect(screen, (20, 26, 46), shop_rect, border_radius=20)
            pygame.draw.rect(screen, ACCENT, shop_rect, 5, border_radius=20)
            title = font.render("Gun Shop", True, GOLD)
            screen.blit(title, (shop_rect.centerx - title.get_width()//2, shop_rect.y+24))

            coins_txt = desc_font.render(f"Kills: {score}", True, (220,220,220))
            screen.blit(coins_txt, (shop_rect.right-190, shop_rect.y+12))

            btn_w, btn_h = 420, 64
            btn_x = shop_rect.centerx - btn_w//2
            btn_y = shop_rect.y + 110

            for idx, gun in enumerate(shop_items):
                is_selected = (selected == idx)
                color = (14, 44, 60) if not is_selected else (10, 80, 90)
                pygame.draw.rect(screen, color, (btn_x, btn_y+idx*78, btn_w, btn_h), border_radius=12)
                enough = score >= gun["kills_cost"]
                txt_col = UI_TEXT if enough else (140,140,150)
                gun_name = item_font.render(f"{gun['name']} [ {gun['kills_cost']} ]", True, txt_col)
                screen.blit(gun_name, (btn_x+18, btn_y+idx*78+8))
                desc = desc_font.render(gun["desc"], True, (160,220,240))
                screen.blit(desc, (btn_x+18, btn_y+idx*78+36))
                pygame.draw.rect(screen, gun["color"], (btn_x+btn_w-64, btn_y+idx*78+12, 44, 40), border_radius=8)

            info = desc_font.render("Arrows: Select   Enter: Buy   Esc: Close", True, (200,200,210))
            screen.blit(info, (shop_rect.centerx-info.get_width()//2, shop_rect.bottom-56))

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
                        if pygame.Rect(btn_x, btn_y+idx*78, btn_w, btn_h).collidepoint(mx, my):
                            gun = shop_items[idx]
                            if score >= gun["kills_cost"]:
                                owned_guns.append(GUNS.index(gun))
                                running_shop = False

    if doInstructions:
        Instructions(BG_TOP, BUTTON_COLOUR, UI_TEXT, titleofquiz, p1=strikeZone_p1, p2=strikeZone_p2, p3=strikeZone_p3)

    if doCountdown:
        countdown(titleofquiz, BG_TOP, UI_TEXT)

    button_answer = Button("Answer Question", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 100), 300, 50, UI_TEXT)
    button_shop = Button("Shop", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 190), 300, 50, UI_TEXT)
    button_end = Button("End Game", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 250), 300, 50, UI_TEXT)
    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 310), 250, 40, UI_TEXT)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 360), 250, 40, UI_TEXT)

    can_shoot = True
    fire_cooldown = 0

    while running:
        draw_background(screen)
        current_time = pygame.time.get_ticks()
        if shield_active and current_time > shield_timer:
            shield_active = False

        button_answer.draw(screen, BUTTON_COLOUR)
        button_shop.draw(screen, BUTTON_COLOUR)
        button_end.draw(screen, BUTTON_COLOUR, enabled=leaveGame)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)

        display_message(f'Health: {player["health"]}', 10, 24, UI_TEXT)
        display_message(f'Ammo: {ammo}', 40, 24, UI_TEXT)
        display_message(f'Score: {score}', 70, 24, UI_TEXT)
        gun_strs = []
        for idx in owned_guns:
            if idx == current_gun_index:
                gun_strs.append(f"[{GUNS[idx]['name']}]")
            else:
                gun_strs.append(GUNS[idx]['name'])
        display_message("Guns: " + "  ".join(gun_strs), 100, 20, ACCENT)

        glow_s = pygame.Surface((player["rect"].width*4, player["rect"].height*4), pygame.SRCALPHA)
        gw, gh = glow_s.get_size()
        pygame.draw.circle(glow_s, (*PLAYER_COLOR, 28), (gw//2, gh//2), max(gw, gh)//2)
        screen.blit(glow_s, (player["rect"].centerx - gw//2, player["rect"].centery - gh//2))
        screen.blit(player["image"], player["rect"])

        for projectile in projectiles:
            pygame.draw.circle(screen, projectile["color"], projectile["rect"].center, 7)
            try:
                pygame.draw.circle(screen, (255,255,255,20), projectile["rect"].center, 3)
            except Exception:
                pygame.draw.circle(screen, (255,255,255), projectile["rect"].center, 2)

        for enemy in enemies:
            shadow = pygame.Surface((enemy["rect"].width, enemy["rect"].height), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0,0,0,60), shadow.get_rect(), border_radius=8)
            screen.blit(shadow, (enemy["rect"].x+3, enemy["rect"].y+4))
            screen.blit(enemy["image"], enemy["rect"])

        for powerup in powerups:
            screen.blit(powerup["image"], powerup["rect"])
            try:
                pygame.draw.circle(screen, (255,255,255,8), powerup["rect"].center, 18, 2)
            except Exception:
                pygame.draw.circle(screen, (255,255,255), powerup["rect"].center, 18, 2)

        if shield_active:
            pygame.draw.rect(screen, (255, 165, 60), player["rect"], 5, border_radius=6)

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
                        now = pygame.time.get_ticks()
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
                                    "explosion_size": gun.get("explosion_size", 200),
                                    "owner": "player",
                                    "spawn_time": now,
                                    "can_hurt_player_after": now + 400,
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
                                "explosion_size": gun.get("explosion_size", 200),
                                "owner": "player",
                                "spawn_time": now,
                                "can_hurt_player_after": now + 400, 
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
                elif button_end.is_clicked(pos):
                    endGameScreen("You Win!", SUCCESS)
                    return
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

        current_time = pygame.time.get_ticks()
        for projectile in projectiles[:]:
            if projectile.get("owner") == "player":
                if current_time >= projectile.get("can_hurt_player_after", 0):
                    if player["rect"].colliderect(projectile["rect"]):
                        hit.play()
                        player["health"] -= 1
                        projectiles.remove(projectile)

        enemy_spawn_counter += 1
        if enemy_spawn_counter >= ENEMY_SPAWN_RATE:
            enemy_spawn_counter = 0
            max_attempts = 20
            safe_distance = 160
            spawn_x, spawn_y = None, None
            for _ in range(max_attempts):
                player_x = random.randint(0, SCREEN_WIDTH - 50)
                player_y = random.randint(0, SCREEN_HEIGHT - 50)
                player_rect = pygame.Rect(player_x, player_y, 50, 50)
                dx = player_rect.centerx - player["rect"].centerx
                dy = player_rect.centery - player["rect"].centery
                distance = math.hypot(dx, dy)
                if not player_rect.colliderect(player["rect"]) and distance > safe_distance:
                    spawn_x, spawn_y = player_x, player_y
                    break
            if spawn_x is None or spawn_y is None:
                spawn_x = random.randint(0, SCREEN_WIDTH - 50)
                spawn_y = random.randint(0, SCREEN_HEIGHT - 50)
            enemies.append({
                "image": pygame.Surface((50, 50)),
                "rect": pygame.Rect(spawn_x, spawn_y, 50, 50)
            })
            enemies[-1]["image"].fill(ENEMY_COLOR)

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
            powerup_type = random.choices(types, weights=[50, 30, 5, 15])[0]
            powerup_color = {
                "yellow": GOLD,
                "green": SUCCESS,
                "white": UI_TEXT,
                "orange": POWERUP_GLOW,
            }[powerup_type]
            w = 30
            powerups.append({
                "image": pygame.Surface((w, w), pygame.SRCALPHA),
                "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - w), random.randint(0, SCREEN_HEIGHT - w), w, w),
                "type": powerup_type
            })
            pu_surf = powerups[-1]["image"]
            pu_surf.fill((0,0,0,0))
            pygame.draw.circle(pu_surf, powerup_color, (w//2, w//2), w//2)
            pygame.draw.circle(pu_surf, (255,255,255,30), (w//2, w//2), w//2-4, 2)

        for powerup in powerups[:]:
            if player["rect"].colliderect(powerup["rect"]):
                handle_question(forPowerup=True, powerup_type=powerup["type"])
                powerups.remove(powerup)

        if all_out_shot_active:
            all_out_shot_radius += 12
            pygame.draw.circle(screen, (220, 240, 255), all_out_shot_center, all_out_shot_radius, 5)

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

        if question_index == questionLength and score > questionLength*10:
            leaveGame = True

        if player["health"] <= 0 or (question_index == questionLength and ammo <= 0): # <= if it is impossible for the player to win 
            explosion.play()
            endGameScreen("You Lose!", DANGER)
            return

        fire_cooldown = max(0, fire_cooldown-16)

        pygame.display.flip()
        pygame.time.Clock().tick(60)