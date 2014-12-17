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
#from Item import EggDrop
from projectile import Projectile
from projectile import LettuceCutter
import Globals

class Egg(Enemy):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, xlocation, ylocation, level, fps=1):
        ######unique attributes parent class doesn't have
        self.enemy_ID = 5  # icecream ID
        self.image = PI.load("FPGraphics/emptyImg.png") \
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
        pass

    def move(self, player, interval):
        ran = random.randint(0, 10)
        move_dist = 0
        
        dist = int(self.speed)
        # distance moved in 1 frame, try changing it to 5
        move_dist = math.ceil(dist*interval)


        if(ran < 3):  # slow him down cuz he hella scary when he's fast
            if(random.randint(0, 200) == 0):
                self.direction = random.randint(0, 5)
            # distance moved in 1 frame, try changing it to 5
            if (self.direction == 0):  # down key
                self.rect.y += move_dist  # move down
                self.face = 'd'
            elif (self.direction == 1):  # up key
                self.rect.y -= move_dist  # move up
                self.face = 'u'
            elif (self.direction == 2):  # right key
                self.rect.x += move_dist  # move right
                self.face = 'r'
            elif (self.direction == 3):  # left key
                self.rect.x -= move_dist  # move left
                self.face = 'l'

    def drop_item(self, surface):
#        return EggDrop(self.rect.x, self.rect.y, surface)
        pass


    def get_face(self):
        return self.face

    def get_ID(self):
        return self.enemy_ID

    def is_alive(self):
        if self.health <= 0:
            #then the enemy is dead
            pass

    def load_images(self):
        sheetR = PI.load("FPGraphics/egg/eggRightWalk.png") \
            .convert_alpha()
        sheetL = PI.load("FPGraphics/egg/eggLeftWalk.png") \
            .convert_alpha()
        sheetF = PI.load("FPGraphics/egg/eggFrontWalk.png") \
            .convert_alpha()
        sheetB = PI.load("FPGraphics/egg/eggBackWalk.png") \
            .convert_alpha()
        self.IMAGES_RIGHT = self.load_images_helper(self.IMAGES_RIGHT,
                                                    sheetR)
        self.IMAGES_LEFT = self.load_images_helper(self.IMAGES_LEFT,
                                                   sheetL)
        self.IMAGES_FRONT = self.load_images_helper(self.IMAGES_FRONT,
                                                    sheetF)
        self.IMAGES_BACK = self.load_images_helper(self.IMAGES_BACK,
                                                   sheetB)
