##Mapper##

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
import random




##Main function test##
def main():
    PG.init()
    PDI.init()
    screen=PDI.set_mode((1280,1000))
    running = True
    mapper=Mapper(testmap,resolution)
    mapper.create_grid()
    while running:
        for event in PE.get():
            if event.type == PG.QUIT:
                running = False
            elif event.type == PG.KEYDOWN:
                if event.key == PG.K_ESCAPE:
                    running = False
        screen.fill(PC.Color('white'))
        allsprites.draw(screen)
        PDI.flip()
    PDI.quit()
    PG.quit()














##Maps## For ease of drawing, maps are multiplied by a x10 factor for tiles
######## This means each tile in the map below represents one 10x10 tile in terms of images

#  #=Wall
#  .=Floor
#  S=Start
#  F=Finish

##Testmap

images = dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
wall=PI.load('wall.png')
images['wall']=wall
floor=PI.load('floor.png')
images['floor']=floor

resolution=[1280,1000]

allsprites=PS.Group()

testmap = [
    ("####################"),
    ("#S...#...#...#.....#"),
    ("#..###...#...#.....#"),
    ("#....#.............#"),
    ("#....#.......#######"),
    ("#.......#..........#"),
    ("#....##########....#"),
    ("#....#........#....#"),
    ("#....#..........#..#"),
    ("#....####..####..#.#"),
    ("#....#........#..###"),
    ("#.............##..F#"),
    ("#..............#...#"),
    ("#..............#...#"),
    ("####################")
    ]
#20Wx15H

#Holds subgrids, which are sprites with a grid location.
class Grid(object):
    def __init__(self, xIndex,yIndex,gridtype,gridw,gridh):
        
        self.TYPE=gridtype
        self.WIDTH=gridw
        self.HEIGHT=gridh
        self.XINDEX=xIndex
        self.YINDEX=yIndex
        self.XSTART=xIndex*gridw
        self.YSTART=yIndex*gridw
       
        self.SUBGRIDS=[(SubGrid(self,0,0)),(SubGrid(self,1,0)),(SubGrid(self,2,0)),(SubGrid(self,3,0)),(SubGrid(self,4,0)),(SubGrid(self,5,0)),(SubGrid(self,6,0)),(SubGrid(self,7,0)),(SubGrid(self,8,0)),(SubGrid(self,9,0)),
                       (SubGrid(self,0,1)),(SubGrid(self,1,1)),(SubGrid(self,2,1)),(SubGrid(self,3,1)),(SubGrid(self,4,1)),(SubGrid(self,5,1)),(SubGrid(self,6,1)),(SubGrid(self,7,1)),(SubGrid(self,8,1)),(SubGrid(self,9,1)),
                       (SubGrid(self,0,2)),(SubGrid(self,1,2)),(SubGrid(self,2,2)),(SubGrid(self,3,2)),(SubGrid(self,4,2)),(SubGrid(self,5,2)),(SubGrid(self,6,2)),(SubGrid(self,7,2)),(SubGrid(self,8,2)),(SubGrid(self,9,2)),
                       (SubGrid(self,0,3)),(SubGrid(self,1,3)),(SubGrid(self,2,3)),(SubGrid(self,3,3)),(SubGrid(self,4,3)),(SubGrid(self,5,3)),(SubGrid(self,6,3)),(SubGrid(self,7,3)),(SubGrid(self,8,3)),(SubGrid(self,9,3)),
                       (SubGrid(self,0,4)),(SubGrid(self,1,4)),(SubGrid(self,2,4)),(SubGrid(self,3,4)),(SubGrid(self,4,4)),(SubGrid(self,5,4)),(SubGrid(self,6,4)),(SubGrid(self,7,4)),(SubGrid(self,8,4)),(SubGrid(self,9,4)),
                       (SubGrid(self,0,5)),(SubGrid(self,1,5)),(SubGrid(self,2,5)),(SubGrid(self,3,5)),(SubGrid(self,4,5)),(SubGrid(self,5,5)),(SubGrid(self,6,5)),(SubGrid(self,7,5)),(SubGrid(self,8,5)),(SubGrid(self,9,5)),
                       (SubGrid(self,0,6)),(SubGrid(self,1,6)),(SubGrid(self,2,6)),(SubGrid(self,3,6)),(SubGrid(self,4,6)),(SubGrid(self,5,6)),(SubGrid(self,6,6)),(SubGrid(self,7,6)),(SubGrid(self,8,6)),(SubGrid(self,9,6)),
                       (SubGrid(self,0,7)),(SubGrid(self,1,7)),(SubGrid(self,2,7)),(SubGrid(self,3,7)),(SubGrid(self,4,7)),(SubGrid(self,5,7)),(SubGrid(self,6,7)),(SubGrid(self,7,7)),(SubGrid(self,8,7)),(SubGrid(self,9,7)),
                       (SubGrid(self,0,8)),(SubGrid(self,1,8)),(SubGrid(self,2,8)),(SubGrid(self,3,8)),(SubGrid(self,4,8)),(SubGrid(self,5,8)),(SubGrid(self,6,8)),(SubGrid(self,7,8)),(SubGrid(self,8,8)),(SubGrid(self,9,8)),
                       (SubGrid(self,0,9)),(SubGrid(self,1,9)),(SubGrid(self,2,9)),(SubGrid(self,3,9)),(SubGrid(self,4,9)),(SubGrid(self,5,9)),(SubGrid(self,6,9)),(SubGrid(self,7,9)),(SubGrid(self,8,9)),(SubGrid(self,9,9))]

