# Assignment 2
# Frying Pan

try:
	import pygame as PG
	from pygame.locals import *
	import pygame.time as PT
	import sys
	from Player import Player
	from Enemy import Enemy
	import pygame.sprite as PS
	import pygame.display as PD
	import pygame.color as PC
	import pygame.event as PE
	import Map
	import camera as cam
	import pygame.font as PF
	
except ImportError, err:
	print "%s Failed to Load Module: %s" % (__file__, err)
	import sys
	sys.exit(1)

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

def initialize():
	# num_enemies = 13
	# interval = 0.005
	# fps = 40
	# game = Game(interval, fps, num_enemies)
	Locals.CHANGESTATE = 'Game'
	


class Game(object):

	def __init__(self, interval, fps, num_enemies):
		self.interval = interval
		self.fps = fps
		self.num_enemies=num_enemies
	
		PG.init()
		self.screen = PD.set_mode((800, 600))
		self.screen_rect = self.screen.get_rect()
		self.screen.fill((255,255,255))
		PD.set_caption("Master Chef's wicked adventure with his ice cream buddies")
		
		self.fps = fps
		self.speed = 4*self.fps
		#sprite group containing all sprites
		self.all_sprites = PS.Group()

		#Initialize objects on screen----------------
		self.character = Player(self.speed)
		self.all_sprites.add(self.character)


		#create enemy group 
		self.enemy_list = PS.Group()

		#add all the enemies to the list of enemies
		for e in range(num_enemies):  
			enemy = Enemy(self.screen, self.speed)
			self.enemy_list.add(enemy)

		self.map = Map.Map('mapfile.txt')
		#get block sprite group from the map file
		self.block_group = self.map.get_object_group()
		#add the blocks to the sprite group containing all sprites
		for block in self.block_group:
			#if block.get_color != 'yellow':
			self.all_sprites.add(block) # only has map sprites
			#else:
			   # self.key_sprite.add(block)

		self.bigmap_rect = Rect(0,0, 1600, 1200)

		self.camera = cam.Camera(self.map.get_surface())


		#I don't actually know what this does
		PE.set_allowed([QUIT, KEYDOWN])

		self.clock = PT.Clock()
		self.current_time = PT.get_ticks()
		self.updates = 0
		self.interval = interval
		Locals.CHANGESTATE = 'Game'

				#fonts
		self.font = PF.SysFont('Arial', 25)
		s = "Score: " + str(self.character.score) #Must have some variable. Add variable name here, uncomment, should work.
		self.screen.blit(self.font.render(s, True, (255,255,255)), (25, 550))
		h = "Health: " + str(self.character.health) #Must have some variable. Add variable name here, uncomment, should work.
		self.screen.blit(self.font.render(s, True, (255,255,255)), (25, 520))
	
	def run(self):
		running = True
		while running:
			new_time = PT.get_ticks()
			frame_time = (new_time - self.current_time)/1000.0
			self.current_time = new_time
			self.clock.tick()

			running = self.handleEvents()
			if(running == False):
				return False
			#Key Handling----------------------------

			# self.screen.fill((0,0,0)) # fill the screen with white
			self.map.fill()

			#draw blocks
			self.map.draw_map()


			#move and draw the enemies
			player_face = self.character.get_face()
			for enemy in self.enemy_list.sprites():
				Enemy_face = enemy.get_face()
				enemy.draw(self.map.get_surface())

			#draw blocks
			self.map.draw_map()

			self.character.draw(self.map.get_surface(), self.block_group) # draw the character to the screen

			#update camera's position on the map
			background = self.camera.update(self.character.get_coordinates(), self.screen, self.map.get_surface())

			# self.screen.blit(background, (0,0))

			PD.flip()

			self.updates = 0

			#clock is added
			clock = PT.Clock()

			while frame_time > 0.0:
				delta = min(frame_time, self.interval)
				for enemy in self.enemy_list.sprites():
                                        enemy.update(delta)
				self.character.handle_keys(self.block_group, self.interval)
				frame_time -= delta
				self.updates += 1

				last = PT.get_ticks()

				clock.tick()

				PD.flip()

				elapsed = (PT.get_ticks() - last) / 1000.0
				if (PG.key.get_pressed()):
					self.update(self.character, elapsed)

			PD.update() # update the screen
			
	def update(self, player, delta):
			s = "Score: " + str(player.score) #Must have some variable. Add variable name here, uncomment, should work.
			self.screen.blit(self.font.render(s, True, (255,255,255)), (25, 550))
			s = "Health: " + str(player.health) #Must have some variable. Add variable name here, uncomment, should work.
			self.screen.blit(self.font.render(s, True, (255,255,255)), (25, 520))
			player.update(delta, self.block_group)

	def handleEvents(self):
		for event in PE.get():
			if event.type == PG.QUIT:
				return False

			# handle user input
			elif event.type == KEYDOWN:
			# if the user presses escape, quit the event loop.
				if event.key == K_ESCAPE:
					Locals.CHANGESTATE = 'Menu'
					return False
		return True

		'''def addScoreText(self, player):
			s = "Score: " + str(player.score) #Must have some variable. Add variable name here, uncomment, should work.
			self.screen.blit(self.font.render(s, True, (255,255,255)), (25, 550))
			PD.update()

		def addHitPointsText(self, player):
			s = "Health: " + str(player.health) #Must have some variable. Add variable name here, uncomment, should work.
			self.screen.blit(self.font.render(s, True, (255,255,255)), (25, 520))
			PD.update()'''

