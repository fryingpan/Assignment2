#Drawing Functions
import sys as SYS
import random
import pygame as PG
import pygame.display as PDI
import pygame.event as PE
import pygame.font as PF
import pygame.sprite as PS
import pygame.image as PI
import pygame.time as PT
import pygame.color as PC
import pygame.mixer as PX
from collections import deque

mapcolors = {'D': (154, 205, 50),
			 'W': (30, 144, 255), 'K': (255, 255, 0, 255)}


class Globals(object):
	SCREEN = None  # Surface
	SCREENSURFACE = None
	OPTIONS = None  # Options list from options.txt
	WIDTH = None
	HEIGHT = None
	STATE = None
	RUNNING = None
	OBJECTS = {'None': None}
	GRID = {'Null': 0}
	INITIALGRID = {'Null': 0}


#Block sprite class
class Block(PG.sprite.DirtySprite):
	def __init__(self, img, rect, t):
		PG.sprite.DirtySprite.__init__(self)
		self.image = img
		self.rect = rect
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		Globals.SCREEN = PDI.get_surface()
		self.type = t

	def get_type(self):
		return self.type

	def draw_block(self, map_surface):
		map_surface.blit(self.image, self.rect)

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

	def update(self, delta, bg, player):
		if self.type == 'K' or self.type == 'D':
			self.dirty = 1

