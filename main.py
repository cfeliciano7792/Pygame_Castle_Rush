# import libraries
import pygame
import math

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
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
bullet_width = bullet_img.get_width()
bullet_height = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(bullet_width*0.075), int(bullet_height*0.075)))

# define colors
WHITE = (255, 255, 255)


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

    def shoot(self):
        # retrieves coordinates of mouse position
        pos = pygame.mouse.get_pos()
        x_distance = pos[0] - self.rect.midleft[0]
        y_distance = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_distance, x_distance))

        pygame.draw.line(screen, WHITE, (self.rect.midleft[0], self.rect.midleft[1]), pos)

    def draw(self):
        self.image = self.image100
        screen.blit(self.image, self.rect)


#  bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle) # converts input angle into radians
        self.speed = 10


castle = Castle(castle_full_health, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)
# game loop
run = True
while run:

    clock.tick(FPS)

    screen.blit(back_ground, (0, 0))

    # draw castle
    castle.draw()
    castle.shoot()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.update()
pygame.quit()
