#Drawing Functions
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



def draw_text_box(text, textcolor, boxcolor, x1, x2, y1, y2, ref):

    rect = PG.rect.Rect(x1,y1,(x2-x1),(y2-y1))
    surf = PG.Surface([rect.width,rect.height])
    surf.fill(boxcolor)
    Globals.SCREEN.blit(surf,rect)
    surf = Locals.FONT.render(text, True, textcolor)
    Globals.SCREEN.blit(surf, rect)
    Globals.OBJECTS[ref] = rect
    
    
def draw_box(color,x1,x2,y1,y2,ref):

    rect = PG.rect.Rect(x1,y1,(x2-x1),(y2-y1))
    surf = PG.Surface([rect.width,rect.height])
    surf.fill(color)
    Globals.SCREEN.blit(surf,rect)
    Globals.OBJECTS[ref] = rect
def draw_rect_box(color,rect):

    surf = PG.Surface([rect.width,rect.height])
    surf.fill(color)
    Globals.SCREEN.blit(surf,rect)
    



    
def draw_map(mapfile):
    f = open(mapfile,'r')
    mapLines = list(f)
    f.close()
    
    

    Globals.SCREEN = PDI.get_surface()

    
    
    listLines = list()
    y=0
    for item in mapLines:
        y = y+1
        item=item.strip('n')
        item=item.strip('/')
        charList=list(item)
        listLines.append(charList)
        

    x = len(listLines[0])
 
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
       
        if o == 'WIDTH':
            Globals.WIDTH = int(v)
        elif o == 'HEIGHT':
            Globals.HEIGHT = int(v)



    ###WRONG MATH HERE, NEEDS FIXING### figure out how to import screen dimensions from masterstate
    print x
    rectHeight=100
    print y
    rectWidth=60
    
    rectLeft = 0
    for z in range(0,x-1):
        
        rectTop = 0   
        for q in range(0, y):
            
            
            zS=str(z)
            
            qS=str(q)
           
            newRect = PG.Rect(rectTop,rectLeft,rectHeight,rectWidth)
            Globals.GRID[zS+qS] = newRect
            rectTop = rectTop + rectHeight
           
            Globals.INITIALGRID[zS+qS] = listLines[z][q]
            draw_map_objects(listLines[z][q],zS,qS)
            


            
        rectLeft = rectLeft + rectWidth
  #At this point the grid is a dict of rects, 00 being the first block, 10 being to the right, and 01 being down


def draw_map_objects(char,zS,qS):
    if char == '#':
        draw_rect_box(PC.Color('blue'),Globals.GRID[zS+qS])
    elif char == 'S':
        draw_rect_box(PC.Color('red'),Globals.GRID[zS+qS])

    else:
        return False




    
def main():
    PG.init() #Initialize pygame
    PDI.init() #Initialize display
    Globals.SCREEN = PDI.set_mode((1000, 1000), PG.DOUBLEBUF|PG.HWSURFACE)
    SCREENSURFACE = PDI.get_surface() #Sets SCREEN
    Globals.SCREEN.fill(PC.Color('white'))
    PDI.flip()

    draw_map('mapfile.txt')
    PDI.flip()
    print Globals.GRID
    print Globals.INITIALGRID
    





if __name__ == "__main__":
    main()
