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
import Globals
import State


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



objectList = {"null":0}

#Draw Text Box, Adds Rect to objectList
def drawtextbox(text, textcolor, boxcolor, x, y, width, height, referencestr):

    screen_width = Globals.SCREEN.get_width()
    
    rect = PG.rect.Rect((screen_width/2 - width/2) - 310, y, width, height)
    
    surf = PG.Surface([rect.width,rect.height])
    surf.fill(boxcolor)


    font = PG.font.Font(None, 35)

    # surf = render_text(text, font, rect, textcolor, boxcolor)
    # Globals.SCREEN.blit(surf,rect) #rectangle highlighting the text box

    surf = font.render(text, True, textcolor)
    Globals.SCREEN.blit(surf,rect)
  
    objectList[referencestr] = rect

##########################################
    #Class Defining the state#

class Menu():
  

    #Declares variables for first creation of state and intializes very basic sound and color modules
    def __init__(self):
        self.color = PC.Color("blue")
        self.time = 0.1
        self.sound = PX.Sound("thx.wav")
        self.sound.play()
                
    def render(self):

        Globals.SCREEN.fill(PC.Color('black'))
        
        
        drawtextbox("Title",PC.Color("red"),PC.Color("blue"),10, 20,60,30,"title")
        drawtextbox("Scores",PC.Color("red"),PC.Color("blue"), 10,50,85,30,"scores")
        drawtextbox("Game",PC.Color("red"),PC.Color("blue"),10,80,75,30,"game")
        drawtextbox("Quit",PC.Color("red"),PC.Color("blue"),10,110,60,40,"quit")
        drawtextbox("Brightness", (37, 200,100), PC.Color("blue"), 10,140,130,30, "brightness")
        drawtextbox("Volume", (37, 200, 100), PC.Color("blue"), 10,170,90, 30, 'volume')
        
        PDI.flip()
        
    def update(self):
        self.time += self.time
        #Fade in code, linear fade based on time
        if self.time < Locals.FADEINTIME:
            ratio = self.time / Locals.FADEINTIME
            value = int(ratio * 255)
            self.color = PC.Color(value, value, value)
    def event(self, events):
        mousePress = PG.mouse.get_pressed()
        M_M1 = mousePress[0]
        #Allows quitting pygame and changing states, added changes for multiple states to allow testing
        for event in events:
            if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                Globals.RUNNING = False
            elif M_M1 == 1:
                if objectList['title'].collidepoint(PG.mouse.get_pos()) == 1:
                    Globals.STATE = "Title"
                elif objectList['scores'].collidepoint(PG.mouse.get_pos()) == 1:
                    Globals.STATE = "Score"
                elif objectList['game'].collidepoint(PG.mouse.get_pos()) == 1:
                    Globals.STATE = "Game"
                elif objectList['quit'].collidepoint(PG.mouse.get_pos()) == 1:
                    Globals.STATE = "Quit"
                    return False




