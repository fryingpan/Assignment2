# Assignment 2
# Frying Pan

try:
    import pygame
    from pygame.locals import *
    import sys
    import Player
    import Enemy
    
except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    import sys
    sys.exit(1)

class Game(object):

    def __init__(self):
    
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Master Chef's wicked adventure with his ice cream buddies")
        
        #Initialize objects on screen----------------
        self.character = Player.Player()
        # bad = Enemy()
        self.charrect = self.character.image.get_rect()
        # badrect = bad.image.get_rect()

        #I don't actually know what this does
        pygame.event.set_allowed([QUIT, KEYDOWN])
    
    def run(self):
        running = True
        while running:
            self.clock.tick()
            running = self.handleEvents()
            #Key Handling----------------------------
            
            self.character.handle_keys() # handle the keys
            #----------------------------------------

            #Display Handling------------------------
            self.screen.fill((255,255,255)) # fill the screen with white
            self.character.draw(self.screen) # draw the bird to the screen
            i = 0
            j = 0
            pygame.display.update() # update the screen
            
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # handle user input
            elif event.type == KEYDOWN:
            # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    return False
        return True
                  
# create a game and run it
if __name__ == '__main__':
    game = Game()
    game.run()

