import pygame
import random
import time
import os
import math

from pygame.locals import *
from modules.elements import *
from modules.checker import isItHalloweenTimeNow
from modules.extendedText import spaceInvaders_p1, spaceInvaders_p2
from modules.otherWindows import countdown, standard_end_window, Instructions

WHITE = (255, 255, 255)
BUTTON_TEXT = (240, 245, 255)
DEEP_SPACE = (8, 12, 30)
NEBULA_ACCENT = (20, 45, 80) 
NEON_A = (110, 200, 255)
NEON_B = (170, 110, 255)
HUD_PANEL = (12, 18, 34, 200)
HUD_TEXT = (230, 245, 255)
HUD_SECONDARY = (180, 200, 255)
BUTTON_COLOUR = (24, 28, 48)
BUTTON_HIGHLIGHT = (100, 180, 255)
GLOW_ALPHA = 110

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
    {"name": "Extra Ammo", "desc": "+100 ammo", "cost": 20, "type": "ammo"},
    {"name": "Ammo Bonus", "desc": "+10 ammo per answer for 1 minute", "cost": 15, "type": "ammo_bonus"},
    {"name": "Shield", "desc": "Invulnerable for 15s", "cost": 20, "type": "shield"},
    {"name": "Auto-Fire", "desc": "Auto-shoot for 10s", "cost": 6, "type": "autofire"},
]


def make_glow_surface(size, color, alpha=GLOW_ALPHA):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size // 2
    cy = size // 2
    radius = size // 2
    for r in range(radius, 0, -4):
        a = int(alpha * (r / radius) ** 1.2)
        pygame.draw.circle(surf, color + (a,), (cx, cy), r)
    return surf

def draw_rounded_panel(surface, rect, color, border_color=None, border_width=0, radius=18):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border_color and border_width > 0:
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=radius)


