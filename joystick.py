'''
Fryingpan
authors:
Carla Castro
Mary Yen
Katie Chang
Reference code from Peter
'''

# we only need sys for exit() to stop the game
import sys as SYS
# the basic PyGame module
import pygame as PG
# handles the main game screen
import pygame.display as PD
# draw complex shapes
import pygame.draw as PR
# allows us to load images
import pygame.image as PI
# rotate and zoom images
import pygame.transform as PT
# react to user input
import pygame.event as PE
# support for joysticks/gamepads
import pygame.joystick as PJ
# global variables
import Globals
import time

class ManageEvent():
    def __init__ (self, key, down):
        self.key = key
        self.down = down
        self.up = not down

class Joystick():

    # all joystick-related events
    JOYSTICK = set([
        PG.JOYAXISMOTION, PG.JOYHATMOTION,
        PG.JOYBUTTONUP, PG.JOYBUTTONDOWN
    ])

    #our game is one player, will have only one joysticks
    def __init__(self):
        try:
            PJ.init()  # initializes PJ module, NOT joystick itself
            self.names = []

            self.joystick = PJ.Joystick(0)
            self.joystick.init()

            ##assuming just 1 joystick
            self.names.append(PJ.Joystick(0).get_name())


            #A is attack (space)
            #B is pick up (s)
            #x is set trap (a)
            #y is drop (d)
            #r is eat (e)

            self.buttons = [False for i in range(self.joystick.get_numbuttons())]
            ##test
            self.axishats = [False, False, False]  # axis 0, 1; hat 0
            self.button_pos = [(216, 74), (236, 92), (255, 74), (236, 56),
                (608, 88), (476, 104), (606, 118), (476, 136),
                (134, 56), (188, 56)]

    #        self.buttons = ['up', 'down', 'left', 'right', 'start', 'attack', 'pickup', 'settrap', 'drop', 'eat']
    #        self.key_map = {
    #                    PG.K_UP : 'up',
    #                    PG.K_DOWN : 'down',
    #                    PG.K_LEFT : 'left',
    #                    PG.K_RIGHT : 'right',
    #                    PG.K_RETURN : 'start',
    #                    PG.K_a : 'attack',
    #                    PG.K_b : 'pickup',
    #                    PG.K_x : 'settrap',
    #                    PG.K_y : 'drop',
    #                    PG.K_l : 'eat'
    #                }

            self.keys_pressed = {}
            for button in self.buttons:
                self.keys_pressed[button] = False

            self.joystick_config = {}

            self.quit_attempt = False

        except PG.error, err:
            pass

    def is_pressed(self, button):
        for i in range(len(self.buttons)):
            if self.buttons[i]:
                return True

    def get_events(self):
        joyEvent = []
        for event in PE.get():
            if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
                self.quit_attempt = True

        for button in self.buttons:
            config = self.joystick_config.get(button)
            if config != None:
                if config[0] == 'is_button':
                    pushed = self.joystick.get_button(config[1])
                    if pushed != self.keys_pressed[button]:
                        joyEvent.append(ManageEvent(button, pushed))
                        self.keys_pressed[button] = pushed

                elif config[0] == 'is_hat':  # direction pad
                    status = self.joystick.get_hat(config[1])
                    if config[2] == 'x':
                        amount = status[0]
                    else:
                        amount = status[1]
                    if config[3] == 1:
                        pushed = amount > 0.5
                    else:
                        pushed = amount < -0.5
                    if pushed != self.keys_pressed[button]:
                        joyEvent.append(ManageEvent(button, pushed))
                        self.keys_pressed[button] = pushed

                elif config[0] == 'is_axis':
                    status = self.joystick.get_axis(config[1])
                    if config[2] == 1:
                        pushed = status > 0.5
                    else:
                        pushed = status < -0.5
                    if pushed != self.keys_pressed[button]:
                        joyEvent.append(ManageEvent(button, pushed))
                        self.keys_pressed[button] = pushed
        return joyEvent

    def config_button(self, button):
        joy = self.joystick

        ##button activity
        for buttonindex in range(joy.get_numbuttons()):
            buttonpushed = joy.get_button(buttonindex)
            if buttonpushed and not self.is_button_used(buttonindex):
                self.joystick_config[button] = ('is_button', buttonindex)
                return True

        ##do hats
        for hatindex in range(joy.get_numhats()):
            hatstatus = joy.get_hat(hatindex)
            if hatstatus[0] < -.5 and not self.is_hat_used(hatindex, 'x', -1):
                self.joystick_config[button] = ('is_hat', hatindex, 'x', -1)
                return True
            elif hatstatus[0] > .5 and not self.is_hat_used(hatindex, 'x', 1):
                self.joystick_config[button] = ('is_hat', hatindex, 'x', 1)
                return True
            if hatstatus[1] < -.5 and not self.is_hat_used(hatindex, 'y', -1):
                self.joystick_config[button] = ('is_hat', hatindex, 'y', -1)
                return True
            elif hatstatus[1] > .5 and not self.is_hat_used(hatindex, 'y', 1):
                self.joystick_config[button] = ('is_hat', hatindex, 'y', 1)
                return True

        ##axis activity
        for axisindex in range(joy.get_numaxes()):
            axisstatus = joy.get_axis(axisindex)
            if axisstatus < -.5 and not self.is_axis_used(axisindex, -1):
                self.joystick_config[button] = ('is_axis', axisindex, -1)
                return True
            elif axisstatus > .5 and not self.is_axis_used(axisindex, 1):
                self.joystick_config[button] = ('is_axis', axisindex, 1)
                return True

        return False

    def is_button_used(self, buttonindex):
        for button in self.buttons:
            config = self.joystick_config.get(button)
            if config != None and config[0] == 'is_button' and config[1] == buttonindex:
                return True
        return False

    def is_hat_used(self, hatindex, axis, direction):
        for button in self.buttons:
            config = self.joystick_config.get(button)
            if config != None and config[0] == 'is_hat':
                if config[1] == hatindex and config[2] == axis and config[3] == direction:
                    return True
        return False

    def is_axis_used(self, axisindex, direction):
        for button in self.buttons:
            config = self.joystick_config.get(button)
            if config != None and config[0] == 'is_axis':
                if config[1] == axisindex and config[2] == direction:
                    return True
        return False






