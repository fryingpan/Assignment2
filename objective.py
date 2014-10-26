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

class Objective(object):
    def __init__(self):
        self.image = PI.load("FPGraphics/specialEffects/objective.png").convert_alpha()


    def updateObjective(self, whichText):
        text = []
        text.append("Objective: Kill all the food people. They're terrible and not nice.")

        if whichText == 0:


    def lactoseText(self, screen):

    def killedText(self, screen):
        killed = []
        killed.append("pick up it up to use as a weapon!"
        killed.append("You can either eat its corpse-uh-drop-for health or")
        killed.append("You just killed a food person!")
