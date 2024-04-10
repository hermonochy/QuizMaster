#!/usr/bin/env python
import pygame
import sys
import PySimpleGUI as sg
import json
import random
from modules.persistence import QuizQuestion
from pygame.locals import *



music_list = ['music1.mp3', 'music2.mp3', 'music3.mp3']
music = (random.choice(music_list))

pygame.mixer.init()
pygame.mixer.music.load(music)

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 700
LIGHT_BLUE = (173, 216, 230)
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
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(text, text_rect)
            y_position += text.get_height()
    else:
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        
        y_position += text.get_height()

    return y_position
def quiz_game(questionList,titleofquiz):
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    background_color = LIGHT_BLUE
    incorrect_questions = []

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        time_remaining = TIMER

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
            buttons.append(button)

        pygame.mixer.music.play(-1)

        while running and time_remaining > 0 and user_answer is None:
            screen.fill(background_color)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET)

            for button in buttons:
                button.draw(screen, LIGHT_BLUE if user_answer is None else LIGHT_BLUE)

            display_message(f"Time remaining: {time_remaining}", SCREEN_HEIGHT - QUESTION_OFFSET)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.mixer.music.stop()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx
                            break
                if event.type == KEYDOWN:
                    if event.key in[pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
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

    screen.fill(background_color)
    display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2-200)
    if correctAnswers/totalQuestions > 0.7:
           display_message(f"Well Done! You know alot about {titleofquiz}!", SCREEN_HEIGHT // 2-175)
    else:
           display_message(f"You might want to revise {titleofquiz}", SCREEN_HEIGHT // 2-175)
    pygame.display.update()

    y_position = SCREEN_HEIGHT // 2-150
    for idx, question in enumerate(incorrect_questions):
        y_position += display_message(f"Incorrect - Question: {question.question}", y_position)
        y_position += display_message(f"Correct Answer: {question.correctAnswer}", y_position)
        pygame.display.update()
        pygame.time.wait(3000)

def main():
    running = True
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

    while running:
        filename = sg.popup_get_file("Please select a quiz:",button_color= "blue", \
                            no_window=True, file_types=(('Quiz files', '.json'),))
        if not filename:
            break

        try:
            questionList, titleofquiz = load_quiz(filename)
        except Exception:
            sg.Popup("What you selected is not a quiz!")
            continue
            return

        screen.fill(LIGHT_BLUE)
        display_message(titleofquiz, QUESTION_OFFSET)
        pygame.display.update()
        pygame.time.wait(2000)

        quiz_game(questionList, titleofquiz)
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                elif event.key == K_l:
                    print('bye!')
                    break

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
