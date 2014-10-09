#Drawing Functions
import sys as SYS
import pygame as PG
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX

mapcolors = {'D': (154, 205, 50), 
			'W' : (30, 144, 255),
			'K' : (255, 255, 0)}

class Globals(object):
	SCREEN = None #Surface
	SCREENSURFACE = None
	OPTIONS = None #Options list from options.txt
	WIDTH = None
	HEIGHT = None
	STATE = None
	RUNNING = None
	OBJECTS = {'None': None }
	GRID = {'Null':0}
	INITIALGRID = {'Null':0}

#Block sprite class
class Block(PG.sprite.Sprite):
	def __init__(self, color, rect):
		PG.sprite.Sprite.__init__(self)
		self.image = PG.Surface([rect.width, rect.height])
		

		self.color = color
		self.image.fill(self.color)
		self.rect = rect
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		Globals.SCREEN = PDI.get_surface()

	def draw_block(self):
		Globals.SCREEN.blit(self.image, self.rect)

	def get_color(self):
			return self.color

	def get_rect(self):
		return self.rect

	def get_right(self):
		return self.x + self.rect.width

	def get_left(self):
		return self.x

	def get_top(self):
		return self.y

	def get_bottom(self):
		return self.y + self.rect.height

	def set_rectLeft(self, rectLeft):
		self.x = rectLeft

	def set_rectTop(self, rectTop):
		self.y = rectTop

class Map(object):
	def __init__(self, mapfile):
		self.map = self.get_map(mapfile)
		self.not_drawables = ['.']
		self.objects = ['D', 'W', 'K'] #Door, Wall, Key
		#size of an individual block in the grid
		self.grid_size = [40, 30]
		self.grid_dimensions = self.get_dimensions(self.map)
		self.pix_dimensions = [self.grid_dimensions[0] * 50, self.grid_dimensions[1] * 50]
		self.surface = PG.Surface(self.pix_dimensions)
		#group of sprites in the map
		self.object_group = PG.sprite.Group()

	#returns list of lines in the mapfile
	def get_map(self, mapfile):
		with open(mapfile, 'r') as f:
			lines = f.readlines()
		return lines

	def get_dimensions(self, m):
		height = len(m)
		line = list(m[0])
		width = len(line) - 1 #subtract the \n character
		return [height, width]

	def get_object_group(self):
		self.objectify_map()
		return self.object_group

	def objectify_map(self):
		#the x and y coordinates as you traverse the map
		x_coor = 0 
		y_coor = 0

		#traverse the map, creating block sprites
		for x in range(self.grid_dimensions[0]):
			#get the list of characters in the mapfile
			char_list = list(self.map[x])
			x_coor = 0
			for y in range(self.grid_dimensions[1]):
			#wall blocks
				if char_list[y] == 'W':
					new_block = create_Block(mapcolors['W'], PG.Rect(x_coor, y_coor, self.grid_size[0], self.grid_size[1]))
					new_block.set_rectTop(y_coor)
					new_block.set_rectLeft(x_coor)
					self.object_group.add(new_block)

				#key block
				elif char_list[y] == 'K':
					new_block = create_Block(mapcolors['K'], PG.Rect(x_coor, y_coor, self.grid_size[0], self.grid_size[1]))
					new_block.set_rectTop(y_coor)
					new_block.set_rectLeft(x_coor)
					self.object_group.add(new_block)
				#Door blocks
				elif char_list[y] == 'D':
					new_block = create_Block(mapcolors['D'], PG.Rect(x_coor, y_coor, self.grid_size[0], self.grid_size[1]))
					new_block.set_rectTop(y_coor)
					new_block.set_rectLeft(x_coor)
					self.object_group.add(new_block)

				x_coor += self.grid_size[0]

			y_coor += self.grid_size[1]

	def draw_map(self):
		for block in self.object_group:
			block.draw_block()

#creates a new block sprite
def create_Block(color, rect):
	new_block = Block(color, rect)
	return new_block

	