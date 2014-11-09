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
    def __init__(self, screen):
        self.image = PI.load("FPGraphics/specialEffects/objective.png").convert_alpha()
        self.font = PF.SysFont('Arial', 25)
        self.text_color = (0,0,0)
        self.current_obj = []
        self.current_obj.append("")
        self.current_obj.append("Objective: Kill all the food people. They're terrible and not nice.")
        self.current_obj.append("Press 'n' to remember your ingenious plans.")
        self.current_text = self.current_obj.pop()
        self.screen = screen

    #puts banner and then objective on top
    def updateObjective(self):
        Globals.SCREEN.blit(self.image, (0, 0))
        Globals.SCREEN.blit(self.font.render(self.current_text, True, self.text_color), (50, 30))
        #self.updateBanner()

        # if whichText == 0:
        #     self.screen.blit(self.font.render(text.pop(), True, self.text_color), (50, 30))
        #     self.current_obj = text
        # elif whichText == 1:
        #     self.lactoseText()
        # elif whichText == 2:
        #     self.killedText()

    def changeObj(self, whichText):
        if whichText == 0:
            self.screen.blit(self.font.render(text.pop(), True, self.text_color), (50, 30))
            self.current_obj = text
        elif whichText == 1:
            self.lactoseText()
        elif whichText == 2:
            self.killedText()        

    def updateBanner(self):
        # print len(self.current_obj)
        if(len(self.current_obj) > 0):
            #print("banner up")
            #print(str(self.current_obj))
            # self.screen.blit(self.image, (0, 0))
            # self.screen.blit(self.font.render(self.current_obj.pop(), True, self.text_color), (50, 30))
            self.current_text = self.current_obj.pop()
            # return True if there are still more instructions to show
            if (len(self.current_obj) > 0):
                return True
        # return False if there are no more instructions to show
        return False

    def lactoseText(self):
        lactose = []
        lactose.append("")
        lactose.append("cheese walls. Look for lactase pills to take to eat through them!")
        lactose.append("You are lactose-intolerant, and therefore you can't eat through")
        self.current_obj = lactose
        self.updateBanner()

    def killedText(self):
        killed = []
        killed.append("")
        killed.append("-eat its drop-for health or pick up it up for a weapon!")
        killed.append("uh")
        killed.append("eat its corpse-")
        killed.append("You just killed a food person! In celebration, you can")
        self.current_obj = killed
        key = PG.key.get_pressed()
        self.updateBanner()
