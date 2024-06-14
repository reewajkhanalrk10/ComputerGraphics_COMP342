import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Set display resolution
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Set display mode
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Graphics Environment Setup")

    # Display resolution
    print("Display Resolution: {}x{}".format(screen_width, screen_height))

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
