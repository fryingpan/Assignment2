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
from Item import IceCreamScoop


class IceCream(Enemy):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, xlocation, ylocation, fps=1):
        ######unique attributes parent class doesn't have
        self.enemy_ID = 1  # icecream ID
        self.image = PI.load("FPGraphics/Food/IceCreamFront.png") \
            .convert_alpha()
        self.front_image = self.image
        #######
        #attributes to be passed to parent for parent function use
        self.health = 1
        self.speed = 1*fps
        self.rect = self.image.get_rect()
        self.rect.x = xlocation
        self.rect.y = ylocation

        self.IMAGES_RIGHT = []
        self.IMAGES_LEFT = []
        self.IMAGES_FRONT = []
        self.IMAGES_BACK = []
        self.load_images()
        Enemy.__init__(self, self.rect, self.IMAGES_RIGHT,
                       self.IMAGES_LEFT, self.IMAGES_FRONT,
                       self.IMAGES_BACK, self.health, self.speed)

    # def drop_item(self):
    #     return IceCreamScoop(self.rect.x, self.rect.y, self.enemy_ID)

    def attack(self, surface):
        #create puddle at your location
        return Puddle(PG.Rect(self.rect.x+25, self.rect.y+25, 50, 50), surface)

    def move(self, player, interval):
        if(random.randint(0, 200) == 0):
            self.direction = random.randint(0, 5)
        dist = int(self.speed)
        # distance moved in 1 frame, try changing it to 5
        if self.direction == 0:  # down key
            self.rect.y += int(dist)  # move down
            self.face = 'd'
        elif self.direction == 1:  # up key
            self.rect.y -= int(dist)  # move up
            self.face = 'u'
        elif self.direction == 2:  # right key
            self.rect.x += int(dist)  # move right
            self.face = 'r'
        elif self.direction == 3:  # left key
            self.rect.x -= int(dist)  # move left
            self.face = 'l'

    def drop_item(self, surface):
        return IceCreamScoop(self.rect.x, self.rect.y, surface)

    def get_face(self):
        return self.face

    def get_ID(self):
        return self.enemy_ID

    def is_alive(self):
        if self.health == 0:
            #then the enemy is dead
            pass

    def load_images(self):
        sheetR = PI.load("FPGraphics/Food/IceCreamWalkRight.png") \
            .convert_alpha()
        sheetL = PI.load("FPGraphics/Food/IceCreamWalkLeft.png") \
            .convert_alpha()
        sheetF = PI.load("FPGraphics/Food/IceCreamWalkFront.png") \
            .convert_alpha()
        sheetB = PI.load("FPGraphics/Food/IceCreamWalkBack.png") \
            .convert_alpha()
        self.IMAGES_RIGHT = self.load_images_helper(self.IMAGES_RIGHT,
                                                    sheetR)
        self.IMAGES_LEFT = self.load_images_helper(self.IMAGES_LEFT,
                                                   sheetL)
        self.IMAGES_FRONT = self.load_images_helper(self.IMAGES_FRONT,
                                                    sheetF)
        self.IMAGES_BACK = self.load_images_helper(self.IMAGES_BACK,
                                                   sheetB)
