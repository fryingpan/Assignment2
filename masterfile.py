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
import pygame.mixer as PM


PG.init()
#import titlegamestate as Title
import newmenugamestate as Menu
import Setup as Game
import highscores as Score
import title
import Globals


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
    Globals.SCREEN = PDI.set_mode((1280, 1020), PG.DOUBLEBUF | PG.HWSURFACE)
    Globals.WIDTH = Globals.SCREEN.get_width()
    Globals.HEIGHT = Globals.SCREEN.get_height()
    Globals.FONT = PF.Font(None, 48)
    Globals.STATE = "Title"


def loop():
    interval = 0

    clock = PT.Clock()
    current = PT.get_ticks()

    while Globals.RUNNING:

        new = PT.get_ticks()
        elapsed = (new - current) / 1000.0
        current = new
        clock.tick()

        # figure out timestep
        # for physics only
        if Globals.STATE == "Title" and Globals.CURRENTSTATE != "Title":
            Globals.CURRENTSTATE = "Title"
            state = title.Title()
        elif Globals.STATE == "Menu" and Globals.CURRENTSTATE != "Menu":
            Globals.CURRENTSTATE = "Menu"
            state = Menu.Menu()
        elif Globals.STATE == "Game" and Globals.CURRENTSTATE != "Game":
            Globals.CURRENTSTATE = "Game"
            state = Game.Game()
        elif Globals.STATE == "Score" and Globals.CURRENTSTATE != "Score":
            Globals.CURRENTSTATE = "Score"
            state = Score.HighScores()
        elif Globals.STATE == "Quit" and Globals.CURRENTSTATE != "Quit":
            Globals.CURRENTSTATE = "Quit"
            Globals.RUNNING = False


        state.update()
        interval += elapsed

        while interval > .03:
            #print elapsed
#fix later? only needed in the game state.
            Globals.DELTA = elapsed

            state.render()

            event = PE.get()
            if event:
                state.event(event)

            interval -= .03


#elif Globals.STATE == "Game":

#    Globals.STATE = Game.Locals.CHANGESTATE
#    while Globals.STATE == "Game":
#        new_time = PT.get_ticks()
#        frame_time = (new_time - self.current_time)/1000.0
#        self.current_time = new_time
#        self.clock.tick()

#        Globals.State = Game.Locals.CHANGESTATE
#        interval = 0.005
#        if(gamerino.run() is False):
#            Globals.STATE = Game.Locals.CHANGESTATE
#    gameScore = Game.Locals.SCORE


#elif Globals.STATE == "Scores":
#    if gameScore != 0:
#        highscores.Locals.SCORE = gameScore
#        # give new gamescore to highscores class FIRST
#    highscores.initialize()
#    Globals.STATE = highscores.Locals.CHANGESTATE
#    while Globals.STATE == "Scores":
#        Globals.STATE = highscores.Locals.CHANGESTATE
#        last = PT.get_ticks()
#        elapsed = (PT.get_ticks() - last) / 1000.0
#        event = PE.get()
#        highscores.run(elapsed, event)


def finalize():
    PG.quit()

if __name__ == "__main__":
    main()
