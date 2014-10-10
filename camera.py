'''
Assignment 2
Fryingpan
Carla Castro
Mary Yen
Katie Chang
Josh Holstein
'''

'''
author: Carla
'''

import pygame as PG
from pygame.locals import *
import sys
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI

#camera variables
WIN_WIDTH = 800
WIN_HEIGHT = 600

class Camera(object):
	def __init__(self, bigmap):
		self.bigmap = bigmap
		self.bigmap_rect = bigmap.get_rect()
		self.rect = Rect(0, 0, WIN_WIDTH, WIN_HEIGHT)
		#camera's coordinates relative to the map
		self.cameraxy = [0,0]
		self.scrollx = 0
		self.scrolly = 0

		self.background = PG.Surface((WIN_WIDTH, WIN_HEIGHT))


	#apply the character's displacement to the camera
	def apply(self, playerxy):
		move = False
		playerx, playery = playerxy

		#camera bounds on the x and y axis to keep the player centered
		boundx = [WIN_WIDTH*(0.4) + self.cameraxy[0], WIN_WIDTH*(0.6) + self.cameraxy[0]]
		boundy = [WIN_HEIGHT*(0.4) + self.cameraxy[1], WIN_HEIGHT*(0.6) + self.cameraxy[1]]


		scrollx = 0
		scrolly = 0
		if playerx < boundx[0]:
			scrollx -= boundx[0] - playerx
		elif playerx > boundx[1]:
			scrollx += playerx - boundx[1]
		if playery < boundy[0]:
			scrolly -= boundy[0] - playery
		elif playery > boundy[1]:
			scrolly += playery - boundy[1]

		if scrollx != 0 or scrolly != 0:
			move = True
			self.cameraxy[0] += scrollx
			self.cameraxy[1] += scrolly
		return move
		

	#update where the camera needs to be in the big map
	def update(self, target_coordinates, screen, bigmap):
		moved = self.apply(target_coordinates)
		if moved:
			self.check_boundary()
			self.background = bigmap.subsurface(self.cameraxy[0], self.cameraxy[1], WIN_WIDTH, WIN_HEIGHT)
			
		screen.blit(self.background, (0,0))


	#check that the camera doesn't go off the map
	def check_boundary(self):
		bigmap_width = self.bigmap_rect.width
		bigmap_height = self.bigmap_rect.height
		#check left
		if self.cameraxy[0] < 0 :
			self.cameraxy[0] = 0
			scrollx = 0
		#check right
		elif self.cameraxy[0] > bigmap_width - WIN_WIDTH:
			self.cameraxy[0] = bigmap_width - WIN_WIDTH
			scrollx = bigmap_width - WIN_WIDTH
		#check top
		if self.cameraxy[1] < 0:
			self.cameraxy[1] = 0
			scrolly = 0
		#check bottom
		elif self.cameraxy[1] > bigmap_height - WIN_HEIGHT:
			self.cameraxy[1] = bigmap_height - WIN_HEIGHT
			scrolly = 0



