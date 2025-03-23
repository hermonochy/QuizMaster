import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
LADDER_WIDTH = 10
RUNG_WIDTH = 5
NUM_RUNGS = 5
RUNG_SPACING = 40
LADDER_HEIGHT = (NUM_RUNGS - 1) * RUNG_SPACING

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)  # Color for the ladder

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Ladder")

# Function to draw the ladder
def draw_ladder(surface, x, y):
    # Draw the side rails
    pygame.draw.rect(surface, BROWN, (x, y, LADDER_WIDTH, LADDER_HEIGHT))  # Left rail
    pygame.draw.rect(surface, BROWN, (x + LADDER_WIDTH, y, LADDER_WIDTH, LADDER_HEIGHT))  # Right rail

    # Draw the rungs
    for i in range(NUM_RUNGS):
        rung_y = y + i * RUNG_SPACING
        pygame.draw.rect(surface, BROWN, (x - RUNG_WIDTH, rung_y, 2 * (LADDER_WIDTH + RUNG_WIDTH), RUNG_WIDTH))  # Rung

# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the background
        screen.fill(WHITE)

        # Draw the ladder
        ladder_x = WIDTH // 2 - LADDER_WIDTH // 2  # Center the ladder
        ladder_y = HEIGHT // 2 - LADDER_HEIGHT // 2  # Center the ladder vertically
        draw_ladder(screen, ladder_x, ladder_y)

        # Update the display
        pygame.display.flip()

# Run the program
if __name__ == "__main__":
    main()

