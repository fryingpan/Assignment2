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
    def __init__(self, lvl=1, stage=1):
        self.image = PI.load("FPGraphics/specialEffects/objective.png").convert_alpha()
        self.font = PF.SysFont('Arial', 25)
        self.text_color = (0,0,0)
        self.lvl = lvl
        self.stage = stage
        self.current_obj = [] #current obj displaying
        self.lvl_objs = []
        self.loadObjectives(lvl, self.stage)
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

    def loadObjectives(self, lvl, stage):
        objs = []
        if(lvl == 1 and stage == 1):  # Will have at least 2 enemies; need to count eggs...
        #!!!note to self: add lots of egg dudes!!!
            objs.append("Press [n] to see the next part of your ingenious plans.")
            objs.append("Objective: Kill all the food people. They're terrible and not nice.")
            self.lvl_objs.append(objs)
            objs = []#1
            objs.append("You are lactose-intolerant, and therefore you can't eat through")
            objs.append("cheese walls. Look for lactase pills")
            objs.append("and then press [space] near a wall to take to eat through it!")
            self.lvl_objs.append(objs)
            objs = []#2
            objs.append("There are food persons up ahead!")
            objs.append("After you kill them, you can")
            objs.append("eat its corpse-")
            objs.append("uh")
            objs.append("-eat its drop (press [e])-for health")
            objs.append("or pick up it (press [s]) to use for a weapon! (press [a])")
            objs.append("If you want a different item, you first have to drop your")
            objs.append("current item (press [d]).")
            self.lvl_objs.append(objs)
        if(lvl == 1 and stage == 2):  # 0
            objs.append("Ice cream dudes are such a mess!")
            objs.append("They drop nasty ice cream puddles, so be careful where you step.")
            objs.append("You can also pick up [s] their drops to drop your own puddles [a].")
            self.lvl_objs.append(objs)
            objs = []#2
            objs.append("Did you notice that you can shoot lettuce leaves through walls?")
            objs.append("Shooting lettuce bends time and space. [a]")
            objs.append("But you should eat healthy [e] and stuff, too.")
            self.lvl_objs.append(objs)

        if(lvl == 2 and stage == 1):  # 0
            objs.append("Is it getting hot in here, or is it just you?")
            objs.append("Or... It could be those ovens!")
            objs.append("Try your best not to step on the ovens...")
            objs.append("...or it could mean your demise.")
            self.lvl_objs.append(objs)
        if(lvl == 2 and stage == 2):  # burgers
            objs.append("Burgers are one of the toughest food persons!")
            objs.append("Must be because of all the foods they're made of.")
            objs.append("They drop bread, which will speed you up if used (press [s]).")
            objs.append("They also drop meat, which gives you a longer invincibility time.")
            objs.append("And they also drop whole burgers sometimes. Super yummy!")
            objs.append("...Legend has it that eating a burger can be lethal, but eh.")
            objs.append("What else are you going to do.")
            self.lvl_objs.append(objs)

        if(lvl == 3 and stage == 1):  # 0
            objs.append("Lookit that sparkly ice! Wanna take a spin?")
            objs.append("Maybe you shouldn't, 'cus they'll make you slooow.")
            self.lvl_objs.append(objs)
            objs = []
            objs.append("There's a snowstorm 'a comin'.")
            objs.append("A snowstorm of icing, that is.")
            objs.append("Watch out for the evil cupcakes,")
            objs.append("because they send hurricanes of their toppings at you.")
            objs.append("Of course, you can send hurricanes too, if you want.")
            self.lvl_objs.append(objs)


"""
Objective: Kill all the food people. They're terrible and not nice.








"""
