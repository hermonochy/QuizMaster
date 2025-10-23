import pygame
import random

from modules.elements import *
from modules.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def drawSpiderWebs(screen):
    spiderWeb = pygame.transform.scale(pygame.image.load("images/spiderWeb.png"), (128, 128))
    spiderWeb = pygame.transform.scale(spiderWeb, (128, 128))
    # Top-right
    screen.blit(spiderWeb, (SCREEN_WIDTH - 128, 0))
    # Top-left
    screen.blit(pygame.transform.rotate(spiderWeb, 90), (0, 0))
    # Bottom-left
    screen.blit(pygame.transform.rotate(spiderWeb, 180), (0, SCREEN_HEIGHT - 128))
    # Bottom-right
    screen.blit(pygame.transform.rotate(spiderWeb, 270), (SCREEN_WIDTH - 128, SCREEN_HEIGHT - 128))