class Map(object):
	TILES_LOADED = False
	GRASS_ARRAY = []

	def __init__(self, mapfile):
		#load the grass images into an array
		if not Map.TILES_LOADED:
			Map.GRASS_ARRAY = self.load_tiles()
			Map.TILES_LOADED = True

		####(prepare to read mapfile)#######
		self.map = self.get_map(mapfile)
		#size of an individual block in the grid
		self.grid_size = [50, 50]
		self.grid_dimensions = self.get_dimensions(self.map)
		self.pix_dimensions = [self.grid_dimensions[0] * self.grid_size[0],
							   self.grid_dimensions[1] * self.grid_size[1]]
		self.surface = PG.Surface(self.pix_dimensions)
		self.object_group = PG.sprite.Group()

		self.grass_array = Map.GRASS_ARRAY
		# list that stores a pair of coordinates for each grass 
		# tile that needs to be drawn
		self.grasstiles = []
		self.grass_type = []

		#block arrays
		self.wallBlocksV = [] #vertical V
		self.wallBlocksH = [] #horizontal H
		self.wallBlocksE = [] #edges/corners; correspond to index num (see load_blocks)
		self.doorBlocks = [] # D
		self.shrubBlocks = [] # S
		#tree top = T, tree bottom = Y
		#so it's like ty thank you isn't that cute
		self.treeBlocksT = [] # T
		self.treeBlocksB = [] # Y
		self.keyBlocks = [] #K
		self.ICBlock = [] #I (icecream spots)
		self.disappearing_blocks = PS.Group()

		#enemy stuff
		self.ic_coord = [] #icecream

		self.spots_to_be_filled = []
		#create map from mapfile
		self.load_blocks(1)
		self.objectify_map()
		self.fill()

	def get_disappearing_blocks(self):
		return self.disappearing_blocks

	def load_tiles(self):
		tile_array = []
		tile_array.append(PI.load("FPGraphics/tiles/grassTile1.png"))
		tile_array.append(PI.load("FPGraphics/tiles/grassTile2.png"))
		tile_array.append(PI.load("FPGraphics/tiles/grassTile3.png"))
		return tile_array

	def load_blocks(self, lvl):
		#note: always load edge blocks with these indeces:
		#0 = HL; 1 = HR; 2 = VD; 3 = VU; 4 = TL; 5 = TR; 6 = BL; 7 = BR
		if(lvl == 1):
			self.wallBlocksV.append(PI.load("FPGraphics/tiles/lv1Wall1.png"))
			self.wallBlocksV.append(PI.load("FPGraphics/tiles/lv1Wall2.png"))
			self.wallBlocksH.append(PI.load("FPGraphics/tiles/lv1WallH1.png"))
			self.wallBlocksH.append(PI.load("FPGraphics/tiles/lv1WallH2.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallEHL.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallEHR.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallEVD.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallEVU.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallETL.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallETR.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallEBL.png"))
			self.wallBlocksE.append(PI.load("FPGraphics/tiles/lv1WallEBR.png"))
			self.doorBlocks.append(PI.load("FPGraphics/tiles/cheeseWall1.png"))
			self.doorBlocks.append(PI.load("FPGraphics/tiles/cheeseWall2.png"))
			self.doorBlocks.append(PI.load("FPGraphics/tiles/cheeseWall3.png"))
			self.shrubBlocks.append(PI.load("FPGraphics/tiles/lv1shrubBroc.png"))
			self.shrubBlocks.append(PI.load("FPGraphics/tiles/lv1shrubCauli.png"))
			self.shrubBlocks.append(PI.load("FPGraphics/tiles/lv1shrubRadish.png"))
			self.treeBlocksT.append(PI.load("FPGraphics/tiles/lv1treeT1.png"))
			self.treeBlocksT.append(PI.load("FPGraphics/tiles/lv1treeT2.png"))
			self.treeBlocksT.append(PI.load("FPGraphics/tiles/lv1treeT3.png"))
			self.treeBlocksB.append(PI.load("FPGraphics/tiles/lv1treeB1.png"))
			self.treeBlocksB.append(PI.load("FPGraphics/tiles/lv1treeB2.png"))
			self.treeBlocksB.append(PI.load("FPGraphics/tiles/lv1treeB3.png"))
			self.keyBlocks.append(PI.load("FPGraphics/tiles/lactasePill.png"))

	def get_surface(self):
			return self.surface

	def fill(self):
		self.surface.fill((0, 0, 0))

	#returns list of lines in the mapfile
	def get_map(self, mapfile):
		with open(mapfile, 'r') as f:
				lines = f.readlines()
		return lines

	def get_dimensions(self, m):
		height = len(m)
		line = list(m[0])
		width = len(line) - 1  # subtract the \n character
		return [width, height]

	def get_object_group(self):
			return self.object_group

	def objectify_map(self):
		#the x and y coordinates as you traverse the map
		x_coor = 0
		y_coor = 0

		#keep track of type of tree block
		treeblockType = deque()

		#traverse the map, creating block sprites
		for x in range(self.grid_dimensions[1]):
			#get the list of characters in the mapfile
			char_list = list(self.map[x])
			x_coor = 0
			for y in range(self.grid_dimensions[0]):
				# wall blocks
				if char_list[y] == 'V':
					new_block = create_Block(self.wallBlocksV[random.randint(0,len(self.wallBlocksV))-1],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
				elif char_list[y] == 'H':
					new_block = create_Block(self.wallBlocksH[random.randint(0,len(self.wallBlocksH))-1],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
				# key block
				elif char_list[y] == 'K':
					#change to just an obj later or whatever
					new_block = create_Block(self.keyBlocks[0],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
					self.disappearing_blocks.add(new_block)
					self.spots_to_be_filled.append((x_coor, y_coor))
				# Door blocks
				elif char_list[y] == 'D':
					new_block = create_Block(self.doorBlocks[random.randint(0,len(self.doorBlocks))-1],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
					self.disappearing_blocks.add(new_block)
					self.spots_to_be_filled.append((x_coor, y_coor))
				elif char_list[y] == 'S':
					new_block = create_Block(self.shrubBlocks[random.randint(0,len(self.shrubBlocks))-1],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
				elif char_list[y] == 'T':
					randType = random.randint(0,len(self.treeBlocksT))-1
					treeblockType.append(randType)
					new_block = create_Block(self.treeBlocksT[randType],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
				elif char_list[y] == 'Y':
					new_block = create_Block(self.treeBlocksB[treeblockType.popleft()],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
				elif char_list[y] == 'I':
					self.ic_coord.append((x_coor, y_coor))
					char_list[y] = '.'
				elif char_list[y] != '.': #edges image are determined by index
					print(char_list[y])
					new_block = create_Block(self.wallBlocksE[int(char_list[y])],
											 PG.Rect(x_coor, y_coor,
													 self.grid_size[0],
													 self.grid_size[1]), char_list[y])
				#set the block & add to obj group
				new_block.set_rectTop(y_coor)
				new_block.set_rectLeft(x_coor)
				self.object_group.add(new_block)

				#####(Tiles)######
				if char_list[y] == '.':
					#add pair of coordinates
					tile_index = random.randint(0,2)
					self.grass_type.append(tile_index)
					self.grasstiles.append((x_coor, y_coor))

				x_coor += self.grid_size[0]

			y_coor += self.grid_size[1]

	def get_enemy_coordx(self, index, enemy_type = 1):
		if enemy_type == 1:
			return self.ic_coord[index][0]

	def get_enemy_coordy(self, index, enemy_type = 1):
		if enemy_type == 1:
			return self.ic_coord[index][1]

	def get_num_enemies(self, enemy_type = 1):
		if enemy_type == 1:
			return len(self.ic_coord)

	def update_background(self):
		background = self.surface
		background = background.convert()
		# for block in self.object_group:
		# 	block.draw_block(background)
		#draw grasstiles to the background
		if len(self.grasstiles) == len(self.grass_type):
			for (grasstile, gtype) in zip(self.grasstiles, self.grass_type):
				background.blit(self.grass_array[gtype], grasstile)
		else:
			print "ERROR: grasstile != grass_type. Map.py line 183"
		for block in self.object_group:
			block.draw_block(background)
		for spot in self.spots_to_be_filled:
			background.blit(self.grass_array[0], spot)

		return background
			


	#called in the setup/game class
	def draw_map(self):
		# if len(self.grasstiles) == len(self.grass_type):
		# 	for (grasstile, gtype) in zip(self.grasstiles, self.grass_type):
		# 		self.surface.blit(self.grass_array[gtype], grasstile)
		# else:
		# 	print "ERROR: grasstile != grass_type. Map.py line 183"


		for block in self.object_group:
			block.draw_block(self.surface)
			
	def create_background(self):
		background = self.surface
		background = background.convert()
		# for block in self.object_group:
		# 	block.draw_block(background)
		#draw grasstiles to the background
		if len(self.grasstiles) == len(self.grass_type):
			for (grasstile, gtype) in zip(self.grasstiles, self.grass_type):
				background.blit(self.grass_array[gtype], grasstile)
		else:
			print "ERROR: grasstile != grass_type. Map.py line 183"
		for block in self.object_group:
			block.draw_block(background)
		return background

#creates a new block sprite
def create_Block(img, rect, t):
	new_block = Block(img, rect, t)
	return new_block


# class Tiles(PS.DirtySprite):
# 	def __init__(self):
# 		PS.DirtySprite.__init__(self, group):
		
