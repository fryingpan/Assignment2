import sys
import pygame as PG
from pygame import color as PC
from pygame import display as PDI
from pygame.locals import *


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
    

class HighScores:
	def __init__(self):
		PG.font.init()

		Globals.SCREEN = PDI.set_mode((800, 600), PG.DOUBLEBUF|PG.HWSURFACE)
		Globals.WIDTH = Globals.SCREEN.get_width()
		Globals.HEIGHT = Globals.SCREEN.get_height()

		self.color = PC.Color("black")
		self.time = 0.0
		Globals.SCREEN.fill(PC.Color("black"))
		self.text_surface = self.get_text_surface()

	def render(self):
		width, height = self.text_surface.get_size()
		Globals.SCREEN.blit(self.text_surface, (Globals.WIDTH/2 - width/2, Globals.HEIGHT/2 - height/2))

	def update(self, time):
		self.time += time
		fadein = 2.0
		if self.time < fadein:
			ratio = self.time / fadein
			value = int(ratio * 255)
			self.color = PC.Color(value, value, value)

	def event(self, event):
		fadeout = 0.2
		if event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
			Globals.RUNNING = False
		elif event.type == PG.KEYDOWN and event.key == PG.K_SPACE:
			PX.music.fadeout(int(fadeout*1000))
			Locals.STATE = Menu()

	def get_text_surface(self):
		rect = Rect(100, 100, 300, 300)
		surface = PG.Surface(rect.size)
		text_color = PC.Color("white")
		font = PG.font.Font(None, 30) 
		surface.fill(self.color)
		with open('scores.txt', 'r') as f:
			scores = f.read()
			surface = render_text(scores, font, rect, text_color, self.color)
		return surface		

def render_text(string, font, rect, text_color, background_color):	
	final_lines = []

	lines = string.splitlines()

	# Create a series of lines that will fit in rect
	for line in lines:
		if font.size(line)[0] > rect.width:
			words = line.split(' ')
			# if the name and score is longer than the width of the surface
			for word in words:
				if font.size(word)[0] >= rect.width:
					raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
		else: 
			final_lines.append(line) 

	# Write onto the surface
	surface = PG.Surface(rect.size) 
	surface.fill(background_color) 

	accumulated_height = 0 
	for line in final_lines: 
		if line != "":
			tempsurface = font.render(line, 1, text_color)
			surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
		accumulated_height += font.size(line)[1]

	return surface


