import sys
import pygame as PG
import pygame.sprite as PS
import pygame.display as PD
import pygame.color as PC
import pygame.time as PT
import pygame.event as PE
from Player import Player

PG.init()
screen = PD.set_mode((800, 600))

clock = PT.Clock()

chefGroup = PS.Group()
chefGroup.add(Player())
#make other groups for animated enemies

while True:
    last = PT.get_ticks()

    screen.fill((0,0,0))
    chefGroup.draw(screen)

    clock.tick()

    PD.flip()

    elapsed = (PT.get_ticks() - last) / 1000.0
    chefGroup.update(elapsed)

    for event in PE.get():
        if event.type == PG.QUIT:
            sys.exit()
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            sys.exit()
