'''
Assignment 2
Fryingpan
Carla Castro
Mary Yen
Katie Chang
Josh Holstein
'''

import pygame as PG
from pygame.locals import *
import sys
import pygame.mixer as PM
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI
from Weapon import Weapon

PG.init()


class Player(PS.DirtySprite):
    IMAGES = None
    IMAGES_RIGHT = None
    IMAGES_LEFT = None
    IMAGES_FRONT = None
    IMAGES_BACK = None
    IMAGES_RIGHT_ACCEL = None
    IMAGES_LEFT_ACCEL = None
    IMAGES_FRONT_ACCEL = None
    IMAGES_BACK_ACCEL = None
    IMAGES_RIGHT_DMG = None
    IMAGES_LEFT_DMG = None
    IMAGES_FRONT_DMG = None
    IMAGES_BACK_DMG = None
    #attack images
    IMG_ATTACK_D = None
    IMG_ATTACK_U = None
    IMG_ATTACK_R = None
    IMG_ATTACK_L = None

    CYCLE = 0.5
    ADCYCLE = .05
    WIDTH = 100
    HEIGHT = 100

    def __init__(self, fps=1):
        # Call the parent class (Sprite) constructor
        PS.DirtySprite.__init__(self)
        self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png") \
            .convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.face = 'd'
        self.load_images()
        self.speed = 8*fps
        self.time = 0.0
        self.frame = 0
        self.got_key = False
        #will turn to True once you've run into the yellow block
        #collision conditions, if true, we will not move in that direction
        self.health = 10
        self.dmg_count = 0
        self.invincibility_frame = PI.load("FPGraphics/emptyImg.png") \
            .convert_alpha()
        self.score = 0
        self.weapon = Weapon()
        self.moved = False
        self.interval = 0
        self.frame_interval = 0
        self.opened_door = False

    def get_open_door(self):
        returned = self.opened_door
        self.opened_door = False
        return returned

    def set_interval(self, interval):
        self.frame_interval = interval

    def get_rect_if_moved(self):
        if self.moved:
            return self.rect
        else:
            return None

    def decrement_health(self, enemy_ID):
        if self.health > 0:
            self.health -= 1
        self.dmg_count = 3

    def invincibility_frames(self):
        self.image = self.invincibility_frame

    def get_face(self):
        return self.face

    def player_got_key(self):
        return self.got_key

    def get_coordinates(self):
        coordinates = [self.rect.x, self.rect.y]
        return coordinates

    def open_door(self, bg):  # pass the enire block group.
        for block in bg:
            if block.get_type() == 'D':
                block.kill()
        self.opened_door = True

    def handle_collision(self, bg):
            collisions = PS.spritecollide(self, bg, False)
            if self.face == 'r' or self.face == 'ra' or self.face == 'rs':
                    collisions = PS.spritecollide(self, bg, False)
                    once = True
                    for collision in collisions:
                            if collision.get_type() == "K":
                                #kills the yellow brick.
                                collision.kill()
                                self.open_door(bg)
                                self.got_key = True
                            elif once:
                                    if(self.rect.x + self.rect.width
                                       ) >= collision.rect.left:
                                        self.rect.x = collision.rect.left \
                                            - self.rect.width
                                        once = False

            elif self.face == 'l' or self.face == 'la' or self.face == 'ls':
                    collisions = PS.spritecollide(self, bg, False)
                    once = True
                    for collision in collisions:
                            if collision.get_type() == "K":
                                #kills the yellow brick.
                                collision.kill()
                                self.open_door(bg)
                                self.got_key = True
                            elif once:
                                    if(self.rect.x) <= (collision.rect.left +
                                                        collision.rect.width):
                                        self.rect.x = (collision.rect.left +
                                                       collision.rect.width)
                                        once = False
            elif self.face == 'd' or self.face == 'da' or self.face == 'ds':
                    once = True
                    for collision in collisions:
                            if collision.get_type() == "K":
                                #kills the yellow brick.
                                collision.kill()
                                self.open_door(bg)
                                self.got_key = True
                            elif once:
                                    if(self.rect.y + self.rect.height
                                       ) >= collision.rect.top:
                                            self.rect.y = collision.rect.top -\
                                                self.rect.height
                                            once = False
            elif self.face == 'u' or self.face == 'ua' or self.face == 'us':
                    collisions = PS.spritecollide(self, bg, False)
                    once = True
                    for collision in collisions:
                            if collision.get_type() == "K":
                                #kills the yellow brick.
                                collision.kill()
                                self.open_door(bg)
                                self.got_key = True
                            elif once:
                                    if(self.rect.y <= (collision.rect.top +
                                                       collision.rect.height)):
                                            self.rect.y = collision.rect.top +\
                                                collision.rect.height
                                            once = False

    def handle_keys(self, bg, enemy_bg, screen, interval=5):
        #add enemy_bg to character_handle_keys in setup
        """ Handles Keys """
        self.interval = interval
        key = PG.key.get_pressed()
        dist = self.speed  # distance moved in 1 frame, try changing it to 5
        if key[PG.K_DOWN]:  # down key
                self.rect.y += dist*self.interval  # move down
                #self.rect = self.image.get_rect()
                self.face = 'd'
                self.handle_collision(bg)
        elif key[PG.K_UP]:  # up key
            self.rect.y -= dist*self.interval  # move up
            #self.rect = self.image.get_rect()
            self.face = 'u'
            self.handle_collision(bg)
        elif key[PG.K_RIGHT]:  # right key
            self.rect.x += dist*self.interval  # move right
            #self.rect = self.image.get_rect()
            self.face = 'r'
            self.handle_collision(bg)
        elif key[PG.K_LEFT]:  # left key
            self.rect.x -= dist*self.interval  # move left
            #self.rect = self.image.get_rect()
            self.face = 'l'
            self.handle_collision(bg)
        elif key[PG.K_SPACE]:  # space key ATTACK
            '''if 'r' in self.face:
                self.image = self.IMG_ATTACK_R
            if 'l' in self.face:
                self.image = self.IMG_ATTACK_L'''
            if 'd' in self.face:
                self.image = self.IMG_ATTACK_D
            '''if 'u' in self.face:
                self.image = self.IMG_ATTACK_U'''
            for x in range(100):
                self.score += self.weapon.attack(self.rect.x, self.rect.y,
                                             self.face, screen, enemy_bg)
                pass
        else:  # ds = down 'standing' (not moving) **********
            if self.face == 'd':
                    self.face = 'ds'
            if self.face == 'u':
                    self.face = 'us'
            if self.face == 'r':
                    self.face = 'rs'
            if self.face == 'l':
                    self.face = 'ls'

    def update(self, delta, bg, selfgroup):
        self.moved = False
        x_location = self.rect.x
        y_location = self.rect.y
        PLAYER_IMAGE_LENGTH = 12 # all player sprite has 12 frames
        #update time and frame
        key = PG.key.get_pressed()
        #camera stuff
        # increment in x direction
        #self.rect.left += self.xvel
        # do x-axis collisions
        # self.collide(self.xvel, 0, platforms)
        # increment in y direction
        #self.rect.top += self.yvel
        #camera stuff end
        self.time = self.time + delta
        if self.time > Player.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Player.CYCLE / PLAYER_IMAGE_LENGTH))
        if frame != self.frame:
            self.frame = frame
            if(self.dmg_count > 0):
                self.dmg_count -= 1
                self.face = list(self.face)[0]
                #DMG
                if(self.face == 'r'):
                    self.update_image(self.IMAGES_RIGHT_DMG)
                elif(self.face == 'u'):
                    self.update_image(self.IMAGES_BACK_DMG)
                elif(self.face == 'l'):
                    self.update_image(self.IMAGES_LEFT_DMG)
                elif(self.face == 'd'):
                    self.update_image(self.IMAGES_FRONT_DMG)
            else:
                if (self.face == 'r'):
                    self.update_image(self.IMAGES_RIGHT)
                elif (self.face == 'u'):
                    self.update_image(self.IMAGES_BACK)
                elif (self.face == 'l'):
                    self.update_image(self.IMAGES_LEFT)
                elif (self.face == 'd'):
                    self.update_image(self.IMAGES_FRONT)
                #standing
                elif(self.face == 'rs'):
                    self.image = self.IMAGES_RIGHT[0]
                elif(self.face == 'us'):
                    self.image = self.IMAGES_BACK[0]
                elif(self.face == 'ls'):
                    self.image = self.IMAGES_LEFT[0]
                elif(self.face == 'ds'):
                    self.image = self.IMAGES_FRONT[0]
                #accel
                elif(self.face == 'ra'):
                    self.update_image(self.IMAGES_RIGHT_ACCEL)
                elif(self.face == 'ua'):
                    self.update_image(self.IMAGES_BACK_ACCEL)
                elif(self.face == 'la'):
                    self.update_image(self.IMAGES_LEFT_ACCEL)
                elif(self.face == 'da'):
                    self.update_image(self.IMAGES_FRONT_ACCEL)
                else:
                    self.image = PI.load("FPGraphics/MC/" +"MCwalk/MCFront.png").convert_alpha()
        self.dirty = 1

    def update_image(self, imageArray):
            try:
                    self.image = imageArray[self.frame].convert_alpha()
            except IndexError:
                    print("IMG ERROR")
                    self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png")\
                        .convert_alpha()
                    self.face = list(self.face)[0]

    def draw(self, screen, block_group):
            """ Draw on surface """
            key = PG.key.get_pressed()
            if key[PG.K_SPACE] and not key[K_RIGHT] and not key[K_LEFT] and not key[K_UP] and not key[K_DOWN]:
                    self.weapon.draw(screen)
            self.check_boundary(screen)
            # blit yourself at your current position
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_boundary(self, screen):
            width = screen.get_width() * 2
            height = screen.get_height() * 2
            if self.rect.x < 0:
                    self.rect.x = 0
            elif self.rect.x > (width - self.image.get_width()):
                    self.rect.x = width - self.image.get_width()
            if self.rect.y < 0:
                    self.rect.y = 0
            elif self.rect.y > (height - self.image.get_height()):
                    self.rect.y = (height - self.image.get_height())

    def load_images_helper_ad(self, imageArray, sheet):
            alphabg = (23, 23, 23)
            for i in range(3):
                    surface = PG.Surface((100, 100))
                    surface.set_colorkey(alphabg)
                    surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
                    imageArray.append(surface)
            return imageArray

    def load_images_helper(self, imageArray, sheet):
            alphabg = (23, 23, 23)
            for i in range(3, 7):
                    surface = PG.Surface((100, 100))
                    surface.set_colorkey(alphabg)
                    surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
                    imageArray.append(surface)
            for i in range(5, 0, -1):
                    surface = PG.Surface((100, 100))
                    surface.set_colorkey(alphabg)
                    surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
                    imageArray.append(surface)
            for i in range(0, 3):
                    surface = PG.Surface((100, 100))
                    surface.set_colorkey(alphabg)
                    surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
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
            Player.IMAGES_RIGHT_DMG = []
            Player.IMAGES_LEFT_DMG = []
            Player.IMAGES_FRONT_DMG = []
            Player.IMAGES_BACK_DMG = []
            sheetR = PI.load("FPGraphics/MC/MCwalk/MCRightWalk.png")\
                .convert_alpha()
            sheetL = PI.load("FPGraphics/MC/MCwalk/MCLeftWalk.png")\
                .convert_alpha()
            sheetF = PI.load("FPGraphics/MC/MCwalk/MCFrontWalk.png")\
                .convert_alpha()
            sheetB = PI.load("FPGraphics/MC/MCwalk/MCBackWalk.png")\
                .convert_alpha()
            #accel
            sheetRA = PI.load("FPGraphics/MC/MCwalk/MCAccelRight.png")\
                .convert_alpha()
            sheetLA = PI.load("FPGraphics/MC/MCwalk/MCAccelLeft.png")\
                .convert_alpha()
            sheetFA = PI.load("FPGraphics/MC/MCwalk/MCAccelFront.png")\
                .convert_alpha()
            sheetBA = PI.load("FPGraphics/MC/MCwalk/MCAccelBack.png")\
                .convert_alpha()
            #damage
            sheetRD = PI.load("FPGraphics/MC/MCwalk/MCDMGRight.png")\
                .convert_alpha()
            sheetLD = PI.load("FPGraphics/MC/MCwalk/MCDMGLeft.png")\
                .convert_alpha()
            sheetFD = PI.load("FPGraphics/MC/MCwalk/MCDMGFront.png")\
                .convert_alpha()
            sheetBD = PI.load("FPGraphics/MC/MCwalk/MCDMGBack.png")\
                .convert_alpha()

            Player.IMAGES_RIGHT = self.load_images_helper(Player.IMAGES_RIGHT,
                                                          sheetR)
            Player.IMAGES_LEFT = self.load_images_helper(Player.IMAGES_LEFT,
                                                         sheetL)
            Player.IMAGES_FRONT = self.load_images_helper(Player.IMAGES_FRONT,
                                                          sheetF)
            Player.IMAGES_BACK = self.load_images_helper(Player.IMAGES_BACK,
                                                         sheetB)
            Player.IMAGES_RIGHT_ACCEL =\
                self.load_images_helper_ad(Player.IMAGES_RIGHT_ACCEL, sheetRA)
            Player.IMAGES_LEFT_ACCEL =\
                self.load_images_helper_ad(Player.IMAGES_LEFT_ACCEL, sheetLA)
            Player.IMAGES_FRONT_ACCEL =\
                self.load_images_helper_ad(Player.IMAGES_FRONT_ACCEL, sheetFA)
            Player.IMAGES_BACK_ACCEL =\
                self.load_images_helper_ad(Player.IMAGES_BACK_ACCEL, sheetBA)
            Player.IMAGES_RIGHT_DMG =\
                self.load_images_helper(Player.IMAGES_RIGHT_DMG, sheetRD)
            Player.IMAGES_LEFT_DMG =\
                self.load_images_helper(Player.IMAGES_LEFT_DMG, sheetLD)
            Player.IMAGES_FRONT_DMG =\
                self.load_images_helper(Player.IMAGES_FRONT_DMG, sheetFD)
            Player.IMAGES_BACK_DMG =\
                self.load_images_helper(Player.IMAGES_BACK_DMG, sheetBD)

            #load attack images
            Player.IMG_ATTACK_D = PI.load("FPGraphics/MC/MCattack/" +
                                          "MCFrontFPatk1.png").convert_alpha()
            '''Player.IMG_ATTACK_U = PI.load("FPGraphics/MC/weapon/FPU.png")\
                .convert_alpha()
            Player.IMG_ATTACK_R = PI.load("FPGraphics/MC/weapon/FPR.png")\
                .convert_alpha()
            Player.IMG_ATTACK_L = PI.load("FPGraphics/MC/weapon/FPL.png")\
                .convert_alpha()'''
