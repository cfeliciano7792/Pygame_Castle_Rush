import pygame


# this class inherits pygame built in Sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, surface):

        self.update_animation()
        # draw image on screen
        surface.blit(self.image, self.rect)

    def update_animation(self):
        # define animation cooldown - How many milliseconds need to pass before moving to the next image
        ANIMATION_COOLDOWN = 50
        # update image based on current action
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
