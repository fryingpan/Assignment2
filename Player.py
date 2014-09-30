'''
Assignment 2
Fryingpan
Carla Castro
Mary Yen
Katie Chang
Josh Holstein
'''

import pygame as PG
import sys
import pygame.mixer as PM
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI

PG.init()

#loading sound
PM.music.load("hitWall.mod")

class Player(PS.Sprite):

    IMAGES = None
    IMAGES_RIGHT = None
    IMAGES_LEFT = None
    IMAGES_FRONT = None
    IMAGES_BACK = None
    IMAGES_RIGHT_ACCEL = None
    IMAGES_LEFT_ACCEL = None
    IMAGES_FRONT_ACCEL = None
    IMAGES_BACK_ACCEL = None
    IMAGES_RIGHT_DECEL = None
    IMAGES_LEFT_DECEL = None
    IMAGES_FRONT_DECEL = None
    IMAGES_BACK_DECEL = None
    CYCLE = 0.6
    WIDTH = 100
    HEIGHT = 100

    def __init__(self, speed = 1):
        # Call the parent class (Sprite) constructor
        PS.Sprite.__init__(self)
        self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.x = 0
        self.y = 0
        self.face = 'd'
        self.load_images()
        self.time = 0.0
        self.frame = 0


    def get_face(self):
        return self.face

    def handle_keys(self, interval = 1):
        """ Handles Keys """
        key = PG.key.get_pressed()
        dist = self.speed # distance moved in 1 frame, try changing it to 5
        if key[PG.K_DOWN]: # down key
            self.y += dist*interval# move down
            self.rect = self.image.get_rect()
            self.face = 'd'
        elif key[PG.K_UP]: # up key
            self.y -= dist*interval # move up
            self.rect = self.image.get_rect()
            self.face = 'u'
        elif key[PG.K_RIGHT]: # right key
            self.x += dist*interval # move right
            self.rect = self.image.get_rect()
            self.face = 'r'
        elif key[PG.K_LEFT]: # left key
            self.x -= dist*interval# move left
            self.rect = self.image.get_rect()
            self.face = 'l'
        else: #ds = down 'standing' (not moving)
            if self.face == 'd':
                self.face = 'ds'
            if self.face == 'u':
                self.face = 'us'
            if self.face == 'r':
                self.face = 'rs'
            if self.face == 'l':
                self.face = 'ls'
    def draw(self, screen):
        """ Draw on surface """
        self.check_boundary(screen)
        # blit yourself at your current position
        screen.blit(self.image, (self.x, self.y))
        PD.flip()
        
    def check_boundary(self, screen):
        if self.x < 0:
            PM.music.stop()
            self.x = 0
            PM.music.play(0)
            PM.music.fadeout(4500)
        elif self.x > (screen.get_width() - self.image.get_width()):
            PM.music.stop()
            self.x = screen.get_width() - self.image.get_width()
            PM.music.play(0)
            PM.music.fadeout(4500)
        if self.y < 0:
            PM.music.stop()
            self.y = 0
            PM.music.play(0)
            PM.music.fadeout(4500)
        elif self.y > (screen.get_height() - self.image.get_height()):
            PM.music.stop()
            self.y = (screen.get_height() - self.image.get_height())
            PM.music.play(0)
            PM.music.fadeout(4500)
        
    def update(self, delta):
        PLAYER_IMAGE_LENGTH = 12 #all player sprite has 12 frames
        #update time
        self.time = self.time + delta
        if self.time > Player.CYCLE:
            self.time = 0.0
        #update frame?
        frame = int(self.time / (Player.CYCLE / PLAYER_IMAGE_LENGTH))
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
                    self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()
        """if frame != self.frame:
                self.frame = frame
                if (self.face == 'r'):
                    self.update_image(self.IMAGES_RIGHT)
                elif (self.face == 'u'):
                    self.update_image(self.IMAGES_BACK)
                elif (self.face == 'l'):
                    self.update_image(self.IMAGES_LEFT)
                else:
                    self.update_image(self.IMAGES_FRONT)"""
        """if frame != self.frame:
            print "frame: " + repr(frame)
            self.frame = frame
            self.update_image(Player.IMAGES_FRONT)"""

    def load_images_helper(self, imageArray, sheet):
        #key = sheet.get_at((0,0))
        #hereeeeee
        alphabg = (23,23,23)
        for i in range(3,7):
            surface = PG.Surface((100, 100))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        for i in range(5,0,-1):
            surface = PG.Surface((100, 100))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        for i in range(0,3):
            surface = PG.Surface((100, 100))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        return imageArray

    def load_images(self):
        Player.IMAGES_RIGHT = []
        Player.IMAGES_LEFT = []
        Player.IMAGES_FRONT = []
        Player.IMAGES_BACK = []
        Player.IMAGES_RIGHT_ACCEL = []
        Player.IMAGES_LEFT_ACCEL = []
        Player.IMAGES_FRONT_ACCEL = []
        Player.IMAGES_BACK_ACCEL = []
        Player.IMAGES_RIGHT_DECEL = []
        Player.IMAGES_LEFT_DECEL = []
        Player.IMAGES_FRONT_DECEL = []
        Player.IMAGES_BACK_DECEL = []
        sheetR = PI.load("FPGraphics/MC/MCwalk/MCRightWalk.png").convert_alpha()
        sheetL = PI.load("FPGraphics/MC/MCwalk/MCLeftWalk.png").convert_alpha()
        sheetF = PI.load("FPGraphics/MC/MCwalk/MCFrontWalk.png").convert_alpha()
        sheetB = PI.load("FPGraphics/MC/MCwalk/MCBackWalk.png").convert_alpha()
        '''sheetRA = PI.load("FPGraphics/MC/MCwalk/MCRightWalk.png").convert_alpha()
        sheetLA = PI.load("FPGraphics/MC/MCwalk/MCLeftWalk.png").convert_alpha()
        sheetFA = PI.load("FPGraphics/MC/MCwalk/MCFrontWalk.png").convert_alpha()
        sheetBA = PI.load("FPGraphics/MC/MCwalk/MCBackWalk.png").convert_alpha()
        sheetRD = PI.load("FPGraphics/MC/MCwalk/MCRightWalk.png").convert_alpha()
        sheetLD = PI.load("FPGraphics/MC/MCwalk/MCLeftWalk.png").convert_alpha()
        sheetFD = PI.load("FPGraphics/MC/MCwalk/MCFrontWalk.png").convert_alpha()
        sheetBD = PI.load("FPGraphics/MC/MCwalk/MCBackWalk.png").convert_alpha()'''
        Player.IMAGES_RIGHT = self.load_images_helper(Player.IMAGES_RIGHT, sheetR)
        Player.IMAGES_LEFT = self.load_images_helper(Player.IMAGES_LEFT, sheetL)
        Player.IMAGES_FRONT = self.load_images_helper(Player.IMAGES_FRONT, sheetF)
        Player.IMAGES_BACK = self.load_images_helper(Player.IMAGES_BACK, sheetB)
        Player.IMAGES_RIGHT_ACCEL = self.load_images_helper_accdec(Player.IMAGES_RIGHT_ACCEL, sheetRA)
        Player.IMAGES_LEFT_ACCEL = self.load_images_helper_accdec(Player.IMAGES_LEFT_ACCEL, sheetLA)
        Player.IMAGES_FRONT_ACCEL = self.load_images_helper_accdec(Player.IMAGES_FRONT_ACCEL, sheetFA)
        Player.IMAGES_BACK_ACCEL = self.load_images_helper_accdec(Player.IMAGES_BACK_ACCEL, sheetBA)
        Player.IMAGES_RIGHT_DECEL = self.load_images_helper_accdec(Player.IMAGES_RIGHT_DECEL, sheetRD)
        Player.IMAGES_LEFT_DECEL = self.load_images_helper_accdec(Player.IMAGES_LEFT_DECEL, sheetLD)
        Player.IMAGES_FRONT_DECEL = self.load_images_helper_accdec(Player.IMAGES_FRONT_DECEL, sheetFD)
        Player.IMAGES_BACK_DECEL = self.load_images_helper_accdec(Player.IMAGES_BACK_DECEL, sheetBD)

def load_images_helper_accdec(self, imageArray, sheet):
    #key = sheet.get_at((0,0))
    #hereeeeee
    alphabg = (23,23,23)
    for i in range(4):
        surface = PG.Surface((100, 100))
        surface.set_colorkey(alphabg)
        surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
        imageArray.append(surface)
    return imageArray

#this will all end up in the key handler
    def update_image(self, imageArray):
        self.image = imageArray[self.frame].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (Player.WIDTH/2, Player.HEIGHT/2)

