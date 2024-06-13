# src/model/player.py

import sys
import pygame
import math

from src.model.enemy import Enemy
from src.model.projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, collisions):
        super().__init__()
        self.images = {
            "up": pygame.transform.scale(pygame.image.load("assets/images/player/up.png"), (64, 64)),
            "right": pygame.transform.scale(pygame.image.load("assets/images/player/right.png"), (64, 64))
        }

        self.image = self.images['up']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.life = 100
        self.collisions = collisions
        self.cooldown = 0
        self.shoot_delay = 20
        self.mask = pygame.mask.from_surface(self.image)  # Create mask for player sprite
        self.direction = pygame.Vector2(1, 0)
        self.gun = None

        # Stats
        self.time = 0
        self.enemies_killed = 0

    def move(self, dx, dy):
        # Calculate the magnitude of the vector
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        
        if magnitude != 0:
            # Normalize the vector
            dx /= magnitude
            dy /= magnitude
        
        # Try moving in x direction
        self.rect.x += dx * self.speed
        if self.check_collision():
            self.rect.x -= dx * self.speed

        # Try moving in y direction
        self.rect.y += dy * self.speed
        if self.check_collision():
            self.rect.y -= dy * self.speed

    def check_collision(self):
        # Check for collision using masks
        for sprite in self.collisions:
            if pygame.sprite.collide_mask(self, sprite):
                return True
        return False

    def update(self, direction):
        if direction == "up":
            self.move(0, -1)
            self.direction = pygame.Vector2(0, -1)
        elif direction == "down":
            self.move(0, 1)
            self.direction = pygame.Vector2(0, 1)
        elif direction == "left":
            self.move(-1, 0)
            self.direction = pygame.Vector2(-1, 0)
        elif direction == "right":
            self.move(1, 0)
            self.direction = pygame.Vector2(1, 0)
        
        self.update_time()
        

    def update_time(self):
        self.time += 1

    def update_health(self, damage):
        self.life -= damage
        if self.life <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

    def update_kills(self):
        self.enemies_killed += 1
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def melee_attack(self):
        for enemy in self.collisions:  # Check all potential collision objects
            if isinstance(enemy, Enemy):  # Ensure it's an enemy
                distance = self.rect.center.distance_to(enemy.rect.center)
                if distance <= self.gun.distance:  # If the enemy is within melee range
                    enemy.hit(10)  # Apply damage to the enemy
                    print("Hit enemy with melee attack")
                    return True
        return False

    # Update the shoot method to use melee attack if the enemy is close enough
    def shoot(self, collisions):
        if self.cooldown <= 0:
            if self.melee_attack():  # Try melee attack first
                self.cooldown = self.shoot_delay  # Apply cooldown after melee attack
                return None
            else:
                direction_vector = self.direction.normalize()
                if self.gun:
                    start_position = self.gun.get_muzzle_position()
                else:
                    start_position = self.rect.center

                projectile = Projectile(start_position[0], start_position[1], direction_vector, collisions)
                self.cooldown = self.shoot_delay
                return projectile

    
    def cooldown_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def hit(self):
        self.life -= 5

        if self.life <= 0:
            print("Game Over")
            # pygame.quit()
            # sys.exit()

    def collide(self):
        self.collisions.add(self)
