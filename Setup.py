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
    from Egg import Egg
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
    from joystick import Joystick
    import pygame.joystick as PJ

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
        self.MAX_STAGE = 2
        #items
        self.pill_img = PI.load("FPGraphics/tiles/" +
                                "lactasePill.png").convert_alpha()
        

        ######(Initialize objects on screen)####
        ##draw map/background
        
        ##draw sprites
        self.character = Player(Globals.DELTA)
        self.INVINCIBILITY_TIME = Globals.DEFAULT_INVINCIBILITY
        self.player_group = PS.GroupSingle(self.character)
        # adding extra since cutscene bug deletes one
        # self.remainingEnemies = self.num_enemies
        #create icecream group
        self.icecream_list = PS.Group()
        self.burger_list = PS.Group()
        self.egg_list = PS.Group()
        self.lettuce_list = PS.Group()
        self.cupcake_list = PS.Group()
        self.enemy_list = PS.Group()  # all enemies
        self.pad_list = PS.Group()
        self.trap_group = PS.Group()
        self.item_group = PS.Group()
        self.projectile_group = PS.Group()
        self.enemies = None

        #allsprites has all dirty sprites (player, enemies, traps, pads)
        self.allsprites = PS.LayeredDirty(self.trap_group,
                                          self.pad_list,
                                          self.item_group,
                                          self.player_group,
                                          self.icecream_list,
                                          self.burger_list,
                                          self.egg_list,
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

        # self.level = 1
        # self.stage = 1
        self.level = 1
        self.stage = 1
        self.change_level(self.level, self.stage)
        self.burn_player = False

        ####Joystick#########
        self.joy = Joystick()
        self.use_joy = str(inbx.ask(Globals.SCREEN, 'Joystick? y/n'))


        self.score_health_background = PI.load("FPGraphics/specialEffects/ScoreHealth.png").convert_alpha()
        self.items_table = PI.load("FPGraphics/specialEffects/ItemsTable.png").convert_alpha()
        #will revert to KEYBOARD if anything else is entered.

#############################
######STUFF WE GOTTA PUT SOMEWHERE##########
#lv1_cutscene = Cutscene(Globals.SCREEN, self.level)
#Must be init only ONCE, figure out where to put later!
##############################

    def update(self):
        ###(variables)####
        trap_attack_player = False  # tells if a trap attacked
        trap_attack_enemy = False
        projectile_attack_player = False  # tells if a projectile attacked
        projectile_attack_enemy = False
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
                if Globals.INVINCIBILITY_COUNT == 0:
                    Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = icecream.get_ID()

        

        #lettuce
          ##projectile handling
        for projectile in self.projectile_group.sprites():
            if (projectile.attacked_player and Globals.INVINCIBILITY_COUNT == 0):
                projectile_attack_player = True
                projectile.attacked_player = False
                break
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
                if Globals.INVINCIBILITY_COUNT == 0:
                    Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = lettuce.get_ID()

##burger attacks
        for burger in self.burger_list.sprites():
            #see if the enemy will release weapon/attack
            if (burger.will_attack(self.level)):
                #get a new puddle sprite
                new_projectile = burger.attack()
                #add the new projectile to the list of projectiles
                self.projectile_group.add(new_projectile)

            if(burger.get_attacked_player() or projectile_attack_player):
                if projectile_attack_player:
                    projectile_attack_player = False
                #if so start invincibility count after attack
                if Globals.INVINCIBILITY_COUNT == 0:
                    Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = burger.get_ID()

##egg attacks
        for egg in self.egg_list.sprites():
            if(egg.get_attacked_player()):
                if Globals.INVINCIBILITY_COUNT == 0:
                    Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = egg.get_ID()

        ##cupcake attacks
        for cupcake in self.cupcake_list.sprites():
            #see if the enemy will release weapon/attack
            if cupcake.will_attack(self.level):
                #get a new puddle sprite
                new_projectile = cupcake.attack()
                #add the new projectile to the list of projectiles
                self.projectile_group.add(new_projectile)

            if(cupcake.get_attacked_player() or projectile_attack_player):
                if projectile_attack_player:
                    projectile_attack_player = False
                #if so start invincibility count after attack
                if Globals.INVINCIBILITY_COUNT == 0:
                    Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                #see which enemy attacked the player
                self.enemy_ID = cupcake.get_ID()

        self.burn_player =  False
        ######Pad damage here
        for pad in self.pad_list.sprites():
            if pad.rect.colliderect(self.character.rect):
                #DEPENDING ON PAD TYPE, CALL DIFFERENT PAD METHODS
                if pad.type == 0:
                    # pad.i_am_hot(self.character)
                    self.burn_player = pad.will_burn()
                    if self.burn_player and Globals.INVINCIBILITY_COUNT == 0:
                        Globals.INVINCIBILITY_COUNT = self.INVINCIBILITY_TIME
                elif pad.type == 1:
                    pad.i_am_cold(self.character)

        ##player damage & invincibility handling
        #If enemy attacked the player while player not invincible
        if((self.enemy_ID != -1 or self.burn_player) and Globals.INVINCIBILITY_COUNT == self.INVINCIBILITY_TIME):
            self.character.decrement_health(self.enemy_ID)
            self.enemy_ID = -1
            self.burn_player = False
        #decrement invincibility count if player is in invincibility
        #handles player flashing during invincibility
        if(Globals.INVINCIBILITY_COUNT > 0):
            if(Globals.INVINCIBILITY_COUNT % 50 == 0):
                self.character.invincibility_frames()
            Globals.INVINCIBILITY_COUNT -= 1

        ###Joystick
        if self.use_joy == 'y':
            self.character.handle_joy(self.block_group, self.enemy_list,
                                      self.item_group, self.map.get_surface())
        else:
            self.character.handle_keys(self.block_group, self.enemy_list,
                                       self.item_group, self.map.get_surface())


        if self.character.chng_invincibility():
            self.INVINCIBILITY_TIME = self.character.get_invincibility()


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

        player_projectiles = self.character.get_player_projectiles()
        for projectile in player_projectiles:
            self.projectile_group.add(projectile)
            projectile.set_enemy_list(self.enemy_list)

        #update the allsprites
        self.allsprites = PS.LayeredDirty(self.trap_group,
                                          self.pad_list,
                                          self.item_group,
                                          self.player_group,
                                          self.icecream_list,
                                          self.burger_list,
                                          self.egg_list,
                                          self.cupcake_list,
                                          self.lettuce_list,
                                          self.projectile_group)

        #cheese/door handling
        if self.character.get_modified_map():
            self.background = self.map.update_background()
            self.map_modified = False
        if self.character.banner != -1: #make sure it doesn't redraw banner already presen t?
            self.objective.changeObj(self.character.banner)
            self.updated_obj = True #allow banner to be drawn in draw()
            self.character.banner = -1

        #update camera's position on the map
        if self.character.update_camera():
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
        PD.update(rects)

        PD.flip()

    def draw_screen(self):
        Globals.SCREEN.blit(self.camera_background, (0, 0))
        # check if objective banner needs to be drawn to screen
        if self.updated_obj:
            self.objective.drawObjective()

        Globals.SCREEN.blit(self.score_health_background, (5, 510))
        Globals.SCREEN.blit(self.items_table, (645, 545))

        s = "Score: " + str(Globals.SCORE)
        Globals.SCREEN.blit(self.font.render(s, True, (0, 0, 0)),
                            (25, 550))
        s = "Health: " + str(self.character.health)
        Globals.SCREEN.blit(self.font.render(s, True, (0, 0, 0)),
                            (25, 520))

        if(Globals.SCORE == self.num_enemies):  # - 1):
                level = self.level
                #^!!!! less than one for cutscene bug
                Globals.SCREEN.blit(self.win_image, self.end_image_position)
                #print(self.end_time)
                if(self.end_time > 0):
                        self.end_time -= 1
                else:
                    
                    if(self.level <= self.MAX_LEVEL):
                        if self.stage < self.MAX_STAGE:
                            self.stage += 1
                        else: 
                            self.level += 1
                            self.stage = 1
                        if(self.level == self.MAX_LEVEL + 1):
                            PM.music.fadeout(1000)
                            if Globals.SCORE > 0:
                                Globals.PLAYERNAME = str(inbx.ask(
                                    Globals.SCREEN, 'Name'))
                                #Globals.SCORE = self.character.score
                                Cutscene(Globals.SCREEN, 5)
                            Globals.STATE = "Menu"
                        else:
                            self.change_level(self.level, self.stage)
                    # elif(self.level == self.MAX_LEVEL and self.stage == self.MAX_STAGE):
                        

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
            Globals.SCREEN.blit(self.character.get_item_img(), (650, 550))
            #PG.draw.circle(Globals.SCREEN, (255,255,255), (720,570), 12)
            if(self.character.is_item_usable() and self.character.item_use_count != -1):
                Globals.SCREEN.blit(self.font.render("x" + str(self.character.item_use_count), True, (0, 0, 0)),
                                (700, 570))
        ###########################################################
        

    def event(self, event):
#        ##joysticks
#            ##self.joy = Joystick()
#        while not self.joy.quit_attempt:
#            self.interaction_phase(Globals.SCREEN, self.character, self.joy)

       #Allows quitting pygame and changing states
        #added changes for multiple states to allow testing
        for ev in event:
            if ev.type in Joystick.JOYSTICK:  # only care about objective switching
                if ev.type == PG.JOYBUTTONUP:
                    self.joy.buttons[ev.button] = False
                elif ev.type == PG.JOYBUTTONDOWN:
                    self.joy.buttons[ev.button] = True

            if ev.type == PG.KEYDOWN and ev.key == PG.K_ESCAPE:
                #Globals.STATE = 'Menu'
                PM.music.fadeout(1000)
                if Globals.SCORE > 0:
                    Globals.PLAYERNAME = str(inbx.ask(Globals.SCREEN, 'Name'))
                    # Globals.SCORE = self.character.score
                Globals.STATE = 'Menu'
                #Globals.RUNNING = False
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_1:
                level = 1
                self.stage = 1
                self.change_level(level, self.stage)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_2:
                level = 2
                self.stage = 1
                self.change_level(level, self.stage)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_3:
                level = 3
                self.stage = 1
                self.change_level(level, self.stage)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_4:
                level = 4
                self.stage = 1
                self.change_level(level, self.stage)
            elif ev.type == PG.KEYDOWN and ev.key == PG.K_5:
                Cutscene(Globals.SCREEN, 5)
                Globals.STATE = "Menu"
            elif (ev.type == PG.KEYDOWN and ev.key == PG.K_p):
                Globals.SCORE = self.num_enemies
            elif (ev.type == PG.KEYDOWN and ev.key == PG.K_n):
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
        for enemy in self.egg_list.sprites():
            self.egg_list.remove(enemy)
        for enemy in self.lettuce_list.sprites():
            self.lettuce_list.remove(enemy)

        # A PS Group
        self.enemy_list.empty()


    def change_level(self, currentLevel, stage):
        self.reset_level()
        self.level = currentLevel
        self.stage = stage
        ldata = Lvl_Data(self.level, stage)
        self.objective = ldata.objective
        self.updated_obj = False ######CHANGED
        PM.music.load(ldata.music_file)
        PM.music.play(-1)
        PM.music.set_volume(0.5)
        ####turn back on only for presentations?
        if self.stage == 1:
            Cutscene(Globals.SCREEN, self.level)
        
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

        self.background = self.map.create_background()
        self.allsprites.clear(Globals.SCREEN, self.background)
        Globals.SCREEN.blit(self.background, (0, 0))
        
        PD.update()

        self.num_enemies += self.map.get_num_enemies(1)  # icecream
        self.num_enemies += self.map.get_num_enemies(2)  # burger
        self.num_enemies += self.map.get_num_enemies(3)  # lettuce
        self.num_enemies += self.map.get_num_enemies(4)  # cupcake
        self.num_enemies += self.map.get_num_enemies(5)  # egg

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
        #egg
        for e in range(self.map.get_num_enemies(5)):
            egg = Egg(self.map.get_enemy_coordx(e, 5),
                            self.map.get_enemy_coordy(e, 5),
                            self.level)
            self.egg_list.add(egg)

        self.enemy_list.add(self.icecream_list)
        self.enemy_list.add(self.burger_list)
        self.enemy_list.add(self.lettuce_list)
        self.enemy_list.add(self.cupcake_list)
        self.enemy_list.add(self.egg_list)

        player_health = 0
        #get enemy health
        if self.stage > 1:
            player_health = self.character.get_health()

        self.character = Player(Globals.DELTA)
        self.player_group = PS.GroupSingle(self.character)

        if self.stage > 1:
            self.character.set_health(player_health, True)

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
                                          self.egg_list,
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
        self.camera_background = self.camera.update(self.character.get_coordinates(),
                               self.map.get_surface())


        
