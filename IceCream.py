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



class IceCream(Enemy):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, xlocation, ylocation,fps=1):
        self.image = PI.load("FPGraphics/Food/IceCreamFront.png") \
            .convert_alpha()
        self.front_image = self.image
        self.rect = self.image.get_rect()
        self.load_images()
        self.rect.x = xlocation
        self.rect.y = ylocation

        self.speed = 4*fps
        self.direction = random.randint(0, 3)
        #self.angle = random.randint(0, 360) * (math.pi/180)
        self.face = 'u'
        self.time = 0.0
        self.frame = 0
        self.WIDTH = 100
        self.HEIGHT = 100
        self.enemy_ID = 1  # icecream ID

        Enemy.__init__(self, self.rect, self.speed)


    def attack(self, surface):
        #create puddle at your location
        return Puddle(PG.Rect(self.rect.x+25, self.rect.y+25, 50, 50), surface)

    def get_face(self):
        return self.face

    def get_ID(self):
        return self.enemy_ID

    def is_alive(self):
        if self.health == 0:
            #then the enemy is dead
            pass

    def load_images(self):
        Enemy.IMAGES_RIGHT = []
        Enemy.IMAGES_LEFT = []
        Enemy.IMAGES_FRONT = []
        Enemy.IMAGES_BACK = []
        sheetR = PI.load("FPGraphics/Food/IceCreamWalkRight.png") \
            .convert_alpha()
        sheetL = PI.load("FPGraphics/Food/IceCreamWalkLeft.png") \
            .convert_alpha()
        sheetF = PI.load("FPGraphics/Food/IceCreamWalkFront.png") \
            .convert_alpha()
        sheetB = PI.load("FPGraphics/Food/IceCreamWalkBack.png") \
            .convert_alpha()
        Enemy.IMAGES_RIGHT = self.load_images_helper(Enemy.IMAGES_RIGHT,
                                                     sheetR)
        Enemy.IMAGES_LEFT = self.load_images_helper(Enemy.IMAGES_LEFT,
                                                    sheetL)
        Enemy.IMAGES_FRONT = self.load_images_helper(Enemy.IMAGES_FRONT,
                                                     sheetF)
        Enemy.IMAGES_BACK = self.load_images_helper(Enemy.IMAGES_BACK,
                                                    sheetB)

