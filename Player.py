# Assignment 2

import pygame
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("FPGraphics/MC/MCFront.png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.velocity = 3
        self.x = 0
        self.y = 0

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 1 # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_DOWN]: # down key
            self.y += dist # move down
            self.image = pygame.image.load("FPGraphics/MC/MCFront.png").convert_alpha()
        elif key[pygame.K_UP]: # up key
            self.y -= dist # move up
            self.image = pygame.image.load("FPGraphics/MC/MCBack.png").convert_alpha()
        if key[pygame.K_RIGHT]: # right key
            self.x += dist # move right
            self.image = pygame.image.load("FPGraphics/MC/MCRight.png").convert_alpha()
        elif key[pygame.K_LEFT]: # left key
            self.x -= dist # move left
            self.image = pygame.image.load("FPGraphics/MC/MCLeft.png").convert_alpha()

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        
pygame.init()        
        
        
