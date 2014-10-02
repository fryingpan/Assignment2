#New Master State control file

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


import drawing as Draw



##################Container for Variables (Global Level)########
class Globals(object):
    SCREEN = None #Surface
    SCREENSURFACE = None
    OPTIONS = None #Options list from options.txt
    WIDTH = None
    HEIGHT = None
    STATE = None
    RUNNING = None
    OBJECTS = {'None': None }
    GRID = {'Null':0}
    INITIALGRID = {'Null':0}


####################Main Executable Loop#######################

#Main function, code enters here.
def main():
    
    initialize()
    
    #loop()
    
    #finalize()

#Initialize function. Creates Screen(surface) and assigns to SCREEN
#Other: Sets WIDTH and HEIGHT from options.txt   
def initialize():
    RUNNING=True

####option file opening####
    f = open('options.txt', 'r')
    Globals.OPTIONS = list(f)
    for item in Globals.OPTIONS:
        strList=item.split("= ")
        if strList[0] != "\n":
            o = strList[0]
        v = strList[1]
        v = v.rstrip()
        v = v.rstrip('n')
        v = v.rstrip('/')
        print o
        print v
        if o == 'WIDTH':
            Globals.WIDTH = int(v)
        elif o == 'HEIGHT':
            Globals.HEIGHT = int(v)
    
    
#Creation of screen#
    PG.init() #Initialize pygame
    PDI.init() #Initialize display
    Globals.SCREEN = PDI.set_mode((Globals.WIDTH, Globals.HEIGHT), PG.DOUBLEBUF|PG.HWSURFACE)
    Globals.SCREENSURFACE = PDI.get_surface() #Sets SCREEN
    Globals.SCREEN.fill(PC.Color('white'))
    PDI.flip()

#This is a test for rendering the map from drawing.py
    print Globals.WIDTH
    print Globals.HEIGHT
    Draw.draw_map('mapfile.txt')
    PDI.flip()
    print Globals.OBJECTS



#def loop():
    #while Globals.RUNNING = True:
        
        #Globals.STATE.run()

#def finalize():
    #PDI.quit()
    #PG.quit()
    #print ("Finished")































if __name__ == "__main__":
    main()
