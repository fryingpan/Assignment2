'''
Assignment 2
Fryingpan
authors:
Carla Castro
Mary Yen
Katie Chang
'''

import pygame as PG
from pygame.locals import *
import sys
import pygame.mixer as PM
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI
from Weapon import Weapon
import Globals
import Item
from Trap import Trap


class Player(PS.DirtySprite):
    IMAGES = None
    IMAGES_RIGHT = None
    IMAGES_LEFT = None
    IMAGES_FRONT = None
    IMAGES_BACK = None
    IMAGES_RIGHT_DMG = None
    IMAGES_LEFT_DMG = None
    IMAGES_FRONT_DMG = None
    IMAGES_BACK_DMG = None
    # attack images
    IMG_ATTACK_D = None  # 100 x 150 dimensions
    IMG_ATTACK_U = None
    IMG_ATTACK_R = None
    IMG_ATTACK_L = None
    # Animation cycle variables
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
        # self.speed both determines the speed of the player &
        # ensures the the player moves at an integer distance
        # during play (arbitrary value)
        self.speed = 1
        self.time = 0.0
        self.frame = 0
        self.got_key = False
        # will turn to True once you've run into the yellow block
        # collision conditions, if true, we will not move in that direction
        self.health = 1000
        self.dmg_count = 0
        self.invincibility_frame = PI.load("FPGraphics/emptyImg.png") \
            .convert_alpha()
        self.weapon = Weapon()
        self.moved = False
        self.interval = 0
        self.modified_map = False
        self.pill = False
        self.at_door_num = -1  # allows player to open door if player has key
        self.attack_pose = False
        
        self.items_of_killed = []
        # Item Variables
        self.grab_item = False
        self.item = False
        self.item_use_count = 0
        self.item_type = 0
        self.player_items = []
        self.player_traps = []
        self.can_eat = False

    def remove_player_item(self, item):
        self.player_items.remove(item)

    def remove_player_trap(self, item):
        self.player_traps.remove(item)

    def get_player_items(self):
        return self.player_items

    def drop_item(self, surface):
        if self.item_type == 1:
            self.player_items.append(Item.IceCreamScoop(self.rect.x,
                                                        self.rect.y, surface))

    def drop_trap(self, surface):
        if (self.item_type == 1):
            image = PI.load("FPGraphics/drops/DropIceCream.png").convert_alpha()
        rect = image.get_rect()
        rect.x = self.rect.x
        rect.y = self.rect.y
        self.player_traps.append(Trap(surface,         # surface to be drawn in
                                     rect,             # rect of the image 
                                     self.item_type,   # the type of trap
                                     'P',              # Player is the user 
                                     1600,             # lifetime 
                                     image,            # image 
                                     False))           # if the trap will be animated
        self.item_use_count -= 1
        if self.item_use_count == 0:
            self.item = False

    def get_player_traps(self):
        return self.player_traps

    def get_items_of_killed(self):
        return self.items_of_killed

    def get_modified_map(self):
        returned = self.modified_map
        self.modified_map = False
        return returned

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
            if block.get_type() == self.at_door_num:
                block.kill()
        self.modified_map = True

    def handle_collision(self, bg):
        collisions = PS.spritecollide(self, bg, False)
        for collision in collisions:
            # check if collided with an item
            if type(collision.get_type()) is int:
                if self.grab_item:
                    self.item = True
                    self.item_use_count = collision.get_use_count()
                    self.item_type = collision.get_type()
                    collision.disappear()
                    # print "got item"

            if collision.get_type() == "K":  # found key
                collision.kill()
                self.pill = True
                # self.open_door(bg)
                self.got_key = True
                self.modified_map = True
            if isinstance(collision.get_type(), str) and collision.get_type().isdigit():  # at a door
                if self.pill:  # unlockable door
                    self.at_door_num = collision.get_type()
                    # print("CAN OPEN " + collision.get_type())
                else:
                    self.at_door_num = -1
            else:
                self.at_door_num = -1
            if self.face == 'r' or self.face == 'ra' or self.face == 'rs':
                if(self.rect.x + self.rect.width
                   ) >= collision.rect.left:
                    self.rect.x = collision.rect.left \
                        - self.rect.width
            elif self.face == 'l' or self.face == 'ls':
                if(self.rect.x) <= (collision.rect.left +
                                    collision.rect.width):
                    self.rect.x = (collision.rect.left +
                                   collision.rect.width)
            elif self.face == 'd' or self.face == 'ds':
                if(self.rect.y + self.rect.height
                   ) >= collision.rect.top:
                        self.rect.y = collision.rect.top -\
                            self.rect.height
            elif self.face == 'u' or self.face == 'us':
                if(self.rect.y <= (collision.rect.top +
                                   collision.rect.height)):
                        self.rect.y = collision.rect.top +\
                            collision.rect.height

    def handle_keys(self, bg, enemy_bg, item_group, screen, interval=0.0065):
        """ Handles Keys """
        self.items_of_killed = []
        self.attack_pose = False
        standing = False
        self.grab_item = False
        self.interval = interval
        key = PG.key.get_pressed()
        temp = self.rect.x
        if key[PG.K_DOWN]:  # down key
            self.rect.y += self.speed  # move down
            # self.rect = self.image.get_rect()
            self.face = 'd'
            self.handle_collision(bg)
        elif key[PG.K_UP]:  # up key
            self.rect.y -= self.speed  # move up
            # self.rect = self.image.get_rect()
            self.face = 'u'
            self.handle_collision(bg)
        elif key[PG.K_RIGHT]:  # right key
            self.rect.x += self.speed  # move right
            # self.rect = self.image.get_rect()
            self.face = 'r'
            self.handle_collision(bg)
        elif key[PG.K_LEFT]:  # left key
            self.rect.x -= self.speed  # move left
            # self.rect = self.image.get_rect()
            self.face = 'l'
            self.handle_collision(bg)

        elif key[PG.K_a]:
            if self.item and self.can_drop:
                self.drop_trap(screen)
                self.can_drop = False

        # grab item if available
        elif key[PG.K_s]:
            # check if you already have an item
            if not self.item:
                self.grab_item = True
                self.handle_collision(item_group)
        # drop item if you have one
        elif key[PG.K_d]:
            if self.item and self.can_drop:
                self.drop_item(screen)
                self.item = False
        elif key[PG.K_SPACE]:  # space key ATTACK
            if 'r' in self.face:
                self.image = self.IMG_ATTACK_R
            if 'l' in self.face:
                self.image = self.IMG_ATTACK_L
            if 'd' in self.face:
                self.image = self.IMG_ATTACK_D
            if 'u' in self.face:
                self.image = self.IMG_ATTACK_U
            # attack collisions
            collisions = PS.spritecollide(self, enemy_bg, False)

            # for x in range(100):
            killed_enemies = self.weapon.attack(self, self.rect.x, self.rect.y,
                                                self.face, screen, enemy_bg)
            for killed in killed_enemies:
                if(killed.last_hit == 0):
                    # print len(killed_enemies)
                    self.items_of_killed.append(killed.drop_item(screen))
                    # self.health += 1
                    killed.decrement_health(1)
                    # self.score += 1
                    # killed.kill()
                    killed.last_hit = 80
                else:
                    killed.last_hit -= 1
            # self.weapon.draw(screen)
            self.attack_pose = True
            standing = True

            #handle locked doors
            if self.at_door_num != -1: 
                self.open_door(bg)
                self.pill = False
        else:  # ds = down 'standing' (not moving) **********
            standing = True
        if not key[PG.K_a]:
            self.can_drop = True
        if standing:
            if self.face == 'd':
                    self.face = 'ds'
            if self.face == 'u':
                    self.face = 'us'
            if self.face == 'r':
                    self.face = 'rs'
            if self.face == 'l':
                    self.face = 'ls'

    def update(self, bg, selfgroup):
        self.moved = False
        PLAYER_IMAGE_LENGTH = 12  # all player sprite has 12 frames
        # update time and frame
        key = PG.key.get_pressed()
        self.time = self.time + Globals.DELTA
        if self.time > Player.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Player.CYCLE / PLAYER_IMAGE_LENGTH))
        if frame != self.frame:
            self.frame = frame
            if(self.dmg_count > 0):
                self.dmg_count -= 1
                self.face = list(self.face)[0]
                # DMG
                if(self.face == 'r'):
                    self.update_image(self.IMAGES_RIGHT_DMG)
                elif(self.face == 'u'):
                    self.update_image(self.IMAGES_BACK_DMG)
                elif(self.face == 'l'):
                    self.update_image(self.IMAGES_LEFT_DMG)
                elif(self.face == 'd'):
                    print(self.frame)
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
                # standing
                elif self.attack_pose is False:
                    if(self.face == 'rs'):
                        self.image = self.IMAGES_RIGHT[0]
                    elif(self.face == 'us'):
                        self.image = self.IMAGES_BACK[0]
                    elif(self.face == 'ls'):
                        self.image = self.IMAGES_LEFT[0]
                    elif(self.face == 'ds'):
                        self.image = self.IMAGES_FRONT[0]
                    else:
                        self.image = PI.load("FPGraphics/MC/" +
                                             "MCwalk/MCFront.png").convert_alpha()
