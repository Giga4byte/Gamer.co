import pygame
import random

# Initialize pygame module
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossy Road Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game clock
clock = pygame.time.Clock()

# Player settings
PLAYER_SIZE = 40
PLAYER_SPEED = 10

# Car settings
CAR_WIDTH = 60
CAR_HEIGHT = 40
CAR_SPEED = 5

# Font
font = pygame.font.SysFont(None, 40)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED

# Car class
class Car(pygame.sprite.Sprite):
    def __init__(self, y_position):
        super().__init__()
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y_position
        self.rect.x = random.randint(0, WIDTH - CAR_WIDTH)

    def update(self):
        self.rect.x += CAR_SPEED
        if self.rect.x > WIDTH:
            self.rect.x = -CAR_WIDTH
            self.rect.y = random.randint(0, HEIGHT - CAR_HEIGHT)

# Main game function
def game_loop():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    cars = pygame.sprite.Group()
    for i in range(3):  # Create 3 cars initially
        car = Car(random.randint(0, HEIGHT - CAR_HEIGHT))
        all_sprites.add(car)
        cars.add(car)

    score = 0
    game_over = False

    while not game_over:
        SCREEN.fill(GREEN)
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        
        keys = pygame.key.get_pressed()
        player.update(keys)
        
        # Update car positions
        cars.update()

        # Collision detection
        if pygame.sprite.spritecollide(player, cars, False):
            game_over = True
        
        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        # Check if player crossed the road
        if player.rect.top <= 0:
            score += 1
            player.rect.center = (WIDTH // 2, HEIGHT - 50)  # Reset player position

        # Draw all sprites
        all_sprites.draw(SCREEN)

        pygame.display.update()

        # Control the game speed
        clock.tick(30)

    # Display Game Over message
    SCREEN.fill(WHITE)
    game_over_text = font.render("Game Over", True, RED)
    SCREEN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds before quitting the game
    pygame.quit()

# Run the game loop
game_loop()
