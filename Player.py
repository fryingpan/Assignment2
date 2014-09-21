# Assignment 2

import pygame
import sys
import pygame.mixer as PM

pygame.init()

#loading sound
PM.music.load("hitWall.mod")

class Player(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("FPGraphics/MC/MCFront.png").convert_alpha()
        self.image_rect = self.image.get_rect()
        self.speed = 1
        self.x = 0
        self.y = 0
        self.face = 'd'

    def get_face(self):
        return self.face

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = self.speed # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_DOWN]: # down key
            self.y += dist # move down
            self.image = pygame.image.load("FPGraphics/MC/MCFront.png").convert_alpha()
            self.face = 'd'
        elif key[pygame.K_UP]: # up key
            self.y -= dist # move up
            self.image = pygame.image.load("FPGraphics/MC/MCBack.png").convert_alpha()
            self.face = 'u'
        if key[pygame.K_RIGHT]: # right key
            self.x += dist # move right
            self.image = pygame.image.load("FPGraphics/MC/MCRight.png").convert_alpha()
            self.face = 'r'
        elif key[pygame.K_LEFT]: # left key
            self.x -= dist # move left
            self.image = pygame.image.load("FPGraphics/MC/MCLeft.png").convert_alpha()
            self.face = 'l'

    def draw(self, screen):
        """ Draw on surface """
        self.check_boundary(screen)
        # blit yourself at your current position
        screen.blit(self.image, (self.x, self.y))

    def check_boundary(self, screen):
        if self.x < 0:
            PM.music.stop()
            self.x = 0
            PM.music.play(0)
            PM.music.fadeout(4500)
        elif self.x > (screen.get_width() - self.image.get_width()):
            PM.music.stop()
            self.x = screen.get_width() - self.image.get_width()
            PM.music.play(0)
            PM.music.fadeout(4500)
        if self.y < 0:
            PM.music.stop()
            self.y = 0
            PM.music.play(0)
            PM.music.fadeout(4500)
        elif self.y > (screen.get_height() - self.image.get_height()):
            PM.music.stop()
            self.y = (screen.get_height() - self.image.get_height())
            PM.music.play(0)
            PM.music.fadeout(4500)
        
        
        
