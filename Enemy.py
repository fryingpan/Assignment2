# Assignment 2

import random
import pygame
import sys
import math

class Enemy(pygame.sprite.Sprite):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None

    def __init__(self, screen):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        if not Enemy.IMAGE_UP and not Enemy.IMAGE_DOWN and not Enemy.IMAGE_LEFT and not Enemy.IMAGE_RIGHT:
            Enemy.IMAGE_UP = pygame.image.load("FPGraphics/Food/IceCreamBack.png").convert_alpha()
            Enemy.IMAGE_DOWN = pygame.image.load("FPGraphics/Food/IceCreamFront.png").convert_alpha()
            Enemy.IMAGE_LEFT = pygame.image.load("FPGraphics/Food/IceCreamLeft.png").convert_alpha()
            Enemy.IMAGE_RIGHT = pygame.image.load("FPGraphics/Food/IceCreamRight.png").convert_alpha()
        self.image_up = Enemy.IMAGE_UP
        self.image_down = Enemy.IMAGE_DOWN
        self.image_right = Enemy.IMAGE_RIGHT
        self.image_left = Enemy.IMAGE_LEFT
        self.image = None

        self.screen = screen
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.x = random.randint(0, self.swidth - self.image_left.get_width())
        self.y = random.randint(0, self.sheight - self.image_up.get_height())

        self.speed = 1
        self.direction = random.randint(0, 1)
        self.angle = random.randint(0, 360) * (math.pi/180)
        self.face = 'u' 


    def update(self, interval = 1):
        self.speed = interval
        self.move()
        #check that the new movement is within the boundaries
        if self.check_collide() is True:
            self.direction = random.randint(0, 1)
            self.angle = random.randint(0, 360) * (math.pi/180) 


    def move(self):
        dist = self.speed
        if self.direction == 0:
            self.x += dist * math.sin(self.angle)
            self.y -= dist * math.cos(self.angle)
        elif self.direction == 1:
            self.x -= dist * math.sin(self.angle)
            self.y += dist * math.cos(self.angle)
        # elif self.direction == 2:
        #     self.y += dist * math.cos(self.angle)
        # elif self.direction == 3:
        #     self.y -= dist * math.cos(self.angle)

    def set_face(self, player_face):
        if player_face == 'u':
            self.image = self.image_down
        elif player_face == 'd':
            self.image = self.image_up
        elif player_face == 'l':
            self.image = self.image_right
        elif player_face == 'r':
            self.image = self.image_left

    def draw(self):
        """ Draw on surface """
        # blit yourself at your current position
        self.screen.blit(self.image, (self.x, self.y))

    def check_collide(self):
        collide = False
        if self.x < 0:
            self.x = 0
            collide = True
        elif self.x > (self.swidth - self.image_right.get_width()):
            self.x = self.swidth - self.image_right.get_width()
            collide = True
        if self.y < 0:
            self.y = 0
            collide = True
        elif self.y > (self.sheight - self.image_down.get_height()):
            self.y = (self.sheight - self.image_down.get_height())
            collide = True
        return collide
                
        
    
    

