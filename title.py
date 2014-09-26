import sys
import math
import pygame as PG
from pygame import color as PC
import pygame.display as PDI

from pygame import image 
from pygame.locals import *
	
from Globals import Globals

class Title:
	FADEINTIME = 5.0
	FADEOUTTIME = 0.2
	def __init__(self):
		self.color = PC.Color("white")
		self.time = 0.0

		Globals.SCREEN = PDI.set_mode((800, 600), PG.DOUBLEBUF|PG.HWSURFACE)
		Globals.WIDTH = Globals.SCREEN.get_width()
		Globals.HEIGHT = Globals.SCREEN.get_height()

		Globals.SCREEN.fill(PC.Color("white"))
		bigfont = PG.font.Font(None, 60)
		white = 100, 205, 230
		self.renderer = textWavey(bigfont, "Frying Pan", white, 7)

	def render(self):
		# surf = Globals.FONT.render("Title Screen", True, self.color)
		self.text = self.renderer.animate().convert()
		width, height = self.text.get_size()
		Globals.SCREEN.blit(self.text, (Globals.WIDTH/2 - width/2, Globals.HEIGHT/4))

	def update(self, time):
		self.time += time
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

class textWavey:
	def __init__(self, font, message, fontcolor, amount=10):
		self.background = PC.Color("white")
		self.base = font.render(message, 0, fontcolor, self.background)
		self.steps = range(0, self.base.get_width(), 2)
		self.amount = amount
		self.size = self.base.get_rect().inflate(0, amount).size
		self.offset = 0.0
		
	def animate(self):
		s = PG.Surface(self.size)
		s.fill(self.background)
		height = self.size[1]
		self.offset += 0.5
		for step in self.steps:
			src = Rect(step, 0, 2, height)
			dst = src.move(0, math.cos(self.offset + step*.02)*self.amount)
			s.blit(self.base, dst, src)
		return s