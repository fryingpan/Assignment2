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
    SCORE = 0


class Game(object):

    def __init__(self):
        PG.init()
        ###(Screen stuff)####
        Globals.SCREEN.fill((255, 255, 255))
        PD.set_caption("Master Chef's wicked adventure " +
                       "with his ice cream buddies")


        ###(Declare interface)#####
        self.objective = Objective(Globals.SCREEN)
        PM.music.load("music/gameplay.mod")

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
        self.end_time = 100
        self.end_image_position = (100, 178)
        #items 
        self.pill_img = PI.load("FPGraphics/tiles/" +
                                 "lactasePill.png").convert_alpha()
        ######(Initialize objects on screen)####
        ##draw map/background
        self.map = Map.Map('mapfile.txt')
        self.background = self.map.create_background()
        self.camera = cam.Camera(self.map.get_surface())
        ##draw sprites
        self.character = Player(Globals.DELTA)
        #Locals.SCORE = self.character.score
        self.player_group = PS.GroupSingle(self.character)
        self.num_enemies = self.map.get_num_enemies(1)  # adding extra since cutscene bug deletes one
        self.remainingEnemies = self.num_enemies
        #create icecream group
        self.icecream_list = PS.Group()


        #place enemies (icecream)
        for e in range(self.map.get_num_enemies(1)):
            icecream = IceCream(self.map.get_enemy_coordx(e), self.map.get_enemy_coordy(e))
            self.icecream_list.add(icecream)

        #get block sprite group from the map file
        self.block_group = self.map.get_object_group()

        #list that holds traps
        self.trap_list = []
        self.trap_group = PS.Group()

        self.item_list = []
        self.item_group = PS.Group()

        #allsprites has all dirty sprites (player, enemies, traps)
        self.allsprites = PS.LayeredDirty(self.player_group, self.icecream_list, self.trap_group, self.item_group)
        self.allsprites.clear(Globals.SCREEN, self.background)

        ####(Level variables)####
        self.invincibility_count = 0 #player's invinicibility frame time
        self.enemy_ID = -1  # what kind of enemy by ID (-1 means no enemy) used for collisions
        self.make_disappear = False #if true, tells map to update w/o key & door
        ##temp obj conditions
        self.cheesed = True
        self.killed = True

