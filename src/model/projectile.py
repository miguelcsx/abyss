# src/model/projectile.py

import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, collisions):
        super().__init__()
        
        self.image = pygame.image.load("assets/images/gun/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 8
        self.direction = direction
        self.collisions = collisions

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Check collision with obstacles or enemies
        if pygame.sprite.spritecollideany(self, self.collisions):
            self.kill()
