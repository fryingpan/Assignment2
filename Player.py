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

	def __init__(self, speed = 1):
		# Call the parent class (Sprite) constructor
		PS.Sprite.__init__(self)
		self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()
                self.rect = self.image.get_rect()
		self.rect.x = 100
		self.rect.y = 1150
		self.face = 'd'
		self.load_images()
		self.speed = speed
		self.time = 0.0
		self.frame = 0
		self.interval = 0
		self.got_key = False #will turn to True once you've run into the yellow block
		#collision conditions, if true, we will not move in that direction
                self.health = 10
                self.score = 0

	def get_face(self):
		return self.face

	def player_got_key(self):
		return self.got_key

	def get_coordinates(self):
		coordinates = [self.rect.x, self.rect.y]
		return coordinates

	def open_door(self,bg): #pass the enire block group.
		for block in bg:
			if block.get_color() == (154, 205, 50):
				block.kill()

	def handle_collision(self, bg):
		collisions = PS.spritecollide(self, bg, False)
		if self.face == 'r' or self.face == 'ra' or self.face == 'rs':
			collisions = PS.spritecollide(self, bg, False)
			once = True
			for collision in collisions:
				if collision.get_color() == (255, 255, 0, 255): #kills the yellow brick. Don't make anything else yellow :/
					collision.kill()
					self.open_door(bg)
					self.got_key = True
				elif once:
					if(self.rect.x + self.rect.width) >= collision.rect.left:
						self.rect.x = collision.rect.left - self.rect.width
						once = False
			
		elif self.face == 'l' or self.face == 'la' or self.face == 'ls':
			collisions = PS.spritecollide(self, bg, False)
			once = True
			for collision in collisions:
				if collision.get_color() == (255, 255, 0, 255): #kills the yellow brick.
					collision.kill()
					self.open_door(bg)
					self.got_key = True
				elif once:
					if (self.rect.x) <= (collision.rect.left + collision.rect.width):
						self.rect.x = collision.rect.left + collision.rect.width
						once = False
		elif self.face == 'd' or self.face == 'da' or self.face == 'ds':
			once = True
			for collision in collisions:
				if collision.get_color() == (255, 255, 0, 255): #kills the yellow brick.
					collision.kill()
					self.open_door(bg)
					self.got_key = True
				elif once:
					if (self.rect.y + self.rect.height) >= collision.rect.top:
						self.rect.y = collision.rect.top - self.rect.height
						once = False
		elif self.face == 'u' or self.face == 'ua' or self.face == 'us':
			collisions = PS.spritecollide(self, bg, False)
			once = True
			for collision in collisions:
				if collision.get_color() == (255, 255, 0, 255): #kills the yellow brick.
					collision.kill()
					self.open_door(bg)
					self.got_key = True
				elif once:
					if (self.rect.y <= (collision.rect.top + collision.rect.height)):
						self.rect.y = collision.rect.top + collision.rect.height
						once = False
	
        def handle_keys(self, bg, interval = 5): #add enemy_bg to character_handle_keys in setup
		""" Handles Keys """
		key = PG.key.get_pressed()
		dist = self.speed # distance moved in 1 frame, try changing it to 5
		self.interval = interval				
		if key[PG.K_DOWN]: # down key
			self.rect.y += dist*interval# move down
			#self.rect = self.image.get_rect()
			self.face = 'd'
			self.handle_collision(bg)
		elif key[PG.K_UP]: # up key
			self.rect.y -= dist*interval # move up
			#self.rect = self.image.get_rect()
                        self.face = 'u'
			self.handle_collision(bg)
		elif key[PG.K_RIGHT]: # right key
			self.rect.x += dist*interval # move right
			#self.rect = self.image.get_rect()
			self.face = 'r'
			self.handle_collision(bg)
		elif key[PG.K_LEFT]: # left key
			self.rect.x -= dist*interval# move left
			#self.rect = self.image.get_rect()
			self.face = 'l'
			self.handle_collision(bg)
                #elif key[PG.K_SPACE]: #space key ATTACK
                        #self.attack(enemy_bg)
		else: #ds = down 'standing' (not moving) **********
			if self.face == 'd':
				self.face = 'ds'
			if self.face == 'u':
				self.face = 'us'
			if self.face == 'r':
				self.face = 'rs'
			if self.face == 'l':
				self.face = 'ls'
		
        '''def attack(self, bg): #this bg is enemy block group
                #collisions with the new weapon rect!
                self.weapon.update_image(self.weaponImage)
                weapon.x = self.rect.x+100
                weapon.y = self.rect.y+50
                collisions = PS.spritecollide(self, bg, False)
                for collision in collisions:
                    self.score = self.score + 1
                    collision.kill()'''

	def update(self, delta, bg):
		PLAYER_IMAGE_LENGTH = 12 #all player sprite has 12 frames
		#update time and frame
		key = PG.key.get_pressed()
		#camera stuff
		# increment in x direction
		#self.rect.left += self.xvel
		# do x-axis collisions
		# self.collide(self.xvel, 0, platforms)
		# increment in y direction
		#self.rect.top += self.yvel
		#camera stuff end


		self.time = self.time + delta
		if self.time > Player.CYCLE:
			self.time = 0.0
		frame = int(self.time / (Player.CYCLE / PLAYER_IMAGE_LENGTH))
		
		if frame != self.frame:
			self.frame = frame
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
		except IndexError:
			self.image = PI.load("FPGraphics/MC/MCwalk/MCFront.png").convert_alpha()
			self.face = list(self.face)[0]
		
	def draw(self, screen, block_group):
		""" Draw on surface """
		self.check_boundary(screen)
		# blit yourself at your current position
		screen.blit(self.image, (self.rect.x, self.rect.y))
		PD.flip()
		
	def check_boundary(self, screen):
		width = screen.get_width() *2
		height = screen.get_height() * 2
		if self.rect.x < 0:
			PM.music.stop()
			self.rect.x = 0
			PM.music.play(0)
			PM.music.fadeout(4500)
		elif self.rect.x > (width - self.image.get_width()):
			PM.music.stop()
			self.rect.x = width - self.image.get_width()
			PM.music.play(0)
			PM.music.fadeout(4500)
		if self.rect.y < 0:
			PM.music.stop()
			self.rect.y = 0
			PM.music.play(0)
			PM.music.fadeout(4500)
		elif self.rect.y > (height - self.image.get_height()):
			PM.music.stop()
			self.rect.y = (height - self.image.get_height())
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
