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
LIGHT_GREEN = (144, 238, 144)  # Softer green for a more appealing look
DARK_GRAY = (50, 50, 50)  # Road color
RED = (255, 0, 0)

# Game clock
clock = pygame.time.Clock()

# Player settings
PLAYER_SIZE = 40
PLAYER_SPEED = 10

# Load assets with transparency
player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Load food images (acting as cars)
bad_food_images = [pygame.image.load("doritos.png").convert_alpha(),
                   pygame.image.load("oreo.png").convert_alpha(),
                   pygame.image.load("burger.png").convert_alpha()]

good_food_images = [pygame.image.load("strawberry.png").convert_alpha(),
                     pygame.image.load("lemon.png").convert_alpha(),
                     pygame.image.load("cheese.png").convert_alpha()]

# Resize food images
bad_food_images = [pygame.transform.scale(img, (40, 50)) for img in bad_food_images]
good_food_images = [pygame.transform.scale(img, (40, 50)) for img in good_food_images]

# Font
font = pygame.font.SysFont(None, 40)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
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

# Moving obstacle class (cars)
class Car(pygame.sprite.Sprite):
    def __init__(self, good=True, y_position=None):
        super().__init__()
        self.image = random.choice(good_food_images if good else bad_food_images)
        self.rect = self.image.get_rect()
        self.rect.y = (y_position) if y_position else random.randint(0, HEIGHT - self.rect.height)
        self.rect.x = -self.rect.width if random.choice([True, False]) else WIDTH
        self.speed = random.randint(5, 10) * (-1 if self.rect.x == WIDTH else 1)
        self.good = good

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = -self.rect.width if self.speed > 0 else WIDTH

# Main game function
def game_loop():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Define road lanes
    road_lanes = [HEIGHT // 5 + 30, 2 * HEIGHT // 5 + 30, 3 * HEIGHT // 5 + 30, 4 * HEIGHT // 5 + 30]  # Move lanes 10px down
    
    # Spawn moving obstacles (cars)
    cars = pygame.sprite.Group()
    for lane in road_lanes:
        for _ in range(2):  # Two cars per lane
            cars.add(Car(good=random.choice([True, False]), y_position=lane))
    all_sprites.add(cars)
    
    score = 0
    game_over = False

    while not game_over:
        SCREEN.fill(LIGHT_GREEN)
        
        # Draw multiple road lanes
        for lane in road_lanes:
            pygame.draw.rect(SCREEN, DARK_GRAY, (0, lane - 20, WIDTH, 40))
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        
        keys = pygame.key.get_pressed()
        player.update(keys)
        cars.update()
        
        # Collision with cars
        for car in pygame.sprite.spritecollide(player, cars, False):
            if car.good:
                score += 5
                car.kill()  # Remove good food once collected
            else:
                game_over = True
        
        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        # Check if player crossed the road
        if player.rect.top <= 0:
            player.rect.center = (WIDTH // 2, HEIGHT - 50)  # Reset player position

        # Draw all sprites
        all_sprites.draw(SCREEN)

        pygame.display.update()

        # Control the game speed
        clock.tick(30)

    # Display Game Over message with score
    SCREEN.fill(WHITE)
    game_over_text = font.render(f"Game Over - Score: {score}", True, RED)
    SCREEN.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds before quitting the game
    pygame.quit()

# Run the game loop
game_loop()
