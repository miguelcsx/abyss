# src/model/gun.py

import pygame

import pygame

class Gun(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.images = {
            'up': pygame.image.load("assets/images/gun/carrot_up.png").convert_alpha(),
            'down': pygame.image.load("assets/images/gun/carrot_down.png").convert_alpha(),
            'left': pygame.image.load("assets/images/gun/carrot_left.png").convert_alpha(),
            'right': pygame.image.load("assets/images/gun/carrot_right.png").convert_alpha()
        }
        
        # Scale all images to the same size
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (64, 64))

        self.image = self.images['right']  # Default image
        self.distance = 35
        self.player = player
        self.direction = pygame.Vector2(1, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.update_position()

    def update_position(self):
        direction_vector = self.player.direction
        if direction_vector == pygame.Vector2(0, -1):  # Up
            self.image = self.images['up']
        elif direction_vector == pygame.Vector2(0, 1):  # Down
            self.image = self.images['down']
        elif direction_vector == pygame.Vector2(-1, 0):  # Left
            self.image = self.images['left']
        elif direction_vector == pygame.Vector2(1, 0):  # Right
            self.image = self.images['right']
        
        self.rect = self.image.get_rect(center=self.player.rect.center + self.player.direction * self.distance)

    def get_muzzle_position(self):
        return self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.player.melee_attack():
            self.melee_animation()

    def update(self):
        self.update_position()
