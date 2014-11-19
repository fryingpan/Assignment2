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
        # self.current_text = self.current_obj.pop()
        self.screen = screen
        self.objPopped = 0

    #puts banner and then objective on top
    def drawObjective(self):
        Globals.SCREEN.blit(self.image, (0, 0))
        Globals.SCREEN.blit(self.font.render(self.current_text, True, self.text_color), (50, 30))
        #self.popNextBannerTxt()

    def changeObj(self, signID):
        temp = []
        print("signID " + str(signID))
        for a in self.lvl_objs[signID]:
            temp.append(a)
        self.current_obj = temp
        print("CURRENT LENGTH " + str(len(self.current_obj)))
        if(self.objPopped == 0):
            self.popNextBannerTxt();
            self.objPopped += 1

    def popNextBannerTxt(self): #update text on banner
        # print len(self.current_obj)
        if(len(self.current_obj) > 0):
            self.current_text = self.current_obj.pop()
            # return True if there are still more instructions to show
            if (len(self.current_obj) > 0):
                return True
        # return False if there are no more instructions to show
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