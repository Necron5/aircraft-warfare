# import

import pygame

# class of MyPlane (child class) is inherited from pygame.sprite.Sprite(parent class) 
class MyPlane(pygame.sprite.Sprite):
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("images/me2.png").convert_alpha()
        self.rect = self.image1.get_rect()
        # get window's size: width and height
        self.width, self.height = bg_size[0], bg_size[1]
        # calculate play object's position
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = self.height - self.rect.height - 60
        # set plane speed
        self.speed = 10

        self.destroy_images = []
        self.destroy_images.extend([pygame.image.load("images/me_destroy_1.png").convert_alpha(), 
        pygame.image.load("images/me_destroy_2.png").convert_alpha(),
        pygame.image.load("images/me_destroy_3.png").convert_alpha(),
        pygame.image.load("images/me_destroy_4.png").convert_alpha()])
        
        self.mask = pygame.mask.from_surface(self.image1)
        self.active = True
        self.invincible = False

        
        
    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = self.height - self.rect.height - 60
        self.active = True
        self.invincible = True