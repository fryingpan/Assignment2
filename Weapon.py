'''
Assignment 2
Fryingpan
Carla Castro
Mary Yen
Katie Chang
Josh Holstein
'''

import pygame as PG
from pygame.locals import *
import sys
import pygame.mixer as PM
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI

PG.init()

class Weapon(PS.Sprite):

        WIDTH = 80
        HEIGHT = 20

        def __init__(self):
                # Call the parent class (Sprite) constructor
                PS.Sprite.__init__(self)
                self.image = PI.load("swordtest.png").convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.x = 100
                self.rect.y = 1150

        def get_coordinates(self):
                coordinates = [self.rect.x, self.rect.y]
                return coordinates

        #so in player, just like holding down r key makes character move r,
        #only when space bar is held is the sword out. so in player is where maybe
        #the weapon will be 'hidden' after space is let go
        def attack(self, playerX, playerY, playerFace, screen, bg): #this bg is enemy block group
                #collisions with the new weapon rect!
                score = 0
                if "r" in playerFace:
                    self.rect.x = playerX+100
                    self.rect.y = playerY+50
                elif "l" in playerFace:
                    self.rect.x = playerX
                    self.rect.y = playerY+50
                elif "u" in playerFace:
                    self.rect.x = playerX+50
                    self.rect.y = playerY
                elif "d" in playerFace:
                    self.rect.x = playerX+50
                    self.rect.y = playerY+100
                else:
                    self.rect.x = playerX
                    self.rect.y = playerY
                self.draw(screen)

                collisions = PS.spritecollide(self, bg, False)
                for collision in collisions:
                    score = score + 1
                    collision.kill()
                return score #to be added to Player's score

       ''' def update_image(self, imageArray):
                try:
                        self.image = imageArray[self.frame].convert_alpha()
                except IndexError:
                        self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()
                        self.face = list(self.face)[0]'''

    #call in Player.py. pass it screen.
        def draw(self, screen):
                """ Draw on surface """
                self.check_boundary(screen)
                # blit yourself at your current position
                screen.blit(self.image, (self.rect.x, self.rect.y))
                PD.flip()


