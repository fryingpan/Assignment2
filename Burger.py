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
from Item import LettuceDrop
from Item import MeatDrop
from Item import BurgerDrop

class Burger(Enemy):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, xlocation, ylocation,fps=1):
        ######unique attributes parent class doesn't have
        self.enemy_ID = 2  # icecream ID
        self.image = PI.load("FPGraphics/burger/burgerFront.png") \
            .convert_alpha()
        self.front_image = self.image
        #######
        #attributes to be passed to parent for parent function use
        self.health = 3
        self.speed = 1
        self.rect = self.image.get_rect()
        self.rect.x = xlocation
        self.rect.y = ylocation

        self.IMAGES_RIGHT = []
        self.IMAGES_LEFT = []
        self.IMAGES_FRONT = []
        self.IMAGES_BACK = []
        self.load_images()
        self.c = 0
        Enemy.__init__(self, self.rect, self.IMAGES_RIGHT, self.IMAGES_LEFT, self.IMAGES_FRONT, self.IMAGES_BACK, self.health, self.speed)
        self.drop_num = 3;

    def attack(self, surface):
        ###
        pass

    def move(self, bg, player, interval):
        ran = random.randint(0,10)
        if(ran < 3): #slow him down cuz he hella scary when he's fast
            dist = int(self.speed)  # distance moved in 1 frame, try changing it to 5
            move_dist = math.ceil(dist*interval)
            if player.sprites()[0].rect.y > self.rect.y:
                self.rect.y += move_dist  # move down
                self.face = 'd'
            else:
                self.rect.y -= move_dist  # move up
                self.face = 'u'
            if player.sprites()[0].rect.x > self.rect.x:
                self.rect.x += move_dist  # move right
                self.face = 'r'
            else:
                self.rect.x -= move_dist  # move left
                self.face = 'l'
        if(self.rect.x <0 and self.c == 0):
            self.c = 1
            print("x " + str(player.sprites()[0].rect.x) + " y " + str(player.sprites()[0].rect.y))

        #print("x " + str(self.rect.x) + " y " + str(self.rect.y))
        self.handle_collision(bg)
        self.handle_collision(player)

    def drop_item(self, surface):
            d = random.randint(0,9)
            if(d == 0):
                return BurgerDrop(self.rect.x, self.rect.y, surface)
            if(d > 0 and d < 4):
                return MeatDrop(self.rect.x, self.rect.y, surface)
            if(d >= 4 and d <7):
                return LettuceDrop(self.rect.x, self.rect.y, surface)
            if(d >= 7):
                return BreadDrop(self.rect.x, self.rect.y, surface)

    def get_face(self):
        return self.face

    def get_ID(self):
        return self.enemy_ID

    def is_alive(self):
        if self.health == 0:
            #then the enemy is dead
            pass

    def load_images(self):
        sheetR = PI.load("FPGraphics/burger/burgerrightWalk.png") \
            .convert_alpha()
        sheetL = PI.load("FPGraphics/burger/burgerleftWalk.png") \
            .convert_alpha()
        sheetF = PI.load("FPGraphics/burger/burgerFrontWalk.png") \
            .convert_alpha()
        sheetB = PI.load("FPGraphics/burger/burgerbackWalk.png") \
            .convert_alpha()
        self.IMAGES_RIGHT = self.load_images_helper(self.IMAGES_RIGHT,
                                                     sheetR)
        self.IMAGES_LEFT = self.load_images_helper(self.IMAGES_LEFT,
                                                    sheetL)
        self.IMAGES_FRONT = self.load_images_helper(self.IMAGES_FRONT,
                                                     sheetF)
        self.IMAGES_BACK = self.load_images_helper(self.IMAGES_BACK,
                                                    sheetB)