# src/gameplay/game.py

import sys
import math
import random
import pygame
from src.gameplay.name_input import NameInput
from src.model.gun import Gun
from src.model.player import Player
from src.model.enemy import Enemy
from src.model.collision import Collision

class Game:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((width, height))
        self.background = pygame.image.load('assets/images/sprites/background.png').convert()
        pygame.display.set_caption("Abyss")
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.collisions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = Player(100, 100, self.collisions)
        self.gun = Gun(self.player)
        self.player.gun = self.gun

        self.spawn_timer = 0
        self.spawn_rate = 60

        self.create_obstacles(10)

        self.player_time = 0
        self.player_health = 100
        self.enemies_killed = 0

        self.font = pygame.font.SysFont('firacode', 20)


    def create_obstacles(self, n):
        radius = 100
        avoid_point = (100, 100) # Player spawn position
        
        for _ in range(n):
            while True:
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                
                # Calculate distance from (x, y) to the avoid_point (50, 50)
                distance = math.sqrt((x - avoid_point[0])**2 + (y - avoid_point[1])**2)
                
                # Check if the distance is greater than the radius (100)
                if distance > radius:
                    break
            
            # If the coordinates are valid, create the obstacle
            collision = Collision((x, y), (32, 32), self.collisions)
            self.collisions.add(collision)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def clear_screen(self):
        self.screen.blit(self.background, (0, 0))

    def update_game(self):
        # Update the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.update("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.update("right")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.update("up")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.update("down")
        if keys[pygame.K_SPACE]:
            self.create_projectile()
        if keys[pygame.K_ESCAPE]:
            self.running = False

        # Update the projectiles
        self.projectiles.update()

        self.player.cooldown_tick()
        self.gun.update()
        self.update_enemies(self.player)

        self.player_time = self.player.time
        self.player_health = self.player.life
        self.enemies_killed = self.player.enemies_killed


    def create_projectile(self):
        projectile = self.player.shoot(self.collisions)
        if projectile:
            self.projectiles.add(projectile)

    def update_enemies(self, player):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_timer = 0
            self.spawn_enemy()

        # Update enemies
        self.enemies.update(player)

        # Apply knockback to enemies and directly hit the player
        for enemy in self.enemies:
            if pygame.sprite.collide_mask(self.player, enemy):
                player_direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(enemy.rect.center)
                enemy.apply_knockback(-player_direction, self.player)  # Apply knockback and directly hit the player

        # Check collisions with projectiles hitting enemies
        for projectile in self.projectiles:
            enemies_hit = pygame.sprite.spritecollide(projectile, self.enemies, True, pygame.sprite.collide_mask)
            for enemy in enemies_hit:
                enemy.hit(10)
                player.update_kills()

            # Check collision with obstacles or enemies
            if pygame.sprite.spritecollideany(projectile, self.collisions):
                projectile.kill()  # Destroy the projectile upon collision



    def spawn_enemy(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        
        # Check if the spawn location is valid (not colliding with any obstacles or enemies)
        colliding_obstacles = pygame.sprite.spritecollideany(Collision((x, y), (32, 32), self.collisions), self.collisions)
        colliding_enemies = pygame.sprite.spritecollideany(Enemy(x, y, self.collisions), self.enemies)
        
        if not colliding_obstacles and not colliding_enemies:
            enemy = Enemy(x, y, self.collisions)
            self.enemies.add(enemy)


    def render_game(self):
        self.clear_screen()
        self.player.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.enemies.draw(self.screen)
        self.collisions.draw(self.screen)
        self.gun.draw(self.screen)
        self.render_player_info()

    def update_display(self):
        pygame.display.flip()

    def cap_frame_rate(self):
        self.clock.tick(self.fps)

    def render_player_info(self):
        text_color = (0, 0, 0)  # Black text color
        padding = 10

        # Render time
        time_text = self.font.render(f"Time: {self.player_time}", True, text_color)
        time_rect = time_text.get_rect()
        time_rect.topleft = (padding, padding)

        # Render health
        health_text = self.font.render(f"Health: {self.player_health}", True, text_color)
        health_rect = health_text.get_rect()
        health_rect.topleft = (padding, time_rect.bottom + padding)

        # Render enemies killed
        enemies_text = self.font.render(f"Enemies Killed: {self.enemies_killed}", True, text_color)
        enemies_rect = enemies_text.get_rect()
        enemies_rect.topleft = (padding, health_rect.bottom + padding)

        # Blit text onto the screen
        self.screen.blit(time_text, time_rect)
        self.screen.blit(health_text, health_rect)
        self.screen.blit(enemies_text, enemies_rect)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Abyss")

        name_input = NameInput(self.width, self.height)

        while not name_input.is_done():
            name_input.handle_events()
            name_input.render(screen)

        player_name = name_input.get_input()

        while self.running:
            self.handle_events()
            self.update_game()
            self.render_game()
            self.update_display()
            self.cap_frame_rate()

        # Game ended, return player's stats
        return (player_name, self.player_time, self.enemies_killed)
