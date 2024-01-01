import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION

# Basic configuration for display settings
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

# Initialize Pygame, font and sound effects
pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Times New Roman", 30)
FONT_SMALL = pygame.font.SysFont("Times New Roman", 20)
hover_sound = pygame.mixer.Sound("Sfx\sfx4.mp3")


def load_images():
    """Load images for node representation"""
    images = {
        "A": pygame.image.load("Image/house.png"),
        "B": pygame.image.load("Image/bookstore.png"),
        "C": pygame.image.load("Image/hospital.png"),
        "D": pygame.image.load("Image/bank.png"),
        "E": pygame.image.load("Image/supermarket.png"),
        "F": pygame.image.load("Image/school.png"),
    }
    return images


def draw_button(screen, button_rect, text, is_hovered):
    """Function to draw buttons on the screen"""
    color = DARK_GREEN if is_hovered else GREEN
    pygame.draw.rect(screen, color, button_rect)
    text_surface = FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)


def show_how_to_play(screen):
    """Display 'How to Play' instructions"""
    pygame.display.set_caption("Gowes To School")
    node_images = load_images()

    back_button = pygame.Rect(50, SCREEN_HEIGHT - 100, 100, 50)

    # Define node_info as a list of tuples
    node_info = [
        ("A", "Rumah (House)"),
        ("B", "Toko Buku (Bookstore)"),
        ("C", "Rumah Sakit (Hospital)"),
        ("D", "Bank"),
        ("E", "Supermarket"),
        ("F", "Sekolah (School)"),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEMOTION:
                # Periksa jika mouse berada di atas tombol dan mainkan sound effect
                if back_button.collidepoint(event.pos):
                    if not hover_played:
                        hover_sound.play()
                        hover_played = True
                else:
                    hover_played = False
            elif event.type == MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # Return to the main menu

        screen.fill(GREY)

        # Display gameplay instructions
        y = 75
        instructions = [
            "Cara Bermain 'Gowes To School':",
            "1. Sebuah grafik akan ditampilkan dengan titik-titik yang mewakili berbagai lokasi.",
            "2. Tugas Anda adalah menemukan jalur terpendek dari titik awal ke tujuan.",
            "3. Masukkan tebakan jalur Anda dengan mengetik urutan titik-titiknya (misal, ABEF).",
            "4. Tekan Enter untuk mengirim tebakan Anda dan periksa apakah itu jalur terpendek yang benar.",
            "5. Cobalah untuk menemukan jalur terpendek dengan jumlah lompatan antar titik yang paling sedikit.",
            "6. Setelah menyelesaikan level saat ini, Anda akan beralih ke level selanjutnya.",
        ]

        for line in instructions:
            text_surface = FONT_SMALL.render(line, True, WHITE)
            screen.blit(text_surface, (70, y))
            y += 40

        # Display node information with images in groups of three
        y += 60
        for i in range(0, len(node_info), 3):
            x = 300  # Starting x position for each group
            for j in range(3):
                if i + j < len(node_info):
                    node, description = node_info[i + j]
                    image = pygame.transform.scale(node_images[node], (40, 40))
                    screen.blit(image, (x, y))
                    text_surface = FONT_SMALL.render(
                        f"{node} - {description}", True, WHITE
                    )
                    screen.blit(text_surface, (x + 50, y))
                    x += 300  # Space out the nodes horizontally
            y += 60  # Move to the next row for the next group

        # Draw the back button
        mouse_pos = pygame.mouse.get_pos()
        back_hovered = back_button.collidepoint(mouse_pos)
        draw_button(screen, back_button, "Back", back_hovered)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    show_how_to_play(main_screen)
