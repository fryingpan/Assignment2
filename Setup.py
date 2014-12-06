# Assignment 2
# Frying Pan

try:
    import pygame as PG
    import pygame.image as PI
    from pygame.locals import *
    import pygame.time as PT
    import sys
    from Lvl_Data import Lvl_Data
    from Player import Player
    from IceCream import IceCream
    from Burger import Burger
    from Lettuce import Lettuce
    from Cupcake import Cupcake
    import pad as Pad
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
    import time

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


class Game(object):

    def __init__(self):
        PM.pre_init(44100, -16, 1, 1024)
        PG.init()
        ###(Screen stuff)####
        Globals.SCREEN.fill((255, 255, 255))
        PD.set_caption("Master Chef's wicked adventure " +
                       "with his ice cream buddies")

        ###(Declare interface)#####
        self.font = PF.SysFont('Arial', 25)

        #Win/Lose items
        self.end_time = 100
        self.win_image = PI.load("FPGraphics/" +
                                 "specialEffects/UWIN.png").convert_alpha()
        self.lose_image = PI.load("FPGraphics/" +
                                  "specialEffects/ULOSE.png").convert_alpha()
        self.MAX_LEVEL = 4
        #items
        self.pill_img = PI.load("FPGraphics/tiles/" +
                                "lactasePill.png").convert_alpha()
        ######(Initialize objects on screen)####
        ##draw map/background
        
        ##draw sprites
        self.character = Player(Globals.DELTA)
        self.INVINCIBILITY_TIME =  1000
        self.player_group = PS.GroupSingle(self.character)
        # adding extra since cutscene bug deletes one
        # self.remainingEnemies = self.num_enemies
        #create icecream group
        self.icecream_list = PS.Group()
        self.burger_list = PS.Group()
        self.lettuce_list = PS.Group()
        self.cupcake_list = PS.Group()
        self.enemy_list = PS.Group()  # all enemies
        self.pad_list = PS.Group()
        self.trap_group = PS.Group()
        self.item_group = PS.Group()
        self.projectile_group = PS.Group()

        #allsprites has all dirty sprites (player, enemies, traps, pads)
        self.allsprites = PS.LayeredDirty(self.trap_group,
                                          self.pad_list,
                                          self.item_group,
                                          self.player_group,
                                          self.icecream_list,
                                          self.burger_list,
                                          self.lettuce_list,
                                          self.cupcake_list,
                                          self.projectile_group)
        
        #variables to be handled in change_level method
        self.objective = None
        self.objectiveBlit = True
        self.updated_obj = False
        self.map = None
        self.num_enemies = 0
        self.background = None
        self.end_time = 100
        self.end_image_position = (100, 178)
        self.block_group = None

        ####(Level variables)####
        Globals.INVINCIBILITY_COUNT = 0  # player's invinicibility frame time
        #what kind of enemy by ID (-1 means no enemy) used for collisions
        self.enemy_ID = -1
        #if true, tells map to redraw
        self.map_modified = False

        self.level = 1
        self.change_level(self.level)

