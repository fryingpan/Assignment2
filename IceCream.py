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

PG.init()

class IceCream(Enemy):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, fps=1):
        self.image = PI.load("FPGraphics/Food/IceCreamFront.png").convert_alpha()
        self.front_image = self.image
        self.rect = self.image.get_rect()
        self.load_images()
        self.rect.x = 800
        self.rect.y = 1150

        self.speed = 4*fps
        self.direction = random.randint(0, 3)
        #self.angle = random.randint(0, 360) * (math.pi/180)
        self.face = 'u' 
        self.time = 0.0
        self.frame = 0
        self.WIDTH = 100
        self.HEIGHT = 100
        self.enemy_ID = 1 #icecream ID
        
        Enemy.__init__(self, self.rect, self.speed)

        #list of puddles to draw
        self.puddles = []


    def attack(self):
        #create puddle at your location
        new_puddle = Puddle(self.rect)
        self.puddles.append(new_puddle)
        print "added"

    def weapon_update(self, surface):
        for puddle in self.puddles:
            puddle.draw(surface)
            if puddle.count == 0:
                puddle.disapear()
                self.puddles.remove(puddle)
                print "removed"
            # if not puddle.dropped:
            #     puddle.drop_animation()

    def get_face(self):
        return self.face

    def get_ID(self):
        return self.enemy_ID
    
    def is_alive(self):
        if self.health == 0:
            #then the enemy is dead
            pass

    #def attack(self):

    def load_images(self):
        Enemy.IMAGES_RIGHT = []
        Enemy.IMAGES_LEFT = []
        Enemy.IMAGES_FRONT = []
        Enemy.IMAGES_BACK = []
        sheetR = PI.load("FPGraphics/Food/IceCreamWalkRight.png").convert_alpha()
        sheetL = PI.load("FPGraphics/Food/IceCreamWalkLeft.png").convert_alpha()
        sheetF = PI.load("FPGraphics/Food/IceCreamWalkFront.png").convert_alpha()
        sheetB = PI.load("FPGraphics/Food/IceCreamWalkBack.png").convert_alpha()
        Enemy.IMAGES_RIGHT = self.load_images_helper(Enemy.IMAGES_RIGHT, sheetR)
        Enemy.IMAGES_LEFT = self.load_images_helper(Enemy.IMAGES_LEFT, sheetL)
        Enemy.IMAGES_FRONT = self.load_images_helper(Enemy.IMAGES_FRONT, sheetF)
        Enemy.IMAGES_BACK = self.load_images_helper(Enemy.IMAGES_BACK, sheetB)

class Puddle(PS.Sprite):

    IMAGE = None

    def __init__(self, rect):
        PS.Sprite.__init__(self)
        if not Puddle.IMAGE:
            Puddle.IMAGE = PI.load("FPGraphics/Food/testPuddle.png").convert_alpha()
        self.image = Puddle.IMAGE
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.count = 500
        self.dropped = False
        self.disappear = False

    def drop_puddle(self):
        self.drop_animation()

    def drop_animation(self):
        pass

    def draw(self, surface):
        if self.count > 0:
            surface.blit(self.image, (self.x, self.y))
        self.count -= 1        

    def disappear(self):
        pass

