import sys
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI

class Chef(PS.Sprite):
    IMAGES = None
    CYCLE = 0.6

    def __init__(self):
        PS.Sprite.__init__(self)
        #load if necessary
        if not Chef.IMAGES:
            self.load_images()
        self.time = 0.0
        self.frame = 0
        self.update_image()

    def update(self, delta):
        #update time
        self.time = self.time + delta
        if self.time > Chef.CYCLE:
            self.time = 0.0
        #update frame?
        frame = int(self.time / (Chef.CYCLE / len(Chef.IMAGES)))
        if frame != self.frame:
            self.frame = frame
            self.update_image()

    def load_images(self):
        Chef.IMAGES = []
        sheet = PI.load("MCFrontWalk.png").convert_alpha()
        key = sheet.get_at((0,0))
        #hereeeeee
        for i in range(3,7):
            surface = PG.Surface((100, 100)).convert_alpha()
            surface.set_colorkey(key)
            surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
            Chef.IMAGES.append(surface)
        for i in range(5,0,-1):
            surface = PG.Surface((100, 100)).convert_alpha()
            surface.set_colorkey(key)
            surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
            Chef.IMAGES.append(surface)
        for i in range(0,3):
            surface = PG.Surface((100, 100)).convert_alpha()
            surface.set_colorkey(key)
            surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
            Chef.IMAGES.append(surface)

    def update_image(self):
        self.image = Chef.IMAGES[self.frame]
        self.rect = self.image.get_rect()
        #self.rect.center = (WIDTH/2, HEIGHT/2)

