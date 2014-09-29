#High Score

#Imports

import sys as SYS
import pygame as PG
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX


class Locals:
    SCREEN = PDI.set_mode((500, 1020), PG.DOUBLEBUF|PG.HWSURFACE)
    FONT = PF.Font(None, 48)
    CHANGESTATE = "Scores"
    f = open('highscore.txt', 'r')
    string = f.read()
    rect = PG.rect.Rect(0,0,0,0)
    


def initialize():
    rect = PG.rect.Rect(0,0,0,0)
    Locals.SCREEN.blit(Locals.FONT.render(Locals.string, True, PC.Color("red")),Locals.rect)
def run():
    Locals.SCREEN.fill(PC.Color("white"))
    Locals.SCREEN.blit(Locals.FONT.render(Locals.string, True, PC.Color("red")),Locals.rect)
    PDI.flip()
