import pygame
import sys
import random

class Enemy:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Bounce off the walls
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]

    def move_random(self):
        # Move randomly
        random_direction = random.choice(["up", "down", "left", "right"])
        random_speed = random.uniform(0.1, 0.5)
        
        if random_direction == "up" and self.rect.top > 0:
            self.speed = [0, -random_speed]
        elif random_direction == "down" and self.rect.bottom < height:
            self.speed = [0, random_speed]
        elif random_direction == "left" and self.rect.left > 0:
            self.speed = [-random_speed, 0]
        elif random_direction == "right" and self.rect.right < width:
            self.speed = [random_speed, 0]

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Player variables
player_size = 30
player_pos = [width // 2, height // 2]

# Load and resize the image
parent_image = pygame.image.load("parent.png")
parent_size = 60
parent_image = pygame.transform.scale(parent_image, (parent_size, parent_size))
parent_rect = parent_image.get_rect(center=(random.randint(0, width - parent_size), random.randint(0, height - parent_size)))

# Obstacles (rectangles that the user must avoid)
obstacle_size = 30
num_obstacles = 15
obstacles = [pygame.Rect(random.randint(0, width - obstacle_size), random.randint(0, height - obstacle_size), obstacle_size, obstacle_size) for _ in range(num_obstacles)]

# Enemies (rectangles that move around at random)
num_enemies_random = 50  # Increased from 30 to 50
enemies_random = [Enemy(random.randint(0, width - obstacle_size), random.randint(0, height - obstacle_size), obstacle_size, [random.uniform(0.1, 0.5), random.uniform(0.1, 0.5)]) for _ in range(num_enemies_random)]

# Enemies (green rectangles that move from left to right)
num_enemies_left_to_right = 10
enemy_speed_left_to_right = 2
enemies_left_to_right = [Enemy(0, random.randint(0, height - obstacle_size), obstacle_size, [enemy_speed_left_to_right, 0]) for _ in range(num_enemies_left_to_right)]

# Font for the "You Win!" screen
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
win_screen_duration = 5000  # 5 seconds
win_screen_timer = 0
win = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player_speed = 5
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
        player_pos[1] += player_speed

    # Move enemies randomly
    for enemy in enemies_random:
        enemy.move_random()

    # Move enemies from left to right
    for enemy in enemies_left_to_right:
        enemy.move()

    # Check for collision with obstacles and enemies
    for obstacle in obstacles + [enemy.rect for enemy in enemies_random] + [enemy.rect for enemy in enemies_left_to_right]:
        if pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(obstacle):
            print("Game Over!")
            pygame.quit()
            sys.exit()

    # Check for winning condition
    if not win and pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(parent_rect):
        win = True
        win_screen_timer = pygame.time.get_ticks()

    # Draw everything
    screen.fill(white)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, black, obstacle)

    # Draw random enemies
    for enemy in enemies_random:
        pygame.draw.rect(screen, black, enemy.rect)

    # Draw left-to-right enemies
    for enemy in enemies_left_to_right:
        pygame.draw.rect(screen, green, enemy.rect)

    # Draw player
    pygame.draw.rect(screen, blue, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw parent image
    screen.blit(parent_image, parent_rect.topleft)

    # Display "You Win!" screen if the player wins
    if win:
        win_time_elapsed = pygame.time.get_ticks() - win_screen_timer
        if win_time_elapsed < win_screen_duration:
            win_text = font.render("You Win!", True, red)
            win_rect = win_text.get_rect(center=(width // 2, height // 2))
            screen.blit(win_text, win_rect.topleft)

    pygame.display.flip()
    clock.tick(30)  # Adjust the frame rate as needed
