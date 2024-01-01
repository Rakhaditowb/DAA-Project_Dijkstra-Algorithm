import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION

# Basic configuration for the display menu
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
NODE_RADIUS = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (238, 105, 105)
GREEN = (159, 226, 191)
BLUE = (167, 199, 231)
DARK_GREEN = (0, 163, 108)
GREY = (45, 45, 48)
DEFAULT_IMAGE_SIZE = (250, 250)

# Initialize Pygame, font, and sound effects
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Courier New", 28)
hover_sound = pygame.mixer.Sound("Sfx\sfx4.mp3")

# Load and scale the game logo
logo_image = pygame.image.load("Image\logo.png")  # Replace with the correct path
logo_image = pygame.transform.scale(logo_image, DEFAULT_IMAGE_SIZE)
logo_rect = logo_image.get_rect()
logo_rect.center = (SCREEN_WIDTH // 2, 150)  # Center the logo on the screen


def draw_button(screen, button_rect, text, is_hovered):
    """Draw buttons on the screen"""
    color = DARK_GREEN if is_hovered else GREEN
    pygame.draw.rect(screen, color, button_rect)
    text_surface = FONT.render(text, True, GREY)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


def show_menu(screen):
    """Display the main menu of the game"""
    pygame.display.set_caption("Gowes To School")

    # Define the 'Play' and 'How to Play' buttons
    play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
    how_to_play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                # Periksa jika mouse berada di atas tombol dan mainkan sound effect
                if play_button.collidepoint(
                    event.pos
                ) or how_to_play_button.collidepoint(event.pos):
                    if not hover_played:
                        hover_sound.play()
                        hover_played = True
                else:
                    hover_played = False

            elif event.type == MOUSEBUTTONDOWN:
                # Check if a button is pressed
                if play_button.collidepoint(event.pos):
                    return "play"  # Player chooses to start the game
                elif how_to_play_button.collidepoint(event.pos):
                    return "how_to_play"  # Player chooses to view how to play

        mouse_pos = pygame.mouse.get_pos()
        play_hovered = play_button.collidepoint(mouse_pos)
        how_to_play_hovered = how_to_play_button.collidepoint(mouse_pos)

        screen.fill(GREY)
        screen.blit(logo_image, logo_rect)  # Display the logo
        draw_button(screen, play_button, "Play", play_hovered)
        draw_button(screen, how_to_play_button, "How to Play", how_to_play_hovered)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    show_menu(main_screen)