class StarField:
    def __init__(self, screen_w, screen_h, layers=2, density=0.0001):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.layers = []
        for i in range(layers):
            speed = i * 0.2
            count = max(5, int(screen_w * screen_h * density * (i * 0.5)))
            stars = []
            for _ in range(count):
                x = random.uniform(0, screen_w)
                y = random.uniform(0, screen_h)
                size = random.randint(1, 2 + i)
                base = 180 - i * 20
                col = (base + random.randint(0, 40), base + random.randint(0, 40), 255)
                stars.append([x, y, size, col])
            self.layers.append({"speed": speed, "stars": stars})
        
        self.nebula = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        self._generate_nebula()

    def _generate_nebula(self):
        for i in range(4):
            s = random.randint(180, 420)
            surf = pygame.Surface((s, s), pygame.SRCALPHA)
            cx = s // 2
            cy = s // 2
            base_color = (30 + random.randint(10, 40), 40 + random.randint(10, 40), 80 + random.randint(10, 40), 16 + random.randint(6, 18))
            for r in range(s//2, 0, -6):
                a = int(base_color[3] * (r / (s//2)) ** 2.0)
                c = (base_color[0], base_color[1], base_color[2], a)
                pygame.draw.circle(surf, c, (cx, cy), r)
            x = random.randint(-s//2, self.screen_w)
            y = random.randint(-s//2, self.screen_h)
            self.nebula.blit(surf, (x, y), special_flags=pygame.BLEND_ADD)

    def update_and_draw(self, screen, dt):
        screen.blit(self.nebula, (0, 0))
        for idx, layer in enumerate(self.layers):
            speed = layer["speed"]
            for star in layer["stars"]:
                star[1] += speed * dt * 0.04
                if star[1] > self.screen_h:
                    star[0] = random.uniform(0, self.screen_w)
                    star[1] = -2
                tw = 30 + int(30 * math.sin(pygame.time.get_ticks() / (800 + idx * 120) + star[0]))
                col = (min(255, star[3][0] + tw//6), min(255, star[3][1] + tw//6), min(255, star[3][2] + tw//6))
                pygame.draw.circle(screen, col, (int(star[0]), int(star[1])), star[2])


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    if not words:
        return lines
    cur = words[0]
    for w in words[1:]:
        test = cur + " " + w
        if font.size(test)[0] <= max_width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def spaceInvaders(questionList, titleofquiz, doCountdown, doInstructions, v):
    if questionList is None or len(questionList) == 0:
        return

    if doInstructions:
        Instructions(DEEP_SPACE, BUTTON_COLOUR, HUD_TEXT, titleofquiz, p1=spaceInvaders_p1, p2=spaceInvaders_p2)

    if doCountdown:
        countdown(titleofquiz, DEEP_SPACE, HUD_TEXT)

    running = True
    lives = int(len(questionList) // 3 + 1)
    ammo = 0
    aliens = []
    projectiles = []
    alien_projectiles = []
    explosions = []
    particles = []
    player_width, player_height = 56, 56
    alien_width, alien_height = 44, 44
    alien_speed = 1.0
    projectile_speed = 2
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - 110
    question_index = 0
    total_questions = len(questionList)
    kill_currency = 0
    
    starfield = StarField(SCREEN_WIDTH, SCREEN_HEIGHT, layers=2, density=0.0005)
    
    shop_bg_color = (12, 18, 32, 220)
    shop_border_color = NEON_B
    shop_title_color = NEON_A
    shop_item_bg = (22, 28, 46)
    shop_highlight = (100, 230, 255)
    shop_text_color = (220, 230, 255)
    shop_desc_color = (160, 200, 255)
    shop_unavailable_color = (90, 90, 100)

    
    ALIEN_IMAGES = {}
    for atype in ALIEN_TYPES:
        img = pygame.image.load(atype["img"]).convert_alpha()
        img = pygame.transform.smoothscale(img, (alien_width, alien_height))
        ALIEN_IMAGES[atype["name"]] = img

    player_laser_img = pygame.image.load('images/Laser.png').convert_alpha()
    alien_laser_img = pygame.image.load('images/Laser.png').convert_alpha()
    hit = pygame.mixer.Sound('sounds/soundEffects/hit.ogg')
    player_img = pygame.image.load('images/Spaceship.png').convert_alpha()
    explosion_img = pygame.image.load('images/explosion.png')

    if isItHalloweenTimeNow():
        explosion_sound = pygame.mixer.Sound('sounds/soundEffects/scream.ogg')
        cannonFire = pygame.mixer.Sound('sounds/soundEffects/laserFire.ogg')
        strongCannonFire = pygame.mixer.Sound('sounds/soundEffects/laserFire.ogg')
    else:
        explosion_sound = pygame.mixer.Sound('sounds/soundEffects/explosion.ogg')
        cannonFire = pygame.mixer.Sound('sounds/soundEffects/cannonFire.ogg')
        strongCannonFire = pygame.mixer.Sound('sounds/soundEffects/cannonFire.ogg')

    cannonFire.set_volume(v)
    explosion_sound.set_volume(v)
    hit.set_volume(v)
    strongCannonFire.set_volume(min(v * 1.5, 1))

    
    player_img = pygame.transform.smoothscale(player_img, (player_width, player_height))
    player_laser_img = pygame.transform.smoothscale(player_laser_img, (14, 48))
    alien_laser_img = pygame.transform.smoothscale(alien_laser_img, (18, 56))
    explosion_img = pygame.transform.smoothscale(explosion_img, (72, 72))

    player_glow = make_glow_surface(max(player_width, player_height) + 10, NEON_A, alpha=70)
    alien_glow = make_glow_surface(max(alien_width, alien_height) + 30, NEON_B, alpha=60)
    
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
        gap_x = alien_width + 12
        gap_y = alien_height + 10
        total_w = cols * gap_x
        start_x = max(20, (SCREEN_WIDTH - total_w) // 2)
        start_y = 110 - alien_height
        for row in range(rows):
            for col in range(cols):
                atype = choose_alien_type()
                aliens.append({
                    "x": start_x + col * gap_x,
                    "y": start_y - row * gap_y,
                    "alive": True,
                    "type": atype["name"],
                    "health": atype["health"],
                    "max_health": atype["health"],
                    "gun": atype["gun"]
                })

    if total_questions < 40:
        rows = max(1, total_questions // 8 + 1)
        cols = max(3, total_questions // 2 + 2)
    else:
        cols = 20
        rows = total_questions - 32
    generate_aliens(rows, cols)

    timed_effects = {}

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

    def spawn_particles(x, y, count=18, color=(255, 180, 80), speed=1.6):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            vel = [math.cos(angle) * random.uniform(0.6, speed), math.sin(angle) * random.uniform(0.6, speed)]
            life = random.randint(300, 900)
            size = random.randint(2, 5)
            particles.append({"x": x, "y": y, "vx": vel[0], "vy": vel[1], "life": life, "born": pygame.time.get_ticks(), "size": size, "color": color})

    
    def render_fit_text(surface, text, base_size, color, max_width, pos):
        size = base_size
        while size > 10:
            font = pygame.font.Font(None, size)
            if font.size(text)[0] <= max_width:
                surface.blit(font.render(text, True, color), pos)
                return
            size -= 2
        
        font = pygame.font.Font(None, base_size)
        surf = font.render(text, True, color)
        surface.blit(surf, pos)

    def handle_shop():
        nonlocal kill_currency, lives, ammo, timed_effects
        shop_width = 640
        shop_height = 680
        shop_rect = pygame.Rect((SCREEN_WIDTH - shop_width)//2, (SCREEN_HEIGHT - shop_height)//2, shop_width, shop_height)
        font = pygame.font.Font(None, 52)
        item_font_base = 36
        desc_font_base = 24
        selected = 0
        clock = pygame.time.Clock()
        running_shop = True

        for alpha in range(0, 200, 20):
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((5, 8, 20, alpha))
            screen.blit(dim, (0, 0))
            pygame.display.update()
            pygame.time.wait(6)

        while running_shop:
            screen.fill(DEEP_SPACE)
            starfield.update_and_draw(screen, dt=1)
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((8, 12, 28, 180))
            screen.blit(dim, (0, 0))

            panel = pygame.Rect(shop_rect)
            draw_rounded_panel(screen, panel, shop_bg_color, border_color=shop_border_color, border_width=5, radius=20)
            title = font.render("Galactic Shop", True, shop_title_color)
            screen.blit(title, (panel.centerx - title.get_width()//2, panel.y+18))

            coins_txt = pygame.font.Font(None, 26).render(f"Kills: {kill_currency}", True, (255,240,160))
            screen.blit(coins_txt, (panel.right-180, panel.y+14))

            btn_w, btn_h = 380, 64
            btn_x = panel.centerx - btn_w//2
            btn_y = panel.y + 100

            for idx, item in enumerate(SHOP_ITEMS):
                is_selected = (selected == idx)
                bg_col = shop_highlight if is_selected else shop_item_bg
                item_rect = pygame.Rect(btn_x, btn_y+idx*82, btn_w, btn_h)
                pygame.draw.rect(screen, bg_col, item_rect, border_radius=12)
                if is_selected:
                    pygame.draw.rect(screen, NEON_A, item_rect, 3, border_radius=12)
                enough = kill_currency >= item["cost"]
                txt_col = shop_text_color if enough else shop_unavailable_color
                
                render_fit_text(screen, f"{item['name']} [ {item['cost']} ]", item_font_base, txt_col, btn_w - 24, (item_rect.x+18, item_rect.y+6))
                
                desc_font = pygame.font.Font(None, desc_font_base)
                lines = wrap_text(item["desc"], desc_font, btn_w - 36)
                for li, line in enumerate(lines):
                    screen.blit(desc_font.render(line, True, shop_desc_color), (item_rect.x+18, item_rect.y+34 + li*18))

            info_font = pygame.font.Font(None, 22)
            info = info_font.render("Arrows: Select   Enter: Buy   Esc: Close", True, HUD_SECONDARY)
            screen.blit(info, (panel.centerx-info.get_width()//2, panel.bottom-48))

            pygame.display.update()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key in [K_DOWN, K_s]:
                        selected = (selected + 1) % len(SHOP_ITEMS)
                    if event.key in [K_UP, K_w]:
                        selected = (selected - 1) % len(SHOP_ITEMS)
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
                            elif item["type"] == "ammo_bonus":
                                set_effect("ammo_per_answer", 18, 60000)
                            elif item["type"] == "ammo":
                                ammo += 100
                            elif item["type"] == "shield":
                                set_effect("shield", True, 15000)
                            elif item["type"] == "autofire":
                                set_effect("autofire", True, 10000)
                            running_shop = False
                            break
                    if event.key == K_ESCAPE:
                        running_shop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for idx in range(len(SHOP_ITEMS)):
                        rect = pygame.Rect(btn_x, btn_y+idx*82, btn_w, btn_h)
                        if rect.collidepoint(mx, my):
                            item = SHOP_ITEMS[idx]
                            if kill_currency >= item["cost"]:
                                kill_currency -= item["cost"]
                                if item["type"] == "speed":
                                    set_effect("speed", 11, 15000)
                                elif item["type"] == "laser":
                                    set_effect("laser_power", 2.5, 15000)
                                elif item["type"] == "life":
                                    lives += 10
                                elif item["type"] == "ammo_bonus":
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
        btn_w, btn_h = 420, 30
        base_x = SCREEN_WIDTH//2 - btn_w//2
        base_y = SCREEN_HEIGHT//2 - 100
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (base_x, base_y + idx * (btn_h + 12)), btn_w, btn_h, WHITE)
            buttons.append(button)

        
        while user_answer is None:
            starfield.update_and_draw(screen, dt=1)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((6, 10, 22, 180))
            screen.blit(overlay, (0, 0))

            panel_w, panel_h = min(860, SCREEN_WIDTH - 80), 500 + 10*len(answerOptions)
            panel = pygame.Rect((SCREEN_WIDTH-panel_w)//2, (SCREEN_HEIGHT-panel_h)//2, panel_w, panel_h)
            draw_rounded_panel(screen, panel, (18, 24, 48, 240), border_color=NEON_A, border_width=3, radius=20)

            
            title_font = pygame.font.Font(None, 36)
            question_font = pygame.font.Font(None, 28)
            title_surf = title_font.render("Question", True, HUD_TEXT)
            screen.blit(title_surf, (panel.x + 28, panel.y + 18))

            
            wrap_w = panel_w - 56
            q_lines = wrap_text(current_question.question, question_font, wrap_w)
            for i, line in enumerate(q_lines[:4]):  
                surf = question_font.render(line, True, HUD_SECONDARY)
                screen.blit(surf, (panel.x + 28, panel.y + 64 + i * 30))

            
            for button in buttons:
                button.draw(screen, BUTTON_COLOUR, border_radius=5)
                pygame.draw.rect(screen, (30, 110, 160), button.rect, 2, border_radius=12)

            
            hint_font = pygame.font.Font(None, 20)
            hint = hint_font.render("Click an answer or press 1-9. Cancel to skip.", True, HUD_SECONDARY)
            screen.blit(hint, (panel.x + 28, panel.bottom - 38))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx
                            break
                if event.type == KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if idx < len(answerOptions):
                            user_answer = idx
                            break
                    if event.key == K_ESCAPE:
                        return False

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
    clock = pygame.time.Clock()

    
    while running and lives > 0:
        dt = clock.tick(60)
        screen.fill(DEEP_SPACE)
        starfield.update_and_draw(screen, dt)

        
        hud_rect = pygame.Rect(24, 10, 700, 68)
        hud_surf = pygame.Surface((hud_rect.w, hud_rect.h), pygame.SRCALPHA)
        hud_surf.fill(HUD_PANEL)
        screen.blit(hud_surf, hud_rect.topleft)
        pygame.draw.rect(screen, NEON_B, hud_rect, 2, border_radius=12)

        display_message(f"Money: ${kill_currency}", 45, 36, HUD_TEXT, x_position=120)
        display_message(f"Lives: {lives}", 45, 40, HUD_TEXT, x_position=260)
        display_message(f"Ammo: {ammo}", 45, 40, HUD_TEXT, x_position=400)
        display_message(f"Question: {question_index}/{total_questions}", 45, 40, HUD_TEXT, x_position=580)
        
        xfx = SCREEN_WIDTH - 260
        yfx = 14
        for fx in list(timed_effects.keys()):
            exp, _ = timed_effects[fx]
            remain = max(0, (exp - pygame.time.get_ticks()) // 1000)
            color = NEON_A if remain > 0 else (160, 160, 160)
            display_message(f"{fx} ({remain}s)", yfx, 30, color, x_position=xfx)
            yfx += 28

        
        button_answer.draw(screen, BUTTON_COLOUR)
        button_shop.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)
        for btn in (button_answer, button_shop, button_go_back, button_leave):
            pygame.draw.rect(screen, (18, 110, 160), btn.rect, 1, border_radius=12)

        
        if get_effect("shield", False):
            s = pygame.Surface((player_width+32, player_height+32), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (80, 220, 255, 80), s.get_rect())
            screen.blit(s, (player_x-16, player_y-16), special_flags=pygame.BLEND_ADD)

        
        numAliens = 0
        max_alien_y = -float('inf')
        for alien in aliens:
            if alien["alive"]:
                numAliens += 1
                gx = int(alien["x"] + alien_width/2 - alien_glow.get_width()/2)
                gy = int(alien["y"] + alien_height/2 - alien_glow.get_height()/2)
                screen.blit(alien_glow, (gx, gy), special_flags=pygame.BLEND_ADD)
                screen.blit(ALIEN_IMAGES[alien["type"]], (alien["x"], alien["y"]))
                if alien["max_health"] > 1:
                    health_ratio = max(0.0, alien["health"] / alien["max_health"])
                    bar_width = int(alien_width * health_ratio)
                    pygame.draw.rect(screen, (30, 30, 30), (alien["x"], alien["y"] - 8, alien_width, 6))
                    pygame.draw.rect(screen, (255, 80, 80), (alien["x"], alien["y"] - 8, bar_width, 6))
                    if alien["health"] < alien["max_health"]:
                        alien["health"] = min(alien["max_health"], alien["health"] + 0.0005)

                alien["x"] += alien_speed
                if alien["x"] > SCREEN_WIDTH - alien_width or alien["x"] < 0:
                    alien_speed *= -1
                    for a in aliens:
                        a["y"] += 22 / max(1, numAliens)

                shoot_chance = 0.015 if alien["gun"] == "normal" else 0.05
                if random.random() < shoot_chance * (1 / max(1, numAliens)):
                    if alien["gun"] == "strong":
                        strongCannonFire.play()
                        alien_projectiles.append({
                            "x": alien["x"] + alien_width // 2,
                            "y": alien["y"] + alien_height,
                            "speed": projectile_speed * 1.8,
                            "color": (255, 80, 120)
                        })
                    else:
                        cannonFire.play()
                        alien_projectiles.append({
                            "x": alien["x"] + alien_width // 2,
                            "y": alien["y"] + alien_height,
                            "speed": projectile_speed,
                            "color": (120, 200, 255)
                        })

                if alien["y"] > max_alien_y:
                    max_alien_y = alien["y"]

        
        for projectile in projectiles[:]:
            pygame.draw.rect(screen, NEON_A, (projectile["x"], projectile["y"], 4, 18))
            pygame.draw.rect(screen, (255, 255, 255), (projectile["x"]+1, projectile["y"]+4, 2, 10))
            projectile["y"] -= projectile_speed * (1 + get_effect("speed", 0) / 10)
            if projectile["y"] < -10:
                projectiles.remove(projectile)

        
        for alien_projectile in alien_projectiles[:]:
            col = alien_projectile.get("color", (255, 255, 255))
            pygame.draw.rect(screen, col, (alien_projectile["x"], alien_projectile["y"], 6, 12), border_radius=3)
            alien_projectile["y"] += alien_projectile.get("speed", projectile_speed)
            if alien_projectile["y"] > SCREEN_HEIGHT + 20:
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
                            "size": 80,
                            "start_time": pygame.time.get_ticks(),
                            "duration": 700
                        })
                        spawn_particles_x = alien["x"] + alien_width // 2
                        spawn_particles_y = alien["y"] + alien_height // 2
                        spawn_particles(spawn_particles_x, spawn_particles_y,
                                        count=20,
                                        color=(220, 160, 40) if alien["type"] == "normal" else (255, 120, 200),
                                        speed=2.4)
                        for t in ALIEN_TYPES:
                            if alien["type"] == t["name"]:
                                kill_currency += t["kill_value"]
                                break
                    else:
                        hit.play()
                        spawn_particles(projectile["x"], projectile["y"], count=8, color=(255,220,140), speed=1.4)
                    if projectile in projectiles:
                        projectiles.remove(projectile)

        
        for explosion in explosions[:]:
            elapsed = pygame.time.get_ticks() - explosion["start_time"]
            dur = explosion["duration"]
            if elapsed > dur:
                explosions.remove(explosion)
                continue
            prog = elapsed / dur
            if prog <= 0.5:
                scale = 0.6 + 0.9 * (prog / 0.5)
            else:
                scale = 1.5 - 0.9 * ((prog - 0.5) / 0.5)
            size = int(explosion["size"] * scale)
            try:
                exp_img_scaled = pygame.transform.smoothscale(explosion_img, (size, size))
                screen.blit(exp_img_scaled, (explosion["x"] - size // 2, explosion["y"] - size // 2), special_flags=pygame.BLEND_ADD)
            except Exception:
                
                surf = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 200, 80, int(160 * (1 - abs(0.5-prog)*2))), (size//2, size//2), size//2)
                screen.blit(surf, (explosion["x"] - size // 2, explosion["y"] - size // 2), special_flags=pygame.BLEND_ADD)
            if 0.35 < prog < 0.65:
                ring = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                alpha_ring = int(80 * (1 - abs(0.5-prog)*2))
                pygame.draw.circle(ring, (255, 220, 100, alpha_ring), (size, size), int(size*0.8), width=6)
                screen.blit(ring, (explosion["x"] - size, explosion["y"] - size), special_flags=pygame.BLEND_ADD)

        
        for p in particles[:]:
            age = pygame.time.get_ticks() - p["born"]
            if age > p["life"]:
                particles.remove(p)
                continue
            p["x"] += p["vx"] * (dt / 16.0)
            p["y"] += p["vy"] * (dt / 16.0)
            fade = 1.0 - age / p["life"]
            col = (int(p["color"][0] * fade), int(p["color"][1] * fade), int(p["color"][2] * fade))
            pygame.draw.circle(screen, col, (int(p["x"]), int(p["y"])), max(1, int(p["size"] * fade)))

        
        
        px_gx = player_x + player_width // 2 - player_glow.get_width() // 2
        px_gy = player_y + player_height // 2 - player_glow.get_height() // 2
        screen.blit(player_glow, (px_gx, px_gy), special_flags=pygame.BLEND_ADD)
        screen.blit(player_img, (player_x, player_y))

        if all(not alien["alive"] for alien in aliens):
            display_message("You Win!", SCREEN_HEIGHT // 2, 96, (120, 255, 180))
            pygame.display.update()
            pygame.time.wait(2000)
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

    
    if lives <= 0 or (question_index >= total_questions and all(alien["alive"] for alien in aliens)) or max_alien_y + alien_height >= player_y + player_height // 2:
        explosion_sound.play()
        screen.fill(DEEP_SPACE)
        display_message("You Lose!", SCREEN_HEIGHT // 2, 96, (255, 100, 100))
        pygame.display.update()
        pygame.time.wait(2000)