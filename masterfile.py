#Game State Implementation


#Imports


import os
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

PG.init()
#import titlegamestate as Title
import newmenugamestate as Menu
import Setup as Game
import highscores
import title


#Container for global variables
class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None

#Main Executable entry point
def main():
    initialize()
    loop()
    finalize()

def initialize():
    #Creates pygame module and intializes global variables.

    
    passed, failed = PG.init()
    if failed > 0:
        print "warning: %d PyGame modules failed to initialize" % failed
    Globals.SCREEN = PDI.set_mode((1280, 1020), PG.DOUBLEBUF|PG.HWSURFACE)
    Globals.WIDTH = Globals.SCREEN.get_width()
    Globals.HEIGHT = Globals.SCREEN.get_height()
    Globals.FONT = PF.Font(None, 48)
    Globals.STATE = "Title"


def loop():
    gameScore = 0
    while Globals.RUNNING:
    
        if Globals.STATE == "Title":
            title.initialize()
            Globals.STATE = title.Locals.CHANGESTATE
            while Globals.STATE == "Title":
                Globals.STATE = title.Locals.CHANGESTATE
                last = PT.get_ticks()
                elapsed = (PT.get_ticks() - last) / 1000.0
                event = PE.get()
                title.run(elapsed,event)

        elif Globals.STATE == "Game":
            gamerino = Game.Game(.00625)
            Game.initialize()
            Globals.STATE = Game.Locals.CHANGESTATE
            while Globals.STATE == "Game":
                Globals.State = Game.Locals.CHANGESTATE
                interval = 0.005
                if(gamerino.run() == False):
                    Globals.STATE = Game.Locals.CHANGESTATE
            gameScore = Game.Locals.SCORE
            print("gamescore: " + str(gameScore))

        elif Globals.STATE == "Menu":
            Menu.initialize()
            Globals.STATE = Menu.Locals.CHANGESTATE
            while Globals.STATE == "Menu":
                Globals.STATE = Menu.Locals.CHANGESTATE
                last = PT.get_ticks()
                elapsed = (PT.get_ticks() - last) / 1000.0
                event = PE.get()
                if(Menu.run(elapsed,event) == False):
                    return 0
            
        elif Globals.STATE == "Scores":
            highscores.initialize()
            Globals.STATE = highscores.Locals.CHANGESTATE
            if gameScore != 0:
                highscores.Locals.SCORE = gameScore
            while Globals.STATE == "Scores":
                Globals.STATE = highscores.Locals.CHANGESTATE
                last = PT.get_ticks()
                elapsed = (PT.get_ticks() - last) / 1000.0
                event = PE.get()
                highscores.run(elapsed,event)

        

def finalize():
    PG.quit()

if __name__ == "__main__":
    main()
