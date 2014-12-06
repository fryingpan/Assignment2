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
    ##NOT ANYMORE. PAD WILL NOW BE AN 'ENEMY' THAT DOESN'T MOVE.


###### Hot / Cold Pad Class
class Pad(PS.DirtySprite):
    IMAGES = None

    CYCLE = .6

    def __init__(self, xcoord, ycoord, t):
        PS.DirtySprite.__init__(self)
        self.image = PI.load("FPGraphics/tiles/lv2Tiles/heatPad.png") \
            .convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = xcoord
        self.rect.y = ycoord
        self.width = 0
        self.height = 0
        #type can be hot or cold
        self.type = t
        ##Images for animation
        self.IMAGES = []
        self.load_images(self.type)
        self.time = 0.0
        self.frame = 0
        self.burn = False

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

    def will_burn(self):
        if Globals.INVINCIBILITY_COUNT <= 0:
            return True
        else:
            return False

    ###hurts player
    # def i_am_hot(self, player):
    #         toHurt = random.randrange(100)
    #         #this is a lame hack but it does slow down
    #         #the player's impending death...
    #         #also ANIMATE THESE PADS SOON
    #         if toHurt == 1:
    #             player.health -= 1

    ###slows down player
    def i_am_cold(self, player):
            start = PT.get_ticks()
            while PT.get_ticks() - start < 10:
                continue

    def load_images(self, t):
        ##load hot pad images
        if t == 0:
            sheet = PI.load("FPGraphics/tiles/lv2Tiles/heatPadAnim.png") \
                .convert_alpha()
        ##load cold pad images
        if t == 1:
            sheet = PI.load("FPGraphics/tiles/lv3Tiles/coldPadAnim.png") \
                .convert_alpha()
        #else:
        self.IMAGES = self.load_images_helper(self.IMAGES, sheet)

    def load_images_helper(self, imageArray, sheet):
        alphabg = (23, 23, 23)
        for i in range(0, 5):
            surface = PG.Surface((50, 50))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*50, 0, 50, 50))
            imageArray.append(surface)
        for i in range(3, -1, -1):
            surface = PG.Surface((50, 50))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*50, 0, 50, 50))
            imageArray.append(surface)
        return imageArray

    def update(self, bg, player):
        PAD_IMAGE_LENGTH = 9
        self.time = self.time + Globals.DELTA
        if self.time > Pad.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Pad.CYCLE / PAD_IMAGE_LENGTH))
        if frame != self.frame:
            self.frame = frame
            self.update_image(self.IMAGES)

    def update_image(self, imageArray):
        try:
            self.image = imageArray[self.frame].convert_alpha()
        except IndexError:
            self.image = imageArray[0].convert_alpha()


##creates a new pad sprite
#called by Map.py
def create_Pad(x, y, t):
    new_pad = Pad(x, y, t)
    return new_pad
