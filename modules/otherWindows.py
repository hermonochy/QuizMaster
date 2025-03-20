import pygame
import pygame_widgets
import webbrowser

from modules.elements import *


def about(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):

    description_p1 = """
     QuizMaster is an engaging, interactive game designed to challenge your knowledge and cognitive skills across a variety of topics. Whether you're a super nerd or simply looking to test your memory, QuizMaster offers to sharpen your intellect while still having fun. The game's structure incorporates different modes, allowing players to select their preferred play style, ensuring each session is both enjoyable and educational.
    """
    description_p2 = """
    QuizMaster features a variety of game modes tailored for different levels of difficulty and gameplay preferences. From the classic countdown to speed runs that challenge your quick thinking, each mode is designed to provide a unique experience. Players can also enjoy a preferences window that allows customization of song choices, volume, and background colours, making the game truly your own.
    """
    description_p3 = """
    Join the QuizMaster community today, and contribute to a growing repository of quizzes while testing the extent of your knowledge. Learning can be a fun and exciting journey with QuizMaster!
    """

    running = True

    while running:
        screen.fill(BACKGROUND_COLOUR)
        button_license = Button("Licenses", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 250), 250, 40)
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 300), 250, 40)
        button_website = Button("For more information, please vist our website...", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 10), 600, 40, text_colour=(0,0,255))
        button_tutorial = Button("...or view our basic tutorial.", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 75), 600, 40, text_colour=(0,0,255))
        display_message("About QuizMaster", SCREEN_HEIGHT // 8, 75, BLACK)
        display_message(description_p1, SCREEN_HEIGHT // 5, 30, BLACK)
        display_message(description_p2, SCREEN_HEIGHT // 3, 30, BLACK)
        display_message(description_p3, SCREEN_HEIGHT // 2.2, 30, BLACK)
        button_website.draw(screen, BACKGROUND_COLOUR)
        button_tutorial.draw(screen, BACKGROUND_COLOUR)
        button_license.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_go_back.is_clicked(pos):
                    return
                if button_website.is_clicked(pos):
                    webbrowser.open("https://quizmaster-world.github.io/index.html")
                if button_tutorial.is_clicked(pos):
                    webbrowser.open("https://quizmaster-world.github.io/Tutorials/QuizMaster.html")
                if button_license.is_clicked(pos):
                    Licenses(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)

def Licenses(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    with open("LICENSE", 'r') as GPL:
        GPL_license = str(GPL.read())
    licenses_text = """
    This project is primarily licensed under the GPL license. Additionally, the quizzes created within the framework are licensed under the Creative Commons license. For more details, please view the license using the links below:"""
    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Licensing", SCREEN_HEIGHT // 8, 75, BLACK)
        display_message(licenses_text, SCREEN_HEIGHT // 5, 40, BLACK)
        button_GPL = Button("GPL v3", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50), 250, 40, text_colour=(0,0,255))
        button_CC = Button("Creative Commons", (SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2), 300, 40, text_colour=(0,0,255))
        button_go_back = Button("Go Back", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 300), 250, 40)
        button_GPL.draw(screen, BACKGROUND_COLOUR)
        button_CC.draw(screen, BACKGROUND_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_GPL.is_clicked(pos):
                    webbrowser.open("https://raw.githubusercontent.com/hermonochy/QuizMaster/refs/heads/main/LICENSE")
                if button_CC.is_clicked(pos):
                    webbrowser.open("https://raw.githubusercontent.com/hermonochy/QuizMaster/refs/heads/main/quizzes/LICENSE")
                if button_go_back.is_clicked(pos):
                    return
