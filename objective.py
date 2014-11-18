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

    #puts banner and then objective on top
    def drawObjective(self):
        Globals.SCREEN.blit(self.image, (0, 0))
        Globals.SCREEN.blit(self.font.render(self.current_text, True, self.text_color), (50, 30))
        #self.updateBanner()

    def changeObj(self, signID):
        self.current_obj = self.lvl_objs[signID]
        updateBanner()

    def loadObjectives(self, lvl):
        objs = []
        if(lvl == 1):#0
            objs.append("Objective: Kill all the food people. They're terrible and not nice.")
            objs.append("Press 'n' to remember your ingenious plans.")
            self.lvl_objs.append(objs)
            objs = []#1
            objs.append("cheese walls. Look for lactase pills to take to eat through them!")
            objs.append("You are objs-intolerant, and therefore you can't eat through")
            self.lvl_objs.append(objs)
            objs = []#2
            objs.append("-eat its drop-for health or pick up it up for a weapon!")
            objs.append("uh")
            objs.append("eat its corpse-")
            objs.append("You just objs a food person! In celebration, you can")
            self.lvl_objs.append(objs)

    def updateBanner(self): #update text on banner
        # print len(self.current_obj)
        if(len(self.current_obj) > 0):
            self.current_text = self.current_obj.pop()
            # return True if there are still more instructions to show
            if (len(self.current_obj) > 0):
                return True
        # return False if there are no more instructions to show
        return False