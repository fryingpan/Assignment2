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


#Container for global variables
class Globals(object):
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None
    FADEINTIME = 5.0
    FADEOUTTIME = 0.2
    
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
    surf = Globals.FONT.render(text, True, textcolor)
    Globals.SCREEN.blit(surf, rect)
   
    objectList[referencestr] = rect



class Menu(State):
  

    #Declares variables for first creation of state and intializes very basic sound and color modules
    def __init__(self):
        State.__init__(self)
        self.color = PC.Color("blue")
        self.time = 0.0
        self.sound = PX.Sound("thx.wav")
        self.sound.play()
        Globals.SCREEN.fill(PC.Color("white"))

                
    def render(self):
        
        drawtextbox("Title",PC.Color("red"),PC.Color("blue"),0,400,0,100,"title")
        drawtextbox("Scores",PC.Color("red"),PC.Color("blue"),100,500,200,300,"scores")
        drawtextbox("Game",PC.Color("red"),PC.Color("blue"),200,600,400,500,"game")
        drawtextbox("Quit",PC.Color("red"),PC.Color("blue"),300,700,600,700,"quit")
        
        
    def update(self, time):
        self.time += time
        #Fade in code, linear fade based on time
        if self.time < Globals.FADEINTIME:
            ratio = self.time / Globals.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
    def event(self, event):
        mousePress = PG.mouse.get_pressed()
        M_M1 = mousePress[0]
        #Allows quitting pygame and changing states, added changes for multiple states to allow testing
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif M_M1 == 1:
            if objectList['title'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Globals.CHANGESTATE = "Title"
            elif objectList['scores'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Globals.CHANGESTATE = "Scores"
            elif objectList['game'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Globals.CHANGESTATE = "Game"
            elif objectList['quit'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                Globals.CHANGESTATE = "Quit"
                
                #PG.quit()
            #elif objectList['test1'].collidepoint(PG.mouse.get_pos()) == 1:
                #print('this is a test')

        
       
        #print(objectList['hello'].collidepoint(PG.mouse.get_pos()))
        #print(objectList['test1'].collidepoint(PG.mouse.get_pos()))





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
    Globals.STATE = Menu()
    Globals.CHANGESTATE = "Menu"

def loop():
    while Globals.RUNNING and Globals.CHANGESTATE=="Menu":
        last = PT.get_ticks()
        #Renders the current state
        Globals.STATE.render()
        PDI.flip()
        #Updates the current state
        elapsed = (PT.get_ticks() - last) / 1000.0
        Globals.STATE.update(elapsed)

        for event in PE.get():
            if event.type == PG.QUIT:
                Globals.RUNNING = False
            else:
                Globals.STATE.event(event)

def finalize():
    PG.quit()

if __name__ == "__main__":
    main()