#############################
######STUFF WE GOTTA PUT SOMEWHERE##########
#lv1_cutscene = Cutscene(Globals.SCREEN, self.level)
#Must be init only ONCE, figure out where to put later!
##############################

    def update(self):
        ###(variables)####
        trap_attack_player = False  # tells if a trap attacked
        trap_attack_enemy = False
        enemy_attacked = None
        self.enemy_ID = -1

        ###(attacks on player)####
        ##trap handling
        for trap in self.trap_group.sprites():
            if (trap.get_trap_attack_player() and Globals.INVINCIBILITY_COUNT == 0):
                trap_attack_player = True
            if (trap.get_trap_attack_enemy()):
                enemies_attacked = trap.get_enemies_attacked()
                if enemies_attacked is not None:
                    for enemy in enemies_attacked:
                        enemy.decrement_health(1)
            if trap.will_remove():
                self.trap_group.remove(trap)
        ##icecream attacks
        for icecream in self.icecream_list.sprites():
            #see if the enemy will release weapon/attack
            if (icecream.will_attack(self.level)):
                #get a new puddle sprite
                    #sending level through to tell it to make a puddle
                    #with a longer life
                new_trap = icecream.attack(self.map.get_surface(), self.level)
                #add the new trap to the list of traps
                self.trap_group.add(new_trap)

            if(icecream.get_attacked_player() or trap_attack_player):
                if trap_attack_player:
                    trap_attack_player = False
                #if so start invincibility count after attack
                Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = icecream.get_ID()

        ##burger attacks
        for burger in self.burger_list.sprites():
            if(burger.get_attacked_player()):
                #if so start invincibility count after attack
                Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = burger.get_ID()

        projectile_attack_player = False  # tells if a projectile attacked
        projectile_attack_enemy = False

        #lettuce
          ##projectile handling
        for projectile in self.projectile_group.sprites():
            if (projectile.attacked_player and Globals.INVINCIBILITY_COUNT == 0):
                projectile_attack_player = True
            if (projectile.projectile_attack_enemy):
                enemies_attacked = projectile.get_enemies_attacked()
                if enemies_attacked is not None:
                    for enemy in enemies_attacked:
                        enemy.decrement_health(1)
            # if projectile.will_remove():
            #     self.projectile_group.remove(projectile)
        ##lettuce attacks
        for lettuce in self.lettuce_list.sprites():
            #see if the enemy will release weapon/attack
            if (lettuce.will_attack(self.level)):
                #get a new puddle sprite
                new_projectile = lettuce.attack()
                #add the new projectile to the list of projectiles
                self.projectile_group.add(new_projectile)

            if(lettuce.get_attacked_player() or projectile_attack_player):
                if projectile_attack_player:
                    projectile_attack_player = False
                #if so start invincibility count after attack
                Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = lettuce.get_ID()

        ##cupcake attacks
        for cupcake in self.cupcake_list.sprites():
            #see if the enemy will release weapon/attack
            if (cupcake.will_attack(self.level)):
                #get a new puddle sprite
                new_projectile = cupcake.attack()
                #add the new projectile to the list of projectiles
                self.projectile_group.add(new_projectile)

            if(cupcake.get_attacked_player() or projectile_attack_player):
                if projectile_attack_player:
                    projectile_attack_player = False
                #if so start invincibility count after attack
                Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = cupcake.get_ID()


        ##player damage & invincibility handling
        #If enemy attacked the player while player not invincible
        #print("inv " + str(Globals.INVINCIBILITY_COUNT))
        if(self.enemy_ID != -1 and Globals.INVINCIBILITY_COUNT == self.INVINCIBILITY_TIME):
                self.character.decrement_health(self.enemy_ID)
                self.enemy_ID = -1
        #decrement invincibility count if player is in invincibility
        #handles player flashing during invincibility
        if(Globals.INVINCIBILITY_COUNT > 0):
                if(Globals.INVINCIBILITY_COUNT % 50 == 0):
                        self.character.invincibility_frames()
                Globals.INVINCIBILITY_COUNT -= 1

        ######Pad damage here
        for pad in self.pad_list.sprites():
            if pad.rect.colliderect(self.character.rect):
                #DEPENDING ON PAD TYPE, CALL DIFFERENT PAD METHODS
                if pad.type == 0:
                    pad.i_am_hot(self.character)
                elif pad.type == 1:
                    pad.i_am_cold(self.character)


        self.character.handle_keys(self.block_group, self.enemy_list,
                                   self.item_group, self.map.get_surface())

        #get new items from the killed enemies
        new_items = self.character.get_items_of_killed()
        for item in new_items:
            if(item != None):
                self.item_group.add(item)
            #check if any of the items need to be removed (lifetime == 0)
            # if(item != None):
        for item in self.item_group.sprites():
            if item.will_remove():
                self.item_group.remove(item)

        player_traps = self.character.get_player_traps()
        for trap in player_traps:
            self.trap_group.add(trap)
            trap.set_enemy_list(self.enemy_list)
        # for traps in player_traps:
            if trap.will_remove():
                self.character.remove_player_trap(trap)

        #update the allsprites
        self.allsprites = PS.LayeredDirty(self.trap_group,
                                          self.pad_list,
                                          self.item_group,
                                          self.player_group,
                                          self.icecream_list,
                                          self.burger_list,
                                          self.cupcake_list,
                                          self.lettuce_list,
                                          self.projectile_group)

        #cheese/door handling
        if self.character.get_modified_map():
            self.background = self.map.update_background()
            self.map_modified = False
        if self.character.banner != -1: #make sure it doesn't redraw banner already present?
            self.objective.changeObj(self.character.banner)
            self.updated_obj = True #allow banner to be drawn in draw()
            self.character.banner = -1

        #update camera's position on the map
        self.camera_background = self.camera.update(self.character.get_coordinates(),
                           self.map.get_surface())

        self.allsprites.update(self.block_group, self.player_group)

        if(Locals.CHANGESTATE == "Menu"):
                PM.music.fadeout(1000)
                # Globals.SCORE = self.character.score
                return False

        PD.update()  # update the screen

    def render(self):

