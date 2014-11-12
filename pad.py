import sys
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI
import Globals
import pygame.time as PT
import random

###### this class will be called by Map.py
    ## ~ Block class


###### Hot / Cold Pad Class
class Pad(PS.DirtySprite):
    IMAGES = None

    CYCLE = .6

    def __init__(self, img, rect, t):
        PS.DirtySprite.__init__(self)
        self.image = img
        self.rect = rect
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        #type can be hot or cold
        self.type = t
        ##Images for animation
        self.IMAGES = []
        self.load_images(self.type)

    #hot or cold?
    def get_type(self):
        return self.type

    #I don't think this is ever being used...
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
            toHurt = random.randrange(100)
            #this is a lame hack but it does slow down
            #the player's impending death...
            #also ANIMATE THESE PADS SOON
            if toHurt == 1:
                player.health -= 1

    ###slows down player
    def i_am_cold(self, player):
            print "herro i am cold"
            for x in range(50):
                #SPEED player.
                player.speed = 3
            #return to NORMAL after the time
            player.speed = 1

    def load_images(self, t):
        ##load hot pad images
        if t == 0:
            sheet = PI.load("FPGraphics/tiles/lv2Tiles/heatPadAnim.png") \
                .convert_alpha()
        ##load cold pad images
        #else:
        self.IMAGES = self.load_images_helper(self.IMAGES, sheet)

    def load_images_helper(self, imageArray, sheet):
        alphabg = (23, 23, 23)
        for i in range(0, 5):
            surface = PG.Surface((100, 100))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        return imageArray


##creates a new pad sprite
#called by Map.py
def create_Pad(img, rect, t):
    new_pad = Pad(img, rect, t)
    return new_pad
