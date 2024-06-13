# src/model/collision.py

import pygame

class Collision(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__()
        self.image = pygame.image.load("assets/images/sprites/obstacle.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center = pos)
