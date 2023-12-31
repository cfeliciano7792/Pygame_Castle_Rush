# import libraries
import pygame
import math
import random
import os
from enemy import Enemy
import button

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

# game variables
level = 1
high_score = 0
level_difficulty = 0
target_difficulty = 1000
DIFFICULTY_MULTIPLIER = 1.1
game_over = False
next_level = False
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
max_towers = 4
TOWER_COST = 5000
tower_positions = [
    [SCREEN_WIDTH - 250, SCREEN_HEIGHT - 200],
    [SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150],
    [SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150],
    [SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150],
]

# load high score
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())

# define colors
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

# define font
font = pygame.font.SysFont('Futura', 30)
font60 = pygame.font.SysFont('Futura', 60)

# load images
back_ground = pygame.image.load('img/bg.png').convert_alpha()
castle_full_health = pygame.image.load('img/castle/castle_100.png').convert_alpha()
castle_half_health = pygame.image.load('img/castle/castle_50.png').convert_alpha()
castle_quarter_health = pygame.image.load('img/castle/castle_25.png').convert_alpha()

tower_full_health = pygame.image.load('img/tower/tower_100.png').convert_alpha()
tower_half_health = pygame.image.load('img/tower/tower_50.png').convert_alpha()
tower_quarter_health = pygame.image.load('img/tower/tower_25.png').convert_alpha()

bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
bullet_width = bullet_img.get_width()
bullet_height = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(bullet_width * 0.075), int(bullet_height * 0.075)))

# load enemy images
enemy_animations = []
enemy_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin']
enemy_health = [75, 100, 125, 150]

animation_types = ['walk', 'attack', 'death']
for enemy in enemy_types:
    # load animations
    animation_list = []
    for animation in animation_types:
        # reset temp list of images
        temp_list = []
        num_of_frames = 20
        for i in range(num_of_frames):
            img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
            enemy_width = img.get_width()
            enemy_height = img.get_height()
            img = pygame.transform.scale(img, (int(enemy_width * 0.2), int(enemy_height * 0.2)))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

# button images
# repair image
repair_img = pygame.image.load('img/repair.png').convert_alpha()
# armor image
armor_img = pygame.image.load('img/armour.png').convert_alpha()


# funtion for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# funtion to show player stats
def show_info():
    draw_text('Money: ' + str(castle.money), font, GREY, 10, 10)
    draw_text('Score: ' + str(castle.score), font, GREY, 180, 10)
    draw_text('High Score: ' + str(high_score), font, GREY, 180, 30)
    draw_text('Level: ' + str(level), font, GREY, SCREEN_WIDTH // 2, 10)
    draw_text('Health: ' + str(castle.health) + " / " + str(castle.max_health), font, GREY, SCREEN_WIDTH - 230,
              SCREEN_HEIGHT - 50)
    draw_text('1000', font, GREY, SCREEN_WIDTH - 220, 60)
    draw_text(str(TOWER_COST), font, GREY, SCREEN_WIDTH - 150, 60)
    draw_text('500', font, GREY, SCREEN_WIDTH - 70, 60)


# castle class
class Castle:
    def __init__(self, image100, image50, image25, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        self.money = 0
        self.score = 0

        width = castle_full_health.get_width()
        height = castle_full_health.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        # retrieves coordinates of mouse position
        pos = pygame.mouse.get_pos()
        x_distance = pos[0] - self.rect.midleft[0]
        y_distance = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_distance, x_distance))
        # get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired is False and pos[1] > 70:
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)
        # reset mouseclick
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

    def draw(self):
        # check which castle image to use based on current health
        if self.health >= 500:
            self.image = self.image100
        elif self.health >= 250:
            self.image = self.image50
        else:
            self.image = self.image25

        screen.blit(self.image, self.rect)

    def repair(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.health += 500
            self.money -= 1000
            if castle.health > castle.max_health:
                castle.health = castle.max_health

    def armor(self):
        if self.money >= 500:
            self.max_health += 250
            self.money -= 500


# tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self, image100, image50, image25, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.got_target = False
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
        self.image = self.image100
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, enemy_group):
        self.got_target = False
        for e in enemy_group:
            if e.alive:
                target_x, target_y = e.rect.midright
                self.got_target = True
                break

        if self.got_target:
            x_distance = target_x - self.rect.midleft[0]
            y_distance = -(target_y - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_distance, x_distance))

            shot_cooldown = 1000
            # fire bullet
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                self.last_shot = pygame.time.get_ticks()
                bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)

        if castle.health >= 500:
            self.image = self.image100
        elif castle.health >= 250:
            self.image = self.image50
        else:
            self.image = self.image25