#                    self.attack_pose = False
        self.dirty = 1

    def update_image(self, imageArray):
            try:
                self.image = imageArray[self.frame].convert_alpha()

            except IndexError:
                print("PLAYER IMG ERROR")
                self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png")\
                    .convert_alpha()
                self.face = list(self.face)[0]

    def draw(self, screen, block_group):
            """ Draw on surface """
            # key = PG.key.get_pressed()
            self.check_boundary(screen)
            # blit yourself at your current position
#            print "player's draw 332"
#            if self.attack_pose is True and 'l' in self.face:
#                screen.blit(self.image, (self.rect.x-50, self.rect.y))
#            else:
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
            Player.IMAGES_RIGHT_DMG = []
            Player.IMAGES_LEFT_DMG = []
            Player.IMAGES_FRONT_DMG = []
            Player.IMAGES_BACK_DMG = []
            #walking imgs
            sheetR = PI.load("FPGraphics/MC/MCwalk/MCRightWalk.png")\
                .convert_alpha()
            sheetL = PI.load("FPGraphics/MC/MCwalk/MCLeftWalk.png")\
                .convert_alpha()
            sheetF = PI.load("FPGraphics/MC/MCwalk/MCFrontWalk.png")\
                .convert_alpha()
            sheetB = PI.load("FPGraphics/MC/MCwalk/MCBackWalk.png")\
                .convert_alpha()
            Player.IMAGES_RIGHT = self.load_images_helper(Player.IMAGES_RIGHT,
                                                          sheetR)
            Player.IMAGES_LEFT = self.load_images_helper(Player.IMAGES_LEFT,
                                                         sheetL)
            Player.IMAGES_FRONT = self.load_images_helper(Player.IMAGES_FRONT,
                                                          sheetF)
            Player.IMAGES_BACK = self.load_images_helper(Player.IMAGES_BACK,
                                                         sheetB)
            #dmg imgs
            sheetDR = PI.load("FPGraphics/MC/MCwalk/MCDMGRight.png")\
                .convert_alpha()
            sheetDL = PI.load("FPGraphics/MC/MCwalk/MCDMGLeft.png")\
                .convert_alpha()
            sheetDF = PI.load("FPGraphics/MC/MCwalk/MCDMGFront.png")\
                .convert_alpha()
            sheetDB = PI.load("FPGraphics/MC/MCwalk/MCDMGBack.png")\
                .convert_alpha()
            Player.IMAGES_RIGHT_DMG = self.load_images_helper(Player.IMAGES_RIGHT_DMG,
                                                          sheetDR)
            Player.IMAGES_LEFT_DMG = self.load_images_helper(Player.IMAGES_LEFT_DMG,
                                                         sheetDL)
            Player.IMAGES_FRONT_DMG = self.load_images_helper(Player.IMAGES_FRONT_DMG,
                                                          sheetDF)
            Player.IMAGES_BACK_DMG = self.load_images_helper(Player.IMAGES_BACK_DMG,
                                                         sheetDB)
            # load attack images
            Player.IMG_ATTACK_D = PI.load("FPGraphics/MC/MCattack/" +
                                          "MCFrontFPOnePiece.png").convert_alpha()
            Player.IMG_ATTACK_U = PI.load("FPGraphics/MC/MCattack/" +
                                          "MCBackPOnePiece.png").convert_alpha()
            Player.IMG_ATTACK_R = PI.load("FPGraphics/MC/MCattack/" +
                                          "MCRightFPOnePiece.png").convert_alpha()
            Player.IMG_ATTACK_L = PI.load("FPGraphics/MC/MCattack/" +
                                          "MCLeftFPOnePiece.png").convert_alpha()
