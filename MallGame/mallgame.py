import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Where's Waldo")

# Define the Sprite class for decoys
class Decoy(pygame.sprite.Sprite):
    def __init__(self, color, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

# Create Waldo rectangle
waldo_rect = pygame.Rect(
    random.randint(0, WIDTH - 50),
    random.randint(0, HEIGHT - 50),
    50,
    50
)

# Create instances of the sprites
waldo_sprite = pygame.sprite.Sprite()
waldo_sprite.image = pygame.Surface((50, 50))
waldo_sprite.image.fill(RED)
waldo_sprite.rect = waldo_sprite.image.get_rect()
waldo_sprite.rect.topleft = waldo_rect.topleft

decoy_sprites = pygame.sprite.Group()
for _ in range(30):  # Adjust the number of decoys as needed
    decoy_sprite = Decoy(BLACK, (20, 20))  # Adjust the size as needed
    decoy_sprite.rect.topleft = (random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20))  # Adjust the size and frequency
    decoy_sprites.add(decoy_sprite)

# Create sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(waldo_sprite, decoy_sprites)

# Main game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is on Waldo
            if waldo_rect.collidepoint(event.pos):
                print("Congratulations! You found Waldo!")

    # Clear the screen
    screen.fill(WHITE)

    # Draw Waldo
    pygame.draw.rect(screen, RED, waldo_rect)

    # Draw all sprites (including decoys)
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
