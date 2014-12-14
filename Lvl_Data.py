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
    def __init__(self, lvl = 1, stage=1):
        self.music_file = ""
        self.map_file = ""
        self.cutscene = None
        self.objective = None
        self.character_pos_x = 0
        self.character_pos_y = 0
        self.load(lvl, stage)

    def load(self,lvl, stage):
        if(lvl == 1):
            if stage == 1:
                self.map_file = 'mapfile.txt'
            elif stage == 2 :
                self.map_file = 'mapfile.txt'
            elif stage == 3:
                self.map_file = 'mapfile.txt'
            self.music_file = "music/gameplay.mod"
            self.cutscene = None
            self.objective = Objective(lvl, stage)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 2):
            if stage == 1:
                self.map_file = 'mapfilelvl2.txt'
            elif stage == 2:
                self.map_file = 'mapfilelvl2.txt'
            elif stage == 3:
                self.map_file = 'mapfilelvl2.txt'
            self.music_file = "music/gameplay.mod"
            self.cutscene = None
            self.objective = Objective(lvl, stage)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 3):
            if stage == 1:
                self.map_file = 'mapfilelvl3.txt'
            elif stage == 2:
                self.map_file = 'mapfilelvl3.txt'
            elif stage == 3:
                self.map_file = 'mapfilelvl3.txt'
            self.music_file = "music/gameplay.mod"
            self.cutscene = None
            self.objective = Objective(lvl, stage)
            self.character_pos_x = 100
            self.character_pos_y = 100
        elif(lvl == 4):
            if stage == 1:
                self.map_file = 'mapfilelvl4.txt'
            elif stage == 2:
                self.map_file = 'mapfilelvl4.txt'
            elif stage == 3:
                self.map_file = 'mapfilelvl4.txt'
            self.music_file = "music/gameplay.mod"
            self.cutscene = None
            self.objective = Objective(lvl, stage)
            self.character_pos_x = 100
            self.character_pos_y = 100
        return self.map_file

