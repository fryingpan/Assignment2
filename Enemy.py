# Assignment 2


import pygame
import sys

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("fbwall.png").convert()
        self.image_rect = self.image.get_rect()
        self.x = 100
        self.y = 100

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        
pygame.init()        
        
        
    
    

