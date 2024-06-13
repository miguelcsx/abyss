import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, collisions):
        super().__init__()
        self.images = {
            'right': pygame.image.load("assets/images/enemy/right.png"),
            'left': pygame.image.load("assets/images/enemy/left.png")
        }
        self.image = self.images['right']  # Start with the right image
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.max_life = 50  # Maximum life of the enemy
        self.life = self.max_life  # Current life of the enemy
        self.collisions = collisions
        self.mask = pygame.mask.from_surface(self.image)  # Create mask for enemy sprite
        self.direction = 'right'  # Initial direction

    def update(self, player):
        # Move towards the player
        player_position = pygame.math.Vector2(player.rect.centerx, player.rect.centery)
        enemy_position = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        player_direction = player_position - enemy_position
        player_distance = player_direction.length()

        if player_distance != 0:
            player_direction /= player_distance
        
        # Calculate desired movement vector towards player
        desired_vector = player_direction * self.speed

        # Determine direction based on movement vector
        if desired_vector.x > 0:
            self.direction = 'right'
            self.image = self.images['right']
        elif desired_vector.x < 0:
            self.direction = 'left'
            self.image = self.images['left']

        self.image = pygame.transform.scale(self.image, (128, 128))  # Resize image if needed

        # Try moving towards the player
        new_rect = self.rect.move(desired_vector)

        # Check for collisions with obstacles
        collided_sprites = pygame.sprite.spritecollide(self, self.collisions, False, pygame.sprite.collide_mask)
        
        if not collided_sprites:
            self.rect = new_rect
        else:
            # If there's a collision, try to navigate around the obstacle
            for obstacle in collided_sprites:
                obstacle_rect = obstacle.rect
                
                if desired_vector.x > 0:
                    self.rect.right = obstacle_rect.left
                elif desired_vector.x < 0:
                    self.rect.left = obstacle_rect.right
                if desired_vector.y > 0:
                    self.rect.bottom = obstacle_rect.top
                elif desired_vector.y < 0:
                    self.rect.top = obstacle_rect.bottom

    def apply_knockback(self, direction_vector, player):
        knockback_distance = 10  # Adjust the knockback distance
        knockback_vector = direction_vector.normalize() * knockback_distance

        self.rect.move_ip(knockback_vector)

        # Ensure enemy does not move out of bounds or into obstacles
        collided_sprites = pygame.sprite.spritecollide(self, self.collisions, False, pygame.sprite.collide_mask)
        if collided_sprites:
            for obstacle in collided_sprites:
                obstacle_rect = obstacle.rect
                if knockback_vector.x > 0:
                    self.rect.right = obstacle_rect.left
                elif knockback_vector.x < 0:
                    self.rect.left = obstacle_rect.right
                if knockback_vector.y > 0:
                    self.rect.bottom = obstacle_rect.top
                elif knockback_vector.y < 0:
                    self.rect.top = obstacle_rect.bottom

        # Directly hit the player when knockback is applied
        player.hit()

    def hit(self, damage):
        self.life -= damage
        if self.life <= 0:
            self.kill()
            print("Enemy killed")