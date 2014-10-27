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

        IMAGE_RIGHT = None
        IMAGE_LEFT = None
        IMAGE_DOWN = None
        IMAGE_UP = None

        def __init__(self):
                # Call the parent class (Sprite) constructor
                PS.Sprite.__init__(self)
                self.image = PI.load("FPGraphics/MC/weapon/FPD.png") \
                    .convert_alpha()
                self.load_images()
                self.rect = self.image.get_rect()
                self.surface = PG.Surface((50, 50))
                alphabg = (23, 23, 23)
                self.surface.set_colorkey(alphabg)
                #self.surface.blit(self.image, (0, 0))
                self.image = self.surface

        def get_coordinates(self):
                coordinates = [self.rect.x, self.rect.y]
                return coordinates

        #so in player, just like holding down r key makes character move r,
        #only when space bar is held is the sword out.
        #so in player is where maybe
        #the weapon will be 'hidden' after space is let go
        def attack(self, playerX, playerY, playerFace, screen, bg):
                #this bg is enemy block group
                #collisions with the new weapon rect!
                score = 0

                if "r" in playerFace:
                    self.width = 50
                    self.height = 15
                    self.surface = PG.Surface((self.width, self.height))
                    self.update_image(self.IMAGE_RIGHT)
                    self.rect.x = playerX+100
                    self.rect.y = playerY+50
                elif "l" in playerFace:
                    self.width = 50
                    self.height = 15
                    self.surface = PG.Surface((self.width, self.height))
                    self.update_image(self.IMAGE_LEFT)
                    self.rect.x = playerX-self.width
                    self.rect.y = playerY+50
                elif "u" in playerFace:
                    self.width = 15
                    self.height = 50
                    self.surface = PG.Surface((self.width, self.height))
                    self.update_image(self.IMAGE_UP)
                    self.rect.x = playerX+50
                    self.rect.y = playerY-self.height
                elif "d" in playerFace:
                    self.width = 15
                    self.height = 50
                    self.surface = PG.Surface((self.width, self.height))
                    self.update_image(self.IMAGE_DOWN)
                    self.rect.x = playerX+50
                    self.rect.y = playerY+100

                collisions = PS.spritecollide(self, bg, False)
                for collision in collisions:
                    score = score + 1
                    collision.kill()
                return score  # to be added to Player's score

        def update_image(self, image):
                self.image = image

    #call in Player.py. pass it screen.
        def draw(self, screen):
                """ Draw on surface """
                # blit yourself at your current position
                screen.blit(self.image, (self.rect.x, self.rect.y))
                PD.flip()

        def load_images(self):
            Weapon.IMAGE_RIGHT = PI.load("FPGraphics/MC/weapon/FPR.png") \
                .convert_alpha()
            Weapon.IMAGE_LEFT = PI.load("FPGraphics/MC/weapon/FPL.png") \
                .convert_alpha()
            Weapon.IMAGE_DOWN = PI.load("FPGraphics/MC/weapon/FPD.png") \
                .convert_alpha()
            Weapon.IMAGE_UP = PI.load("FPGraphics/MC/weapon/FPU.png") \
                .convert_alpha()
