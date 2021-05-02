import pygame
from random import *

# Small
class SmallEnemy(pygame.sprite.Sprite):
    energy = 2

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        # get window's size: width and height
        self.width, self.height = bg_size[0], bg_size[1]
        # set plane speed
        self.speed = 2

        self.rect.left = randint(0, (self.width - self.rect.width))
        self.rect.top = randint(-5 * self.rect.height, -5)

        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("images/enemy1_down1.png").convert_alpha(),
        pygame.image.load("images/enemy1_down2.png").convert_alpha(),
        pygame.image.load("images/enemy1_down3.png").convert_alpha(),
        pygame.image.load("images/enemy1_down4.png").convert_alpha()])

        self.mask = pygame.mask.from_surface(self.image)
        self.active = True

        self.energy = SmallEnemy.energy
        self.hit = False


    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left = randint(0, (self.width - self.rect.width))
        self.rect.top = randint(-5 * self.rect.height, -5)
        self.active = True
        self.hit = False
        self.energy = SmallEnemy.energy


# Medium
class MediumEnemy(pygame.sprite.Sprite):
    energy = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1

        self.rect.left = randint(0, (self.width - self.rect.width))
        self.rect.top = randint(-10 * self.rect.height, -10)
    
        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("images/enemy2_down1.png").convert_alpha(),
        pygame.image.load("images/enemy2_down2.png").convert_alpha(),
        pygame.image.load("images/enemy2_down3.png").convert_alpha(),
        pygame.image.load("images/enemy2_down4.png").convert_alpha()])

        self.mask = pygame.mask.from_surface(self.image)
        self.active = True

        self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.energy = MediumEnemy.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left = randint(0, (self.width - self.rect.width))
        self.rect.top = randint(-10 * self.rect.height, -10)
        self.active = True
        self.hit = False
        self.energy = MediumEnemy.energy

# Large
class LargeEnemy(pygame.sprite.Sprite):
    energy = 15

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1

        self.rect.left = randint(0, (self.width - self.rect.width))
        self.rect.top = randint(-10 * self.rect.height, -10)

        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("images/enemy3_down1.png").convert_alpha(),
        pygame.image.load("images/enemy3_down2.png").convert_alpha(),
        pygame.image.load("images/enemy3_down3.png").convert_alpha(),
        pygame.image.load("images/enemy3_down4.png").convert_alpha(),
        pygame.image.load("images/enemy3_down5.png").convert_alpha(),
        pygame.image.load("images/enemy3_down6.png").convert_alpha()])


        self.mask = pygame.mask.from_surface(self.image1)
        self.active = True

        self.energy = LargeEnemy.energy
        self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        self.hit = False
    
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left = randint(0, (self.width - self.rect.width))
        self.rect.top = randint(-10 * self.rect.height, -10)
        self.active = True
        self.hit = False
        self.energy = LargeEnemy.energy