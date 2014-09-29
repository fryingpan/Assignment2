#Game State Implementation


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


PG.init()
#import titlegamestate as Title
import newmenugamestate as Menu
import Setup as Game


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
    print(1)
    loop()
    print(2)
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
    Globals.STATE = "Menu"

def loop():
    while Globals.RUNNING:
    
        if Globals.STATE == "Title":
            Title.initialize()
            Globals.STATE = Title.Locals.STATE
            print(3)
            while Globals.STATE == "Title":
                Globals.STATE = Title.Locals.CHANGESTATE
                print (Globals.STATE)
                last = PT.get_ticks()
                elapsed = (PT.get_ticks() - last) / 1000.0
                event = PE.get()
                Title.run(elapsed,event)

        elif Globals.STATE == "Game":
            gamerino = Game.Game(0.005, 40, 13)
            while Globals.STATE == "Game":


                num_enemies = 13
                interval = 0.005
                fps = 40
                if(gamerino.run() == False):
                    return 0


        elif Globals.STATE == "Menu":
            print (Globals.STATE)
            Menu.initialize()
            Globals.STATE = Menu.Locals.CHANGESTATE
            print(3)
            while Globals.STATE == "Menu":
                Globals.STATE = Menu.Locals.CHANGESTATE
                #print(Globals.STATE)
                last = PT.get_ticks()
                elapsed = (PT.get_ticks() - last) / 1000.0
                event = PE.get()
                if(Menu.run(elapsed,event) == False):
                    return 0
            
        elif Globals.STATE == "Scores":
            Scores.run(elapsed,event)
        

def finalize():
    PG.quit()

if __name__ == "__main__":
    main()
