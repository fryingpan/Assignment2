'''
Team: fryingpan
author: Carla, Mary, Katie
edited: Carla, Mary, Katie
'''
import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
from Player import Player
import Globals


class Enemy(PG.sprite.DirtySprite):
    # Class variables
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']
    CYCLE = .6

    def __init__(self, rect, r, l, f, b, health=1):
        # Call the parent class (Sprite) constructor
        PG.sprite.DirtySprite.__init__(self)
        # take attributes from derived class
        self.rect = rect
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.health = health
        self.IMAGES_RIGHT = r
        self.IMAGES_LEFT = l
        self.IMAGES_FRONT = f
        self.IMAGES_BACK = b
        self.WIDTH = rect.width
        self.HEIGHT = rect.height
        self.direction = random.randint(0, 3)
        self.face = 'u'
        self.time = 0.0
        self.frame = 0
        # Globals.INVINCIBILITY_COUNT = 0
        self.attacked_player = False
        self.last_hit = 0
        self.last_hit_save = -1

    def get_rect(self):
        return self.rect

    def get_face(self):
        return self.face

    def get_last_hit(self):
        return self.last_hit

    def get_attacked_player(self):
        return self.attacked_player

    def decrement_health(self, dmg):
        # print(self.last_hit)
        self.health -= dmg
        if(self.health == 0):
            Globals.SCORE += 1  # change num of points per type of enemy?
            self.kill()
        # print("health " + str(self.health))

    def move_back(self, face, bg):
        dist = 60
        moved = 0
        collided = False
        while moved < dist and not collided:
            if 'u' in face:
                self.rect.y -= 15
                moved += 15
            elif 'd' in face:
                self.rect.y += 15
                moved += 15
            elif 'r' in face:
                self.rect.x += 15
                moved += 15
            elif 'l' in face:
                self.rect.x -= 15
                moved += 15
            collided = self.handle_collision(bg)


    ##only used by ice cream?
    def will_attack(self, level):
        if level == 2:  # if in hot level, more often
            attack_prob = random.randint(0, 75)
            if attack_prob == 1:
                return True
        if level == 3:  # in cold level
            attack_prob = random.randint(0, 1000)
            if attack_prob == 1:
                return True
        attack_prob = random.randint(0, 600)
        if (attack_prob == 1):
            return True
        return False

    def handle_player(self, player):
        collisions = PS.spritecollide(self, player, False)
        if(len(collisions) == 1 and isinstance(collisions[0], Player)):
            if(Globals.INVINCIBILITY_COUNT <= 0):
                self.attacked_player = True
                # Globals.INVINCIBILITY_COUNT = 200

    def handle_collision(self, bg):
        collisions = PS.spritecollide(self, bg, False)
        if self.face == 'r':
            for collision in collisions:
                if(self.rect.x +
                   self.rect.width) >= collision.rect.left:
                    self.rect.x = collision.rect.left - self.rect.width
        elif self.face == 'l':
            for collision in collisions:
                if (self.rect.x) <= (collision.rect.left +
                                     collision.rect.width):
                    self.rect.x = collision.rect.left + \
                        collision.rect.width
        elif self.face == 'd':
            for collision in collisions:
                if(self.rect.y +
                   self.rect.height) >= collision.rect.top:
                    self.rect.y = collision.rect.top - self.rect.height
        elif self.face == 'u':
            for collision in collisions:
                if (self.rect.y <= (collision.rect.top +
                                    collision.rect.height)):
                    self.rect.y = collision.rect.top + \
                        collision.rect.height
        return (collisions is None)

    def update(self, bg, player):
        self.attacked_player = False
        self.move(player, Globals.DELTA)
        self.handle_collision(bg)
        self.handle_player(player)
            # print("invisib " + str(Globals.INVINCIBILITY_COUNT))
        # check that the new movement is within the boundaries
        # if self.check_collide() is True:
        # self.direction = random.randint(0, 1)
        # self.angle = random.randint(0, 360) * (math.pi/180)

        ENEMY_IMAGE_LENGTH = 4  # all Enemy sprite has 12 frames
        # update time
        self.time = self.time + Globals.DELTA
        if self.time > Enemy.CYCLE:
            self.time = 0.0
        # update frame?
        frame = int(self.time / (Enemy.CYCLE / ENEMY_IMAGE_LENGTH))
        if frame != self.frame:
                self.frame = frame
                if (self.face == 'r'):
                    self.update_image(self.IMAGES_RIGHT)
                elif (self.face == 'u'):
                    self.update_image(self.IMAGES_BACK)
                elif (self.face == 'l'):
                    self.update_image(self.IMAGES_LEFT)
                elif (self.face == 'd'):
                    self.update_image(self.IMAGES_FRONT)
                elif(self.face == 'rs'):
                    self.image = self.IMAGES_RIGHT[0]
                elif(self.face == 'us'):
                    self.image = self.IMAGES_BACK[0]
                elif(self.face == 'ls'):
                    self.image = self.IMAGES_LEFT[0]
                elif(self.face == 'ds'):
                    self.image = self.IMAGES_FRONT[0]
                else:
                    self.image = self.front_image.convert_alpha()
        self.dirty = 1

    def set_face(self, Enemy_face):
        if Enemy_face == 'u':
            self.update_image(self.IMAGES_FRONT)
            self.face = 'd'
        elif Enemy_face == 'd':
            self.update_image(self.IMAGES_BACK)
            self.face = 'u'
        elif Enemy_face == 'l':
            self.update_image(self.IMAGES_RIGHT)
            self.face = 'r'
        elif Enemy_face == 'r':
            self.update_image(self.IMAGES_LEFT)
            self.face = 'l'
        elif(self.face == 'rs'):
            self.update_image(self.IMAGES_LEFT)
        elif(self.face == 'us'):
            self.update_image(self.IMAGES_FRONT)
        elif(self.face == 'ls'):
            self.update_image(self.IMAGES_RIGHT)
        elif(self.face == 'ds'):
            self.update_image(self.IMAGES_BACK)

    # def draw(self, screen):
    #     """ Draw on surface """
    #     # blit yourself at your current position
    #     screen.blit(self.image, (self.rect.x, self.rect.y))

    # def check_collide(self): #check screen collision
    #     collide = False
    #     if self.rect.x < 50:
    #         self.rect.x = 40
    #         collide = True
    #     elif self.rect.x > (self.swidth - self.WIDTH):
    #         self.rect.x = (self.swidth - self.WIDTH - 40)
    #         collide = True
    #     if self.rect.y < 50:
    #         self.rect.y = 40
    #         collide = True
    #     elif self.rect.y > (self.sheight - self.HEIGHT):
    #         self.rect.y = (self.sheight - self.HEIGHT - 40)
    #         collide = True
    #     return collide

    def load_images_helper(self, imageArray, sheet):
        # key = sheet.get_at((0,0))
        # hereeeeee
        alphabg = (23, 23, 23)
        for i in range(0, 4):
            surface = PG.Surface((100, 100))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        return imageArray

    # this will all end up in the key handler
    def update_image(self, imageArray):
        try:
            self.image = imageArray[self.frame].convert_alpha()
        except IndexError:
            self.image = self.front_image.convert_alpha()
            self.face = list(self.face)[0]
