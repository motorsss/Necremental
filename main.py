import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 1500
FPS = 60

# Colors
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game Variables
mana = 0
skeleton_count = 0
skeletons = []
slime = None

# Base Classes
class Unit:
    def __init__(self, health, attack, speed):
        self.health = health
        self.attack = attack
        self.speed = speed
        self.attack_timer = 1  # Timer to track attack intervals

class Monster:
    def __init__(self, health, attack, speed):
        self.health = health
        self.attack = attack
        self.speed = speed
        self.attack_timer = 1  # Timer to track attack intervals

# Derived Classes
class Skeleton(Unit):
    def __init__(self):
        super().__init__(health=10, attack=2, speed=1)

class Slime(Monster):
    def __init__(self):
        super().__init__(health=10, attack=1, speed=1)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apprentice Necromancer")

# Canvas dimensions
CANVAS_WIDTH, CANVAS_HEIGHT = 800, 800
CANVAS_X, CANVAS_Y = 100, 300

# Button positions
BUTTON_X = 20
GATHER_MANA_Y = 20
SUMMON_SKELETON_Y = 60

# Font
font = pygame.font.Font(None, 36)

def gather_mana():
    global mana
    mana += 1

def summon_skeleton():
    global mana, skeleton_count
    if mana >= 10:
        mana -= 10
        skeleton_count += 1
        skeletons.append(Skeleton())

def spawn_new_monster():
    global slime
    slime = Slime()  # Spawn a new slime

def battle():
    global slime
    if slime is None:
        spawn_new_monster()  # Initialize slime if it doesn't exist

    # Battle logic
    for skeleton in skeletons:
        skeleton.attack_timer += 1 / FPS  # Increment attack timer
        if skeleton.attack_timer >= 1 / skeleton.speed:  # Check if it's time to attack
            slime.health -= skeleton.attack
            skeleton.attack_timer = 0  # Reset attack timer

    # Slime attacks skeletons if it's still alive
    if slime.health > 0:
        for skeleton in skeletons[:]:  # Iterate over a copy of the list
            skeleton.attack_timer += 1 / FPS  # Increment attack timer
            if skeleton.health > 0 and slime.health > 0:
                if slime.attack_timer >= 1 / slime.speed:  # Check if it's time to attack
                    skeleton.health -= slime.attack
                    slime.attack_timer = 0  # Reset attack timer

    # Check for dead units and monsters
    for skeleton in skeletons[:]:  # Iterate over a copy of the list
        if skeleton.health <= 0:
            skeletons.remove(skeleton)  # Remove dead skeleton

    if slime.health <= 0:
        print("Slime defeated!")
        spawn_new_monster()  # Spawn a new slime

def draw_health_bar(health, max_health, x, y):
    health_ratio = health / max_health
    pygame.draw.rect(screen, RED, (x, y, 100, 10))  # Background health bar
    pygame.draw.rect(screen, GREEN, (x, y, 100 * health_ratio, 10))  # Current health

def draw_units():
    # Draw skeletons
    for index, skeleton in enumerate(skeletons):
        x = CANVAS_X + 50 + index * 50
        y = CANVAS_Y + 50
        screen.blit(font.render('@', True, BLACK), (x, y))  # Draw skeleton
        draw_health_bar(skeleton.health, 10, x, y + 15)  # Draw health bar

    # Draw slime
    if slime is not None:
        x = CANVAS_X + 400
        y = CANVAS_Y + 50
        screen.blit(font.render('A', True, BLACK), (x, y))  # Draw slime
        draw_health_bar(slime.health, 10, x, y + 15)  # Draw health bar

def draw_button(text, x, y):
    button_surface = font.render(text, True, BLACK)
    button_rect = button_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, GREEN, button_rect.inflate(20, 20))  # Draw button background
    screen.blit(button_surface, button_rect)

def draw():
    screen.fill(GRAY)

    # Draw canvas
    pygame.draw.rect(screen, WHITE, (CANVAS_X, CANVAS_Y, CANVAS_WIDTH, CANVAS_HEIGHT))

    mana_text = font.render(f'Mana: {mana}', True, BLACK)
    skeleton_text = font.render(f'Skeletons: {skeleton_count}', True, BLACK)

    screen.blit(mana_text, (BUTTON_X, GATHER_MANA_Y))
    screen.blit(skeleton_text, (BUTTON_X, SUMMON_SKELETON_Y))

    draw_button('Gather Mana', BUTTON_X, GATHER_MANA_Y + 40)
    draw_button('Summon Skeleton (10 Mana)', BUTTON_X, SUMMON_SKELETON_Y + 40)

    draw_units()  # Draw units and health bars

    pygame.display.flip()

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if Gather Mana button is clicked
            if BUTTON_X < mouse_x < BUTTON_X + 200 and GATHER_MANA_Y + 40 < mouse_y < GATHER_MANA_Y + 80:
                gather_mana()
            # Check if Summon Skeleton button is clicked
            if BUTTON_X < mouse_x < BUTTON_X + 200 and SUMMON_SKELETON_Y + 40 < mouse_y < SUMMON_SKELETON_Y + 80:
                summon_skeleton()

    battle()  # Handle battle logic
    draw()    # Draw everything
    clock.tick(FPS)
