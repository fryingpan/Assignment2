# Assignment 2
# Frying Pan

try:
    import pygame as PG
    import pygame.image as PI
    from pygame.locals import *
    import pygame.time as PT
    import sys
    from Player import Player
    from IceCream import IceCream
    from Burger import Burger
    import pygame.sprite as PS
    import pygame.display as PD
    import pygame.color as PC
    import pygame.event as PE
    import Map
    import camera as cam
    import pygame.font as PF
    import random
    from Trap import Puddle
    from Cutscene import Cutscene
    from objective import Objective
    import pygame.mixer as PM
    import Globals
    import inputbox as inbx

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
    #SCORE = 0


class Game(object):

    def __init__(self):
        PG.init()
        ###(Screen stuff)####
        Globals.SCREEN.fill((255, 255, 255))
        PD.set_caption("Master Chef's wicked adventure " +
                       "with his ice cream buddies")

        ###(Declare interface)#####
        self.objective = Objective(Globals.SCREEN)
        self.updated_obj = True
        PM.music.load("music/gameplay.mod")
        PM.music.play(-1)

        #Globals.SCREEN = PD.set_mode((800, 600))
        #do we use this SCREEN_rect?
#        Globals.SCREEN_rect = Globals.SCREEN.get_rect()
        #fonts
        self.font = PF.SysFont('Arial', 25)

        #Win/Lose items
        self.win_image = PI.load("FPGraphics/" +
                                 "specialEffects/UWIN.png").convert_alpha()
        self.lose_image = PI.load("FPGraphics/" +
                                  "specialEffects/ULOSE.png").convert_alpha()
        self.end_time = 200
        self.end_image_position = (100, 178)
        #items
        self.pill_img = PI.load("FPGraphics/tiles/" +
                                "lactasePill.png").convert_alpha()
        ######(Initialize objects on screen)####
        ##draw map/background
        self.level = 1
        self.map = Map.Map('mapfile.txt', self.level)
        self.background = self.map.create_background()
        self.camera = cam.Camera(self.map.get_surface())
        self.camera_background = None
        ##draw sprites
        self.character = Player(Globals.DELTA)
        self.player_group = PS.GroupSingle(self.character)
        # adding extra since cutscene bug deletes one
        self.num_enemies = 0
        self.num_enemies += self.map.get_num_enemies(1)  # icecream
        self.num_enemies += self.map.get_num_enemies(2)  # burger
        self.remainingEnemies = self.num_enemies
        print("b " + str(self.map.get_num_enemies(2)) + " i " +
              str(self.map.get_num_enemies(1)))
        #create icecream group
        self.icecream_list = PS.Group()
        self.burger_list = PS.Group()
        self.enemy_list = PS.Group()  # all enemies

        #place enemies (icecream)
        for e in range(self.map.get_num_enemies(1)):
            icecream = IceCream(self.map.get_enemy_coordx(e, 1),
                                self.map.get_enemy_coordy(e, 1))
            self.icecream_list.add(icecream)
        #burger
        for e in range(self.map.get_num_enemies(2)):
            burger = Burger(self.map.get_enemy_coordx(e, 2),
                            self.map.get_enemy_coordy(e, 2))
            self.burger_list.add(burger)

        self.enemy_list.add(self.icecream_list)
        self.enemy_list.add(self.burger_list)

        #get block sprite group from the map file
        self.block_group = self.map.get_object_group()

        #list that holds traps
        self.trap_list = []
        self.trap_group = PS.Group()

        self.item_list = []
        self.item_group = PS.Group()

        #allsprites has all dirty sprites (player, enemies, traps)
        self.allsprites = PS.LayeredDirty(self.item_group, 
                                          self.trap_group,
                                          self.player_group,
                                          self.icecream_list,
                                          self.burger_list)
        self.allsprites.clear(Globals.SCREEN, self.background)

        ####(Level variables)####
        self.invincibility_count = 0  # player's invinicibility frame time
        #what kind of enemy by ID (-1 means no enemy) used for collisions
        self.enemy_ID = -1
        #if true, tells map to update w/o key & door
        self.make_disappear = False
        ##temp obj conditions
        self.cheesed = True
        self.killed = True


