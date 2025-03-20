import pygame
import sys

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
    global BLACK
    if (R + G + B < 200 and max(R,G,B) < 100) or isItChristmasTimeNow():
        return (255, 255, 255)
    else:
        return (0, 0, 0)

class Button:
    def __init__(self, text, position, width=300, height=60, text_colour = (0,0,0)):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.text_colour = text_colour

    def draw(self, screen, colour):
        pygame.draw.rect(screen, colour, self.rect)
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
                if font.size(test_line)[0] <= self.width - 20:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            if len(lines) * font.get_height() <= self.height - 15:
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

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.handle_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_y = event.pos[1] - self.handle_rect.y
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION:
            if self.dragging:
                new_y = event.pos[1] - self.offset_y
                new_y = max(self.rect.y, min(new_y, self.rect.y + self.rect.height - self.handle_rect.height))
                self.handle_rect.y = new_y

    def get_offset(self):
        return int((self.handle_rect.y - self.rect.y) * self.total_items // self.height)

# For later
class Checkbox:
    def __init__(self, text, position, width=20, height=20, checked=False):
        self.text = text
        self.position = position
        self.checked = checked
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def draw(self, screen, box_color, check_color, text_color=(0, 0, 0)):
        pygame.draw.rect(screen, box_color, self.rect)
        
        if self.checked:
            pygame.draw.line(screen, check_color, (self.rect.left, self.rect.centery), (self.rect.centerx, self.rect.bottom), 2)
            pygame.draw.line(screen, check_color, (self.rect.centerx, self.rect.bottom), (self.rect.right, self.rect.top), 2)
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_clicked(event.pos):
                self.checked = not self.checked

def display_message(message, y_position, font_size, colour):
    font = pygame.font.Font(None, font_size)
    words = message.split()
    
    if len(message) > 60:
        text_lines = []
        line = ""
        
        for word in words:
            if font.size(line + word)[0] < SCREEN_WIDTH * 0.9: # Padding
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

