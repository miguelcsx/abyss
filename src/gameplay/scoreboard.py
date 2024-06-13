# src/gameplay/scoreboard.py

import pygame
import csv

SCOREBOARD_FILE = 'assets/scoreboard.csv'

class Scoreboard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load('assets/images/sprites/background.png').convert()
        self.background = pygame.transform.scale(self.background, (width, height))
        self.font = pygame.font.SysFont('firacode', 24)
        self.header_font = pygame.font.SysFont('firacode', 36, bold=True)
        self.running = True
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(SCOREBOARD_FILE, mode='r', newline='') as file:
                reader = csv.reader(file)
                scores = list(reader)
                # Sort scores by kills (index 2) in descending order
                scores.sort(key=lambda x: int(x[2]), reverse=True)
                # Return top 10 scores
                return scores[:10]
        except FileNotFoundError:
            return []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def render(self):
        self.screen.blit(self.background, (0, 0))  # Draw background image

        title_text = "Scoreboard"
        title_color = (255, 255, 255)

        title_surface = self.header_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(self.width / 2, 50))
        self.screen.blit(title_surface, title_rect)

        # Headers
        header_names = ['Name', 'Time', 'Kills']
        header_y = title_rect.bottom + 30  # Increased spacing between title and headers
        header_x_start = 100

        for idx, header_name in enumerate(header_names):
            header_surface = self.header_font.render(header_name, True, (255, 255, 255))
            header_rect = header_surface.get_rect()
            header_rect.topleft = (header_x_start + idx * 200, header_y)
            self.screen.blit(header_surface, header_rect)

        # Display scores
        y_position = header_y + 50  # Increased spacing between header and first score entry
        for idx, score in enumerate(self.scores):
            name_text = self.font.render(score[0], True, (255, 255, 255))
            time_text = self.font.render(score[1], True, (255, 255, 255))
            kills_text = self.font.render(score[2], True, (255, 255, 255))

            name_rect = name_text.get_rect(topleft=(header_x_start, y_position + idx * 40))  # Increased vertical spacing between entries
            time_rect = time_text.get_rect(topleft=(header_x_start + 200, y_position + idx * 40))
            kills_rect = kills_text.get_rect(topleft=(header_x_start + 400, y_position + idx * 40))

            self.screen.blit(name_text, name_rect)
            self.screen.blit(time_text, time_rect)
            self.screen.blit(kills_text, kills_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
