import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI


class Trap(PS.DirtySprite):

    IMAGE = None
    IMAGES_APPEAR = None
    IMAGES_DISAPPEAR = None

    def __init__(self, surface, rect, thetype, user, lifetime=8000, image=None,
                 animation=True):
        PS.DirtySprite.__init__(self)
        self.rect = rect
        # the life of the trap
        if image is not None:
            self.image = image
        self.lifetime = lifetime
        self.x = self.rect.x
        self.y = self.rect.y
        self.type = thetype
        self.user = user
        self.animation = animation
        # booleans to start animation
        self.dropped = False
        self.disappear = False
        self.set_anim_start()
        # number of animation frames
        self.num_frames = 3
        # whether the trap has collided with the player
        self.ptrap_attack = False
        self.etrap_attack = False
        # whether the trap need to be removed from the list of traps in SetUp
        self.remove = False
        self.surface = surface
        if animation:
            self.load_images()

    def update(self, bg, player_group):
        self.trap_attack = False
        if self.animation:
            # start drop animation once item is dropped
            if not self.dropped:
                self.drop_animation()
                self.draw(self.surface, False)
            # start disappear animation
            elif self.lifetime <= 300:
                self.disappear_animation()
                if not self.disappear:
                    self.draw(self.surface, False)
                else:
                    self.remove = True
            # else display the static image
            else:
                self.draw(self.surface, True)
            # check if enemy trap collides with the player
            if self.user == 'E':
                collisions = self.handle_collisions(player_group)
                if len(collisions) > 0:
                    self.trap_attack = True
        else:
            collisions = self.handle_collisions(bg)
        self.dirty = 1

    def get_type(self):
        return self.type

    def will_remove(self):
        return self.remove

    def get_trap_attack(self):
        return self.trap_attack

    def handle_collisions(self, group):
        return PS.spritecollide(self, group, False)

    def set_anim_start(self):
        # start at index 0 of image array(array containing animation frames)
        self.frame_num = 0
        # time of each animation frame
        self.frame_count = 100

    def drop_animation(self):
        if not self.dropped:
            # set the image to the correct animation frame
            self.update_anim(Trap.IMAGES_APPEAR, self.frame_num)
            # change the animation frame to display
            if self.frame_count == 0 and self.frame_num < self.num_frames:
                self.frame_num += 1
                self.frame_count = 80
            # decrement the lifetime of the frame
            elif self.frame_count > 0:
                self.frame_count -= 1
            # animation is done so the item is done being dropped
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
            # set the image to the correct animation frame
            self.update_anim(Trap.IMAGES_DISAPPEAR, self.frame_num)
            # change the animation frame
            if self.frame_count == 0 and self.frame_num < self.num_frames:
                self.frame_num += 1
                self.frame_count = 80
            # decrement the lifetime of the frame
            elif self.frame_count > 0:
                self.frame_count -= 1
                self.lifetime -= 1
            # once disappear animation id done, item should disappear
            else:
                self.disappear = True

    def update_anim(self, imageArray, index):
        try:
            self.image = imageArray[index].convert_alpha()
        except IndexError:
            pass


class Puddle(Trap):
    # Class variables
    IMAGE = None
    IMAGES_APPEAR = None
    IMAGES_DISAPPEAR = None

    def __init__(self, rect, surface):
        # how long the puddle will last before it disappears
        self.lifetime = 6000
        # if not Trap.IMAGE:
        Trap.IMAGE = PI.load("FPGraphics/Food/IceCreamPuddle.png") \
            .convert_alpha()
        Trap.static_image = Trap.IMAGE
        Trap.image = self.static_image
        # load animation images
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
        self.type = 'E'
        # initialize parent class
        Trap.__init__(self, surface, rect, self.type, 'E', self.lifetime)

    # load animation images
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
        # split images into an array. Each individual
        # imagae in the sheet is 50x50
        alphabg = (23, 23, 23)
        for i in range(0, 3):
            surface = PG.Surface((50, 50))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*50, 0, 50, 50))
            imageArray.append(surface)
        return imageArray
