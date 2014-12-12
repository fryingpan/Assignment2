import pygame as PG
import pygame.image as PI
import pygame.time as PT
import sys
import pygame.sprite as PS
import pygame.display as PD
import pygame.color as PC
import pygame.event as PE
import pygame.font as PF
import random
import Globals

from objective import Objective

class Lvl_Data(object):
    def __init__(self, lvl = 1):
        self.music_file = ""
        self.map_file = ""
        self.cutscene = None
        self.objective = None
        self.character_pos_x = 0
        self.character_pos_y = 0
        self.load(lvl)

    def load(self,lvl):
        print(lvl)
        print("load lvl")
        if(lvl == 1):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 1.1):
            print("got to 1.1")
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 1.2):
            print("got to 1.2")
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 2):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfilelvl2.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 2.1):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 2.2):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 3):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfilelvl3.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 3.1):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 3.2):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 4):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfilelvl4.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 4.1):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 4.2):
            self.music_file = "music/gameplay.mod"
            self.map_file = 'mapfile.txt'
            self.cutscene = None
            self.objective = Objective(lvl)
            self.character_pos_x = 100
            self.character_pos_y = 100
        return self.map_file

