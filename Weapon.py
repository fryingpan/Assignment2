'''
Assignment 2
Fryingpan
Carla Castro
Mary Yen
Katie Chang
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
                self.imagerl = PI.load("FPGraphics/MC/MCattack/MCRightFPOnePiece.png").convert_alpha()
                self.imageud = PI.load("FPGraphics/MC/MCattack/MCBackPOnePiece.png").convert_alpha()
                self.rectrl = self.imagerl.get_rect()
                self.rectud = self.imageud.get_rect()
                # self.image = PI.load("FPGraphics/MC/weapon/FPD.png") \
                #     .convert_alpha()
                # self.load_images()
                self.surface = PG.Surface((50, 50))
                alphabg = (23, 23, 23)
                self.surface.set_colorkey(alphabg)
                self.image = self.surface

        def get_coordinates(self):
                coordinates = [self.rect.x, self.rect.y]
                return coordinates

        #so in player, just like holding down r key makes character move r,
        #only when space bar is held is the sword out.
        #so in player is where maybe
        #the weapon will be 'hidden' after space is let go
        def attack(self, player, playerX, playerY, playerFace, screen, bg):
                #this bg is enemy block group
                #collisions with the new weapon rect!
                score = 0
                collision_list = []
                if "r" in playerFace:
                    self.rectrl.x = playerX
                    self.rectrl.y = playerY
                    self.rect = self.rectrl
                elif "l" in playerFace:
                    self.rectrl.x = playerX
                    self.rectrl.y = playerY
                    self.rect = self.rectrl
                elif "u" in playerFace:
                    self.rectud.x = playerX
                    self.rectud.y = playerY
                    self.rect = self.rectud
                elif "d" in playerFace:
                    self.rectud.x = playerX
                    self.rectud.y = playerY
                    self.rect = self.rectud

                collisions = PS.spritecollide(self, bg, False)
                for collision in collisions:
                    collision_list.append(collision)
                return collision_list  # to be added to Player's score