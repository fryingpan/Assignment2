# Assignment 2

import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
from Player import Player

PG.init()

class Enemy(PG.sprite.Sprite):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, rect, speed=1):
        # Call the parent class (Sprite) constructor
        PG.sprite.Sprite.__init__(self)
        #if not Enemy.IMAGE_UP and not Enemy.IMAGE_DOWN and not Enemy.IMAGE_LEFT and not Enemy.IMAGE_RIGHT:
         #   Enemy.IMAGE_UP = PG.image.load("FPGraphics/Food/IceCreamBack.png").convert_alpha()
          #  Enemy.IMAGE_DOWN = PG.image.load("FPGraphics/Food/IceCreamFront.png").convert_alpha()
           # Enemy.IMAGE_LEFT = PG.image.load("FPGraphics/Food/IceCreamLeft.png").convert_alpha()
           # Enemy.IMAGE_RIGHT = PG.image.load("FPGraphics/Food/IceCreamRight.png").convert_alpha()
        """self.image_up = Enemy.IMAGE_UP
        self.image_down = Enemy.IMAGE_DOWN
        self.image_right = Enemy.IMAGE_RIGHT
        self.image_left = Enemy.IMAGE_LEFT"""
        #self.image = None
        self.image = PI.load("FPGraphics/Food/IceCreamWalkFront.png").convert_alpha()
        self.rect = rect
        self.load_images()
        self.rect.x = rect.x
        self.rect.y = rect.y

        self.speed = speed
        self.direction = random.randint(0, 3)
        #self.angle = random.randint(0, 360) * (math.pi/180)
        self.face = 'u' 
        self.time = 0.0
        self.frame = 0
        self.WIDTH = 100
        self.HEIGHT = 100
        self.count = 0

    def get_face(self):
        return self.face

    def handle_collision(self, bg):
        collisions = PS.spritecollide(self, bg, False)
        if( len(collisions) == 1 and isinstance(collisions[0], Player) ):
            self.count = self.count + 1
            #print("player coll " + str(self.count))
            #print(collisions[0].rect.x)
            #print("enemy right x " + str(self.rect.x) + " y " +str(self.rect.y))
        else:
            if self.face == 'r':
                collisions = PS.spritecollide(self, bg, False)
                once = True
                for collision in collisions:
                    if once:
                        if(self.rect.x + self.rect.width) >= collision.rect.left:
                            self.rect.x = collision.rect.left - self.rect.width
                            once = False
                
            elif self.face == 'l':
                collisions = PS.spritecollide(self, bg, False)
                once = True
                for collision in collisions:
                    if once:
                        if (self.rect.x) <= (collision.rect.left + collision.rect.width):
                            self.rect.x = collision.rect.left + collision.rect.width
                            once = False
            elif self.face == 'd':
                once = True
                for collision in collisions:
                    if once:
                        if (self.rect.y + self.rect.height) >= collision.rect.top:
                            self.rect.y = collision.rect.top - self.rect.height
                            once = False
            elif self.face == 'u':
                collisions = PS.spritecollide(self, bg, False)
                once = True
                for collision in collisions:
                    if once:
                        if (self.rect.y <= (collision.rect.top + collision.rect.height)):
                            self.rect.y = collision.rect.top + collision.rect.height
                            once = False
    

    def update(self, bg, player, delta = 1):
        self.speed
        self.move(bg, player, delta)
        #check that the new movement is within the boundaries
        #if self.check_collide() is True:
        #    self.direction = random.randint(0, 1)
         #   self.angle = random.randint(0, 360) * (math.pi/180)

        ENEMY_IMAGE_LENGTH = 4 #all Enemy sprite has 12 frames
        #update time
        self.time = self.time + delta
        if self.time > Enemy.CYCLE:
            self.time = 0.0
        #update frame?
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


    def move(self, bg, player, interval):
        if(random.randint(0,50) == 0):
            self.direction = random.randint(0, 3)
        dist = self.speed # distance moved in 1 frame, try changing it to 5
        self.interval = interval
        move_dist = 1*dist*interval                
        if self.direction == 0: # down key
            self.rect.y += move_dist# move down
            #self.rect = self.image.get_rect()
            self.face = 'd'
            self.handle_collision(bg)
        elif self.direction == 1: # up key
            self.rect.y -= move_dist # move up
            #self.rect = self.image.get_rect()
            self.face = 'u'
            self.handle_collision(bg)
        elif self.direction == 2: # right key
            self.rect.x += move_dist # move right
            #self.rect = self.image.get_rect()
            self.face = 'r'
            self.handle_collision(bg)
        elif self.direction == 3: # left key
            self.rect.x -= move_dist# move left
            #self.rect = self.image.get_rect()
            self.face = 'l'
            self.handle_collision(bg)
        self.handle_collision(player)
        
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

    def draw(self, screen):
        """ Draw on surface """
        # blit yourself at your current position
        screen.blit(self.image, (self.rect.x, self.rect.y))
        PD.flip()

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
        #key = sheet.get_at((0,0))
        #hereeeeee
        alphabg = (23,23,23)
        for i in range(0,4):
            surface = PG.Surface((100, 100))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        return imageArray

    #this will all end up in the key handler
    def update_image(self, imageArray):
        try:
            self.image = imageArray[self.frame].convert_alpha()
        except IndexError:
            self.image = self.front_image.convert_alpha()
            self.face = list(self.face)[0]
