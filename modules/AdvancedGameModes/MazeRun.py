import pygame
import random

from pygame.locals import *

from modules.elements import *
from modules.otherWindows import countdown

TILE_SIZE = 40
PLAYER_SIZE = 30

def mazeRun(questionList, titleofquiz, doCountdown, BACKGROUND_COLOUR, BUTTON_COLOUR):
    BLACK = screen_mode(BACKGROUND_COLOUR)

    if doCountdown:
        countdown(titleofquiz, BACKGROUND_COLOUR, BLACK)

    def generate_maze():
        # Use Prim's Algorithm to ensure a solvable maze
        rows = SCREEN_HEIGHT // TILE_SIZE
        cols = SCREEN_WIDTH // TILE_SIZE
        maze = [[1 for _ in range(cols)] for _ in range(rows)]
        start = (1, 1)
        stack = [start]
        maze[start[0]][start[1]] = 0

        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

        while stack:
            current = stack[-1]
            random.shuffle(directions)
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                if 1 <= ny < rows - 1 and 1 <= nx < cols - 1 and maze[ny][nx] == 1:
                    maze[ny][nx] = 0
                    maze[current[0] + dy // 2][current[1] + dx // 2] = 0
                    stack.append((ny, nx))
                    break
            else:
                stack.pop()

        return maze

    def draw_maze(maze):
        for y, row in enumerate(maze):
            for x, tile in enumerate(row):
                color = (200, 200, 200) if tile == 1 else BACKGROUND_COLOUR
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_questions(positions):
        for qy, qx in positions:
            pygame.draw.circle(screen, (255, 0, 0), (qx * TILE_SIZE + TILE_SIZE // 2, qy * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)

    def draw_player(player_pos):
        pygame.draw.rect(screen, (0, 255, 0), (
            player_pos[1] * TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) // 2,
            player_pos[0] * TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) // 2,
            PLAYER_SIZE, PLAYER_SIZE))

    def check_question(player_pos, question_positions, questionList):
        if tuple(player_pos) in question_positions:
            idx = question_positions.index(tuple(player_pos))
            question = questionList[idx]
            ask_question(question)
            question_positions.pop(idx)
            return True
        return False

    def ask_question(question):
        running = True
        correct = False

        user_answer = None

        answerOptions = [question.correctAnswer] + question.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40, BLACK)
            buttons.append(button)
        while running and user_answer is None:

            screen.fill(BACKGROUND_COLOUR)
            display_message(question.question, QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40, BLACK)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40, BLACK)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40, BLACK)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()                        
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                        return
                    if button_leave.is_clicked(pos):
                        quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1
                    if event.key == pygame.K_y and pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_SHIFT):
                        user_answer =  answerOptions.index(currentQuestion.correctAnswer)

        correct_answer_index = answerOptions.index(question.correctAnswer)

    def is_path_to_endpoint(maze, start, endpoint):
        rows, cols = len(maze), len(maze[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        stack = [start]

        while stack:
            y, x = stack.pop()
            if (y, x) == endpoint:
                return True
            for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and not visited[ny][nx] and maze[ny][nx] == 0:
                    visited[ny][nx] = True
                    stack.append((ny, nx))
        return False

    def check_endpoint(player_pos, endpoint, question_positions):
        return tuple(player_pos) == endpoint and not question_positions

    maze = generate_maze()
    player_pos = [1, 1]
    endpoint = (len(maze) - 2, len(maze[0]) - 2)

    while not is_path_to_endpoint(maze, (1, 1), endpoint):
        maze = generate_maze()

    question_positions = []
    for y in range(1, len(maze), 2):
        for x in range(1, len(maze[0]), 2):
            if len(question_positions) < len(questionList) and (y, x) != (1, 1) and (y, x) != endpoint:
                question_positions.append((y, x))

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOUR)
        draw_maze(maze)
        draw_questions(question_positions)
        draw_player(player_pos)
        pygame.draw.rect(screen, (0, 0, 255), (
            endpoint[1] * TILE_SIZE, endpoint[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                new_y, new_x = player_pos
                if event.key == K_UP:
                    new_y -= 1
                elif event.key == K_DOWN:
                    new_y += 1
                elif event.key == K_LEFT:
                    new_x -= 1
                elif event.key == K_RIGHT:
                    new_x += 1

                if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]) and maze[new_y][new_x] == 0:
                    player_pos = [new_y, new_x]

        if check_question(player_pos, question_positions, questionList):
            pass

        if check_endpoint(player_pos, endpoint, question_positions):
            display_message("Maze Completed!", SCREEN_HEIGHT // 2, 50, (0, 255, 0))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

        clock.tick(30)