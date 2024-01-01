import sys
import pygame
from menu import show_menu
from lvl1 import Level1
from lvl2 import Level2
from howtoplay import show_how_to_play

# Constants for GUI
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Initialize pygame font
pygame.font.init()
FONT = pygame.font.SysFont("Courier New", 20)


def main():
    # Initialize pygame and set up the screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Main game loop
    while True:
        # Display menu and get player's choice
        menu_choice = show_menu(screen)

        if menu_choice == "play":
            # Start Level 1
            level1 = Level1(screen)
            play_level(level1, screen)

            # After Level 1 completion, continue to Level 2
            level2 = Level2(screen)
            play_level(level2, screen)

        elif menu_choice == "how_to_play":
            # Display how to play instructions
            show_how_to_play(screen)


def play_level(level, screen):
    # Function to play a given level
    running = True
    while running:
        # Event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update and draw the level
        level.update(events)
        level.draw()

        # Check if the level is completed
        if isinstance(level, Level1) and level.level_completed:
            show_success_message(screen, "Level 1 Completed! Starting Level 2...")
            running = False
        elif isinstance(level, Level2) and level.level_completed:
            show_success_message(screen, "Level 2 Completed! Congratulations!")
            running = False

        # Update the display
        pygame.display.flip()


def show_success_message(screen, message):
    # Function to show a success message
    text_surface = FONT.render(message, True, (0, 255, 0))  # Green color
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds


if __name__ == "__main__":
    main()
