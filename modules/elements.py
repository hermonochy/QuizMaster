import pygame
import sys
import colorsys

from pygame.locals import *

from modules.checker import isItChristmasTimeNow
from modules.extendedText import asciiartstart, asciiartend
from modules.constants import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def quit():
    print(asciiartend)
    pygame.quit()
    sys.exit()

def screen_mode(BACKGROUND_COLOUR):
    R = BACKGROUND_COLOUR[0]
    G = BACKGROUND_COLOUR[1]
    B = BACKGROUND_COLOUR[2]
    _,_,v = colorsys.rgb_to_hsv(R,G,B)
    if v < 120 or isItChristmasTimeNow():
        return (255, 255, 255)
    else:
        return (0, 0, 0)

def darken(colour):
    h, s, v = colorsys.rgb_to_hsv(colour[0], colour[1], colour[2])
    v = max(0, v - 25)
    return colorsys.hsv_to_rgb(h, s, v)

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
        shadow_colour = darken(colour)
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

class ButtonArray:
    def __init__(self, button_texts, start_position, button_spacing=10, button_width=300, button_height=60, text_colour=(0, 0, 0), screen_width=SCREEN_WIDTH):

        self.buttons = []
        current_x, current_y = start_position

        for text in button_texts:
            if current_x + button_width > screen_width:
                current_x = start_position[0]
                current_y += button_height + (button_spacing//1.5)

            button = Button(
                text=text,
                position=(current_x, current_y),
                width=button_width,
                height=button_height,
                text_colour=text_colour
            )
            self.buttons.append(button)
            current_x += button_width + button_spacing

    def draw(self, screen, colour, border_radius=15, shadow_offset=4):
        for button in self.buttons:
            button.draw(screen, colour, border_radius, shadow_offset)

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_clicked(pos):
                return True, button.text
        return None, None

class Slider:
    def __init__(self, position, width, min=0, max=100, step=1, initial=0, bar_height=10, bar_colour=(175, 175, 175), handleColour=(100, 100, 100), handleRadius=15):
        self.position = position
        self.width = width
        self.bar_height = bar_height
        self.bar_color = bar_colour
        self.handle_color = handleColour
        self.min_val = min
        self.max_val = max
        self.step = step
        self.value = initial
        self.handle_radius = handleRadius

        self.bar_rect = pygame.Rect(position[0], position[1] - bar_height // 2, width, bar_height)
        self.handle_x = self.value_to_position(initial)
        self.handle_y = position[1]
        self.dragging = False

    def value_to_position(self, value):
        proportion = (value - self.min_val) / (self.max_val - self.min_val)
        return int(self.position[0] + proportion * self.width)

    def position_to_value(self, pos_x):
        proportion = (pos_x - self.position[0]) / self.width
        proportion = max(0, min(proportion, 1))
        raw_value = self.min_val + proportion * (self.max_val - self.min_val)
        return round(raw_value / self.step) * self.step

    def draw(self, screen):
        self.screen = screen
        pygame.draw.rect(self.screen, self.bar_color, self.bar_rect)

        pygame.draw.circle(self.screen, self.handle_color, (self.handle_x, self.handle_y), self.handle_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.handle_x - event.pos[0]) ** 2 + (self.handle_y - event.pos[1]) ** 2 <= self.handle_radius ** 2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_x = max(self.position[0], min(event.pos[0], self.position[0] + self.width))
                self.value = self.position_to_value(self.handle_x)

    def get(self):
        return self.value

class Checkbox:
    def __init__(self, text, position, width=20, height=20, checked=False):
        self.text = text
        self.position = position
        self.checked = checked
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def draw(self, screen, box_color = (253,245,230), check_color = (0,0,0), text_color=(0, 0, 0)):
        pygame.draw.rect(screen, box_color, self.rect)
        
        if self.checked:
            pygame.draw.line(screen, check_color, (self.rect.left, self.rect.centery), (self.rect.centerx, self.rect.bottom), 3)
            pygame.draw.line(screen, check_color, (self.rect.centerx, self.rect.bottom), (self.rect.right, self.rect.top), 3)
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_clicked(event.pos):
                self.checked = not self.checked
    
    def get(self):
        return self.checked

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
            if event.key == K_DOWN:
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
