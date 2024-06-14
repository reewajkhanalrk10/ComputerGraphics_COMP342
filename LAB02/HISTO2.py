import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
BG_COLOR = (255, 255, 255)
BAR_WIDTH = 60
BAR_GAP = 0  # Reduced gap between bars to zero
BAR_THICKNESS = 20

# Data for histogram
frequencies = [30, 50, 20, 60, 40, 70, 10, 35, 45, 55]

# Colors for histogram lines
LINE_COLORS = [(140, 19, 185), (52, 60, 147), (0, 128, 0), (255, 69, 0), (255, 215, 0), (255, 20, 147), (0, 191, 255), (255, 105, 180), (128, 128, 128), (0, 0, 0)]

# Initialize the screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Histogram using DDA")

def draw_line(x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x = x1
    y = y1
    for _ in range(int(steps)):
        pygame.draw.rect(screen, color, (int(x), int(y), BAR_THICKNESS, 1))
        x += x_inc
        y += y_inc

def draw_histogram(frequencies):
    x = 14
    max_freq = max(frequencies)
    for freq, color in zip(frequencies, LINE_COLORS):
        scaled_freq = freq * (WINDOW_SIZE[1] - 100) / max_freq  # Scale the frequency to fit the window height
        draw_line(x, WINDOW_SIZE[1] - 50, x, WINDOW_SIZE[1] - 50 - scaled_freq, color)
        x += BAR_THICKNESS  # Adjusted x-coordinate for the next bar

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        draw_histogram(frequencies)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
