import pygame
import random
import time

from pygame.locals import *
from modules.elements import *
from modules.extendedText import farmFrenzy_p1, farmFrenzy_p2
from modules.otherWindows import countdown, Instructions

SKY_BLUE = (135, 206, 250)
GRASS_GREEN = (120, 220, 80)
DIRT_BROWN = (180, 120, 60)
CROP_YELLOW = (255, 240, 80)
CROP_RED = (255, 110, 110)
CROP_ORANGE = (255, 180, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (250, 225, 100)
BUTTON_OUTLINE = (90, 70, 0)
PEST_COLOR = (80, 80, 120)
PEST_OUTLINE = (255, 0, 120)
HEALTH_COLOR = (255, 70, 70)
COIN_COLOR = (255, 230, 46)
SEED_COLOR = (220, 220, 255)

CROP_TYPES = [
    {"name": "Wheat", "grow_time": 4500, "value": 10, "color": CROP_YELLOW},
    {"name": "Tomato", "grow_time": 6000, "value": 18, "color": CROP_RED},
    {"name": "Carrot", "grow_time": 7500, "value": 25, "color": CROP_ORANGE},
]

SHOP_ITEMS = [
    {"name": "Sprinkler", "desc": "Crops grow 2x faster for 20s", "cost": 40, "type": "grow_boost"},
    {"name": "Friendly Dog", "desc": "Blocks pests for 30s", "cost": 50, "type": "dog"},
    {"name": "Seed Bag", "desc": "+4 seeds", "cost": 18, "type": "seeds"},
    {"name": "Farm Snack", "desc": "Restore 1 farm heart", "cost": 25, "type": "heal"},
]

def farmFrenzy(questionList, titleofquiz, doCountdown, doInstructions, v):
    if questionList is None or len(questionList) == 0:
        return

    running = True
    farm_hearts = 5
    seeds = 6
    coins = 0
    crops = []
    pests = []
    pest_timer = 0
    pest_grace_questions = max(2, len(questionList) // 3)
    grow_boost = 1.0
    dog_active = False
    dog_timer = 0
    question_index = 0
    total_questions = len(questionList)
    last_plant_time = 0

    if doInstructions:
        Instructions(SKY_BLUE, BUTTON_COLOR, BLACK, titleofquiz, p1=farmFrenzy_p1, p2=farmFrenzy_p2)

    if doCountdown:
        countdown(titleofquiz, SKY_BLUE, BLACK)

    button_answer = Button("Answer Question", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 190), 300, 50, BLACK)
    button_shop = Button("Shop", (SCREEN_WIDTH // 2 + 325, SCREEN_HEIGHT // 2 + 250), 300, 50, BLACK)
    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 310), 250, 40, BLACK)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 360), 250, 40, BLACK)

    plot_rects = []
    n_plots = 7
    for i in range(n_plots):
        x = 90 + i * 110
        y = SCREEN_HEIGHT // 2 + 40
        plot_rects.append(pygame.Rect(x, y, 80, 60))

    clock = pygame.time.Clock()

    def handle_question():
        nonlocal seeds, farm_hearts, question_index, coins
        if question_index >= total_questions:
            return False
        current_question = questionList[question_index]
        question_index += 1

        user_answer = None
        answerOptions = [current_question.correctAnswer] + current_question.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, 120 + idx * 60), 400, 40, BLACK)
            buttons.append(button)

        while user_answer is None:
            screen.fill(SKY_BLUE)
            display_message(f"Question: {current_question.question}", 60, 50, BLACK)
            for button in buttons:
                button.draw(screen, BUTTON_COLOR)
                pygame.draw.rect(screen, BUTTON_OUTLINE, button.rect, 3, border_radius=12)
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
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_index = answerOptions.index(current_question.correctAnswer)
        if user_answer == correct_index:
            seeds += 2
            coins += 8
            return True
        else:
            farm_hearts -= 1
            return False

    def handle_shop():
        nonlocal coins, grow_boost, dog_active, dog_timer, seeds, farm_hearts
        shop_width = 520
        shop_height = 350
        shop_rect = pygame.Rect((SCREEN_WIDTH - shop_width)//2, (SCREEN_HEIGHT - shop_height)//2, shop_width, shop_height)
        font = pygame.font.Font(None, 48)
        item_font = pygame.font.Font(None, 32)
        desc_font = pygame.font.Font(None, 26)
        selected = 0
        running_shop = True

        for alpha in range(0, 170, 15):
            dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            dim.fill((135, 206, 250, alpha))
            screen.blit(dim, (0, 0))
            pygame.display.update()
            pygame.time.wait(10)

        while running_shop:
            screen.fill(SKY_BLUE)
            pygame.draw.rect(screen, BUTTON_COLOR, shop_rect, border_radius=24)
            pygame.draw.rect(screen, BUTTON_OUTLINE, shop_rect, 6, border_radius=24)
            title = font.render("Farm Shop", True, BLACK)
            screen.blit(title, (shop_rect.centerx - title.get_width()//2, shop_rect.y+18))
            coins_txt = desc_font.render(f"Coins: {coins}", True, COIN_COLOR)
            screen.blit(coins_txt, (shop_rect.right-180, shop_rect.y+10))

            btn_w, btn_h = 320, 48
            btn_x = shop_rect.centerx - btn_w//2
            btn_y = shop_rect.y + 80

            for idx, item in enumerate(SHOP_ITEMS):
                is_selected = (selected == idx)
                color = (255,255,170) if is_selected else (255,220,120)
                pygame.draw.rect(screen, color, (btn_x, btn_y+idx*56, btn_w, btn_h), border_radius=13)
                pygame.draw.rect(screen, BUTTON_OUTLINE, (btn_x, btn_y+idx*56, btn_w, btn_h), 3, border_radius=13)
                enough = coins >= item["cost"]
                txt_col = BLACK if enough else (160,160,160)
                item_name = item_font.render(f"{item['name']} [ {item['cost']} ]", True, txt_col)
                screen.blit(item_name, (btn_x+12, btn_y+idx*56+6))
                desc = desc_font.render(item["desc"], True, (120,100,100))
                screen.blit(desc, (btn_x+18, btn_y+idx*56+26))

            info = desc_font.render("Arrows: Select   Enter: Buy   Esc: Close", True, BLACK)
            screen.blit(info, (shop_rect.centerx-info.get_width()//2, shop_rect.bottom-38))

            pygame.display.update()
            pygame.time.wait(16)

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
                        if coins >= item["cost"]:
                            coins -= item["cost"]
                            if item["type"] == "grow_boost":
                                grow_boost = 0.5
                                pygame.time.set_timer(USEREVENT+1, 20000)
                            elif item["type"] == "dog":
                                dog_active = True
                                dog_timer = pygame.time.get_ticks() + 30000
                            elif item["type"] == "seeds":
                                seeds += 4
                            elif item["type"] == "heal":
                                farm_hearts = min(farm_hearts+1, 7)
                            running_shop = False
                    if event.key == K_ESCAPE:
                        running_shop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for idx in range(len(SHOP_ITEMS)):
                        if pygame.Rect(btn_x, btn_y+idx*56, btn_w, btn_h).collidepoint(mx, my):
                            item = SHOP_ITEMS[idx]
                            if coins >= item["cost"]:
                                coins -= item["cost"]
                                if item["type"] == "grow_boost":
                                    grow_boost = 0.5
                                    pygame.time.set_timer(USEREVENT+1, 20000)
                                elif item["type"] == "dog":
                                    dog_active = True
                                    dog_timer = pygame.time.get_ticks() + 30000
                                elif item["type"] == "seeds":
                                    seeds += 4
                                elif item["type"] == "heal":
                                    farm_hearts = min(farm_hearts+1, 7)
                                running_shop = False

    while running:
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, GRASS_GREEN, (0, SCREEN_HEIGHT//2+90, SCREEN_WIDTH, SCREEN_HEIGHT//2-90))
        pygame.draw.rect(screen, DIRT_BROWN, (0, SCREEN_HEIGHT//2+70, SCREEN_WIDTH, 40))

        for i in range(farm_hearts):
            pygame.draw.circle(screen, HEALTH_COLOR, (50 + i*34, 50), 16)
            pygame.draw.circle(screen, BLACK, (50 + i*34, 50), 16, 2)

        display_message(f"Seeds: {seeds}", 12, 90, SEED_COLOR)
        display_message(f"Coins: {coins}", 40, 90, COIN_COLOR)

        for i, rect in enumerate(plot_rects):
            pygame.draw.ellipse(screen, (255,255,255), rect, 0)
            pygame.draw.ellipse(screen, (200,180,120), rect, 0)
            pygame.draw.ellipse(screen, BLACK, rect, 2)
            for crop in crops:
                if crop["plot"] == i and not crop["harvested"]:
                    grow_percent = min(1, (pygame.time.get_ticks() - crop["plant_time"]) / (crop["grow_time"] * grow_boost))
                    crop_center = (rect.centerx, rect.centery+5)
                    crop_rad = int(18 + grow_percent*18)
                    pygame.draw.circle(screen, crop["color"], crop_center, crop_rad)
                    pygame.draw.circle(screen, BLACK, crop_center, crop_rad, 2)
                    if grow_percent >= 1:
                        pygame.draw.circle(screen, WHITE, crop_center, crop_rad+3, 3)
                        display_message("Ready!", rect.y+rect.height+2, 18, crop["color"], x_position=rect.x+rect.width//2-24)

        for pest in pests:
            pygame.draw.circle(screen, PEST_COLOR, (pest["x"], pest["y"]), 18)
            pygame.draw.circle(screen, PEST_OUTLINE, (pest["x"], pest["y"]), 18, 3)
            pygame.draw.circle(screen, WHITE, (pest["x"]-6, pest["y"]-4), 4)
            pygame.draw.circle(screen, WHITE, (pest["x"]+6, pest["y"]-4), 4)
            pygame.draw.circle(screen, BLACK, (pest["x"]-6, pest["y"]-4), 2)
            pygame.draw.circle(screen, BLACK, (pest["x"]+6, pest["y"]-4), 2)
            pygame.draw.line(screen, PEST_OUTLINE, (pest["x"]-10, pest["y"]-14), (pest["x"]-18, pest["y"]-24), 2)
            pygame.draw.line(screen, PEST_OUTLINE, (pest["x"]+10, pest["y"]-14), (pest["x"]+18, pest["y"]-24), 2)

        if dog_active and pygame.time.get_ticks() < dog_timer:
            pygame.draw.ellipse(screen, (255, 210, 110), (SCREEN_WIDTH-170, SCREEN_HEIGHT//2+40, 88, 52))
            pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH-104, SCREEN_HEIGHT//2+60), 15)
            pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH-104, SCREEN_HEIGHT//2+60), 6)
            display_message("Dog!", SCREEN_HEIGHT//2+100, 18, BLACK, x_position=SCREEN_WIDTH-140)

        for btn in [button_answer, button_shop, button_go_back, button_leave]:
            btn.draw(screen, BUTTON_COLOR)
            pygame.draw.rect(screen, BUTTON_OUTLINE, btn.rect, 3, border_radius=14)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_7:
                    plot_idx = event.key - pygame.K_1
                    if 0 <= plot_idx < n_plots and seeds > 0 and not any(c["plot"] == plot_idx and not c["harvested"] for c in crops):
                        crop_type = random.choice(CROP_TYPES)
                        crops.append({
                            "plot": plot_idx,
                            "plant_time": pygame.time.get_ticks(),
                            "grow_time": crop_type["grow_time"],
                            "value": crop_type["value"],
                            "color": crop_type["color"],
                            "harvested": False
                        })
                        seeds -= 1
                if event.key == K_ESCAPE:
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_answer.is_clicked(pos):
                    handle_question()
                elif button_shop.is_clicked(pos):
                    handle_shop()
                elif button_go_back.is_clicked(pos):
                    if popup("Go Back?", "Are you sure you want to go back?", buttons=("Return", "Stay")) == "Return":
                        return
                elif button_leave.is_clicked(pos):
                    quit()
                for i, rect in enumerate(plot_rects):
                    if rect.collidepoint(pos):
                        for crop in crops:
                            if crop["plot"] == i and not crop["harvested"]:
                                if pygame.time.get_ticks() - crop["plant_time"] >= crop["grow_time"] * grow_boost:
                                    crop["harvested"] = True
                                    coins += crop["value"]
            elif event.type == USEREVENT+1:
                grow_boost = 1.0
                pygame.time.set_timer(USEREVENT+1, 0)

        if question_index >= pest_grace_questions:
            pest_timer += 1
            pest_spawn_rate = 130
            if pest_timer > pest_spawn_rate and random.random() < 0.05:
                target_plot = random.randint(0, n_plots-1)
                x, y = plot_rects[target_plot].center
                pests.append({"plot": target_plot, "x": x, "y": y-90, "target_y": y+8})
                pest_timer = 0

        for pest in pests[:]:
            if pest["y"] < pest["target_y"]:
                pest["y"] += 2
            else:
                for crop in crops:
                    if crop["plot"] == pest["plot"] and not crop["harvested"]:
                        crop["harvested"] = True
                        pests.remove(pest)
                        break
                else:
                    if dog_active and pygame.time.get_ticks() < dog_timer:
                        pests.remove(pest)
                    else:
                        farm_hearts -= 1
                        pests.remove(pest)
            if farm_hearts <= 0:
                running = False

        if farm_hearts <= 0:
            display_message("You Lost!", SCREEN_HEIGHT // 2, 100, HEALTH_COLOR)
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        if question_index == total_questions and farm_hearts > 0:
            display_message("You Won!", SCREEN_HEIGHT // 2, 100, CROP_YELLOW)
            pygame.display.flip()
            pygame.time.wait(3000)
            return

        pygame.display.flip()
        clock.tick(60)