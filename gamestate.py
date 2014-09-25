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


textBoxList = {"null":0}


def drawtextbox(text, color, x, y, referencestr):

    surf = Globals.FONT.render(text, True, color)

    Globals.SCREEN.blit(surf, (x,y))
    textBoxList[referencestr] = surf.get_rect()
    




class Title(State):
    #Constants for the state
    FADEINTIME = 5.0
    FADEOUTTIME = 0.2

    #Declares variables for first creation of state and intializes very basic sound and color modules
    def __init__(self):
        State.__init__(self)
        self.color = PC.Color("black")
        self.time = 0.0
        self.sound = PX.Sound("thx.wav")
        self.sound.play()
        Globals.SCREEN.fill(PC.Color("black"))

        
    def render(self):
        #Creates a surface that is simple text, uses rendering method of FONT basic var
        surf = Globals.FONT.render("Title Screen", True, self.color)
        #Loads image in same folder titleimg.png
        titleimg = PG.image.load('titleimg.png')
        #Retreive size of surface
        width, height = surf.get_size()
        #Draw surf to screen, can do this with any number of things, image added for example
        Globals.SCREEN.blit(surf, (Globals.WIDTH/2 - width/2, Globals.HEIGHT/2 - height/2))
        #Renders titleimg
        Globals.SCREEN.blit(titleimg,(0,0))

        
    def update(self, time):
        self.time += time
        #Fade in code, linear fade based on time
        if self.time < Title.FADEINTIME:
            ratio = self.time / Title.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
    def event(self, event):
        #Allows quitting pygame and changing states, added changes for multiple states to allow testing
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
            self.sound.fadeout(int(Title.FADEOUTTIME*1000))
            Globals.STATE = Menu()
        elif event.type == PG.KEYDOWN and event.key == PG.K_I:
            self.sound.fadeout(int(Title.FADEOUTTIME*1000))
            #Globals.STATE = Menu()
        elif event.type == PG.KEYDOWN and event.key == PG.K_O:
            self.sound.fadeout(int(Title.FADEOUTTIME*1000))
            #Globals.STATE = Menu()
        elif event.type == PG.KEYDOWN and event.key == PG.K_P:
            self.sound.fadeout(int(Title.FADEOUTTIME*1000))
           # Globals.STATE = Menu()


class Menu(State):
    #Constants for the state
    FADEINTIME = 5.0
    FADEOUTTIME = 0.2

    #Declares variables for first creation of state and intializes very basic sound and color modules
    def __init__(self):
        State.__init__(self)
        self.color = PC.Color("blue")
        self.time = 0.0
        self.sound = PX.Sound("thx.wav")
        self.sound.play()
        Globals.SCREEN.fill(PC.Color("black"))

                
    def render(self):
      
       drawtextbox("Hello Screen", PC.Color("red"), 20, 20, "hello")

       drawtextbox("Hello Test 1", PC.Color("blue"), 100, 100, "test1")
       
       

        
    def update(self, time):
        self.time += time
        #Fade in code, linear fade based on time
        if self.time < Title.FADEINTIME:
            ratio = self.time / Title.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
    def event(self, event):
        mousePress = PG.mouse.get_pressed()
        M_M1 = mousePress[0]
        #Allows quitting pygame and changing states, added changes for multiple states to allow testing
        if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            Globals.RUNNING = False
        elif M_M1 == 1:
            if textBoxList['hello'].collidepoint(PG.mouse.get_pos()) == 1:
                print("success")
                PG.quit()
            elif textBoxList['test1'].collidepoint(PG.mouse.get_pos()) == 1:
                print('this is a test')

        
        print(textBoxList['hello'].collidepoint(PG.mouse.get_pos()))
        print(textBoxList['test1'].collidepoint(PG.mouse.get_pos()))
        print(textBoxList['hello'])
        






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
    Globals.SCREEN = PDI.set_mode((800, 600), PG.DOUBLEBUF|PG.HWSURFACE)
    Globals.WIDTH = Globals.SCREEN.get_width()
    Globals.HEIGHT = Globals.SCREEN.get_height()
    Globals.FONT = PF.Font(None, 48)
    Globals.STATE = Title()

def loop():
    while Globals.RUNNING:
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