#############################
######STUFF WE GOTTA PUT SOMEWHERE##########
#lv1_cutscene = Cutscene(Globals.SCREEN, self.level)
#Must be init only ONCE, figure out where to put later!
#music
#-1 loop should loop forever
#        PM.music.play(-1) Put with cutscene
##############################

    def update(self):
        ###(variables)####
        trap_attack = False  # tells if a trap attacked
        self.enemy_ID = -1

        ###(attacks on player)####

        ##trap handling
        for trap in self.trap_list:
                trap.update(None, self.player_group)
                if (trap.get_trap_attack() and self.invincibility_count == 0):
                        trap_attack = True
                if trap.will_remove():
                        self.trap_list.remove(trap)
                        self.trap_group.remove(trap)
                #self.allsprites = PS.LayeredDirty(self.player_group,
                    #self.icecream_list, self.trap_group, self.item_group)
        ##icecream attacks
        for icecream in self.icecream_list.sprites():
                #see if the enemy will release weapon/attack
                if (icecream.will_attack()):
                        #get a new puddle sprite
                        new_trap = icecream.attack(self.map.get_surface())
                        #add the new trap to the list of traps
                        self.trap_list.append(new_trap)
                        self.trap_group.add(new_trap)
                #self.allsprites = PS.LayeredDirty(self.player_group,
                    #self.icecream_list, self.trap_group, self.item_group)

                if(icecream.get_attacked_player() or trap_attack):
                        if trap_attack:
                                trap_attack = False
                        #if so start invincibility count after attack
                        self.invincibility_count = 200
                        #see which enemy attacked the player
                        self.enemy_ID = icecream.get_ID()

#        ##Icecream & puddle attack on player
#        for icecream in self.icecream_list.sprites():
#                #update position and collisions
#                #see if ice cream collided with player
#                if(icecream.get_attacked_player() or trap_attack):
#                        if trap_attack:
#                                trap_attack = False
#                        #if so start invincibility count after attack
#                        self.invincibility_count = 200
#                        #see which enemy attacked the player
#                        self.enemy_ID = icecream.get_ID()

        ##player damage & invincibility handling
        #If enemy attacked the player while player not invincible
        if(self.enemy_ID != -1 and self.invincibility_count == 200):
                self.character.decrement_health(self.enemy_ID)
                self.enemy_ID = -1
        #decrement invincibility count if player is in invincibility
        #handles player flashing during invincibility
        if(self.invincibility_count > 0):
                if(self.invincibility_count % 50 == 0):
                        self.character.invincibility_frames()
                self.invincibility_count -= 1

        self.character.handle_keys(self.block_group, self.enemy_list,
                                   self.item_group, self.map.get_surface())
        #get new items from the killed enemies
        new_items = self.character.get_items_of_killed()
        for item in new_items:
            self.item_list.append(item)
            if(item != None):
                self.item_group.add(item)

        #check if any of the items need to be removed (lifetime == 0)
        for item in self.item_list:
            if(item != None):
                if item.will_remove():
                    self.item_list.remove(item)
                    self.item_group.remove(item)

        player_items = self.character.get_player_items()
        for item in player_items:
            self.item_list.append(item)
            self.item_group.add(item)

        for item in player_items:
            if item.will_remove():
                self.item_list.remove(item)
                self.item_group.remove(item)

        #update the allsprites
        self.allsprites = PS.LayeredDirty(self.item_group, 
                                          self.trap_group,
                                          self.player_group,
                                          self.icecream_list,
                                          self.burger_list)

        #cheese/door handling
        self.make_disappear = self.character.get_open_door()

        if self.make_disappear:
                self.background = self.map.update_background()
                self.make_disappear = False

        #update camera's position on the map
        self.camera_background = self.camera.update(self.character.get_coordinates(),
                           self.map.get_surface())
        #####temporary code to detect for door objective###############
        if(self.character.rect.x > 2200 and self.character.rect.x < 2700
                and self.character.rect.y > 250 and self.character.rect.y < 400
                and self.cheesed is True):
                self.cheesed = False
                self.objective.changeObj(1)

        self.allsprites.update(self.block_group, self.player_group)

        if(Locals.CHANGESTATE == "Menu"):
                PM.music.fadeout(1000)
                # Globals.SCORE = self.character.score
                return False

        #######Pad Handling############
        self.map.pad_hurt_player(self.character)

        PD.update()  # update the screen

    def render(self):

