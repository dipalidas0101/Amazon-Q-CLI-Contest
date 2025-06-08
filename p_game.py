import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player settings
player_size = 40
player_speed = 5
player_health = 100

# Bullet settings
bullet_speed = 10
bullets = []

# Enemy settings
enemy_size = 30
enemies = []
enemy_speed = 2

# Clock
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((player_size, player_size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.direction = (0, 0)

    def update(self, keys):
        self.direction = (0, 0)
        if keys[pygame.K_LEFT]:
            self.direction = (-1, 0)
        if keys[pygame.K_RIGHT]:
            self.direction = (1, 0)
        if keys[pygame.K_UP]:
            self.direction = (0, -1)
        if keys[pygame.K_DOWN]:
            self.direction = (0, 1)
        self.rect.move_ip(self.direction[0] * player_speed, self.direction[1] * player_speed)

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - 2, self.rect.centery - 2, 4, 4)
        bullets.append(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * bullet_speed
        self.rect.y += self.direction[1] * bullet_speed
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.direction = (0, 0)

    def update(self):
        self.direction = (
            random.choice([-1, 0, 1]),
            random.choice([-1, 0, 1])
        )
        self.rect.x += self.direction[0] * enemy_speed
        self.rect.y += self.direction[1] * enemy_speed
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

# Initialize game objects
player = Player()
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()

# Spawn enemies
for _ in range(5):
    enemies.add(Enemy())
    all_sprites.add(Enemy())

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    keys = pygame.key.get_pressed()
    player.update(keys)
    all_sprites.draw(screen)

    # Update bullets
    for bullet in bullets:
        bullet.update()
        screen.blit(pygame.Surface((4, 4)), bullet.topleft)

    # Spawn new enemies
    if random.random() < 0.02:
        enemies.add(Enemy())
        all_sprites.add(Enemy())

    # Collision detection
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        for enemy in hit_enemies:
            player_health += 10
            if player_health > 100:
                player_health = 100

    # Check for collisions with enemies
    if pygame.sprite.spritecollide(player, enemies, False):
        player_health -= 10
        if player_health <= 0:
            running = False

    # Draw health bar
    pygame.draw.rect(screen, GREEN, (10, 10, player_health, 20))

    # Game over screen
    if player_health <= 0:
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 36))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
