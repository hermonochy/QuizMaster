import pygame
import sys
import colorsys

from pygame.locals import *

from modules.initialise import *
from modules.checker import isItChristmasTimeNow
from modules.extendedText import asciiartstart, asciiartend
from modules.constants import *

click = pygame.mixer.Sound('sounds/soundEffects/click.ogg')

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

def clamp(value):
    return max(0, min(255, value))

def button_colour(R, G, B):
    if all(i < 245 for i in (R, G, B)):
        return (clamp(R + 10), clamp(G + 10), clamp(B + 10))
    else:
        return (clamp(R - 10), clamp(G - 10), clamp(B - 10))

def getOppositeRGB(rgb):
    contrasting_rgb = tuple(255 - value for value in rgb)
    return contrasting_rgb

def darken(colour, amount=50):
    h, s, v = colorsys.rgb_to_hsv(colour[0], colour[1], colour[2])
    v = max(0, v - amount)
    return colorsys.hsv_to_rgb(h, s, v)

class Button:
    def __init__(
        self,
        text,
        position,
        width=300,
        height=60,
        text_colour=(0, 0, 0),
        use_outline=False,
        outline_color=(0,0,0)
    ):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.text_colour = text_colour
        self.use_outline = use_outline
        self.outline_color = outline_color

    def draw(self, screen, colour, border_radius=15, shadow_offset=4, enabled=True):

        self.enabled = enabled

        shadow_colour = darken(colour)
        shadow_rect = pygame.Rect(self.rect.x + shadow_offset, self.rect.y + shadow_offset, self.width, self.height)
        pygame.draw.rect(screen, shadow_colour, shadow_rect, border_radius=border_radius)
        if not self.enabled:
            colour = darken(colour, 25)
        pygame.draw.rect(screen, colour, self.rect, border_radius=border_radius)
        if self.use_outline:
            pygame.draw.rect(screen, self.outline_color, self.rect, 3, border_radius=border_radius)
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
            label = font.render(line.strip(), True, self.text_colour if self.enabled else darken(self.text_colour))
            text_rect = label.get_rect(center=(self.rect.centerx, self.rect.y + y_offset + font.get_height() // 2))
            screen.blit(label, text_rect)
            y_offset += font.get_height()

    def is_clicked(self, pos):
        if self.enabled:
            if self.rect.collidepoint(pos):
                click.play()
                return True
        return False

class ButtonArray:
    def __init__(self, button_texts, start_position, button_spacing=10, button_width=300, button_height=60, text_colour=(0, 0, 0), screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, orientation='horizontal'):
        self.buttons = []

        current_x, current_y = start_position

        for text in button_texts:
            if orientation == 'horizontal':
                if current_x + button_width > screen_width:
                    current_x = start_position[0]
                    current_y += button_height + (button_spacing // 1.5)
            elif orientation == 'vertical':
                if screen_height is not None and current_y + button_height > start_position[1] + screen_height:
                    current_y = start_position[1]
                    current_x += button_width + button_spacing
                else:
                    current_x = start_position[0]

            button = Button(
                text=text,
                position=(current_x, current_y),
                width=button_width,
                height=button_height,
                text_colour=text_colour
            )
            self.buttons.append(button)

            if orientation == 'horizontal':
                current_x += button_width + button_spacing
            elif orientation == 'vertical':
                current_y += button_height + button_spacing

    def draw(self, screen, colour, border_radius=15, shadow_offset=4):
        for button in self.buttons:
            button.draw(screen, colour, border_radius, shadow_offset)

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_clicked(pos):
                return True, button.text
        return None, None

class TextBox:
    def __init__(self, x, y, width, height, font_size=36, text_color=(30,30,30), bg_color=(245,245,245), border_color=(90,90,90), border_width=3, 
                 placeholder="", placeholder_color=(140, 140, 140), max_length=64, border_radius=12, active_color=(70,120,255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.max_length = max_length
        self.border_radius = border_radius
        self.active_color = active_color
        self.active = False
        self.cursor_visible = True
        self.cursor_counter = 0
        self.cursor_pos = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
            elif event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_RETURN:
                pass
            elif len(self.text) < self.max_length and event.unicode and event.unicode.isprintable():
                self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                self.cursor_pos += 1

    def get(self):
        return self.text

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        border_col = self.active_color if self.active else self.border_color
        pygame.draw.rect(screen, border_col, self.rect, self.border_width, border_radius=self.border_radius)

        render_text = self.text if self.text else self.placeholder
        color = self.text_color if self.text else self.placeholder_color
        txt_surf = self.font.render(render_text, True, color)
        txt_rect = txt_surf.get_rect(midleft=(self.rect.x+14, self.rect.centery))
        screen.blit(txt_surf, txt_rect)

        if self.active:
            self.cursor_counter = (self.cursor_counter + 1) % 60
            if self.cursor_counter < 30:
                cursor_x = self.font.size(self.text[:self.cursor_pos])[0] + self.rect.x + 14
                cursor_y = self.rect.y + 8
                cursor_h = self.rect.height - 16
                pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_h), 2)

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
            elif self.bar_rect.collidepoint(event.pos):
                self.handle_x = max(self.position[0], min(event.pos[0], self.position[0] + self.width))
                self.value = self.position_to_value(self.handle_x)
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
    def __init__(self, text, position, width=30, height=30, checked=False):
        self.text = text
        self.position = position
        self.checked = checked
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, (width + height // 3))
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.text_rect = None

    def draw(self, screen, box_color = (253,245,230), check_color = (0,0,0), text_color=(0, 0, 0)):
        pygame.draw.rect(screen, box_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, check_color, self.rect, 2, border_radius=5)
        
        if self.checked:
            padding = max(3, self.width // 6)
            x1, y1 = self.rect.left + padding, self.rect.centery
            x2, y2 = self.rect.centerx - padding // 2, self.rect.bottom - padding
            x3, y3 = self.rect.right - padding, self.rect.top + padding

            pygame.draw.lines(
                screen, check_color, False,
                [(x1, y1), (x2, y2), (x3, y3)],
                4
            )
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        screen.blit(text_surf, text_rect)
        self.text_rect = text_rect

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) or (self.text_rect is not None and self.text_rect.collidepoint(pos))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_clicked(event.pos):
                self.checked = not self.checked

    def get(self):
        return self.checked

class ProgressBar:
    def __init__(self, position, size, min_value=0, max_value=100, current_value=0, 
                 bar_color=(30, 144, 255), bg_color=(220, 220, 220), border_color=(0, 0, 0), border_width=2, show_percentage=False):
        self.position = position
        self.size = size
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value
        self.bar_color = bar_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.show_percentage = show_percentage
        self.font = pygame.font.Font(None, int(self.size[1] * 0.7))

    def set_value(self, value):
        self.current_value = max(self.min_value, min(self.max_value, value))

    def draw(self, screen):
        x, y = self.position
        width, height = self.size

        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.bg_color, bg_rect, border_radius=int(height*0.4))
        progress = (self.current_value - self.min_value) / (self.max_value - self.min_value)
        progress_width = int(width * progress)
        if progress_width > 0:
            progress_rect = pygame.Rect(x, y, progress_width, height)
            pygame.draw.rect(screen, self.bar_color, progress_rect, border_radius=int(height*0.4))
        pygame.draw.rect(screen, self.border_color, bg_rect, self.border_width, border_radius=int(height*0.4))

        if self.show_percentage:
            percent = int(100 * progress)
            text_surf = self.font.render(f"{percent}%", True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
            screen.blit(text_surf, text_rect)


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

def popup(
    title="Popup",
    message="",
    buttons=("OK",),
    width=420,
    height=240,
    font_title_size=44,
    font_msg_size=28,
    popup_color=(250, 250, 255),
    border_radius=18,
    shadow_offset=5,
    shadow_color=(120, 120, 120),
    border_color=(80, 140, 255),
    border_width=4,
    title_color=(40, 60, 120),
    msg_color=(35, 35, 35),
    button_color=(80, 140, 255),
    button_text_color=(255, 255, 255),
    button_hover_color=(60, 120, 235)
):

    popup_rect = pygame.Rect(
        (screen.get_width() - width) // 2,
        (screen.get_height() - height) // 2,
        width, height
    )
    shadow_rect = popup_rect.move(shadow_offset, shadow_offset)

    font_title = pygame.font.Font(None, font_title_size)
    font_msg = pygame.font.Font(None, font_msg_size)

    btn_width = 120
    btn_height = 48
    spacing = 20
    total_btn_width = len(buttons) * btn_width + (len(buttons) - 1) * spacing
    btn_y = popup_rect.y + height - btn_height - 30
    btn_x = popup_rect.x + (width - total_btn_width) // 2

    btn_rects = []
    for i in range(len(buttons)):
        btn_rect = pygame.Rect(
            btn_x + i * (btn_width + spacing),
            btn_y,
            btn_width,
            btn_height
        )
        btn_rects.append(btn_rect)

    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = current + word + " "
            if font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word + " "
        if current:
            lines.append(current)
        return lines

    hover = [False] * len(buttons)

    def draw():
        pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=border_radius)
        pygame.draw.rect(screen, popup_color, popup_rect, border_radius=border_radius)
        pygame.draw.rect(screen, border_color, popup_rect, border_width, border_radius=border_radius)
        title_surf = font_title.render(title, True, title_color)
        title_rect = title_surf.get_rect(center=(popup_rect.centerx, popup_rect.y + 38))
        screen.blit(title_surf, title_rect)
        y_msg = title_rect.bottom + 16
        lines = wrap_text(message, font_msg, width - 60)
        for line in lines:
            msg_surf = font_msg.render(line, True, msg_color)
            msg_rect = msg_surf.get_rect(center=(popup_rect.centerx, y_msg))
            screen.blit(msg_surf, msg_rect)
            y_msg += msg_surf.get_height() + 2
        for i, btn_rect in enumerate(btn_rects):
            col = button_hover_color if hover[i] else button_color
            pygame.draw.rect(screen, col, btn_rect, border_radius=10)
            txt_surf = font_msg.render(str(buttons[i]), True, button_text_color)
            txt_rect = txt_surf.get_rect(center=btn_rect.center)
            screen.blit(txt_surf, txt_rect)
        pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEMOTION:
                mouse = e.pos
                for i, rect in enumerate(btn_rects):
                    hover[i] = rect.collidepoint(mouse)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, rect in enumerate(btn_rects):
                    if rect.collidepoint(e.pos):
                        return buttons[i]
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return buttons[0]
                elif e.key == pygame.K_ESCAPE and len(buttons) > 1:
                    return buttons[-1]
        dim = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 250))
        screen.blit(dim, (0, 0))
        draw()

def display_message(message, y_position, font_size, colour, x_position=SCREEN_WIDTH // 2):
    """
    Display a message on the screen at a given y_position and font_size and colour.
    """
    font = pygame.font.Font(None, font_size)
    lines = []

    message_lines = message.split('\n')
    for msg_line in message_lines:
        words = msg_line.split()
        if len(msg_line) > 60:
            line = ""
            for word in words:
                if font.size(line + word)[0] < SCREEN_WIDTH * 0.9:
                    line += word + " "
                else:
                    lines.append(line)
                    line = word + " "
            if line:
                lines.append(line)
        else:
            lines.append(msg_line)

    for line in lines:
        text = font.render(line, True, colour)
        text_rect = text.get_rect(center=(x_position, y_position))
        screen.blit(text, text_rect)
        y_position += text.get_height()

    return y_position