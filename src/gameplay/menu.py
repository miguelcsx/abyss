# src/gameplay/menu.py

import pygame

class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load('assets/images/sprites/background.png').convert()
        self.background = pygame.transform.scale(self.background, (width, height))
        self.font = pygame.font.SysFont('firacode', 36)
        self.title_font_large = pygame.font.SysFont('firacode', 72)
        self.title_font_small = pygame.font.SysFont('firacode', 48)
        self.options = ["Play", "Scoreboard", "Quit"]
        self.selected_option = 0
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # Play
                        return "play"
                    elif self.selected_option == 1:  # Scoreboard
                        return "scoreboard"
                    elif self.selected_option == 2:  # Quit
                        return "quit"

    def render(self):
        self.screen.blit(self.background, (0, 0))  # Draw background image

        title_large_text = "Abyss".upper()
        title_small_text = "The escape of the bunny"
        title_large_color = (255, 255, 255)
        title_small_color = (255, 255, 255)

        title_large_surface = self.title_font_large.render(title_large_text, True, title_large_color)
        title_large_rect = title_large_surface.get_rect(center=(self.width / 2, self.height / 4))
        self.screen.blit(title_large_surface, title_large_rect)

        title_small_surface = self.title_font_small.render(title_small_text, True, title_small_color)
        title_small_rect = title_small_surface.get_rect(center=(self.width / 2, self.height / 4 + 60))
        self.screen.blit(title_small_surface, title_small_rect)

        # Calculate starting vertical position for options
        options_start_y = title_small_rect.bottom + 50

        for idx, option in enumerate(self.options):
            text_color = (255, 255, 255) if idx != self.selected_option else (255, 0, 0)
            text = self.font.render(option, True, text_color)
            text_rect = text.get_rect(center=(self.width / 2, options_start_y + idx * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()


    def run(self):
        while self.running:
            action = self.handle_events()
            if action == "play":
                return "play"
            elif action == "quit":
                pygame.quit()
                quit()
            self.render()
