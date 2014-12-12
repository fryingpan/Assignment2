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
from projectile import Projectile
from projectile import LettuceCutter
import Globals

class Burger(Enemy):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, xlocation, ylocation, level, fps=1):
        ######unique attributes parent class doesn't have
        self.enemy_ID = 2  # icecream ID
        self.image = PI.load("FPGraphics/burger/burgerFront.png") \
            .convert_alpha()
        self.front_image = self.image
        self.bound_factor = 2
        #######
        #attributes to be passed to parent for parent function use
        self.health = self.set_health(level)
        self.speed = self.set_speed(level)
        self.rect = self.image.get_rect()
        self.rect.x = xlocation
        self.rect.y = ylocation
        self.xboundl = xlocation - self.rect.width*self.bound_factor
        self.yboundt = ylocation - self.rect.width*self.bound_factor
        self.xboundr = xlocation + self.rect.width*self.bound_factor
        self.yboundb = ylocation + self.rect.width*self.bound_factor
        self.detect_distance = 250
        self.IMAGES_RIGHT = []
        self.IMAGES_LEFT = []
        self.IMAGES_FRONT = []
        self.IMAGES_BACK = []
        self.load_images()
        Enemy.__init__(self, self.rect, self.IMAGES_RIGHT,
                       self.IMAGES_LEFT, self.IMAGES_FRONT,
                       self.IMAGES_BACK, self.health)
        self.drop_num = 3

    ##set health depending on level.
    def set_health(self, level):
        if level == Globals.COLD_LEVEL:  # cold level, more HP
            return 6
        else:  # regular amount otherwise
            return 3

    ##set speed depending on level.
    def set_speed(self, level):
        if level == Globals.HOT_LEVEL:  # hot level, faster
            return 6
        else:
            return 1

    def attack(self):
        self.pdx = random.randint(-1, 1)
        self.pdy = random.randint(-1, 1)
        if(self.pdx == 0 and self.pdy==0):
            self.pdx = 1
        return LettuceCutter(self,self)

    def move(self, player, interval):
        ran = random.randint(0, 10)
        move_dist = 0
        
        dist = int(self.speed)
        # distance moved in 1 frame, try changing it to 5
        move_dist = math.ceil(dist*interval)

        if(player.sprites()[0].rect.y > self.yboundt
        and player.sprites()[0].rect.y < self.yboundb
        and player.sprites()[0].rect.x > self.xboundl
        and player.sprites()[0].rect.x < self.xboundr
        ):
            if(ran < 5):  # slow him down cuz he hella scary when he's fast
                if player.sprites()[0].rect.y > self.rect.y and \
                self.rect.y <= self.yboundb:
                    self.rect.y += move_dist  # move down
                    self.face = 'd'
                elif player.sprites()[0].rect.y < self.rect.y and \
                self.rect.y >= self.yboundt:
                    self.rect.y -= move_dist  # move up
                    self.face = 'u'
                if player.sprites()[0].rect.x > self.rect.x and \
                self.rect.x <= self.xboundr:
                    self.rect.x += move_dist  # move right
                    self.face = 'r'
                elif player.sprites()[0].rect.x < self.rect.x and \
                self.rect.x >= self.xboundl:
                    self.rect.x -= move_dist  # move left
                    self.face = 'l'
        else:
            if(ran < 3):  # slow him down cuz he hella scary when he's fast
                if(random.randint(0, 200) == 0):
                    self.direction = random.randint(0, 5)
                # distance moved in 1 frame, try changing it to 5
                if (self.direction == 0
                and self.rect.y <= self.yboundb):  # down key
                    self.rect.y += move_dist  # move down
                    self.face = 'd'
                elif (self.direction == 1
                and self.rect.y >= self.yboundt):  # up key
                    self.rect.y -= move_dist  # move up
                    self.face = 'u'
                elif (self.direction == 2
                and self.rect.x <= self.xboundr):  # right key
                    self.rect.x += move_dist  # move right
                    self.face = 'r'
                elif (self.direction == 3
                and self.rect.x >= self.xboundl):  # left key
                    self.rect.x -= move_dist  # move left
                    self.face = 'l'


            # if player.sprites()[0].rect.y > self.rect.y and \
            # self.rect.y <= self.yboundb:
            #     self.rect.y += move_dist  # move down
            #     self.face = 'd'
            # elif player.sprites()[0].rect.y < self.rect.y and \
            # self.rect.y >= self.yboundt:
            #     self.rect.y -= move_dist  # move up
            #     self.face = 'u'
            # if player.sprites()[0].rect.x > self.rect.x and \
            # self.rect.x <= self.xboundr:
            #     self.rect.x += move_dist  # move right
            #     self.face = 'r'
            # elif player.sprites()[0].rect.x < self.rect.x and \
            # self.rect.x >= self.xboundl:
            #     self.rect.x -= move_dist  # move left
            #     self.face = 'l'

            # if(player.sprites()[0].rect.y > self.rect.y - self.detect_distance
            #     and player.sprites()[0].rect.y < self.rect.y + self.detect_distance
            #     and player.sprites()[0].rect.x > self.rect.x - self.detect_distance
            #     and player.sprites()[0].rect.x < self.rect.x + self.detect_distance
            #     ):
            #     if player.sprites()[0].rect.y > self.rect.y:
            #         self.rect.y += move_dist  # move down
            #         self.face = 'd'
            #     elif player.sprites()[0].rect.y < self.rect.y:
            #         self.rect.y -= move_dist  # move up
            #         self.face = 'u'
            #     if player.sprites()[0].rect.x > self.rect.x:
            #         self.rect.x += move_dist  # move right
            #         self.face = 'r'
            #     elif player.sprites()[0].rect.x < self.rect.x:
            #         self.rect.x -= move_dist  # move left
            #         self.face = 'l'

    def drop_item(self, surface):
            d = random.randint(0, 9)
            if(d == 0):
                return BurgerDrop(self.rect.x, self.rect.y, surface)
            if(d > 0 and d < 4):
                return MeatDrop(self.rect.x, self.rect.y, surface)
            if(d >= 4 and d < 7):
                return LettuceDrop(self.rect.x, self.rect.y, surface)
            if(d >= 7):
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
