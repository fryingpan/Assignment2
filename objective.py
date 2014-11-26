# Assignment 2
# Frying Pan

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

class Objective(object):
    def __init__(self, screen, lvl =1):
        self.image = PI.load("FPGraphics/specialEffects/objective.png").convert_alpha()
        self.font = PF.SysFont('Arial', 25)
        self.text_color = (0,0,0)
        self.lvl = lvl
        self.current_obj = [] #current obj displaying
        self.lvl_objs = []
        self.loadObjectives(lvl)
        self.screen = screen
        self.current_txt_index = 0

    #puts banner and then objective on top
    def drawObjective(self):
        Globals.SCREEN.blit(self.image, (0, 0))
        Globals.SCREEN.blit(self.font.render(self.current_text, True, self.text_color), (50, 30))

    #given the sign ID, change to current obj sign's obj and make obj appear
    #should only be called once when player first reads a sign
    def changeObj(self, signID):
        temp = []
        self.current_obj = self.lvl_objs[signID]
        #space bar's inaccurate sensitivity often calls this method
        #more than once; this check prevents probs
        if(self.current_txt_index == 0):
            self.current_text = self.current_obj[self.current_txt_index]
            self.current_txt_index += 1

    def nextBannerTxt(self): #update text on banner
        if(len(self.current_obj) > self.current_txt_index):
            self.current_text = self.current_obj[self.current_txt_index]
            self.current_txt_index += 1
            # return True if there are still more instructions to show
            return True
            if (len(self.current_obj) > self.current_txt_index):
                return True
        # return False if there are no more instructions to show
        self.current_txt_index = 0
        return False

    def loadObjectives(self, lvl):
        objs = []
        if(lvl == 1):#0
            objs.append("Press 'n' to see the next part of your ingenious plans.")
            objs.append("Objective: Kill all the food people. They're terrible and not nice.")
            self.lvl_objs.append(objs)
            objs = []#1
            objs.append("You are lactose-intolerant, and therefore you can't eat through")
            objs.append("cheese walls. Look for lactase pills to take to eat through them!")
            self.lvl_objs.append(objs)
            objs = []#2
            objs.append("After you kill food persons, in celebration you can")
            objs.append("eat its corpse-")
            objs.append("uh")
            objs.append("-eat its drop-for health or pick up it up for a weapon!")
            self.lvl_objs.append(objs)
