# import libraries
import pygame

# initialize pygame
pygame.init()

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Rush')

clock = pygame.time.Clock()
FPS = 60

# load images
back_ground = pygame.image.load('img/bg.png')


# game loop
run = True
while run:

    clock.tick(FPS)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
