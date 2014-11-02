import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
from Player import Player
from Enemy import Enemy


class Item(PS.Sprite):
	def __init__(self, rect, theType, lifetime = 500):
		PS.Sprite.__init__(self)
		self.rect = None
		self.rect.x = rect.x
		self.rect.y = rect.y
		self.lifetime = 1000
		self.type = theType
		self.lifetime = lifetime
		self.image = Item.IMAGE
		self.grabbed = False


	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))

	def update(self, surface, player = None):
		self.draw(surface)
		self.lifetime -= 1
		if self.lifetime == 0:
			pass
			# self.disappear()

		# collided = self.handle_collisions(player)
		# if collided:
		# 	self.grabbed = True


	def handle_collisions(self, player):
		collisions = PS.spritecollide(self, player, False)
		if len(collisions) > 0:
			return True
		return False

	def disappear(self):
		pass

	def appear(self):
		pass

	def use(self):
		pass

class IceCreamScoop(Item):
	def __init__(self, x_coor, y_coor):
		Item.IMAGE = PI.load("FPGraphics/MC/weapon/FPR.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x_coor
		self.rect.y = y_coor
		self.type = 1
		self.lifetime = 800

		Item.__init__(self, self.rect, self.type, self.lifetime)