#  bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)  # converts input angle into radians
        self.speed = 10
        # calculate the horizontal and vertical speeds based on angle
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        # check if bullet has gone off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        # move bullets
        self.rect.x += self.dx
        self.rect.y += self.dy


class Crosshair:
    def __init__(self, scale):
        image = pygame.image.load('img/crosshair.png').convert_alpha()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # hide mouse
        pygame.mouse.set_visible(False)

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)


castle = Castle(castle_full_health, castle_half_health, castle_quarter_health, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300,
                0.2)

# create crosshair
crosshair = Crosshair(0.025)

# create buttons
repair_button = button.Button(SCREEN_WIDTH - 220, 10, repair_img, .5)
tower_button = button.Button(SCREEN_WIDTH - 140, 10, tower_full_health, .1)
armor_button = button.Button(SCREEN_WIDTH - 75, 10, armor_img, 1.4)

# create groups
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# game loop
run = True
tower_added = False
while run:

    clock.tick(FPS)
    if not game_over:

        screen.blit(back_ground, (0, 0))

        # draw castle
        castle.draw()
        castle.shoot()
        # draw towers
        tower_group.draw(screen)
        tower_group.update(enemy_group)

        # draw crosshair
        crosshair.draw()

        # draw bullets
        bullet_group.update()
        bullet_group.draw(screen)

        # draw enemy
        enemy_group.update(screen, castle, bullet_group)

        # show player stats
        show_info()

        # draw buttons
        if repair_button.draw(screen):
            castle.repair()
        if tower_button.draw(screen):
            # check if there is enough money for tower
            if castle.money >= TOWER_COST and len(
                    tower_group) < max_towers:  # limit on how many towers a player can build
                tower = Tower(
                    tower_full_health,
                    tower_half_health,
                    tower_quarter_health,
                    tower_positions[len(tower_group)][0],  # checks to see how many towers are placed so game knows
                    tower_positions[len(tower_group)][1],  # where the next tower should be built
                    0.2
                )
                tower_group.add(tower)
                castle.money -= TOWER_COST
                tower_added = True
        if armor_button.draw(screen):
            castle.armor()

        # create enemies
        # check if max number of enemies have been reached
        if level_difficulty < target_difficulty:
            if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
                # creating enemies
                e = random.randint(0, len(enemy_types) - 1)
                enemy = Enemy(enemy_health[e], enemy_animations[e], -100, SCREEN_HEIGHT - 100, 1)
                enemy_group.add(enemy)
                # reset enemy timer
                last_enemy = pygame.time.get_ticks()
                # increase level difficulty by enemy health
                level_difficulty += enemy_health[e]

        # check if all enemies have been created
        if level_difficulty >= target_difficulty:
            # check how many enemies are still alive
            enemies_alive = 0
            for e in enemy_group:
                if e.alive:
                    enemies_alive += 1
            # if no more enemies alive then level complete
            if enemies_alive == 0 and next_level == False:
                next_level = True
                level_reset_time = pygame.time.get_ticks()

        # move to next level
        if next_level:
            draw_text('LEVEL COMPLETE', font60, WHITE, 200, 300)
            # update high score
            if castle.score > high_score:
                high_score = castle.score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            if pygame.time.get_ticks() - level_reset_time > 1500:
                next_level = False
                level += 1
                last_enemy = pygame.time.get_ticks()
                target_difficulty *= DIFFICULTY_MULTIPLIER
                level_difficulty = 0
                enemy_group.empty()

        # check game over
        if castle.health <= 0:
            game_over = True

    else:
        draw_text("GAME OVER!", font, GREY, 300, 300)
        draw_text("Press 'SPACE' TO PLAY AGAIN!", font, GREY, 250, 360)
        pygame.mouse.set_visible(True)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # reset variables
            game_over = False
            level = 1
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            tower_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.money = 0
            pygame.mouse.set_visible(False)



    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.update()
pygame.quit()
