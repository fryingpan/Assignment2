import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
from Player import Player
from Enemy import Enemy

class Trap(PS.DirtySprite):

    IMAGE = None
    IMAGES_APPEAR = None
    IMAGES_DISAPPEAR = None

    def __init__(self, surface, rect, lifetime):
        PS.DirtySprite.__init__(self)
        self.rect = rect
        # the life of the trap
        self.lifetime = lifetime
        self.x = self.rect.x
        self.y = self.rect.y
        # booleans to start animation 
        self.dropped = False
        self.disappear = False
        self.set_anim_start()
        # number of animation frames
        self.num_frames = 3
        # whether the trap has collided with the player
        self.trap_attack = False
        # whether the trap need to be removed from the list of traps in SetUp
        self.remove = False
        self.surface = surface
        self.load_images()



    def update(self, delta, bg, player_group):
        self.trap_attack = False
        if not self.dropped:
            self.drop_animation()
            self.draw(self.surface, False)
        elif self.lifetime <= 70:
            self.disappear_animation()
            if not self.disappear:
                self.draw(self.surface, False)
            else:
                self.remove = True
        else:
            self.draw(self.surface, True)
        collisions = self.handle_collisions(player_group)
        if len(collisions) > 0:
            self.trap_attack = True
        self.dirty = 1


    def will_remove(self):
        return self.remove

    def get_trap_attack(self):
        return self.trap_attack

    def handle_collisions(self, player_group):
        return PS.spritecollide(self, player_group, False)

    def set_anim_start(self):
        # start at index 0 of image array(array containing animation frames)
        self.frame_num = 0
        # time of each animation frame
        self.frame_count = 12

    def drop_animation(self):
        if not self.dropped:
            self.update_anim(Trap.IMAGES_APPEAR, self.frame_num)
            if self.frame_count == 0 and self.frame_num < self.num_frames:
                self.frame_num += 1
                self.frame_count = 12
            elif self.frame_count > 0:
                self.frame_count -= 1
            else:
                self.dropped = True
                self.set_anim_start()
        self.lifetime -= 1

    def draw(self, surface, static_image):
        if self.lifetime > 0:
            if static_image:
                surface.blit(self.static_image, (self.x, self.y))
            else:
                surface.blit(self.image, (self.x, self.y))
        self.lifetime -= 1

    def disappear_animation(self):
        if not self.disappear:
            self.update_anim(Trap.IMAGES_DISAPPEAR, self.frame_num)
            if self.frame_count == 0 and self.frame_num < self.num_frames:
                self.frame_num += 1
                self.frame_count = 12
            elif self.frame_count > 0:
                self.frame_count -= 1
                self.lifetime -= 1
            else:
                self.disappear = True

    def update_anim(self, imageArray, index):
        try:
            self.image = imageArray[index].convert_alpha()
        except IndexError:
            pass
            # self.image = self.static_image.convert_alpha()
            # self.face = list(self.face)[0]


class Puddle(Trap):

    IMAGE = None
    IMAGES_APPEAR = None
    IMAGES_DISAPPEAR = None

    def __init__(self, rect, surface):
        #how long the puddle will last before it disappears
        self.lifetime = 500
        # if not Trap.IMAGE:
        Trap.IMAGE = PI.load("FPGraphics/Food/IceCreamPuddle.png") \
                .convert_alpha()
        Trap.static_image = Trap.IMAGE
        Trap.image = self.static_image

        self.load_images()

        if not Puddle.IMAGE:
            Puddle.IMAGE = PI.load("FPGraphics/Food/IceCreamPuddle.png") \
                .convert_alpha()
        self.static_image = Puddle.IMAGE
        self.image = self.static_image
        self.load_images()
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.dropped = False
        self.disappear = False
        self.set_anim_start()
        self.num_frames = 3

        #initialize parent class
        Trap.__init__(self, surface, rect, self.lifetime)


    #load animation images
    def load_images(self):
        Trap.IMAGES_APPEAR = []
        Trap.IMAGES_DISAPPEAR = []
        sheetA = PI.load("FPGraphics/Food/IceCreamPuddleDrop.png") \
            .convert_alpha()
        sheetD = PI.load("FPGraphics/Food/IceCreamPuddleDry.png") \
            .convert_alpha()
        Trap.IMAGES_APPEAR = self.load_images_helper(
            Trap.IMAGES_APPEAR, sheetA)
        Trap.IMAGES_DISAPPEAR = self.load_images_helper(
            Trap.IMAGES_DISAPPEAR, sheetD)

    def load_images_helper(self, imageArray, sheet):
        #split images into an array. Each individual imagae in the sheet is 50x50
        alphabg = (23, 23, 23)
        for i in range(0, 3):
            surface = PG.Surface((50, 50))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*50, 0, 50, 50))
            imageArray.append(surface)
        return imageArray


#to add to Set up

#From Trap import Puddle

# self.trap_list = []


# weapon_attack = False

#             for trap in self.trap_list:
#                 trap.weapon_update(self.map.get_surface(),
#                                        self.player_group)
#                 if (trap.get_trap_attack() and self.invincibility_count == 0):
#                     weapon_attack = True
#                 if trap.will_remove():
#                     self.trap_list.remove(trap)


#             for icecream in self.icecream_list.sprites():
#                 icecream_face = icecream.get_face()
#                 #see if the enemy will release weapon/attack
#                 if (icecream.will_attack()):
#                     #get a new puddle sprite
#                     new_trap = icecream.attack()
#                     #add the new trap to the list of traps
#                     self.trap_list.append(new_trap)
#                 icecream.draw(self.map.get_surface())
