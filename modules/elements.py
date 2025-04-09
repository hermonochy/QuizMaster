import pygame
import sys
import colorsys

from pygame.locals import *

from modules.checker import isItChristmasTimeNow

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
FONT_SIZE = 40
QUESTION_OFFSET = 50
ANSWER_OFFSET = 200
OPTION_HEIGHT = 50

     
asciiartstart=(r"""
  ___                _            ___  ___                     __                        __
 / _ \     _   _    (_)    ____   |  \/  |     __ _     ___    | |_      ___     _ __    | |
| | | |   | | | |   | |   |_  /   | |\/| |    / _` |   / __|   | __|    / _ \   | '__|   | |
| |_| |   | |_| |   | |    / /    | |  | |   | (_| |   \__ \   | |_    |  __/   | |      |_|
 \__\_\    \__,_|   |_|   /___|   |_|  |_|    \__,_|   |___/    \__|    \___|   |_|      (_)
                                                                     
""")          

asciiartend=(r"""

 ____                         _ 
| __ )     _   _      ___    | |
|  _ \    | | | |    / _ \   | |
| |_) |   | |_| |   |  __/   |_|
|____/     \__, |    \___|   (_)
           |___/                

""")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def quit():
    print(asciiartend)
    pygame.quit()
    sys.exit()

def screen_mode(BACKGROUND_COLOUR):
    R = BACKGROUND_COLOUR[0]
    G = BACKGROUND_COLOUR[1]
    B = BACKGROUND_COLOUR[2]
    if R + G + B < 200 and max(R,G,B) < 100 or isItChristmasTimeNow():
        return (255, 255, 255)
    else:
        return (0, 0, 0)

class Button:
    def __init__(self, text, position, width=300, height=60, text_colour=(0, 0, 0)):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.text_colour = text_colour

    def draw(self, screen, colour, border_radius=15, shadow_offset=4):

        h, s, v = colorsys.rgb_to_hsv(colour[0], colour[1], colour[2])
        v = max(0, v - 25)
        shadow_colour = colorsys.hsv_to_rgb(h, s, v)
        #shadow_colour = (colour[0]-10, colour[1]-30, colour[2]-10)
        shadow_rect = pygame.Rect(self.rect.x + shadow_offset, self.rect.y + shadow_offset, self.width, self.height)
        pygame.draw.rect(screen, shadow_colour, shadow_rect, border_radius=border_radius)
        pygame.draw.rect(screen, colour, self.rect, border_radius=border_radius)
        
        self.render_text(screen)

    def render_text(self, screen):
        words = self.text.split()
        lines = []
        current_line = ""
        font_size = FONT_SIZE

        while font_size > 8:
            font = pygame.font.Font(None, font_size)
            for word in words:
                test_line = current_line + word + " "
                if font.size(test_line)[0] <= self.width - 15:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            if len(lines) * font.get_height() <= self.height - 10:
                break
            else:
                lines = []
                current_line = ""
                font_size -= 2

        font = pygame.font.Font(None, font_size)
        y_offset = (self.rect.height - len(lines) * font.get_height()) // 2
        for line in lines:
            label = font.render(line.strip(), True, self.text_colour)
            text_rect = label.get_rect(center=(self.rect.centerx, self.rect.y + y_offset + font.get_height() // 2))
            screen.blit(label, text_rect)
            y_offset += font.get_height()

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Scrollbar:
    def __init__(self, position, height, total_items, items_per_page):
        self.position = position
        self.height = height
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.rect = pygame.Rect(position[0], position[1], 20, height)
        self.handle_rect = pygame.Rect(position[0], position[1], 20, int(height * items_per_page // total_items))
        self.dragging = False
        self.offset_y = 0
        self.arrow_height = 20
        self.up_arrow_rect = pygame.Rect(position[0], position[1], 20, self.arrow_height)
        self.down_arrow_rect = pygame.Rect(position[0], position[1] + height - self.arrow_height, 20, self.arrow_height)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.handle_rect)

        pygame.draw.rect(screen, (150, 150, 150), self.up_arrow_rect)
        pygame.draw.rect(screen, (150, 150, 150), self.down_arrow_rect)

        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.up_arrow_rect.centerx, self.up_arrow_rect.y + 5),
            (self.up_arrow_rect.x + 5, self.up_arrow_rect.y + self.arrow_height - 5),
            (self.up_arrow_rect.right - 5, self.up_arrow_rect.y + self.arrow_height - 5)
        ])

        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.down_arrow_rect.centerx, self.down_arrow_rect.bottom - 5),
            (self.down_arrow_rect.x + 5, self.down_arrow_rect.bottom - self.arrow_height + 5),
            (self.down_arrow_rect.right - 5, self.down_arrow_rect.bottom - self.arrow_height + 5)
        ])

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_y = event.pos[1] - self.handle_rect.y
            elif self.up_arrow_rect.collidepoint(event.pos):
                self.scroll_up()
            elif self.down_arrow_rect.collidepoint(event.pos):
                self.scroll_down()
        if event.type == MOUSEBUTTONUP:
            self.dragging = False
        if event.type == MOUSEMOTION:
            if self.dragging:
                new_y = event.pos[1] - self.offset_y
                new_y = max(self.rect.y + self.arrow_height, min(new_y, self.rect.y + self.rect.height - self.handle_rect.height - self.arrow_height))
                self.handle_rect.y = new_y
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.scroll_up()
            elif event.key == K_DOWN:
                self.scroll_down()

    def scroll_up(self):
        new_y = self.handle_rect.y - 10
        new_y = max(self.rect.y + self.arrow_height, new_y)
        self.handle_rect.y = new_y

    def scroll_down(self):
        new_y = self.handle_rect.y + 10
        new_y = min(self.rect.y + self.rect.height - self.handle_rect.height - self.arrow_height, new_y)
        self.handle_rect.y = new_y

    def get_offset(self):
        return int((self.handle_rect.y - self.rect.y - self.arrow_height) * self.total_items // (self.height - 2 * self.arrow_height))

def display_message(message, y_position, font_size, colour):
    font = pygame.font.Font(None, font_size)
    words = message.split()
    
    if len(message) > 60:
        text_lines = []
        line = ""
        
        for word in words:
            if font.size(line + word)[0] < SCREEN_WIDTH * 0.9: # padding
                line += word + " "
            else:
                text_lines.append(line)
                line = word + " "
        
        if line:
            text_lines.append(line)

        for line in text_lines:
            text = font.render(line, True, colour)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 , y_position))
            screen.blit(text, text_rect)
            y_position += text.get_height()
    else:
        text = font.render(message, True, colour)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        
        y_position += text.get_height()

    return y_position

