# Assignment 2

import random
import pygame as PG
import pygame.display as PD
import sys
import math
import pygame.image as PI

PG.init()

class Enemy(PG.sprite.Sprite):
    IMAGE_UP = None
    IMAGE_DOWN = None
    IMAGE_RIGHT = None
    IMAGE_LEFT = None
    FACE_STRING = ['u', 'd', 'r', 'l']

    CYCLE = .6

    def __init__(self, screen, speed=1):
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
        self.rect = self.image.get_rect()
        self.load_images()
        self.screen = screen
        self.swidth = screen.get_width()*2
        self.sheight = screen.get_height()*2
        self.rect.x = 100.0
        self.rect.y = 1150.0

        self.speed = speed
        self.direction = random.randint(0, 1)
        self.angle = random.randint(0, 360) * (math.pi/180)
        self.face = 'u' 
        self.time = 0.0
        self.frame = 0
        self.WIDTH = 100.0
        self.HEIGHT = 100.0

    def get_face(self):
        return self.face

    def update(self, delta = 1):
        self.move(delta)
        dist = self.speed
        #check that the new movement is within the boundaries
        if self.check_collide() is True:
            self.direction = random.randint(0, 1)
            self.angle = random.randint(0, 360) * (math.pi/180)

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
                    self.image = PI.load("FPGraphics/Food/IceCreamWalkFront.png").convert_alpha()


    def move(self, interval):
        dist = self.speed
        if self.direction == 0:
            print("angle: " + str(self.angle))
            self.rect.x += 2.0*dist*interval*math.cos(self.angle)
            #print(dist*interval*math.cos(self.angle))
            #print("x " + str(self.rect.x) + " y " + str(self.rect.y))
            self.rect.y -= 2.0*dist*interval*math.sin(self.angle)
            print("x " + str(self.rect.x) + " y " + str(self.rect.y))

        elif self.direction == 1:
            self.rect.x -= 2.0*dist * interval*math.cos(self.angle)
            self.rect.y += 2.0*dist * interval*math.sin(self.angle)
        
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

    def check_collide(self): #check screen collision
        collide = False
        if self.rect.x < 50:
            self.rect.x = 40
            collide = True
        elif self.rect.x > (self.swidth - self.WIDTH):
            self.rect.x = (self.swidth - self.WIDTH - 40)
            collide = True
        if self.rect.y < 50:
            self.rect.y = 40
            collide = True
        elif self.rect.y > (self.sheight - self.HEIGHT):
            self.rect.y = (self.sheight - self.HEIGHT - 40)
            collide = True
        return collide
                
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

    #this will all end up in the key handler
    def update_image(self, imageArray):
        try:
            self.image = imageArray[self.frame].convert_alpha()
        except IndexError:
            self.image = PI.load("FPGraphics/Food/IceCreamWalkFront.png").convert_alpha()
            self.face = list(self.face)[0]
