# src/gameplay/name_input.py
import pygame
import sys

class NameInput:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = pygame.image.load('assets/images/sprites/background.png').convert()
        self.background = pygame.transform.scale(self.background, (width, height))
        
        self.input_box = pygame.Rect(width // 2 - 100, height // 2 - 10, 200, 32)
        self.color_inactive = pygame.Color('white')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False

        self.font = pygame.font.Font(None, 32)
        self.prompt_text = self.font.render("Enter Your Name:", True, (255, 255, 255))
        self.prompt_rect = self.prompt_text.get_rect(center=(width // 2, height // 2 - 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.prompt_text, self.prompt_rect)

        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(screen, self.color, self.input_box, 2)

        pygame.display.flip()

    def get_input(self):
        return self.text

    def is_done(self):
        return self.done