#        ###(interface stuff)####
#        #adding objective banner here
#        self.objective.updateObjective()
#        ##change so that banner only appears when necessary

        if self.make_disappear:
                self.background = self.map.update_background()
                self.make_disappear = False

        ##objective; organize later
        self.remainingEnemies = self.num_enemies - Globals.SCORE
        if self.remainingEnemies < self.num_enemies and self.killed is True:
                self.killed = False
                self.objective.changeObj(2)

        ##draw dirty sprites
        rects = self.allsprites.draw(self.map.get_surface(), self.background)
        self.draw_screen()
        PG.display.update(rects)

        PD.flip()

    def draw_screen(self):
        Globals.SCREEN.blit(self.camera_background, (0, 0))
        # check if objective banner needs to be drawn to screen
        if self.updated_obj:
            self.objective.updateObjective()

        s = "Score: " + str(Globals.SCORE)
        Globals.SCREEN.blit(self.font.render(s, True, (255, 255, 255)),
                            (25, 550))
        s = "Health: " + str(self.character.health)
        Globals.SCREEN.blit(self.font.render(s, True, (255, 255, 255)),
                            (25, 520))

        if(Globals.SCORE == self.num_enemies):  # - 1):
                #^!!!! less than one for cutscene bug
                Globals.SCREEN.blit(self.win_image, self.end_image_position)
                if(self.end_time > 0):
                        self.end_time -= 1
                else:
                        if self.level == 1:
                            self.change_level(self.level)
                        else:
                            PM.music.fadeout(1000)
                            if Globals.SCORE > 0:
                                Globals.PLAYERNAME = str(inbx.ask(
                                    Globals.SCREEN, 'Name'))
                                #Globals.SCORE = self.character.score
                            Globals.STATE = "Menu"
        if(self.character.health <= 0):
                Globals.SCREEN.blit(self.lose_image, self.end_image_position)
                if(self.end_time > 0):
                        self.end_time -= 1
                else:
                        PM.music.fadeout(1000)
                        if Globals.SCORE > 0:
                            Globals.PLAYERNAME = str(inbx.ask(
                                Globals.SCREEN, 'Name'))
                            #Globals.SCORE = self.character.score
                        Globals.STATE = "Menu"
        ##Item Display
        if (self.character.pill is True):
            Globals.SCREEN.blit(self.pill_img, (750, 550))
        ###########################################################
        

    def event(self, event):
        #Allows quitting pygame and changing states
        #added changes for multiple states to allow testing
        for ev in event:
#            if ev.type == PG.QUIT:  # PG.KEYDOWN and ev.key == PG.K_ESCAPE:
#                Globals.RUNNING = False
            if ev.type == PG.KEYDOWN and ev.key == PG.K_ESCAPE:
                #Globals.STATE = 'Menu'
                PM.music.fadeout(1000)
                if Globals.SCORE > 0:
                    Globals.PLAYERNAME = str(inbx.ask(Globals.SCREEN, 'Name'))
                    # Globals.SCORE = self.character.score
                Globals.STATE = 'Menu'
                #Globals.RUNNING = False
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_n:
                # see if banner still needs to be shown (self.updated_obj gets True)
                self.updated_obj = self.objective.updateBanner()

    def change_level(self, currentLevel):
        self.level = 2
        del self.map
        Map.GRASS_ARRAY = []
        Map.PAD_ARRAY = []
        ##new map is different than level 1's map, of course.
        self.map = Map.Map('mapfilelvl2.txt', self.level)

        self.num_enemies += self.map.get_num_enemies(1)  # icecream
        self.num_enemies += self.map.get_num_enemies(2)  # burger
#        self.map.TILES_LOADED = False
#        self.map.GRASS_ARRAY = []
#        self.map.grass_array = self.map.GRASS_ARRAY
#        self.map.grasstiles = []
#        self.map.grass_type = []

        self.end_time = 200
        self.make_disappear = False

        self.character.rect.x = 100
        self.character.rect.y = 100
        self.background = self.map.create_background()
        Globals.SCREEN.blit(self.background, (0, 0))

        PD.update()

        for e in range(self.map.get_num_enemies(1)):
            icecream = IceCream(self.map.get_enemy_coordx(e, 1),
                                self.map.get_enemy_coordy(e, 1))
            self.icecream_list.add(icecream)
        #burger
        for e in range(self.map.get_num_enemies(2)):
            burger = Burger(self.map.get_enemy_coordx(e, 2),
                            self.map.get_enemy_coordy(e, 2))
            self.burger_list.add(burger)

        self.enemy_list.add(self.icecream_list)
        self.enemy_list.add(self.burger_list)

        #get block sprite group from the map file
        self.block_group = self.map.get_object_group()

        #list that holds traps
        self.trap_list = []
        self.trap_group = PS.Group()

        self.item_list = []
        self.item_group = PS.Group()

        #allsprites has all dirty sprites (player, enemies, traps)
        self.allsprites = PS.LayeredDirty(self.player_group,
                                          self.icecream_list,
                                          self.burger_list, self.trap_group,
                                          self.item_group)
        self.allsprites.clear(Globals.SCREEN, self.background)

        ####(Level variables)####
        self.invincibility_count = 0  # player's invinicibility frame time
        #what kind of enemy by ID (-1 means no enemy) used for collisions
        self.enemy_ID = -1
        #if true, tells map to update w/o key & door
        self.make_disappear = False
        ##temp obj conditions
        self.cheesed = True
        self.killed = True
        self.render()
