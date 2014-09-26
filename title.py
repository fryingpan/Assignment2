import sys
import math
import pygame as PG
from pygame import color as PC
import pygame.display as PDI
import pygame.image as PI

from pygame import image 
from pygame.locals import *
	
from Globals import Globals



class Title:
	FADEINTIME = 5.0
	FADEOUTTIME = 0.2
	IMAGES = None
	def __init__(self):
		self.color = PC.Color("white")
		self.time = 0.0
		if not Title.IMAGES:
			Title.IMAGES = self.load_images()

		Globals.SCREEN = PDI.set_mode((800, 600), PG.DOUBLEBUF|PG.HWSURFACE)
		Globals.WIDTH = Globals.SCREEN.get_width()
		Globals.HEIGHT = Globals.SCREEN.get_height()	

		self.images = Title.IMAGES

		self.enemyx = Globals.WIDTH 
		self.enemyy = Globals.HEIGHT - self.images[0].get_height()
		self.playerx = 0 - self.images[1].get_width()
		self.playery = Globals.HEIGHT - self.images[1].get_height()

		Globals.SCREEN.fill(PC.Color("white"))
		bigfont = PG.font.Font(None, 60)
		self.renderer = textWavey(bigfont, "Frying Pan", (100, 200, 100), 7)


	def load_images(self):
		images = []
		images.append(PI.load("FPGraphics/Title/TitleFood.png").convert_alpha())
		images.append(PI.load("FPGraphics/Title/TitlePlayer.png").convert_alpha())
		return images



	def render(self):
		# surf = Globals.FONT.render("Title Screen", True, self.color)
		Globals.SCREEN.fill(self.color)
		self.text = self.renderer.animate().convert_alpha()

		player_moves = self.move_player()
		self.move_enemy()

		width, height = self.text.get_size()
		Globals.SCREEN.blit(self.images[0], (self.enemyx, self.enemyy))
		Globals.SCREEN.blit(self.images[1], (self.playerx, self.playery))
		Globals.SCREEN.blit(self.text, (Globals.WIDTH/2 - width/2, Globals.HEIGHT/15))


	def move_player(self):
		moves = False
		if self.playerx < -17:
			self.playerx += 20
			moves = True
		return moves

	def move_enemy(self):
		if  self.enemyx > (Globals.WIDTH - self.enemyx) :
			self.enemyx -= 20

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