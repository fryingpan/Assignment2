# Assignment 2
# Frying Pan

try:
	import pygame as PG
	import pygame.image as PI
	from pygame.locals import *
	import pygame.time as PT
	import sys
	from Player import Player
	from IceCream import IceCream
	import pygame.sprite as PS
	import pygame.display as PD
	import pygame.color as PC
	import pygame.event as PE
	import Map
	import camera as cam
	import pygame.font as PF
	import random
	from Trap import Puddle
	from Cutscene import Cutscene
        from objective import Objective
        import pygame.mixer as PM

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
	SCORE = 0


def initialize():
	# interval = 0.005
	# fps = 40
	# game = Game(interval, fps, num_enemies)
	Locals.CHANGESTATE = 'Game'


class Game(object):

	def __init__(self, interval):
                PM.music.load("music/gameplay.mod")
		self.interval = interval
		self.fps = 40
		self.num_enemies = 5
                self.remainingEnemies = self.num_enemies

		PG.init()
		self.screen = PD.set_mode((800, 600))
		self.screen_rect = self.screen.get_rect()
		self.screen.fill((255, 255, 255))
		PD.set_caption("Master Chef's wicked adventure " +
					   "with his ice cream buddies")

		#sprite group containing all sprites
		self.all_sprites = PS.Group()

		#Initialize objects on screen----------------
		self.character = Player(self.fps)
		Locals.SCORE = self.character.score
		self.player_group = PS.GroupSingle(self.character)

		self.all_sprites.add(self.character)

		#create icecream group
		self.icecream_list = PS.Group()
		self.enemy_ID = -1  # no enemy
		self.invincibility_count = 0

		#add all the enemies to the list of enemies
		for e in range(self.num_enemies):
			icecream = IceCream(random.randint(500,1000), random.randint(500,1000),self.fps)
			self.icecream_list.add(icecream)

		self.map = Map.Map('mapfile.txt')
		#get block sprite group from the map file
		self.block_group = self.map.get_object_group()
		#add the blocks to the sprite group containing all sprites
		for block in self.block_group:
			#if block.get_color != 'yellow':
			self.all_sprites.add(block)  # only has map sprites
			#else:
			   # self.key_sprite.add(block)

		self.bigmap_rect = Rect(0, 0, 1600, 1200)

		self.camera = cam.Camera(self.map.get_surface())

		#list that holds traps
		self.trap_list = []

		PE.set_allowed([QUIT, KEYDOWN])
		self.clock = PT.Clock()
		self.current_time = PT.get_ticks()
		self.updates = 0
		self.interval = interval
		Locals.CHANGESTATE = 'Game'

				#fonts
		self.font = PF.SysFont('Arial', 25)
		s = "Score: " + str(self.character.score)
		self.screen.blit(self.font.render(s, True, (255, 255, 255)), (25, 550))
		h = "Health: " + str(self.character.health)
		self.screen.blit(self.font.render(s, True, (255, 255, 255)), (25, 520))
		#Win/Lose items
		self.win_image = PI.load("FPGraphics/" +
								 "specialEffects/UWIN.png").convert_alpha()
		self.lose_image = PI.load("FPGraphics/" +
								  "specialEffects/ULOSE.png").convert_alpha()
		self.end_time = 800
		self.end_image_position = (100, 178)

		self.make_disappear = False


		self.trap_group = PS.Group()
		self.background = self.map.create_background()
		self.allsprites = PS.LayeredDirty(self.player_group, self.icecream_list, self.trap_group)
		self.allsprites.clear(self.screen, self.background)
		self.cheesed = True

                self.objective = Objective()

	def run(self):
                lv1_cutscene = Cutscene(self.screen,1)
		running = True

                #music
                PM.music.play(0)

		while running:
			# self.map.draw_map()
			new_time = PT.get_ticks()
			frame_time = (new_time - self.current_time)/1000.0
			self.current_time = new_time
			self.clock.tick()

			running = self.handleEvents()
			if(running is False):
				return False
			#Key Handling----------------------------

			# self.screen.fill((0,0,0)) # fill the screen with white
			# self.map.fill()

			#draw blocks
			# self.map.draw_map()
			#move and draw the enemies
			player_face = self.character.get_face()
			weapon_attack = False

			for trap in self.trap_list:
				trap.update(None, None, self.player_group)
				if (trap.get_trap_attack() and self.invincibility_count == 0):
					weapon_attack = True
				if trap.will_remove():
					self.trap_list.remove(trap)
					self.trap_group.remove(trap)
					self.allsprites = PS.LayeredDirty(self.player_group, self.icecream_list, self.trap_group)


			for icecream in self.icecream_list.sprites():
				icecream_face = icecream.get_face()
				#see if the enemy will release weapon/attack
				if (icecream.will_attack()):
					#get a new puddle sprite
					new_trap = icecream.attack(self.map.get_surface())
					#add the new trap to the list of traps
					self.trap_list.append(new_trap)
					self.trap_group.add(new_trap)
					self.allsprites = PS.LayeredDirty(self.player_group, self.icecream_list, self.trap_group)
				icecream.draw(self.map.get_surface())


			#draw blocks
			# self.map.draw_map()

			self.character.draw(self.map.get_surface(), self.block_group)
			# draw the character to the screen

			#update camera's position on the map
			background = self.camera.update(self.character.get_coordinates(),
											self.screen, self.map.get_surface()
											)
			#####temporary code to detect for door objective###############
			print("x " + str(self.character.rect.x) + " y " + str(self.character.rect.y))
			if(self.character.rect.x > 2400 and self.character.rect.x < 2700
				and self.character.rect.y > 250 and self.character.rect.y < 400
				and self.cheesed == True):
				print("got here")
				self.cheesed = False
				self.objective.updateObjective(self.screen, 1)

			self.update_score(self.character)

			# self.screen.blit(background, (0,0))

			# PD.flip()

			self.updates = 0

			#clock is added
			clock = PT.Clock()

			while frame_time > 0.0:

                                #adding objective banner here
                                self.objective.updateObjective(self.screen, 0)

				delta = min(frame_time, self.interval)
				self.enemy_ID = -1
				for icecream in self.icecream_list.sprites():
					#update position and collisions
					icecream.update(delta, self.block_group, self.player_group)
					#see if ice cream collided with player
					if(icecream.get_attacked_player() or weapon_attack):
						if weapon_attack:
							weapon_attack = False
						#if so start invincibility count after attack
						self.invincibility_count = 200
						#see which enemy attacked the player
						self.enemy_ID = icecream.get_ID()
				#If enemy attacked the player while player not invincible
				if(self.enemy_ID != -1 and self.invincibility_count == 200):
					self.character.decrement_health(self.enemy_ID)
					self.enemy_ID = -1
				#decrement invincibility count if player is in invincibility
				if(self.invincibility_count > 0):
					if(self.invincibility_count % 50 == 0):
						self.character.invincibility_frames()
					self.invincibility_count -= 1

				self.character.handle_keys(self.block_group,
										   self.icecream_list,
										   self.map.get_surface(),
										   self.interval)

				self.make_disappear = self.character.get_open_door()

				if self.make_disappear:
					self.background = self.map.update_background()
					self.make_disappear = False
				frame_time -= delta
				self.updates += 1

                                self.remainingEnemies = self.num_enemies - self.character.score
                                if self.remainingEnemies < self.num_enemies:
                                    self.objective.updateObjective(self.screen, 2)

				last = PT.get_ticks()

				clock.tick()

				elapsed = (PT.get_ticks() - last) / 1000.0

				self.character.set_interval(elapsed)

				self.character.update(delta, self.block_group, None)

				self.update_score(self.character)
				self.allsprites.update(delta, self.block_group, self.player_group)
				rects = self.allsprites.draw(self.map.get_surface(), self.background)
				PG.display.update(rects)

				PD.flip()

				elapsed = (PT.get_ticks() - last) / 1000.0
				if (PG.key.get_pressed()):
					self.update_player(self.character, elapsed)

			Locals.SCORE = self.character.score
			if(Locals.CHANGESTATE == "Menu"):
                                PM.music.fadeout(1000)
				return False
			PD.update()  # update the screen

	def update_player(self, player, delta):
		if(player.score == self.num_enemies):
			self.screen.blit(self.win_image, self.end_image_position)
			if(self.end_time > 0):
				self.end_time -= 1
			else:
                                PM.music.fadeout(1000)
				Locals.CHANGESTATE = "Menu"
		if(player.health <= 0):
			self.screen.blit(self.lose_image, self.end_image_position)
			if(self.end_time > 0):
				self.end_time -= 1
			else:
                                PM.music.fadeout(1000)
				Locals.CHANGESTATE = "Menu"
		# player.update(delta, self.block_group)

	def update_score(self, player):
		if(player.score == self.num_enemies):
			self.screen.blit(self.win_image, self.end_image_position)
			if(self.end_time > 0):
				self.end_time -= 1
			else:
				Locals.CHANGESTATE = "Menu"
		if(player.health <= 0):
			self.screen.blit(self.lose_image, self.end_image_position)
			if(self.end_time > 0):
				self.end_time -= 1
			else:
				Locals.CHANGESTATE = "Menu"    
		s = "Score: " + str(player.score)
		self.screen.blit(self.font.render(s, True, (255, 255, 255)),
						 (25, 550))
		s = "Health: " + str(player.health)
		self.screen.blit(self.font.render(s, True, (255, 255, 255)),
						 (25, 520))

	def icecreamupdate(self, icecream, delta):
		icecream.update(delta)

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