#        ###(interface stuff)####
#        #adding objective banner here
#        self.objective.updateObjective()
#        ##change so that banner only appears when necessary

        if self.map_modified:
                self.background = self.map.update_background()
                self.map_modified = False

        ##draw dirty sprites
        rects = self.allsprites.draw(self.map.get_surface(), self.background)
        self.draw_screen()
        PG.display.update(rects)

        PD.flip()

    def draw_screen(self):
        Globals.SCREEN.blit(self.camera_background, (0, 0))
        # check if objective banner needs to be drawn to screen
        if self.updated_obj:
            self.objective.drawObjective()

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
                    if(self.level < self.MAX_LEVEL):
                        self.level += 1
                        self.change_level(self.level)
                    elif(self.level == self.MAX_LEVEL):
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
        if (self.character.pill):
            Globals.SCREEN.blit(self.pill_img, (750, 550))

        if self.character.has_item():
            Globals.SCREEN.blit(self.character.get_item_img(), (700, 550))
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
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_1:
                self.level = 1
                self.change_level(self.level)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_2:
                self.level = 2
                self.change_level(self.level)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_3:
                self.level = 3
                self.change_level(self.level)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_4:
                self.level = 4
                self.change_level(self.level)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_n:
                # see if banner still needs to be shown (self.updated_obj gets True)
                self.updated_obj = self.objective.nextBannerTxt() #returns if true if there is more text, false if not
                self.objectiveBlit = False
            else:
                self.objectiveBlit = True
                
    def reset_level(self):
        for item in self.item_group.sprites():
            self.item_group.remove(item)
        for trap in self.trap_group.sprites():
            self.trap_group.remove(trap)
        for proj in self.projectile_group.sprites():
            self.projectile_group.remove(proj)
        for enemy in self.cupcake_list.sprites():
            self.cupcake_list.remove(enemy)
        for enemy in self.icecream_list.sprites():
            self.icecream_list.remove(enemy)
        for enemy in self.burger_list.sprites():
            self.burger_list.remove(enemy)
        for enemy in self.lettuce_list.sprites():
            self.lettuce_list.remove(enemy)

    def change_level(self, currentLevel):
        self.reset_level()
        self.level = currentLevel
        ldata = Lvl_Data(self.level)
        self.objective = ldata.objective
        self.updated_obj = False ######CHANGED
        PM.music.load(ldata.music_file)
        PM.music.play(-1)
        PM.music.set_volume(0.5)
        ####turn back on only for presentations?
        #Cutscene(Globals.SCREEN, self.level)
        
        #interpretting mapfile.txt
        if(self.level > 1):
            del self.map
        Map.GRASS_ARRAY = []
        Map.PAD_ARRAY = []
        self.pad_list.empty()
        ##new map is different than level 1's map, of course.
        self.map = Map.Map(ldata.map_file, self.level)
        self.camera = cam.Camera(self.map.get_surface())
        self.camera_background = None

        self.num_enemies += self.map.get_num_enemies(1)  # icecream
        self.num_enemies += self.map.get_num_enemies(2)  # burger
        self.num_enemies += self.map.get_num_enemies(3)  # lettuce
        self.num_enemies += self.map.get_num_enemies(4)  # cupcake

        #may want to change this to be determined by mapfile.txt
        self.character.rect.x = ldata.character_pos_x
        self.character.rect.y = ldata.character_pos_y

        self.background = self.map.create_background()
        self.allsprites.clear(Globals.SCREEN, self.background)
        Globals.SCREEN.blit(self.background, (0, 0))
        
        PD.update()

        #icecream
        for e in range(self.map.get_num_enemies(1)):
            icecream = IceCream(self.map.get_enemy_coordx(e, 1),
                                self.map.get_enemy_coordy(e, 1))
            self.icecream_list.add(icecream)
        #burger
        for e in range(self.map.get_num_enemies(2)):
            burger = Burger(self.map.get_enemy_coordx(e, 2),
                            self.map.get_enemy_coordy(e, 2),
                            self.level)
            self.burger_list.add(burger)
        #lettuce
        for e in range(self.map.get_num_enemies(3)):
            lettuce = Lettuce(self.map.get_enemy_coordx(e, 3),
                            self.map.get_enemy_coordy(e, 3))
            self.lettuce_list.add(lettuce)
        #cupcake
        for e in range(self.map.get_num_enemies(4)):
            cupcake = Cupcake(self.map.get_enemy_coordx(e, 4),
                            self.map.get_enemy_coordy(e, 4))
            self.cupcake_list.add(cupcake)

        self.enemy_list.add(self.icecream_list)
        self.enemy_list.add(self.burger_list)
        self.enemy_list.add(self.lettuce_list)
        self.enemy_list.add(self.cupcake_list)

        #pads
        for e in range(len(self.map.padtiles)):
            if self.map.pad_type[e] == 0:  # hot
                newPad = Pad.create_Pad(self.map.get_pad_x(e),
                                        self.map.get_pad_y(e), 0)
                self.pad_list.add(newPad)
            elif self.map.pad_type[e] == 1:
                newPad = Pad.create_Pad(self.map.get_pad_x(e),
                                        self.map.get_pad_y(e), 1)
                self.pad_list.add(newPad)

        #get block sprite group from the map file
        self.block_group = self.map.get_object_group()

        #list that holds traps
        self.trap_list = []
        # self.trap_group = PS.Group()

        # self.item_group = PS.Group()

        #allsprites has all dirty sprites (player, enemies, traps)
        self.allsprites = PS.LayeredDirty(self.trap_group,
                                          self.pad_list,
                                          self.item_group,
                                          self.player_group,
                                          self.icecream_list,
                                          self.burger_list,
                                          self.lettuce_list,
                                          self.projectile_group)
        self.allsprites.clear(Globals.SCREEN, self.background)

        ####(Level variables)####
        Globals.INVINCIBILITY_COUNT = 0  # player's invinicibility frame time
        #what kind of enemy by ID (-1 means no enemy) used for collisions
        self.enemy_ID = -1
        #if true, tells map to update w/o key & door
        self.map_modified = False
        ##temp obj conditions
        self.cheesed = True
        self.killed = True
        self.update()
        self.render()

        
