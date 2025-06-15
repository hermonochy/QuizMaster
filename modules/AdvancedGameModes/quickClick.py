import pygame
import random
import time
from pygame.locals import *
from modules.elements import *
from modules.extendedText import quickClick_p1, quickClick_p2
from modules.otherWindows import countdown, standard_end_window, Instructions

class BouncingQuestion:
    def __init__(self, question, x, y):
        self.question = question
        self.x = x
        self.y = y
        self.width = random.randint(75,175)
        self.height = random.randint(25,100)
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-5, 5)
        self.answered = False
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.speed_x *= -1
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - self.height:
            self.speed_y *= -1
            
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)

def quickClick(questionList, titleofquiz, doCountdown, doInstructions):
    if questionList is None or len(questionList) == 0:
        return

    running = True
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BUTTON_COLOUR = (25, 25, 25)
    
    score = 0
    start_time = time.time()
    questions_answered = 0
    total_questions = len(questionList)

    bouncing_questions = []
    for q in questionList:
        x = random.randint(0, SCREEN_WIDTH - 150)
        y = random.randint(0, SCREEN_HEIGHT - 100)
        bouncing_questions.append(BouncingQuestion(q, x, y))

    if doInstructions:
        Instructions(BLACK, BUTTON_COLOUR, WHITE, titleofquiz, p1=quickClick_p1, p2=quickClick_p2)

    if doCountdown:
        countdown(titleofquiz, BLACK, WHITE)

    def handle_question(question):
        nonlocal score, questions_answered
        current_question = question.question
        user_answer = None
        
        answer_options = [current_question.correctAnswer] + current_question.wrongAnswers
        random.shuffle(answer_options)
        
        buttons = []
        for idx, answer in enumerate(answer_options):
            button = Button(
                f"{idx + 1}. {answer}",
                (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT),
                400, 40, WHITE
            )
            buttons.append(button)

            button_back = Button("Back", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, WHITE)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, WHITE)
            display_message(f"Score: {score}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, WHITE)
            button_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            
        while user_answer is None:
            screen.fill(BLACK)
            
            display_message(f"{current_question.question}", 
                          QUESTION_OFFSET, 50, WHITE)
            
            for button in buttons:
                button.draw(screen, BUTTON_COLOUR)
            button_back.draw(screen, BUTTON_COLOUR)
            
            display_message(f"Questions: {questions_answered}/{total_questions}", 
                          SCREEN_HEIGHT - 80, 30, WHITE)
            display_message(f"Score: {score}", 
                          SCREEN_HEIGHT - 50, 30, WHITE)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_back.is_clicked(pos):
                        return False
                    elif button_leave.is_clicked(pos):
                        quit()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx
                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        user_answer = event.key - pygame.K_1

        correct_index = answer_options.index(current_question.correctAnswer)
        if user_answer == correct_index:
            score += 100
            questions_answered += 1
            return True
        return False

    def draw_questions():
        font = pygame.font.Font(None, 24)
        for q in bouncing_questions:
            if not q.answered:
                pygame.draw.rect(screen, q.color, 
                               (q.x, q.y, q.width, q.height))
                number_text = f"Question {questionList.index(q.question) + 1}"
                text = font.render(number_text, True, BLACK)
                text_rect = text.get_rect(center=(q.x + q.width//2, 
                                                q.y + q.height//2))
                screen.blit(text, text_rect)

    button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+250), 250, 40, WHITE)
    button_leave = Button("Quit", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+300), 250, 40, WHITE)

    while running:
        screen.fill(BLACK)
        
        elapsed_time = int(time.time() - start_time)
        
        display_message(f"Time: {elapsed_time}s", 30, 30, WHITE)
        display_message(f"Questions: {questions_answered}/{total_questions}", 
                      60, 30, WHITE)
        display_message(f"Score: {score}", 90, 30, WHITE)
        
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_leave.draw(screen, BUTTON_COLOUR)

        for question in bouncing_questions:
            if not question.answered:
                question.move()
        draw_questions()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Place bouncing questions first in case user clicks a square above main menu or quit buttons.
                for question in bouncing_questions:
                    if not question.answered and question.is_clicked(pos):
                        if handle_question(question):
                            question.answered = True
                            break
                if button_leave.is_clicked(pos):
                    quit()
                if button_go_back.is_clicked(pos):
                    if popup("Go Back?", "Are you sure you want to go back?", buttons=("Return", "Stay")) == "Return":
                        return
                    else:
                        continue
        
        if questions_answered == total_questions:
            display_message("Quiz Complete!", SCREEN_HEIGHT // 2 - 50, 100, (0, 255, 0))
            display_message(f"Time: {elapsed_time}s  Score: {score}", 
                          SCREEN_HEIGHT // 2 + 50, 50, WHITE)
            pygame.display.update()
            pygame.time.wait(3000)
            break
            
        pygame.display.update()

    return