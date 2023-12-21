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
back_ground = pygame.image.load('img/bg.png').convert_alpha()
castle_full_health = pygame.image.load('img/castle/castle_100.png').convert_alpha()


# castle class
class Castle:
    def __init__(self, image100, x, y, scale):
        self.health = 1000
        self.max_health = self.health

        width = castle_full_health.get_width()
        height = castle_full_health.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width*scale), int(height*scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.image = self.image100

        screen.blit(self.image, self.rect)


castle = Castle(castle_full_health, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)
# game loop
run = True
while run:

    clock.tick(FPS)

    screen.blit(back_ground, (0, 0))

    # draw castle
    castle.draw()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.update()
pygame.quit()
