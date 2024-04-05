import pygame
import sys
import PySimpleGUI as sg
import json
import random
from modules.persistence import QuizQuestion
from pygame.locals import *

pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 25
QUESTION_OFFSET = 50
ANSWER_OFFSET = 100
OPTION_HEIGHT = 50
TIMER = 10  


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
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
    screen.blit(text, text_rect)


def quiz_game(questionList):
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    background_color = WHITE

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        time_remaining = TIMER

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)  


        while running and time_remaining > 0:
            screen.fill(background_color)
            display_message(f"Question {questionIndex + 1}: {currentQuestion.question}", QUESTION_OFFSET)

            for idx, answer in enumerate(answerOptions):
                display_message(f"{idx + 1}. {answer}", ANSWER_OFFSET + idx * OPTION_HEIGHT)

            display_message(f"Time remaining: {time_remaining}", SCREEN_HEIGHT - QUESTION_OFFSET)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN: 
                    x, y = pygame.mouse.get_pos()
                    for idx, _ in enumerate(answerOptions):
                        if ANSWER_OFFSET + idx * OPTION_HEIGHT < y < ANSWER_OFFSET + (idx + 1) * OPTION_HEIGHT:
                            user_answer = answerOptions.index(answer)
                            break
                if event.type == KEYDOWN:
                    if event.key in [K_1, K_2, K_3, K_4]:
                        user_answer = event.key - K_1
                        break

            time_remaining -= 1
            pygame.time.wait(1000)

        if user_answer is not None and user_answer == answerOptions.index(currentQuestion.correctAnswer):
            correctAnswers += 1

        questionIndex += 1

    screen.fill(background_color)
    display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2)
    display_message("Press 'Q' to Quit or 'L' to Load another quiz", SCREEN_HEIGHT // 2 + FONT_SIZE)
    pygame.display.update()



def main():
    running = True

    while running:
        filename = sg.popup_get_file("Open quiz", no_window=True)
        if not filename:
            break

        try:
            questionList, titleofquiz = load_quiz(filename)
        except Exception:
            print("Error loading quiz file.")
            return

        screen.fill(WHITE)
        display_message(titleofquiz, QUESTION_OFFSET)
        pygame.display.update()
        pygame.time.wait(2000)

        quiz_game(questionList)

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
