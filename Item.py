'''
Team: Fryingpan
author: Carla
edited: Mary
'''

import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI


class Item(PS.DirtySprite):
    def __init__(self, therect, theType, useCount, lifetime=500, health=3):
        PS.DirtySprite.__init__(self)
        self.rect = Item.IMAGE.get_rect()
        self.rect.x = therect.x
        self.rect.y = therect.y
        self.type = theType
        self.lifetime = lifetime
        self.surface = Item.surface
        self.use_count = useCount
        self.grabbed = False
        self.remove = False
        self.health = health
        self.use_count = useCount

    def get_health(self):
        return self.health

    def get_image(self):
        return self.image

    def get_use_count(self):
        return self.use_count

    def get_type(self):
        return self.type

    def will_remove(self):
        return self.remove

    def draw(self):
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, block_group, player):
        self.draw()
        self.lifetime -= 1
        if self.lifetime == 0:
            self.disappear()
        self.dirty = 1

    def disappear(self):
        self.remove = True


# Ice Cream Drop
class IceCreamScoop(Item):
    def __init__(self, x_coor, y_coor, surface):
        Item.IMAGE = PI.load("FPGraphics/drops/DropIceCream.png")\
            .convert_alpha()
        self.image = Item.IMAGE
        self.rect = self.image.get_rect()
        # x position
        self.rect.x = x_coor + 25
        # y position
        self.rect.y = y_coor + 25
        # from what enemy its from
        self.type = 1
        # how long the item is available to grab
        self.lifetime = 2000
        # surface
        Item.surface = surface
        # how many times the item may be used by the player
        self.use_count = 10
        self.health = 3
        Item.__init__(self, self.rect, self.type, self.use_count,
                      self.lifetime, self.health)


# Burger Drop
class BreadDrop(Item):
    def __init__(self, x_coor, y_coor, surface):
        Item.IMAGE = PI.load("FPGraphics/drops/breadDrop.png").convert_alpha()
        self.image = Item.IMAGE
        self.rect = self.image.get_rect()
        # x position
        self.rect.x = x_coor + 25
        # y position
        self.rect.y = y_coor + 25
        # from what enemy its from
        self.type = 2
        # how long the item is available to grab
        self.lifetime = 2000
        # surface
        Item.surface = surface
        # how many times the item may be used by the player
        self.use_count = 2500
        self.health = 3
        Item.__init__(self, self.rect, self.type, self.use_count,
                      self.lifetime, self.health)


# Burger Drop
class LettuceDrop(Item):
    def __init__(self, x_coor, y_coor, surface):
        Item.IMAGE = PI.load("FPGraphics/drops/lettuceDrop.png")\
            .convert_alpha()
        self.image = Item.IMAGE
        self.rect = self.image.get_rect()
        # x position
        self.rect.x = x_coor + 25
        # y position
        self.rect.y = y_coor + 25
        # from what enemy its from
        self.type = 3
        # how long the item is available to grab
        self.lifetime = 800
        # surface
        Item.surface = surface
        # how many times the item may be used by the player
        self.use_count = 3
        self.health = 5
        Item.__init__(self, self.rect, self.type, self.use_count,
                      self.lifetime, self.health)


# Burger Drop
class MeatDrop(Item):
    def __init__(self, x_coor, y_coor, surface):
        Item.IMAGE = PI.load("FPGraphics/drops/meatDrop.png").convert_alpha()
        self.image = Item.IMAGE
        self.rect = self.image.get_rect()
        # x position
        self.rect.x = x_coor + 25
        # y position
        self.rect.y = y_coor + 25
        # from what enemy its from
        self.type = 4
        # how long the item is available to grab
        self.lifetime = 800
        # surface
        Item.surface = surface
        # how many times the item may be used by the player
        self.use_count = 2500
        self.health = 4
        Item.__init__(self, self.rect, self.type, self.use_count,
                      self.lifetime, self.health)


# Burger Drop
class BurgerDrop(Item):
    def __init__(self, x_coor, y_coor, surface):
        Item.IMAGE = PI.load("FPGraphics/drops/burgerDrop.png").convert_alpha()
        self.image = Item.IMAGE
        self.rect = self.image.get_rect()
        # x position
        self.rect.x = x_coor + 25
        # y position
        self.rect.y = y_coor + 25
        # from what enemy its from
        self.type = 5
        # how long the item is available to grab
        self.lifetime = 800
        # surface
        Item.surface = surface
        # how many times the item may be used by the player
        self.use_count = 3
        self.health = 8
        Item.__init__(self, self.rect, self.type, self.use_count,
                      self.lifetime, self.health)


# Cream Drop
class CreamDrop(Item):
    def __init__(self, x_coor, y_coor, surface):
        Item.IMAGE = PI.load("FPGraphics/drops/creamDrop.png").convert_alpha()
        self.image = Item.IMAGE
        self.rect = self.image.get_rect()
        # x position
        self.rect.x = x_coor + 25
        # y position
        self.rect.y = y_coor + 25
        # from what enemy its from
        self.type = 6
        # how long the item is available to grab
        self.lifetime = 800
        # surface
        Item.surface = surface
        # how many times the item may be used by the player
        self.use_count = 3
        self.health = 3
        Item.__init__(self, self.rect, self.type, self.use_count,
                      self.lifetime, self.health)
