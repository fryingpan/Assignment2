# Assignment 2

import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
from Player import Player
from Enemy import Enemy
from Trap import Puddle
from Item import BreadDrop
from Item import MeatDrop
from Item import BurgerDrop
from projectile import Projectile
from projectile import CreamCutter

class Cupcake(Enemy):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, xlocation, ylocation, fps=1):
        ######unique attributes parent class doesn't have
        self.enemy_ID = 3
        self.image = PI.load("FPGraphics/cupcake/cupcake.png") \
            .convert_alpha()
        self.front_image = self.image
        #######
        #attributes to be passed to parent for parent function use
        self.health = 3
        self.rect = self.image.get_rect()
        self.rect.x = xlocation
        self.rect.y = ylocation
        self.pdx = 0
        self.xchange  = random.randint(0, 3)
        self.pdy = 1

        self.IMAGES_RIGHT = []
        self.IMAGES_LEFT = []
        self.IMAGES_FRONT = []
        self.IMAGES_BACK = []
        self.load_images()
        Enemy.__init__(self, self.rect, self.IMAGES_RIGHT,
                       self.IMAGES_LEFT, self.IMAGES_FRONT,
                       self.IMAGES_BACK, self.health)
        self.drop_num = 3

    def attack(self):
        self.xchange += 1
        self.pdx = self.xchange % 3
        self.pdx = self.pdx*-1
        return CreamCutter(self,self)

    def move(self, player, interval):
        #stationary character; make it face diff ways?
        pass

    def drop_item(self, surface):
        return BreadDrop(self.rect.x, self.rect.y, surface)
    
    def get_face(self):
        return self.face

    def get_ID(self):
        return self.enemy_ID

    def is_alive(self):
        if self.health <= 0:
            #then the enemy is dead
            pass

    def load_images(self):
        sheetB = PI.load("FPGraphics/cupcake/cupcakeFrontAn.png") \
            .convert_alpha()
        self.IMAGES_BACK = self.load_images_helper(self.IMAGES_BACK,
                                                   sheetB)
