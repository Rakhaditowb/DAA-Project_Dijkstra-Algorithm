import sys
import pygame
from pygame.locals import KEYDOWN, K_RETURN
from heapq import heappush
from threading import Thread

# Constants for GUI
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
YELLOW = (255, 255, 0)
START_NODE_COLOR = (255, 165, 0)  # Orange
DEST_NODE_COLOR = (0, 191, 255)  # Bright Blue

# Initialize fonts and sound effects
pygame.font.init()
FONT = pygame.font.SysFont("Courier New", 20)
FONT_SMALL = pygame.font.SysFont("Times New Roman", 18)
pygame.mixer.init()
sfx1 = pygame.mixer.Sound("Sfx\sfx1.mp3")
sfx2 = pygame.mixer.Sound("Sfx\sfx2.mp3")
sfx3 = pygame.mixer.Sound("Sfx\sfx3.mp3")


class Level1:
    def __init__(self, screen):
        """Initialize the Level 1 of the game"""
        # Initialize variables
        self.screen = screen
        self.submit_pressed = False
        self.shortest_path_result = []
        self.solving = False
        self.guessed_path = ""
        self.is_correct = False
        self.text_input = ""
        self.text_input_rect = pygame.Rect(20, 150, 200, 30)
        self.submit_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT - 70, 80, 30
        )
        self.submit_hover = False
        self.visited = []
        self.current_node = None
        self.level_completed = False

        # Load node images
        self.node_images_paths = {
            "A": "Image/house.png",
            "B": "Image/bookstore.png",
            "C": "Image/hospital.png",
            "D": "Image/bank.png",
            "E": "Image/supermarket.png",
            "F": "Image/school.png",
        }
        self.node_images = {
            node: pygame.transform.scale(pygame.image.load(path), (40, 40))
            for node, path in self.node_images_paths.items()
        }

        # GUI labels
        self.gui_source_label = "Rumah"
        self.gui_destination_label = "Sekolah"

        # Graph for the level
        self.graph = {
            "A": {"B": 2, "C": 4},
            "B": {"A": 2, "C": 3, "D": 8},
            "C": {"A": 4, "B": 3, "E": 5, "D": 2},
            "D": {"B": 8, "C": 2, "E": 11, "F": 22},
            "E": {"C": 5, "D": 11, "F": 1},
            "F": {"D": 22, "E": 1},
        }

        # Node positions on the screen
        self.node_positions = {
            "A": (SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.5),
            "B": (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.3),
            "C": (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.7),
            "D": (SCREEN_WIDTH * 0.65, SCREEN_HEIGHT * 0.3),
            "E": (SCREEN_WIDTH * 0.65, SCREEN_HEIGHT * 0.7),
            "F": (SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.5),
        }

        self.thread = None

        self.source = "A"
        self.destination = "F"

    def update(self, events):
        """Update game state based on events"""
        for event in events:
            if event.type == KEYDOWN:
                sfx1.play()
                if event.key == K_RETURN and not self.solving:
                    self.guessed_path = self.text_input
                    self.text_input = ""
                    self.solving = True
                    self.thread = Thread(
                        target=self.dijkstra_thread_func,
                        args=(
                            self.graph,
                            self.source,
                            self.destination,
                            self.screen,
                            self.node_positions,
                        ),
                        daemon=True,
                    )
                    self.thread.start()
                    self.submit_pressed = True
                elif event.key == 8:  # Handle backspace
                    self.text_input = self.text_input[:-1]
                else:  # Handle other key presses
                    if len(self.text_input) < 6:  # Limit the input length
                        self.text_input += event.unicode.upper()

        if self.thread and not self.thread.is_alive():
            self.thread = None

        self.submit_hover = self.submit_button.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        """Draw game elements on the screen"""
        self.draw_graph(
            self.graph,
            self.node_positions,
            self.source,
            self.destination,
            self.guessed_path,
            self.is_correct,
            self.text_input,
        )
        pygame.display.flip()

    def draw_graph(
        self,
        graph,
        node_positions,
        start,
        destination,
        guessed_path,
        is_correct,
        text_input,
    ):
        """Draw the graph, nodes, edges, and texts"""
        self.screen.fill(GREY)

        # Draw edges and edge weights
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors.items():
                start_pos = node_positions[node]
                end_pos = node_positions[neighbor]
                pygame.draw.line(self.screen, WHITE, start_pos, end_pos, 2)

                # Calculate position for weight text
                middle_pos = (
                    (start_pos[0] + end_pos[0]) // 2,
                    (start_pos[1] + end_pos[1]) // 2,
                )
                weight_text = FONT_SMALL.render(str(weight), True, YELLOW)
                self.screen.blit(weight_text, middle_pos)

        # Draw nodes
        for node, position in node_positions.items():
            image = self.node_images[node]
            image_rect = image.get_rect(center=position)
            self.screen.blit(image, image_rect)

            # Node text
            text = FONT.render(node, True, WHITE)
            text_rect = text.get_rect(center=(position[0], position[1]))
            self.screen.blit(text, text_rect)

        # Guessed path and correctness
        guess_text = FONT_SMALL.render("Guess: " + guessed_path, True, WHITE)
        correctness_text = FONT_SMALL.render(
            "Correct!" if is_correct else "Incorrect",
            True,
            GREEN if is_correct else RED,
        )
        self.screen.blit(guess_text, (20, 80))
        self.screen.blit(correctness_text, (20, 110))

        # Text input
        pygame.draw.rect(self.screen, WHITE, self.text_input_rect)
        text_surface = FONT.render(text_input, True, BLACK)
        self.screen.blit(
            text_surface, (self.text_input_rect.x + 5, self.text_input_rect.y + 5)
        )

        # Start and destination labels
        start_text = FONT_SMALL.render("Start: " + self.gui_source_label, True, WHITE)
        destination_text = FONT_SMALL.render(
            "Destination: " + self.gui_destination_label, True, WHITE
        )
        self.screen.blit(start_text, (20, 20))
        self.screen.blit(destination_text, (20, 50))

    def dijkstra(self, graph, src, dest):
        inf = sys.maxsize
        node_data = {node: {"cost": inf, "pred": []} for node in graph}
        node_data[src]["cost"] = 0
        visited = []

        temp = src
        for i in range(len(graph) - 1):
            if temp not in visited:
                visited.append(temp)
                min_heap = []
                for neighbor in graph[temp]:
                    if neighbor not in visited:
                        cost = node_data[temp]["cost"] + graph[temp][neighbor]
                        if cost < node_data[neighbor]["cost"]:
                            node_data[neighbor]["cost"] = cost
                            node_data[neighbor]["pred"] = node_data[temp]["pred"] + [
                                temp
                            ]
                        heappush(min_heap, (node_data[neighbor]["cost"], neighbor))

                if min_heap:
                    temp = min_heap[0][1]
                else:
                    break
        shortest_distance = node_data[dest]["cost"]
        shortest_path = node_data[dest]["pred"] + [dest]
        print("Shortest Distance: " + str(shortest_distance))
        print("Shortest Path: " + str(shortest_path))
        return node_data[dest]["pred"] + [dest]

    def dijkstra_thread_func(self, graph, src, dest, screen, node_positions):
        self.shortest_path_result = self.dijkstra(graph, src, dest)
        self.solving = False
        self.is_correct = self.guessed_path == "".join(self.shortest_path_result)
        if self.is_correct:
            sfx2.play()
            print("Level 1 completed successfully")
            self.level_completed = True
        else:
            sfx3.play()
            print("Level 1 not completed")


# Main function to run the game
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gowes To School - Level 1")

    level1 = Level1(screen)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        level1.update(events)
        level1.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
