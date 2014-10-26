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
        self.font = PF.SysFont('Arial', 25)
        self.text_color = (0,0,0)


    def updateObjective(self, screen, whichText):
        self.updateBanner(screen)
        text = []
        text.append("Objective: Kill all the food people. They're terrible and not nice.")

        if whichText == 0:
            screen.blit(self.font.render(text.pop(), True, self.text_color), (50, 30))
        elif whichText == 1:
            self.lactoseText(screen)
        elif whichText == 2:
            self.killedText(screen)

    def updateBanner(self, screen):
        screen.blit(self.image, (0, 0))

    def lactoseText(self, screen):
        lactose = []
        lactose.append("cheese walls. Look for lactase pills to take to eat through them!")
        lactose.append("You are lactose-intolerant, and therefore you can't eat through")


    def killedText(self, screen):
        self.updateBanner(screen)
        killed = []
        killed.append("pick up it up to use as a weapon!")
        killed.append("You can either eat its corpse-uh-drop-for health or")
        killed.append("You just killed a food person!")

        screen.blit(self.font.render(killed.pop(), True, self.text_color), (50, 30))
