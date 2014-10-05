# Assignment 2
# Frying Pan

try:
    import pygame as PG
    from pygame.locals import *
    import pygame.time as PT
    import sys
    from Player import Player
    from Enemy import Enemy
    import pygame.sprite as PS
    import pygame.display as PD
    import pygame.color as PC
    import pygame.event as PE
    import drawing as Draw
    
except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    import sys
    sys.exit(1)

class Locals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None
    FADEINTIME = 5.0
    FADEOUTTIME = 0.2
    CHANGESTATE = "None"

def initialize():
    # num_enemies = 13
    # interval = 0.005
    # fps = 40
    # game = Game(interval, fps, num_enemies)
    Locals.CHANGESTATE = 'Game'
    


class Game(object):

    def __init__(self, interval, fps, num_enemies):
        self.interval = interval
        self.fps = fps
        self.num_enemies=num_enemies
    
        PG.init()
        self.screen = PD.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        self.screen.fill((255,255,255))
        PD.set_caption("Master Chef's wicked adventure with his ice cream buddies")
        
        self.fps = fps
        self.speed = 4*self.fps
        #sprite group containing all sprites
        self.all_sprites = PS.Group()

        #Initialize objects on screen----------------
        self.character = Player(self.speed)
        self.all_sprites.add(self.character)
        # bad = Enemy()
        #self.charrect = self.character.image_rect
        # badrect = bad.image.get_rect()

        #create enemy group 
        self.enemy_list = PS.Group()

        #add all the enemies to the list of enemies
        for e in range(num_enemies):  
            enemy = Enemy(self.screen, self.speed)
            self.enemy_list.add(enemy)
            # self.all_sprites.add(enemy)

        #get block sprite group from the map file
        self.block_group = Draw.get_block_group('mapfile.txt')
        #add the blocks to the sprite group containing all sprites
        for block in self.block_group:
            self.all_sprites.add(block)


        #I don't actually know what this does
        PE.set_allowed([QUIT, KEYDOWN])

        self.clock = PT.Clock()
        self.current_time = PT.get_ticks()
        self.updates = 0
        self.interval = interval
        Locals.CHANGESTATE = 'Game'
    
    def run(self):
        running = True
        while running:
            new_time = PT.get_ticks()
            frame_time = (new_time - self.current_time)/1000.0
            self.current_time = new_time
            self.clock.tick()

            running = self.handleEvents()
            if(running == False):
                return False
            #Key Handling----------------------------
            # self.character.handle_keys() # handle the keys

            self.screen.fill((0,0,0)) # fill the screen with white

            self.character.handle_collision(self.block_group)

            #move and draw the enemies
            player_face = self.character.get_face()
            for enemy in self.enemy_list.sprites():
                Enemy_face = enemy.get_face()
                enemy.set_face(player_face)
                enemy.draw()

            #draw blocks
            Draw.draw_map(self.block_group)

            self.character.draw(self.screen) # draw the character to the screen
            
            PD.flip()

            self.updates = 0

            #clock is added
            clock = PT.Clock()

            while frame_time > 0.0:
                delta = min(frame_time, self.interval)
                for enemy in self.enemy_list.sprites():
                    enemy.update(delta)
                self.character.handle_keys(self.interval)
                frame_time -= delta
                self.updates += 1
                #adding animantion here?

                last = PT.get_ticks()

                self.character.draw(self.screen)

                clock.tick()

                PD.flip()

                elapsed = (PT.get_ticks() - last) / 1000.0
                if (PG.key.get_pressed()):
                    self.update(self.character, elapsed)

            #Here's animation code...
            '''clock = PT.Clock()

            while PG.key.get_pressed():
                last = PT.get_ticks()

                self.character.draw(self.screen)

                clock.tick()

                PD.flip()

                elapsed = (PT.get_ticks() - last) / 1000.0
                self.character.update(elapsed)

                for event in PE.get():
                    if event.type == PG.QUIT:
                        sys.exit()
                    elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                        sys.exit()
'''
            PD.update() # update the screen
            
    def update(self, player, delta):
            player.update(delta)
            """PLAYER_IMAGE_LENGTH = 12 #all player sprite has 12 frames
            #update time
            player.time = player.time + delta
            if player.time > Player.CYCLE:
                player.time = 0.0
            #update frame?
            frame = int(player.time / (Player.CYCLE / PLAYER_IMAGE_LENGTH))
            if frame != player.frame:
                player.frame = frame
                if (player.face == 'r'):
                    player.update_image(Player.IMAGES_RIGHT)
                elif (player.face == 'u'):
                    player.update_image(Player.IMAGES_BACK)
                elif (player.face == 'l'):
                    player.update_image(Player.IMAGES_LEFT)
                else:
                    player.update_image(Player.IMAGES_FRONT)"""

    def handleEvents(self):
        for event in PE.get():
            if event.type == PG.QUIT:
                return False
                
            # handle user input
            elif event.type == KEYDOWN:
            # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    Locals.CHANGESTATE = 'Menu'
                    return False;
        return True
                  
# create a game and run it


