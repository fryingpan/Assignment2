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
from masterfile import Globals as Globals


#Container for Local variables
class Locals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None
    FADEINTIME = 5.0
    FADEOUTTIME = 0.2
    CHANGESTATE = "None"
    
#State constructor, needs additional class to complete
class State(object):
    def __init__(self):
        pass
    def render(self):
        pass
    def update(self, time):
        pass
    def event(self, event):
        pass


objectList = {"null":0}

#Draw Text Box, Adds Rect to objectList
def drawtextbox(text, textcolor, boxcolor, x1, x2, y1, y2, referencestr):

    
    rect = PG.rect.Rect(x1,y1,(x2-x1),(y2-y1))
    
    surf = PG.Surface([rect.width,rect.height])
    surf.fill(boxcolor)
    
    Globals.SCREEN.blit(surf,rect)
    surf = Locals.FONT.render(text, True, textcolor)
    Globals.SCREEN.blit(surf, rect)
  
    objectList[referencestr] = rect

##########################################
    #Class Defining the state#

class Menu(State):
  

    #Declares variables for first creation of state and intializes very basic sound and color modules
    def __init__(self):
        State.__init__(self)
        self.color = PC.Color("blue")
        self.time = 0.0
        self.sound = PX.Sound("thx.wav")
        self.sound.play()
                
    def render(self):

        Globals.SCREEN.fill(PC.Color('black'))
        
        
        drawtextbox("Title",PC.Color("red"),PC.Color("blue"),0,400,0,100,"title")
        drawtextbox("Scores",PC.Color("red"),PC.Color("blue"),0,400,105,205,"scores")
        drawtextbox("Game",PC.Color("red"),PC.Color("blue"),0,400,210,310,"game")
        drawtextbox("Quit",PC.Color("red"),PC.Color("blue"),0,400,315,415,"quit")
        drawtextbox("Adjust Visual Brightness", (37, 200,100), PC.Color('white'), 0,400,420,420, "AVB")
        drawtextbox("Adjust Volume", (37, 200, 100), PC.Color('white'), 0,400,520, 520, 'volume')
        
        PDI.flip()
        
    def update(self, time):
        self.time += time
        #Fade in code, linear fade based on time
        if self.time < Locals.FADEINTIME:
            ratio = self.time / Locals.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
    def event(self, event):
        mousePress = PG.mouse.get_pressed()
        M_M1 = mousePress[0]
        #Allows quitting pygame and changing states, added changes for multiple states to allow testing
        
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            return False
        elif M_M1 == 1:
            if objectList['title'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Locals.CHANGESTATE = "Title"
                #print(Locals.CHANGESTATE)
            elif objectList['scores'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Locals.CHANGESTATE = "Scores"
                #print(Locals.CHANGESTATE)
            elif objectList['game'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Locals.CHANGESTATE = "Game"
                #print(Locals.CHANGESTATE)
            elif objectList['quit'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Locals.CHANGESTATE = "Quit"
                return False
                #print(Locals.CHANGESTATE)
                

#####################################################################################################
#Main Run Method and Initialization                
     
def run(elapsed,event):
    Locals.STATE.render()
    Locals.STATE.update(elapsed)
    
    for event in PE.get():
            print(PG.QUIT)
            if event.type == PG.QUIT:
                return False
            else:
                if(Locals.STATE.event(event) == False):
                    return False
                #print(Locals.CHANGESTATE)

def initialize():
    #Initializes Local Vars

    Globals.SCREEN = PDI.set_mode((800, 600), PG.DOUBLEBUF|PG.HWSURFACE)

    Locals.FONT = PF.Font(None, 48)
    Locals.STATE = Menu()
    Locals.CHANGESTATE = "Menu"


