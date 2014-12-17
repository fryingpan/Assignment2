# Game State Implementation
# Imports
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
# import titlegamestate as Title
import newmenugamestate as Menu
import Setup as Game
import highscores as Score
import title
import Globals


# Main Executable entry point
def main():
    initialize()
    loop()
    finalize()


def initialize():
    # Creates pygame module and intializes global variables.
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
            Globals.SCORE = 0
            state = Game.Game()
        elif Globals.STATE == "Score" and Globals.CURRENTSTATE != "Score":
            Globals.CURRENTSTATE = "Score"
            state = Score.HighScores()
        elif Globals.STATE == "Quit" and Globals.CURRENTSTATE != "Quit":
            Globals.CURRENTSTATE = "Quit"
            Globals.RUNNING = False

        state.update()
        interval += elapsed

        while interval > .02:
            # print elapsed
            Globals.DELTA = elapsed

            state.render()

            event = PE.get()
            if event:
                state.event(event)

            interval -= .02


def finalize():
    PG.quit()

if __name__ == "__main__":
    main()
