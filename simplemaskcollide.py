### Mask Collision Detection

import pygame

####


allgroup = pygame.sprite.Group()
somegroup = pygame.sprite.Group()


class PygView(object):

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        #self.height = width // 4
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 20, bold=True)

    def run(self):
        """The mainloop
        """
        b = Blob()
        c = Bleb()
        allgroup.add(b)
        somegroup.add(c)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), " "*5, self.playtime))

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

            somegroup.update(self.playtime)
            allgroup.update(self.playtime)
            allgroup.draw(self.screen)
            somegroup.draw(self.screen)
            print(pygame.sprite.groupcollide(allgroup, somegroup, False,
                                             True, pygame.sprite.collide_mask))

        pygame.quit()

    def draw_text(self, text):
        """Center text in window
        """
        fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        surface = self.font.render(text, True, (0, 255, 0))
        # makes integer division in python3
        self.screen.blit(surface, ((self.width - fw) // 2,
                                   (self.height - fh) // 2))


class Blob(pygame.sprite.Sprite):

    def __init__(self):
        super(Blob, self).__init__()
        self.image = pygame.image.load('babytux.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
        #self.image.fill(pygame.color.Color('red'))

    def update(self, time):
        self.rect.top = time*30
        self.rect.left = time*30


class Bleb(pygame.sprite.Sprite):

    def __init__(self):
        super(Bleb, self).__init__()
        self.image = pygame.image.load('alien1.gif').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
        #self.image.fill(pygame.color.Color('red'))

    def update(self, time):
        self.rect.left = 300
        self.rect.top = 240

####

if __name__ == '__main__':

    # call with width of window and fps
    PygView(640, 400).run()
