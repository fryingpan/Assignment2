# Assignment 2
# Frying Pan

try:
    import pygame
    from pygame.locals import *
    import pygame.time as ptime
    import sys
    import Player
    import Enemy
    
except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    import sys
    sys.exit(1)

class Game(object):

    def __init__(self, interval, num_enemies):
    
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Master Chef's wicked adventure with his ice cream buddies")
        
        #Initialize objects on screen----------------
        self.character = Player.Player()
        # bad = Enemy()
        self.charrect = self.character.image_rect
        # badrect = bad.image.get_rect()

        #create enemy group 
        self.enemy_list = pygame.sprite.Group()

        #add all the enemies to the list of enemies
        for e in range(num_enemies):  
            enemy = Enemy.Enemy(self.screen)
            self.enemy_list.add(enemy)


        #I don't actually know what this does
        pygame.event.set_allowed([QUIT, KEYDOWN])

        self.clock = ptime.Clock()
        self.current_time = ptime.ticks()
        self.updates = 0
        self.interval = interval
    
    def run(self):
        running = True
        while running:
            new_time = ptime.get_ticks()
            frame_time = (new_time - self.current_time)/1000.0
            self.current_time = new_time
            self.clock.tick()

            running = self.handleEvents()
            #Key Handling----------------------------
            self.character.handle_keys() # handle the keys

            self.screen.fill((255,255,255)) # fill the screen with white
            #move and draw the enemies
            player_face = self.character.get_face()
            for enemy in self.enemy_list.sprites():
                enemy.set_face(player_face)
                enemy.draw()
            self.character.draw(self.screen) # draw the character to the screen
            
            self.updates = 0
            while frame_time > 0.0:
                delta = min(frame_time, INTERVAL)
                for enemy in self.enemy_list.sprites():
                    enemy.update(delta)

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
    num_enemies = 13
    game = Game(num_enemies)
    game.run()

