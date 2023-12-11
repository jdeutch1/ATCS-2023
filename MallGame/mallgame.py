import pygame
import sys
import random

class FSM:
    def __init__(self, initial_state):
        # Dictionary (input_symbol, current_state) --> (action, next_state).
        self.state_transitions = {}
        self.current_state = initial_state

    def add_transition(self, input_symbol, state, action=None, next_state=None):
        if next_state is not None:
            self.state_transitions[(input_symbol, state)] = (action, next_state)

    def get_transition(self, input_symbol, state):
        return self.state_transitions.get((input_symbol, state), (None, None))

    def process(self, input_symbol):
        action, next_state = self.get_transition(input_symbol, self.current_state)
        if action is not None:
            action()
        if next_state is not None:
            self.current_state = next_state

class Player:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

class Enemy:
    MOVING = 'm'
    SHOW = 's'
    HIDDEN = 'h'

    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.fsm = FSM(self.SHOW)
        self.init_fsm()

    def init_fsm(self):
        self.fsm.add_transition('start_moving_event', self.SHOW, self.move, self.MOVING)
        self.fsm.add_transition('find_parents_event', self.MOVING, self.hide, self.HIDDEN)
        self.fsm.add_transition('next_level_event', self.HIDDEN, self.show, self.SHOW)

    def move(self):
        # Remove vibrating feature
        pass

    def move_random(self):
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

    def hide(self):
        self.rect.x = -100
        self.rect.y = -100

    def show(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mall Game")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Player variables
player_size = 30
player_pos = [0, 0]  # User starts in the top-left corner

# Create player object
player = Player(player_pos[0], player_pos[1], player_size)

# Load and resize the image
parent_image = pygame.image.load("parent.png")
parent_size = 60
parent_image = pygame.transform.scale(parent_image, (parent_size, parent_size))
parent_rect = parent_image.get_rect(center=(random.randint(0, width - parent_size), random.randint(0, height - parent_size)))

# Load and resize the image for obstacles
obstacle_image = pygame.image.load("man.png")
obstacle_size = 60
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_size, obstacle_size))

# Font for the "You Win!" and "Game Over" screens
font = pygame.font.Font(None, 36)

# Initialize levels
levels = [
    {"num_obstacles": 15, "num_enemies_random": 5, "num_enemies_left_to_right": 3, "enemy_speed_left_to_right": 2},
    {"num_obstacles": 20, "num_enemies_random": 10, "num_enemies_left_to_right": 5, "enemy_speed_left_to_right": 3},
    {"num_obstacles": 25, "num_enemies_random": 15, "num_enemies_left_to_right": 7, "enemy_speed_left_to_right": 4},
    {"num_obstacles": 30, "num_enemies_random": 20, "num_enemies_left_to_right": 10, "enemy_speed_left_to_right": 5},
    {"num_obstacles": 35, "num_enemies_random": 25, "num_enemies_left_to_right": 12, "enemy_speed_left_to_right": 6},
]

# Game loop
clock = pygame.time.Clock()
win_screen_duration = 5000  # 5 seconds
win_screen_timer = 0
win = False
current_level = 0

def setup_level(level):
    obstacles = []
    # Ensure no obstacle is placed in the top-left corner
    for _ in range(level["num_obstacles"]):
        obstacle_rect = pygame.Rect(random.randint(obstacle_size, width - obstacle_size), random.randint(obstacle_size, height - obstacle_size), obstacle_size, obstacle_size)
        obstacles.append(obstacle_rect)

    enemies_random = [Enemy(random.randint(0, width - obstacle_size), random.randint(0, height - obstacle_size), obstacle_size, [random.uniform(0.1, 0.5), random.uniform(0.1, 0.5)]) for _ in range(level["num_enemies_random"])]

    # Modify the initial positions and movements of left-to-right enemies
    enemies_left_to_right = [
        Enemy(-obstacle_size, random.randint(0, height - obstacle_size), obstacle_size, [level["enemy_speed_left_to_right"], 0]) for _ in range(level["num_enemies_left_to_right"] // 2)
    ] + [
        Enemy(width, random.randint(0, height - obstacle_size), obstacle_size, [-level["enemy_speed_left_to_right"], 0]) for _ in range(level["num_enemies_left_to_right"] // 2)
    ]

    return obstacles, enemies_random, enemies_left_to_right

obstacles, enemies_random, enemies_left_to_right = setup_level(levels[current_level])

# Flag to track if the parent image is currently visible
parent_visible = True
parent_disappear_timer = 0
parent_disappear_duration = 3000  # Disappear for 3 seconds
parent_appear_duration = 5000  # Appear for 5 seconds

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player_speed = 5

    if keys[pygame.K_LEFT] and player.rect.left > 0:
        player.rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player.rect.right < width:
        player.rect.x += player_speed
    if keys[pygame.K_UP] and player.rect.top > 0:
        player.rect.y -= player_speed
    if keys[pygame.K_DOWN] and player.rect.bottom < height:
        player.rect.y += player_speed

    for enemy in enemies_random:
        enemy.fsm.process('start_moving_event')

    for enemy in enemies_left_to_right:
        enemy.fsm.process('start_moving_event')

    # Check for collisions
    for obstacle in obstacles + [enemy.rect for enemy in enemies_random] + [enemy.rect for enemy in enemies_left_to_right]:
        if player.rect.colliderect(obstacle):
            print("Game Over!")
            pygame.quit()
            sys.exit()

    # Check if it's time to toggle the visibility of the parent image
    current_time = pygame.time.get_ticks()
    if not parent_visible and current_time - parent_disappear_timer >= parent_disappear_duration:
        parent_visible = True
        parent_rect.center = (random.randint(0, width - parent_size), random.randint(0, height - parent_size))
    elif parent_visible and current_time - parent_disappear_timer >= parent_appear_duration:
        parent_visible = False
        parent_disappear_timer = current_time

    screen.fill(white)

    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle.topleft)

    # Display the parent image only if it's currently visible
    if parent_visible:
        screen.blit(parent_image, parent_rect.topleft)

    pygame.draw.rect(screen, blue, player.rect)

    for enemy in enemies_random + enemies_left_to_right:
        screen.blit(obstacle_image, enemy.rect.topleft)

    if win:
        win_time_elapsed = pygame.time.get_ticks() - win_screen_timer
        if win_time_elapsed < win_screen_duration:
            win_text = font.render("You Win!", True, red)
            win_rect = win_text.get_rect(center=(width // 2, height // 2))
            screen.blit(win_text, win_rect.topleft)

            fsm_event = 'next_level_event'
            for enemy in enemies_random:
                enemy.fsm.process(fsm_event)

            for enemy in enemies_left_to_right:
                enemy.fsm.process(fsm_event)

    pygame.display.flip()
    clock.tick(30)
