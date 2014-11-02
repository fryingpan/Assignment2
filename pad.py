import sys
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI
import Globals
import pygame.time as PT

###### this class will be called by Map.py
    ## ~ Block class

###### Hot / Cold Pad Class
class Pad(PS.DirtySprite):
    def __init__(self, img, rect, t):
        PS.DirtySprite.__init__(self)
        self.image = img
        self.rect = rect
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        #type can be hot or cold
        self.type = 0

    #hot or cold?
    def get_type(self):
        return self.type

    def draw_pad(self, map_surface):
            map_surface.blit(self.image, self.rect)

    def get_color(self):
            return self.color

    def get_rect(self):
            return self.rect

    def get_right(self):
            return self.x + self.rect.width

    def get_left(self):
            return self.x

    def get_top(self):
            return self.y

    def get_bottom(self):
            return self.y + self.rect.height

    def set_rectLeft(self, rectLeft):
            self.rect.x = rectLeft

    def set_rectTop(self, rectTop):
            self.rect.y = rectTop

    ###hurts player, enemy (??how??)
    def i_am_hot(self, player):
            print "here"
            player.health -= 1

    ###animates player into an ice cube?
    #def i_am_cold():

#    def update(self, delta, bg, player):
#            if self.type == 'K' or self.type == 'D':
#                    self.dirty = 1


##Load images

##creates a new pad sprite
#called by Map.py
def create_Pad(img, rect, t):
    new_pad = Pad(img, rect, t)
    return new_pad


