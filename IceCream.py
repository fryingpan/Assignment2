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
        self.image = PI.load("FPGraphics/Food/IceCreamFront.png") \
            .convert_alpha()
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
        self.enemy_ID = 1  # icecream ID

        Enemy.__init__(self, self.rect, self.speed)

        #list of puddles to draw
        self.puddles = []
        self.weapon_attack = False
        self.stages = [1, 2, 3]

    def attack(self):
        #create puddle at your location
        new_puddle = Puddle(PG.Rect(self.rect.x, self.rect.y, 100, 100))
        self.puddles.append(new_puddle)

    def weapon_update(self, surface, player_group):
        self.weapon_attack = False
        for puddle in self.puddles:
            if not puddle.dropped:
                puddle.drop_animation()
                puddle.draw(surface, False)
            elif puddle.count <= 70:
                puddle.disappear_animation()
                if not puddle.disappear:
                    puddle.draw(surface, False)
                else:
                    self.puddles.remove(puddle)
            else:
                puddle.draw(surface, True)
            collisions = puddle.handle_collisions(player_group)
            if len(collisions) > 0:
                self.weapon_attack = True

    def get_weapon_attack(self):
        return self.weapon_attack

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


class Puddle(PS.Sprite):

    IMAGE = None
    IMAGES_APPEAR = None
    IMAGES_DISAPPEAR = None

    def __init__(self, rect):
        PS.Sprite.__init__(self)
        if not Puddle.IMAGE:
            Puddle.IMAGE = PI.load("FPGraphics/Food/IceCreamPuddle.png") \
                .convert_alpha()
        self.static_image = Puddle.IMAGE
        self.image = self.static_image
        self.load_images()
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.count = 500
        self.dropped = False
        self.disappear = False
        self.set_anim_start()
        self.num_frames = 3

    def handle_collisions(self, player_group):
        return PS.spritecollide(self, player_group, False)

    def set_anim_start(self):
        self.frame_num = 0
        self.frame_count = 12

    def drop_animation(self):
        if not self.dropped:
            self.update_anim(self.IMAGES_APPEAR, self.frame_num)
            if self.frame_count == 0 and self.frame_num < self.num_frames:
                self.frame_num += 1
                self.frame_count = 12
            elif self.frame_count > 0:
                self.frame_count -= 1
            else:
                self.dropped = True
                self.set_anim_start()
        self.count -= 1

    def draw(self, surface, static_image):
        if self.count > 0:
            if static_image:
                surface.blit(self.static_image, (self.x, self.y))
            else:
                surface.blit(self.image, (self.x, self.y))
        self.count -= 1

    def disappear_animation(self):
        if not self.disappear:
            self.update_anim(self.IMAGES_DISAPPEAR, self.frame_num)
            if self.frame_count == 0 and self.frame_num < self.num_frames:
                self.frame_num += 1
                self.frame_count = 12
            elif self.frame_count > 0:
                self.frame_count -= 1
                self.count -= 1
            else:
                self.disappear = True

    def update_anim(self, imageArray, index):
        try:
            self.image = imageArray[index].convert_alpha()
        except IndexError:
            pass
            # self.image = self.static_image.convert_alpha()
            # self.face = list(self.face)[0]

    def load_images(self):
        Puddle.IMAGES_APPEAR = []
        Puddle.IMAGES_DISAPPEAR = []
        sheetA = PI.load("FPGraphics/Food/IceCreamPuddleDrop.png") \
            .convert_alpha()
        sheetD = PI.load("FPGraphics/Food/IceCreamPuddleDry.png") \
            .convert_alpha()
        Puddle.IMAGES_APPEAR = self.load_images_helper(
            Puddle.IMAGES_APPEAR, sheetA)
        Puddle.IMAGES_DISAPPEAR = self.load_images_helper(
            Puddle.IMAGES_DISAPPEAR, sheetD)

    def load_images_helper(self, imageArray, sheet):
        #key = sheet.get_at((0,0))
        #hereeeeee
        alphabg = (23, 23, 23)
        for i in range(0, 3):
            surface = PG.Surface((100, 100))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        return imageArray
