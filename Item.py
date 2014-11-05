import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
# from Player import Player
# from Enemy import Enemy


class Item(PS.DirtySprite):
	def __init__(self, therect, theType, lifetime = 500):
		PS.DirtySprite.__init__(self)
		self.rect = Item.IMAGE.get_rect()
		self.rect.x = therect.x
		self.rect.y = therect.y
		self.type = theType
		self.lifetime = lifetime
		self.surface = Item.surface
		self.use_count = Item.use_count
		self.grabbed = False
		self.remove = False

	def get_use_count(self):
		return self.use_count

	def get_type(self):
		return self.type

	def will_remove(self):
		return self.remove

	def draw(self):
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

	def update(self, block_group, player):
		self.draw()
		self.lifetime -= 1
		if self.lifetime == 0:
			self.disappear()
		self.dirty = 1

	def disappear(self):
		self.remove = True

	def appear(self):
		pass
		

class IceCreamScoop(Item):
	def __init__(self, x_coor, y_coor, surface):
		Item.IMAGE = PI.load("FPGraphics/drops/DropIceCream.png").convert_alpha()
		self.image = Item.IMAGE
		self.rect = self.image.get_rect()
		self.rect.x = x_coor + 25
		self.rect.y = y_coor + 25
		self.type = 1
		self.lifetime = 800
		Item.surface = surface
		Item.use_count = 3


		Item.__init__(self, self.rect, self.type, self.lifetime)

class BreadDrop(Item):
	def __init__(self, x_coor, y_coor, surface):
		Item.IMAGE = PI.load("FPGraphics/drops/breadDrop.png").convert_alpha()
		self.image = Item.IMAGE
		self.rect = self.image.get_rect()
		self.rect.x = x_coor + 25
		self.rect.y = y_coor + 25
		self.type = 1
		self.lifetime = 800
		Item.surface = surface
		Item.use_count = 3
		Item.__init__(self, self.rect, self.type, self.lifetime)

class LettuceDrop(Item):
	def __init__(self, x_coor, y_coor, surface):
		Item.IMAGE = PI.load("FPGraphics/drops/lettuceDrop.png").convert_alpha()
		self.image = Item.IMAGE
		self.rect = self.image.get_rect()
		self.rect.x = x_coor + 25
		self.rect.y = y_coor + 25
		self.type = 1
		self.lifetime = 800
		Item.surface = surface
		Item.use_count = 3
		Item.__init__(self, self.rect, self.type, self.lifetime)

class MeatDrop(Item):
	def __init__(self, x_coor, y_coor, surface):
		Item.IMAGE = PI.load("FPGraphics/drops/meatDrop.png").convert_alpha()
		self.image = Item.IMAGE
		self.rect = self.image.get_rect()
		self.rect.x = x_coor + 25
		self.rect.y = y_coor + 25
		self.type = 1
		self.lifetime = 800
		Item.surface = surface
		Item.use_count = 3
		Item.__init__(self, self.rect, self.type, self.lifetime)

class BurgerDrop(Item):
	def __init__(self, x_coor, y_coor, surface):
		Item.IMAGE = PI.load("FPGraphics/drops/burgerDrop.png").convert_alpha()
		self.image = Item.IMAGE
		self.rect = self.image.get_rect()
		self.rect.x = x_coor + 25
		self.rect.y = y_coor + 25
		self.type = 1
		self.lifetime = 800
		Item.surface = surface
		Item.use_count = 3
		Item.__init__(self, self.rect, self.type, self.lifetime)