#Sprites representing a backround/wall
class SubGrid(PS.Sprite):
    def __init__(self,grid,x,y):
        super(SubGrid, self).__init__()
        self.WIDTH=grid.WIDTH/9
        self.HEIGHT=grid.HEIGHT/9
        self.image=PG.Surface((grid.WIDTH/10,grid.HEIGHT/10))
        self.rect = self.image.get_rect()
        self.XSTART=grid.XSTART
        self.YSTART=grid.YSTART
        self.rect.width=(grid.WIDTH/10)
        self.rect.height=(grid.HEIGHT/10)
        
        self.XOFFSET=self.XSTART+(self.WIDTH*x)
        self.YOFFSET=self.YSTART+(self.HEIGHT*y)
        self.rect.left=self.XOFFSET
        self.rect.top=self.YOFFSET
        self.SURFACE=None
        allsprites.add(self)
        
        if grid.TYPE=='#':
            self.SURFACE=images['wall']
            self.SURFACE=PG.transform.scale(self.SURFACE, (self.WIDTH, self.HEIGHT))
            self.image=self.SURFACE

        elif grid.TYPE=='.':
            self.SURFACE=images['floor']
            self.SURFACE=PG.transform.scale(self.SURFACE, (self.WIDTH, self.HEIGHT))
            self.image=self.SURFACE
            
        elif grid.TYPE==str:
            return 'Quit'
        
        self.rect=self.image.get_rect()
        self.rect.width=grid.WIDTH/10
        self.rect.height=grid.HEIGHT/10
        self.rect.left=self.XOFFSET
        self.rect.top=self.YOFFSET
        
    


#run function returns several things, in order: gridlist
class Mapper(object):
    def __init__(self,maplist,res):

        #Maplist is used for collision in the future
        self.MAPLIST=maplist
        print(maplist)
        self.WIDTH=res[0]
        self.HEIGHT=res[1]
        self.XLENGTH=len(list(maplist[0]))
        print(self.XLENGTH)
        
        self.YLENGTH=len(maplist)
        print(self.YLENGTH)
        print('######')

        self.GRIDW=self.WIDTH/(self.XLENGTH)
        self.GRIDH=self.HEIGHT/(self.YLENGTH)
        self.GRIDLIST=[]

        
    


   



## Creates the grid that handles wall collision and surface events
    def create_grid(self):
        x=0
        y=0
        for l in range(0,(self.YLENGTH)):
            
            for c in range(0,(self.XLENGTH)):
                cY=self.MAPLIST[l]
                cX=cY[c]
                self.GRIDLIST.append(Grid(x,y,cX,self.GRIDW,self.GRIDH))
                x+=1
                if x==self.XLENGTH:
                    x=0
            y+=1
        
            









if __name__ == '__main__':
    main()






        
    
