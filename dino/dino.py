import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
DINOSAUR_WIDTH = 50
DINOSAUR_HEIGHT = 50
CLOUD_WIDTH = 50
CLOUD_HEIGHT = 20
CACTUS_WIDTH = 20
CACTUS_HEIGHT = 40
FPS = 60
GRAVITY = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load images
dinosaur_img = pygame.image.load("dino.png")
dinosaur_img = pygame.transform.scale(
    dinosaur_img, (DINOSAUR_WIDTH, DINOSAUR_HEIGHT))
cloud_img = pygame.image.load("dino.png")
cloud_img = pygame.transform.scale(cloud_img, (CLOUD_WIDTH, CLOUD_HEIGHT))
cactus_img = pygame.Surface((CACTUS_WIDTH, CACTUS_HEIGHT))
cactus_img.fill(WHITE)

# Game variables
dinosaur_x = 50
dinosaur_y = SCREEN_HEIGHT - GROUND_HEIGHT - DINOSAUR_HEIGHT
dinosaur_vel_y = 0
dinosaur_jump = False

clouds = []
cacti = []

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dinosaur_jump:
                dinosaur_jump = True
                dinosaur_vel_y = -15  # Jump velocity

    # Update dinosaur position
    if dinosaur_jump:
        dinosaur_y += dinosaur_vel_y
        dinosaur_vel_y += GRAVITY

    # Check for collisions with the ground
    if dinosaur_y >= SCREEN_HEIGHT - GROUND_HEIGHT - DINOSAUR_HEIGHT:
        dinosaur_jump = False
        dinosaur_y = SCREEN_HEIGHT - GROUND_HEIGHT - DINOSAUR_HEIGHT

    # Generate clouds and cacti
    if random.randint(0, 100) < 2:
        clouds.append([SCREEN_WIDTH, random.randint(50, 150)])
    if random.randint(0, 100) < 2:
        cacti.append([SCREEN_WIDTH, SCREEN_HEIGHT -
                     GROUND_HEIGHT - CACTUS_HEIGHT])

    # Update cloud and cactus positions
    for cloud in clouds:
        cloud[0] -= 5
    for cactus in cacti:
        cactus[0] -= 5

    # Remove off-screen clouds and cacti
    clouds = [cloud for cloud in clouds if cloud[0] > -CLOUD_WIDTH]
    cacti = [cactus for cactus in cacti if cactus[0] > -CACTUS_WIDTH]

    # Draw everything
    screen.fill(WHITE)

    # Draw ground
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT -
                     GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Draw clouds
    for cloud in clouds:
        screen.blit(cloud_img, (cloud[0], cloud[1]))

    # Draw cacti
    for cactus in cacti:
        screen.blit(cactus_img, (cactus[0], cactus[1]))

    # Draw dinosaur
    screen.blit(dinosaur_img, (dinosaur_x, dinosaur_y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