#############################
######STUFF WE GOTTA PUT SOMEWHERE##########
#lv1_cutscene = Cutscene(Globals.SCREEN,1) Must be init only ONCE, figure out where to put later!
#music
#-1 loop should loop forever
#        PM.music.play(-1) Put with cutscene
##############################


    def update(self):
        ###(variables)####
        trap_attack = False #tells if a trap attacked
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
                # self.allsprites = PS.LayeredDirty(self.player_group, self.icecream_list, self.trap_group, self.item_group)
        ##icecream attacks
        for icecream in self.icecream_list.sprites():
                #see if the enemy will release weapon/attack
                if (icecream.will_attack()):
                        #get a new puddle sprite
                        new_trap = icecream.attack(self.map.get_surface())
                        #add the new trap to the list of traps
                        self.trap_list.append(new_trap)
                        self.trap_group.add(new_trap)
                # self.allsprites = PS.LayeredDirty(self.player_group, self.icecream_list, self.trap_group, self.item_group)

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

        self.character.handle_keys(self.block_group, self.icecream_list, self.item_group, self.map.get_surface()) #self.interval)
        #get new items from the killed enemies
        new_items = self.character.get_items_of_killed()
        for item in new_items:
            self.item_list.append(item)
            self.item_group.add(item)

        #check if any of the items need to be removed (lifetime == 0)
        for item in self.item_list:
            if item.will_remove():
                self.item_list.remove(item)
                self.item_group.remove(item)

        player_items = self.character.get_player_items()
        for item in player_items:
            self.item_list.append(item)
            self.item_group.add(item)

        #update the allsprites    
        self.allsprites = PS.LayeredDirty(self.player_group, self.icecream_list, self.trap_group, self.item_group)



        #cheese/door handling
        self.make_disappear = self.character.get_open_door()

        if self.make_disappear:
                self.background = self.map.update_background()
                self.make_disappear = False


        #update camera's position on the map
        background = self.camera.update(self.character.get_coordinates(),
                                                                        Globals.SCREEN, self.map.get_surface()
                                                                        )
        # print(self.character.get_coordinates())
        #####temporary code to detect for door objective###############
        if(self.character.rect.x > 2200 and self.character.rect.x < 2700
                and self.character.rect.y > 250 and self.character.rect.y < 400
                and self.cheesed == True):
                self.cheesed = False
                self.objective.changeObj(1)

        self.allsprites.update(self.block_group, self.player_group)

        Locals.SCORE = self.character.score
        if(Locals.CHANGESTATE == "Menu"):
                PM.music.fadeout(1000)
                return False

        ###WAS IN RENDER BUT WORKS BETTER IN UPDATE####
        #adding objective banner here
        self.objective.updateObjective() ##change so that banner only appears when necessary

        s = "Score: " + str(self.character.score)
        Globals.SCREEN.blit(self.font.render(s, True, (255, 255, 255)),
                                         (25, 550))
        s = "Health: " + str(self.character.health)
        Globals.SCREEN.blit(self.font.render(s, True, (255, 255, 255)),
                                         (25, 520))

        if(self.character.score == self.num_enemies - 1): #!!!! less than one for cutscene bug
                Globals.SCREEN.blit(self.win_image, self.end_image_position)
                if(self.end_time > 0):
                        self.end_time -= 1
                else:
                        PM.music.fadeout(1000)
                        Globals.STATE = "Menu"
        if(self.character.health <= 0):
                Globals.SCREEN.blit(self.lose_image, self.end_image_position)
                if(self.end_time > 0):
                        self.end_time -= 1
                else:

                        PM.music.fadeout(1000)
                        Globals.STATE = "Menu"
        ##Item Display
        if (self.character.pill == True):
            Globals.SCREEN.blit(self.pill_img, (750,550))
        ###########################################################

        PD.update()  # update the screen

    def render(self):

#        ###(interface stuff)####
#        #adding objective banner here
#        self.objective.updateObjective() ##change so that banner only appears when necessary


        if self.make_disappear:
                self.background = self.map.update_background()
                self.make_disappear = False

        ##objective; organize later
        self.remainingEnemies = self.num_enemies - self.character.score
        if self.remainingEnemies < self.num_enemies and self.killed == True:
                self.killed = False
                self.objective.changeObj(2)

        ##draw dirty sprites
        rects = self.allsprites.draw(self.map.get_surface(), self.background)
        PG.display.update(rects)

#        if(self.character.score == self.num_enemies - 1): #!!!! less than one for cutscene bug
#                Globals.SCREEN.blit(self.win_image, self.end_image_position)
#                if(self.end_time > 0):
#                        self.end_time -= 1
#                else:
#                        PM.music.fadeout(1000)
#                        Globals.STATE = "Menu"
#        if(self.character.health <= 0):
#                Globals.SCREEN.blit(self.lose_image, self.end_image_position)
#                if(self.end_time > 0):
#                        self.end_time -= 1
#                else:

#                        PM.music.fadeout(1000)
#                        Globals.STATE = "Menu"

#        s = "Score: " + str(self.character.score)
#        Globals.SCREEN.blit(self.font.render(s, True, (255, 255, 255)),
#                                         (25, 550))
#        s = "Health: " + str(self.character.health)
#        Globals.SCREEN.blit(self.font.render(s, True, (255, 255, 255)),
#                                         (25, 520))

        PD.flip()

    def event(self, event):
        #Allows quitting pygame and changing states
        #added changes for multiple states to allow testing
        for ev in event:
#            if ev.type == PG.QUIT:  # PG.KEYDOWN and ev.key == PG.K_ESCAPE:
#                Globals.RUNNING = False
            if ev.type == PG.KEYDOWN and ev.key == PG.K_ESCAPE:
                #Globals.STATE = 'Menu'
                PM.music.fadeout(1000)
                Globals.STATE = 'Menu'
                #Globals.RUNNING = False
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_n:
                self.objective.updateBanner()


