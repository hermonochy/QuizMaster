import pygame
import sys
import PySimpleGUI as sg
import json
import random
from modules.persistence import QuizQuestion
from pygame.locals import *


incorrect_questions = []

music_list = ['music1.mp3', 'music2.mp3', 'music3.mp3']
music = (random.choice(music_list))

pygame.mixer.init()
pygame.mixer.music.load(music)

pygame.init()
pygame.font.init()


SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
LIGHT_BLUE = (173,216,230)
BLUE = (173,216,255)
BLACK = (0, 0, 0)
FONT_SIZE = 30
QUESTION_OFFSET = 50
ANSWER_OFFSET = 200
OPTION_HEIGHT = 50
TIMER = 10

class Button:
    def __init__(self, text, position, width, height):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, FONT_SIZE)
        label = font.render(self.text, True, BLACK)
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Quiz Game')

def load_quiz(filename):
    with open(filename, 'r') as file:
        quizDicts = json.load(file)
        questionList = []
        for q in quizDicts["listOfQuestions"]:
            qq = QuizQuestion(**q)
            questionList.append(qq)
        titleofquiz = quizDicts["title"]
    return questionList, titleofquiz

def display_message(message, y_position):
    font = pygame.font.Font(None, FONT_SIZE)
    words = message.split()
    
    if len(message) > 60:
        text_lines = []
        line = ""
        
        for word in words:
            if font.size(line + word)[0] <= SCREEN_WIDTH:
                line += word + " "
            else:
                text_lines.append(line)
                line = word + " "
        
        if line:
            text_lines.append(line)

        for line in text_lines:
            text = font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 , y_position))
            screen.blit(text, text_rect)
            y_position += text.get_height()
    else:
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        
        y_position += text.get_height()

    return y_position
    
def open_new_window(incorrect_questions):
    popup_layout = [
        [sg.Text("Incorrect Questions and Correct Answers")],
        *[[sg.Text(f"{question.question} -> Correct Answer: {question.correctAnswer}")] for question in incorrect_questions],
        [sg.OK()]
    ]
    
    popup_window = sg.Window('Incorrect Answers', popup_layout)
    popup_window.read()

def quiz_game(questionList, titleofquiz):
    global incorrect_questions
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    background_color = LIGHT_BLUE

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        time_remaining = TIMER

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
            buttons.append(button)

        pygame.mixer.music.play(-1)

        while running and time_remaining > 0 and user_answer is None:
            screen.fill(background_color)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET)

            for button in buttons:
                button.draw(screen, BLUE if user_answer is None else LIGHT_BLUE)

            display_message(f"Time remaining: {time_remaining}", SCREEN_HEIGHT - QUESTION_OFFSET)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx
                            break
                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        user_answer = event.key - pygame.K_1
                        break

            time_remaining -= 1
            pygame.time.wait(1000)

        pygame.mixer.music.stop()

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)

        questionIndex += 1

    while True:
        screen.fill(background_color)
        y_position = display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2-200)
        if correctAnswers/totalQuestions > 0.7:
            display_message(f"Well Done! You know a lot about {titleofquiz}!", y_position)
        else:
            display_message(f"You might want to revise {titleofquiz}", y_position)

        button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150 , SCREEN_HEIGHT // 2), 250, 40)
        button_open_file = Button("Play another quiz", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)

        button_show_incorrect.draw(screen, BLUE)
        button_open_file.draw(screen, BLUE)
        pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_show_incorrect.is_clicked(pos):
                    open_new_window(incorrect_questions)
                elif button_open_file.is_clicked(pos):
                     main()
        #pygame.display.update()

def main():
    global incorrect_questions
    running = True
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

    while running:
        filename = sg.popup_get_file("Please select a quiz:", button_color="blue",
                                     no_window=True, file_types=(('Quiz files', '.json'),))
        if not filename:
            break

        try:
            questionList, titleofquiz = load_quiz(filename)
        except Exception:
            sg.Popup("What you selected is not a quiz!")
            continue

        screen.fill(LIGHT_BLUE)
        display_message(titleofquiz, QUESTION_OFFSET)
        pygame.display.update()
        pygame.time.wait(2000)

        incorrect_questions = quiz_game(questionList, titleofquiz)

        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

        button_pressed = False

        while not button_pressed:
            screen.fill(LIGHT_BLUE)
            display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2-200)

            button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 250, 40)
            button_open_file = Button("Play another quiz", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), 250, 40)

            button_show_incorrect.draw(screen, BLUE)
            button_open_file.draw(screen, BLUE)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_show_incorrect.is_clicked(pos):
                        open_new_window(incorrect_questions)
                    elif button_open_file.is_clicked(pos):
                        sg.popup_get_file("Please select a quiz:",no_window=True, file_types=(('Quiz files', '.json'),))
                        break

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
