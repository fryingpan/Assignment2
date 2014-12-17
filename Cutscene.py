import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import pygame.event as PE
import pygame.font as PF
import sys
import math
import pygame.image as PI
from Player import Player
from Enemy import Enemy

#NOTE: IT SEEMS THAT CUTSCENE DELETES AN ENEMY??
#HOW TO FIX LAG AFTER SCENES COMPLETE?!!?


class Cutscene(PS.Sprite):

    def __init__(self, screen, level):
        PS.Sprite.__init__(self)
        self.screen = screen
        self.origin = (0, 0)
        self.scenes = []
        self.load(level)
        self.play(level)

    def load(self, level):
        if(level == 1):
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv1_0.png").
                convert(), self.screen))
            self.scenes.append(Scene(PI.load(
                "FPGraphics/story/lv1_1.png").
                convert(), self.screen))
            #need to load script backwards since I'm using
            #pop what am I doing with my life T~T
            self.scenes[1].add_text(
                "But you couldn't say exactly how.", (200, 80))
            self.scenes[1].add_text(
                "You always knew you were a little different.", (200, 80))
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv1_2.png").
                convert(), self.screen))
            self.scenes[2].add_over_img(
                PI.load("FPGraphics/story/lv1_2_sp.png").
                convert_alpha(), self.origin)
            self.scenes[2].add_text(
                "You're tired of dealing with this disrespect.", (110, 65))
            self.scenes[2].add_text(
                "Maybe that's why no one wanted to play with you.", (110, 65))

            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv1_3.png").
                convert(), self.screen))
            #dear self, consider changing pop mechanism
            #before this gets out of hand
            self.scenes[3].add_over_img(
                PI.load("FPGraphics/story/lv1_3_sp3.png").
                convert_alpha(), (220, 480))
            self.scenes[3].add_over_img(
                PI.load("FPGraphics/story/lv1_3_sp2.png").
                convert_alpha(), (480, 40))
            self.scenes[3].add_over_img(
                PI.load("FPGraphics/story/lv1_3_sp1.png").
                convert_alpha(), (20, 25))
        if(level == 2):
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv2_1.png").
                convert(), self.screen))
            self.scenes[0].add_text("You can't let this continue.", (100, 30))
            self.scenes[0].add_text(
                "-who are still alive and smug and terrible.", (100, 30))
            self.scenes[0].add_text(
                "There are still food people in the nearby chili land-",
                (100, 30))
            self.scenes[0].add_text(
                "As you bask in your glory, you realize something.", (100, 30))
        if(level == 3):
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv3_1.png").
                convert(), self.screen))
            self.scenes[0].add_text(
                "You know what to do.", (100, 30))
            self.scenes[0].add_text(
                "How charming. But full of stupid food people.", (100, 30))
            self.scenes[0].add_text(
                "...Somehow there is an icecream land nearby!", (100, 30))
            self.scenes[0].add_text(
                "But what's this?", (100, 30))
            self.scenes[0].add_text(
                "You've bested the heated and horrible chili land!", (100, 30))
        if(level == 4):
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv4_1.png").
                convert(), self.screen))
            self.scenes[0].add_text(
                "It's the last land, so give it your best shot!", (100, 30))
            self.scenes[0].add_text(
                "Speaking of sweet, check out the sweet candy land nearby.", (100, 30))
            self.scenes[0].add_text(
                "Sweet victory!", (100, 30))
        if(level == 5):
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv5_1_1.png").
                convert(), self.screen))
            self.scenes[0].add_text(
                "Everyone is dead!", (100, 30))
            self.scenes[0].add_text(
                "At long last you've achieved world domination!", (100, 30))
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv5_1_2.png").
                convert(), self.screen))
            self.scenes[1].add_text(
                "Everyone is dead.", (100, 30))
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv5_2.png").
                convert(), self.screen))
            self.scenes[2].add_text(
                "Wait.", (100, 30))
            self.scenes[2].add_text(
                "You really wish you thought things through.", (100, 30))
            self.scenes[2].add_text(
                "...", (100, 30))
            self.scenes[2].add_text(
                "But who cares!", (100, 30))
            self.scenes[2].add_text(
                "Or how lonely you'd be.", (100, 30))
            self.scenes[2].add_text(
                "boring the world would be if everyone was dead.",(100,30))
            self.scenes[2].add_text(
                "Okay, maybe you should have thought about how ", (100, 30))
            self.scenes.append(Scene(
                PI.load("FPGraphics/story/lv5_3.png").
                convert(), self.screen))
            self.scenes[3].add_text(
                "When you start a job, you finish it.", (100, 30))
            self.scenes[3].add_text(
                "Anyway, you should kill them.", (100, 30))
            self.scenes[3].add_text(
                "Or something.", (100, 30))
            self.scenes[3].add_text(
                "Food people reproduce like bunnies.", (100, 30))
            self.scenes[3].add_text(
                "That's right.", (100, 30))
            
    #play all the scenes
    def play(self, level):
        count = 0
        #play_scene() will return False if the user pressed q to skip
        while(count < len(self.scenes) and self.scenes[count].play_scene()):
            count += 1


class Scene(PS.Sprite):

    def __init__(self, image, screen):
        self.screen = screen
        self.img = image
        self.text = []
        self.textcoords = []
        self.over_img = []
        self.over_imgcoords = []
        self.end_cutscene = False
        self.origin = (0, 0)
        self.font = PF.SysFont('Arial', 25)
        self.text_color = (0, 0, 0)

    def add_text(self, txt, txtcoord):
        self.text.append(txt)
        self.textcoords.append(txtcoord)

    def add_over_img(self, oimg, imgcoord):
        self.over_img.append(oimg)
        self.over_imgcoords.append(imgcoord)

    def play_scene(self):
        self.screen.blit(self.img, self.origin)
        while(self.end_cutscene is False):
            PD.flip()
            for event in PE.get():
                if event.type == PG.KEYDOWN and event.key == PG.K_q:
                    #skip cutscene
                    self.end_cutscene = True
                    return False  # end entire cutscene
                elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
                    if(len(self.text) > 0 and len(self.textcoords) > 0):
                        self.screen.blit(self.img, self.origin)
                        #find better way to clear text, maybe layers?
                        txt = self.text.pop()
                        txtcoord = self.textcoords.pop()
                        self.screen.blit(self.font.render(txt, True,
                                                          self.text_color),
                                         txtcoord)
                    elif(len(self.over_img) > 0):
                        oimg = self.over_img.pop()
                        oimgcoord = self.over_imgcoords.pop()
                        self.screen.blit(oimg, oimgcoord)
                    else:
                        self.end_cutscene = True  # no more txt or imgs to add
                        return True  # go to next scene
