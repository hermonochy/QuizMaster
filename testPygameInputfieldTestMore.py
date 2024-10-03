import pygame
import pygame.locals as pl
from pygame_textinput import *
pygame.init()

textinput = TextInputVisualizer()

font = pygame.font.SysFont("Consolas", 55)
manager = TextInputManager(validator = lambda input: len(input) <= 5)
textinput_custom = TextInputVisualizer(manager=manager, font_object=font)
textinput_custom.cursor_width = 4
textinput_custom.cursor_blink_interval = 400 # blinking interval in ms
textinput_custom.antialias = False
textinput_custom.font_color = (0, 85, 170)

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

# Pygame now allows natively to enable key repeat:
pygame.key.set_repeat(200, 25)

while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Feed it with events every frame
    textinput.update(events)
    textinput_custom.update(events)

    # Get its surface to blit onto the screen
    screen.blit(textinput.surface, (10, 10))
    screen.blit(textinput_custom.surface, (10, 50))

    # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
    textinput_custom.font_color = [(c+10)%255 for c in textinput_custom.font_color]

    # Check if user pressed return
    if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
        print(f"User pressed enter! Input so far: {textinput.value}")

    pygame.display.update()
    clock.tick(30)
