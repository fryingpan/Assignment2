'''
Assignment 2
Fryingpan
Carla Castro
Mary Yen
Katie Chang
Josh Holstein
'''

import pygame as PG
from pygame.locals import *
import sys
import pygame.mixer as PM
import pygame.display as PD
import pygame.sprite as PS
import pygame.image as PI

PG.init()

#loading sound
PM.music.load("hitWall.mod")

class Player(PS.Sprite):

	IMAGES = None
	IMAGES_RIGHT = None
	IMAGES_LEFT = None
	IMAGES_FRONT = None
	IMAGES_BACK = None
	IMAGES_RIGHT_ACCEL = None
	IMAGES_LEFT_ACCEL = None
	IMAGES_FRONT_ACCEL = None
	IMAGES_BACK_ACCEL = None
	IMAGES_RIGHT_DECEL = None
	IMAGES_LEFT_DECEL = None
	IMAGES_FRONT_DECEL = None
	IMAGES_BACK_DECEL = None
	CYCLE = 0.2
	ADCYCLE = .05
	WIDTH = 100
	HEIGHT = 100

	def __init__(self, speed = 2):
		# Call the parent class (Sprite) constructor
		PS.Sprite.__init__(self)
		self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = speed
		self.accelSpeed = 0
		self.decelSpeed = speed
		self.rect.x = 100
		self.rect.y = 100
		self.face = 'd'
		self.load_images()
		self.time = 0.0
		self.frame = 0
		self.accel = False
		self.decel = False
		self.accelF = self.speed/4
		self.decelF = - (self.speed/4)
		self.interval = 0
		self.decelFinish = True #If true, we've finished, so we do not decel
		
		#collision conditions, if true, we will not move in that direction

	def get_face(self):
		return self.face

	def handle_collision(self, bg):
		collisions = PS.spritecollide(self, bg, False)
		x_changed = False
		y_changed = False
		for collision in collisions:
			#print("self " + str(self.rect.x + Player.WIDTH) + " coll " + str(collision.get_left()))
			if((self.rect.x + self.rect.width) >= collision.rect.left) and not x_changed:
				print("right collide")
				self.rect.x = collision.rect.left - self.rect.width
				x_changed = True
			elif ((self.rect.x) <= (collision.rect.left + collision.rect.width)) and not x_changed:
				print "Collision rect left: " + str(collision.rect.left)
				print "collision rect width: " + str(collision.rect.width)
				self.rect.x = collision.rect.left + collision.rect.width
				print "left collide"
				x_changed = True

			if((self.rect.y + self.rect.height) >= collision.rect.top) and not y_changed:
				self.rect.y = collision.rect.top - self.rect.height
				print "bottom collide"
				y_changed = True

			elif((self.rect.y >= (collision.rect.top + collision.rect.height))) and not y_changed:
				self.y = collision.rect.top + collision.rect.height
				print "top collide"
				y_changed = True
			# print "X COORDINATE: " + str(self.rect.x)
			# print "Y COORDINATE: " + str(self.rect.y)
	
	def handle_keys(self, bg, interval = 5):
		""" Handles Keys """
		if self.accel == True:
			return 0
		key = PG.key.get_pressed()
		dist = self.speed # distance moved in 1 frame, try changing it to 5
		self.interval = interval
		#accel/decel handling
		for event in PG.event.get():
			if event.type == PG.KEYDOWN:
				self.accel = True
				self.accelSpeed = 0
				
		if key[PG.K_DOWN]: # down key
			self.rect.y += dist*interval# move down
			print(dist)
			print(interval)
			print(self.rect.y)

			collisions = PS.spritecollide(self, bg, False)
			once = True
			for collision in collisions:
				if once:
					if (self.rect.y + self.rect.height) >= collision.rect.top:
						self.rect.y = collision.rect.top - self.rect.height
						print "bottom collide"
						once = False



			#self.rect = self.image.get_rect()
			self.face = 'd'
		elif key[PG.K_UP]: # up key
			self.rect.y -= dist*interval # move up
			#self.rect = self.image.get_rect()

			collisions = PS.spritecollide(self, bg, False)
			once = True
			for collision in collisions:
				if once:
					if (self.rect.y <= (collision.rect.top + collision.rect.height)):
						self.y = collision.rect.top + collision.rect.height
						print "top collide"
						once = False

			self.face = 'u'
		elif key[PG.K_RIGHT]: # right key
			self.rect.x += dist*interval # move right

			#check if it collides right
			collisions = PS.spritecollide(self, bg, False)
			once = True
			for collision in collisions:
				if once:
					if(self.rect.x + self.rect.width) >= collision.rect.left:
						print("right collide")
						self.rect.x = collision.rect.left - self.rect.width
						once = False


			#self.rect = self.image.get_rect()
			self.face = 'r'
		elif key[PG.K_LEFT]: # left key
			self.rect.x -= dist*interval# move left
			#self.rect = self.image.get_rect()

			collisions = PS.spritecollide(self, bg, False)
			once = True
			for collision in collisions:
				if once:
					if (self.rect.x) <= (collision.rect.left + collision.rect.width):
						# print "Collision rect left: " + str(collision.rect.left)
						# print "collision rect width: " + str(collision.rect.width)
						self.rect.x = collision.rect.left + collision.rect.width
						print "left collide"
						once = False


			self.face = 'l'
		else: #ds = down 'standing' (not moving) **********
			if self.face == 'd':
				if(self.decelFinish == False):
					self.decel = True
					self.decelSpeed = self.speed
				self.face = 'ds'
			if self.face == 'u':
				if(self.decelFinish == False):
					self.decel = True
					self.decelSpeed = self.speed
				self.face = 'us'
			if self.face == 'r':
				if(self.decelFinish == False):
					self.decel = True
					self.decelSpeed = self.speed
				self.face = 'rs'
			if self.face == 'l':
				if(self.decelFinish == False):
					self.decel = True
					self.decelSpeed = self.speed
				self.face = 'ls'
		
		 
	def update(self, delta):
		PLAYER_IMAGE_LENGTH = 12 #all player sprite has 12 frames
		PLAYER_AD_IMAGE_LENGTH = 3
		#update time and frame
		key = PG.key.get_pressed()
		if self.accel == True or self.decel == True:
			self.time = self.time + delta
			if self.time > Player.ADCYCLE:
				self.time = 0.0
			#SOMETHING HERE WITH THIS LINE MAYBE V
			frame = int(self.time / (Player.ADCYCLE / PLAYER_AD_IMAGE_LENGTH))
		else:
			self.time = self.time + delta
			if self.time > Player.CYCLE:
				self.time = 0.0
			frame = int(self.time / (Player.CYCLE / PLAYER_IMAGE_LENGTH))
		
		#SOMETHING HERE
		if frame != self.frame:
			self.frame = frame
			if self.accel == True:
				if self.accelSpeed < self.speed:
					a = self.accelSpeed
					if key[PG.K_DOWN]: # down key
						self.rect.y += a*self.interval# move down
						#self.rect = self.image.get_rect()
						self.face = 'da'
					elif key[PG.K_UP]: # up key
						self.rect.y -= a*self.interval # move up
						#self.rect = self.image.get_rect()
						self.face = 'ua'
					elif key[PG.K_RIGHT]: # right key
						self.rect.x += a*self.interval # move right
						#self.rect = self.image.get_rect()
						self.face = 'ra'
					elif key[PG.K_LEFT]: # left key
						self.rect.x -= a*self.interval# move left
						#self.rect = self.image.get_rect()
						self.face = 'la'
					self.accelSpeed = self.accelSpeed + self.accelF
				else:
					self.accel = False
					self.decelFinish = False
			elif self.decel == True:
				if self.decelSpeed > 0:
					d = self.decelSpeed
					if self.face == 'ds': # down key
						self.rect.y += d*self.interval# move down
						#self.rect = self.image.get_rect()
						self.update_image(self.IMAGES_FRONT_DECEL)
					elif self.face == 'us': # up key
						self.rect.y -= d*self.interval # move up
						#self.rect = self.image.get_rect()
						self.update_image(self.IMAGES_BACK_DECEL)
					elif self.face == 'rs': # right key
						self.rect.x += d*self.interval # move right
						#self.rect = self.image.get_rect()
						self.update_image(self.IMAGES_RIGHT_DECEL)
					elif self.face == 'ls': # left key
						self.rect.x -= d*self.interval# move left
						#self.rect = self.image.get_rect()
						self.update_image(self.IMAGES_LEFT_DECEL)
					self.decelSpeed = self.decelSpeed + self.decelF
				else:
					self.decel = False
					self.face = list(self.face)[0]
					self.decelFinish = True
			if (self.face == 'r'):
				self.update_image(self.IMAGES_RIGHT)
			elif (self.face == 'u'):
				self.update_image(self.IMAGES_BACK)
			elif (self.face == 'l'):
				self.update_image(self.IMAGES_LEFT)
			elif (self.face == 'd'):
				self.update_image(self.IMAGES_FRONT)
			#standing
			elif(self.face == 'rs'):
				self.image = self.IMAGES_RIGHT[0]
			elif(self.face == 'us'):
				self.image = self.IMAGES_BACK[0]
			elif(self.face == 'ls'):
				self.image = self.IMAGES_LEFT[0]
			elif(self.face == 'ds'):
				self.image = self.IMAGES_FRONT[0]
			#accel
			elif(self.face == 'ra'):
				self.update_image(self.IMAGES_RIGHT_ACCEL)
			elif(self.face == 'ua'):
				self.update_image(self.IMAGES_BACK_ACCEL)
			elif(self.face == 'la'):
				self.update_image(self.IMAGES_LEFT_ACCEL)
			elif(self.face == 'da'):
				self.update_image(self.IMAGES_FRONT_ACCEL)
			#decel
			elif(self.face == 'rd'):
				self.update_image(self.IMAGES_RIGHT_DECEL)
			elif(self.face == 'ud'):
				self.update_image(self.IMAGES_BACK_DECEL)
			elif(self.face == 'ld'):
				self.update_image(self.IMAGES_LEFT_DECEL)
			else:
				self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()

	def update_image(self, imageArray):
		try:
			self.image = imageArray[self.frame].convert_alpha()
			#self.rect = self.image.get_rect()
			#self.rect.center = (Player.WIDTH/2, Player.HEIGHT/2)
		except IndexError:
			self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()
			self.face = list(self.face)[0]
		
	def draw(self, screen, block_group):
		""" Draw on surface """
		# self.handle_collision(block_group)
		self.check_boundary(screen)
		# blit yourself at your current position
		screen.blit(self.image, (self.rect.x, self.rect.y))
		PD.flip()
		
	def check_boundary(self, screen):
		if self.rect.x < 0:
			PM.music.stop()
			self.rect.x = 0
			PM.music.play(0)
			PM.music.fadeout(4500)
		elif self.rect.x > (screen.get_width() - self.image.get_width()):
			PM.music.stop()
			self.rect.x = screen.get_width() - self.image.get_width()
			PM.music.play(0)
			PM.music.fadeout(4500)
		if self.rect.y < 0:
			PM.music.stop()
			self.rect.y = 0
			PM.music.play(0)
			PM.music.fadeout(4500)
		elif self.rect.y > (screen.get_height() - self.image.get_height()):
			PM.music.stop()
			self.rect.y = (screen.get_height() - self.image.get_height())
			PM.music.play(0)
			PM.music.fadeout(4500)


	def load_images_helper_accdec(self, imageArray, sheet):
		alphabg = (23,23,23)
		for i in range(3):
			surface = PG.Surface((100, 100))
			surface.set_colorkey(alphabg)
			surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
			imageArray.append(surface)
		return imageArray

	def load_images_helper(self, imageArray, sheet):
		alphabg = (23,23,23)
		for i in range(3,7):
			surface = PG.Surface((100, 100))
			surface.set_colorkey(alphabg)
			surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
			imageArray.append(surface)
		for i in range(5,0,-1):
			surface = PG.Surface((100, 100))
			surface.set_colorkey(alphabg)
			surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
			imageArray.append(surface)
		for i in range(0,3):
			surface = PG.Surface((100, 100))
			surface.set_colorkey(alphabg)
			surface.blit(sheet, (0,0), (i*100, 0, 100, 100))
			imageArray.append(surface)
		return imageArray

	def load_images(self):
		Player.IMAGES_RIGHT = []
		Player.IMAGES_LEFT = []
		Player.IMAGES_FRONT = []
		Player.IMAGES_BACK = []
		Player.IMAGES_RIGHT_ACCEL = []
		Player.IMAGES_LEFT_ACCEL = []
		Player.IMAGES_FRONT_ACCEL = []
		Player.IMAGES_BACK_ACCEL = []
		Player.IMAGES_RIGHT_DECEL = []
		Player.IMAGES_LEFT_DECEL = []
		Player.IMAGES_FRONT_DECEL = []
		Player.IMAGES_BACK_DECEL = []
		sheetR = PI.load("FPGraphics/MC/MCwalk/MCRightWalk.png").convert_alpha()
		sheetL = PI.load("FPGraphics/MC/MCwalk/MCLeftWalk.png").convert_alpha()
		sheetF = PI.load("FPGraphics/MC/MCwalk/MCFrontWalk.png").convert_alpha()
		sheetB = PI.load("FPGraphics/MC/MCwalk/MCBackWalk.png").convert_alpha()
		#accel
		sheetRA = PI.load("FPGraphics/MC/MCwalk/MCAccelRight.png").convert_alpha()
		sheetLA = PI.load("FPGraphics/MC/MCwalk/MCAccelLeft.png").convert_alpha()
		sheetFA = PI.load("FPGraphics/MC/MCwalk/MCAccelFront.png").convert_alpha()
		sheetBA = PI.load("FPGraphics/MC/MCwalk/MCAccelBack.png").convert_alpha()
		#decel
		sheetRD = PI.load("FPGraphics/MC/MCwalk/MCDecelRight.png").convert_alpha()
		sheetLD = PI.load("FPGraphics/MC/MCwalk/MCDecelLeft.png").convert_alpha()
		sheetFD = PI.load("FPGraphics/MC/MCwalk/MCDecelFront.png").convert_alpha()
		sheetBD = PI.load("FPGraphics/MC/MCwalk/MCDecelBack.png").convert_alpha()
		Player.IMAGES_RIGHT = self.load_images_helper(Player.IMAGES_RIGHT, sheetR)
		Player.IMAGES_LEFT = self.load_images_helper(Player.IMAGES_LEFT, sheetL)
		Player.IMAGES_FRONT = self.load_images_helper(Player.IMAGES_FRONT, sheetF)
		Player.IMAGES_BACK = self.load_images_helper(Player.IMAGES_BACK, sheetB)
		Player.IMAGES_RIGHT_ACCEL = self.load_images_helper_accdec(Player.IMAGES_RIGHT_ACCEL, sheetRA)
		Player.IMAGES_LEFT_ACCEL = self.load_images_helper_accdec(Player.IMAGES_LEFT_ACCEL, sheetLA)
		Player.IMAGES_FRONT_ACCEL = self.load_images_helper_accdec(Player.IMAGES_FRONT_ACCEL, sheetFA)
		Player.IMAGES_BACK_ACCEL = self.load_images_helper_accdec(Player.IMAGES_BACK_ACCEL, sheetBA)
		Player.IMAGES_RIGHT_DECEL = self.load_images_helper_accdec(Player.IMAGES_RIGHT_DECEL, sheetRD)
		Player.IMAGES_LEFT_DECEL = self.load_images_helper_accdec(Player.IMAGES_LEFT_DECEL, sheetLD)
		Player.IMAGES_FRONT_DECEL = self.load_images_helper_accdec(Player.IMAGES_FRONT_DECEL, sheetFD)
		Player.IMAGES_BACK_DECEL = self.load_images_helper_accdec(Player.IMAGES_BACK_DECEL, sheetBD)
