# Drawing Functions
import sys as SYS
import random
import math
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
import pad as Pad
import Globals


# Block sprite class
class Block(PG.sprite.DirtySprite):
    def __init__(self, img, rect, t, ID=None):
        PG.sprite.DirtySprite.__init__(self)
        self.image = img
        self.rect = rect
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        Globals.SCREEN = PDI.get_surface()
        self.type = t
        self.id = ID

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def draw_block(self, map_surface):
        map_surface.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

    def set_rectLeft(self, rectLeft):
        self.x = rectLeft

    def set_rectTop(self, rectTop):
        self.y = rectTop

    def update(self, delta, bg, player):
        if self.type == 'K' or self.type == 'D':
            self.dirty = 1


class Map(object):
    GRASS_ARRAY = []
    PAD_ARRAY = []

    def __init__(self, mapfile, lvl):
            # load the grass images into an array
            TILES_LOADED = False

            if not TILES_LOADED:
                    Map.GRASS_ARRAY = self.load_grass_tiles(lvl)
                    TILES_LOADED = True

            # (prepare to read mapfile)#######
            self.map = self.get_map(mapfile)
            # size of an individual block in the grid
            self.grid_size = [50, 50]
            self.grid_dimensions = self.get_dimensions(self.map)
            self.pix_dimensions = [self.grid_dimensions[0] * self.grid_size[0],
                                   self.grid_dimensions[1] * self.grid_size[1]]
            self.surface = PG.Surface(self.pix_dimensions)
            self.object_group = PG.sprite.Group()

            self.grass_array = Map.GRASS_ARRAY
            self.pad_array = Map.PAD_ARRAY
            # list that stores a pair of coordinates for each grass
            # tile that needs to be drawn
            self.grasstiles = []
            self.grass_type = []
            self.padtiles = []
            self.pad_type = []  # hot or cold (and/or others)
            self.allPads = PS.Group()
            # block arrays
            self.wallBlocksV = []  # vertical V
            self.wallBlocksH = []  # horizontal H
            self.wallBlocksE = []
            # edges/corners; correspond to index num (see load_blocks)
            self.doorBlocks = []  # D
            self.shrubBlocks = []  # S
            # tree top = T, tree bottom = Y
            # so it's like ty thank you isn't that cute
            self.treeBlocksT = []  # T
            self.treeBlocksB = []  # Y
            self.keyBlocks = []  # K
            self.ICBlock = []  # I (icecream spots)
            self.disappearing_blocks = PS.Group()

            # enemy stuff
            self.ic_coord = []  # icecream
            self.br_coord = []  # burger
            self.lr_coord = []  # lettuce
            self.cc_coord = []  # cupcake
            self.eg_coord = []  # egg

            self.spots_to_be_filled = []
            # create map from mapfile
            self.load_blocks(lvl)
            self.objectify_map()
            self.fill()

    def get_disappearing_blocks(self):
        return self.disappearing_blocks

    def load_grass_tiles(self, lvl):
            tile_array = []
            lvl = math.floor(lvl)
            if(lvl == 1):
                tile_array.append(PI.load("FPGraphics/tiles/grassTile1.png"))
                tile_array.append(PI.load("FPGraphics/tiles/grassTile2.png"))
                tile_array.append(PI.load("FPGraphics/tiles/grassTile3.png"))
            if(lvl == 2):
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv2Tiles/chiliTile.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv2Tiles/chiliTile1.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv2Tiles/chiliTile2.png"))
            if(lvl == 3):
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv3Tiles/ICTile1.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv3Tiles/ICTile2.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv3Tiles/ICTile3.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv3Tiles/ICTile4.png"))
            if(lvl == 4):
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv4Tiles/candyTile1.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv4Tiles/candyTile2.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv4Tiles/candyTile3.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv4Tiles/candyTile4.png"))
                tile_array.append(
                    PI.load("FPGraphics/tiles/lv4Tiles/candyTile5.png"))
            return tile_array

    def load_blocks(self, lvl):
        # note: always load edge blocks with these indeces:
        # 0 = HL; 1 = HR; 2 = VD; 3 = VU; 4 = TL; 5 = TR; 6 = BL; 7 = BR
        # doors are always cheese
        self.doorBlocks.append(PI.load("FPGraphics/tiles/cheeseWall1.png"))
        self.doorBlocks.append(PI.load("FPGraphics/tiles/cheeseWall2.png"))
        self.doorBlocks.append(PI.load("FPGraphics/tiles/cheeseWall3.png"))
        self.keyBlocks.append(PI.load("FPGraphics/tiles/lactasePill.png"))
        self.signImg = (PI.load("FPGraphics/tiles/sign.png"))
        lvl = math.floor(lvl)
        if(lvl == 1):
            self.wallBlocksV.append(PI.load("FPGraphics/tiles/lv1Wall1.png"))
            self.wallBlocksV.append(PI.load("FPGraphics/tiles/lv1Wall2.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv1shrubBroc.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv1shrubCauli.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv1shrubRadish.png"))
            self.treeBlocksT.append(PI.load("FPGraphics/tiles/lv1treeT1.png"))
            self.treeBlocksT.append(PI.load("FPGraphics/tiles/lv1treeT2.png"))
            self.treeBlocksT.append(PI.load("FPGraphics/tiles/lv1treeT3.png"))
            self.treeBlocksB.append(PI.load("FPGraphics/tiles/lv1treeB1.png"))
            self.treeBlocksB.append(PI.load("FPGraphics/tiles/lv1treeB2.png"))
            self.treeBlocksB.append(PI.load("FPGraphics/tiles/lv1treeB3.png"))
        if(lvl == 2):
            self.wallBlocksV.append(
                PI.load("FPGraphics/tiles/lv2Tiles/lv2wall1.png"))
            self.wallBlocksV.append(
                PI.load("FPGraphics/tiles/lv2Tiles/lv2wall2.png"))
            self.wallBlocksV.append(
                PI.load("FPGraphics/tiles/lv2Tiles/lv2wall3.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv1shrubBroc.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv2Tiles/lv2shrub1.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv2Tiles/lv2shrub2.png"))
            self.treeBlocksT.append(
                PI.load("FPGraphics/tiles/lv2Tiles/lv2TreeT1.png"))
            self.treeBlocksT.append(
                PI.load("FPGraphics/tiles/lv1treeT1.png"))
            self.treeBlocksB.append(
                PI.load("FPGraphics/tiles/lv2Tiles/lv2TreesB1.png"))
            self.treeBlocksB.append(
                PI.load("FPGraphics/tiles/lv1treeB1.png"))
        if(lvl == 3):
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3wall1.png"))
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3wall2.png"))
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3wall3.png"))
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3wall4.png"))
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3wall5.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv3Tiles/lv3shrub1.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv3Tiles/lv3shrub2.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv3Tiles/lv3shrub3.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv3Tiles/lv3shrub4.png"))
            self.treeBlocksT.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3TreeT1.png"))
            self.treeBlocksT.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3TreeT2.png"))
            self.treeBlocksB.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3TreeB1.png"))
            self.treeBlocksB.append(PI.load(
                                    "FPGraphics/tiles/lv3Tiles/lv3TreeB2.png"))
        if(lvl == 4):
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4wall1.png"))
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4wall2.png"))
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4wall3.png"))
            self.wallBlocksV.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4wall4.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv4Tiles/lv4shrub1.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv4Tiles/lv4shrub2.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv4Tiles/lv4shrub3.png"))
            self.shrubBlocks.append(
                PI.load("FPGraphics/tiles/lv4Tiles/lv4shrub4.png"))
            self.treeBlocksT.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4TreeT1.png"))
            self.treeBlocksT.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4TreeT2.png"))
            self.treeBlocksT.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4TreeT3.png"))
            self.treeBlocksB.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4TreeB1.png"))
            self.treeBlocksB.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4TreeB2.png"))
            self.treeBlocksB.append(PI.load(
                                    "FPGraphics/tiles/lv4Tiles/lv4TreeB3.png"))

    def get_surface(self):
            return self.surface

    def fill(self):
        self.surface.fill((0, 0, 0))

    # returns list of lines in the mapfile
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
        # the x and y coordinates as you traverse the map
        x_coor = 0
        y_coor = 0

        # keep track of type of tree block
        treeblockType = deque()

        # counter for sign id
        sign_id = 0

        # traverse the map, creating block sprites
        for x in range(self.grid_dimensions[1]):
            # get the list of characters in the mapfile
            char_list = list(self.map[x])
            x_coor = 0
            for y in range(self.grid_dimensions[0]):
                # wall blocks
                if char_list[y] == 'V':
                    new_block = create_Block(self.wallBlocksV
                                             [random.randint(0, len(self.
                                                             wallBlocksV))-1],
                                             PG.Rect(x_coor, y_coor,
                                                     self.grid_size[0],
                                                     self.grid_size[1]),
                                             char_list[y])
                elif char_list[y] == 'H':
                    new_block = create_Block(self.wallBlocksH
                                             [random.randint(0, len(self.
                                                             wallBlocksH))-1],
                                             PG.Rect(x_coor, y_coor,
                                                     self.grid_size[0],
                                                     self.grid_size[1]),
                                             char_list[y])
                # key block
                elif char_list[y] == 'K':
                    # change to just an obj later or whatever
                    new_block = create_Block(self.keyBlocks[0],
                                             PG.Rect(x_coor, y_coor,
                                                     self.grid_size[0],
                                                     self.grid_size[1]),
                                             char_list[y])
                    self.disappearing_blocks.add(new_block)
                    self.spots_to_be_filled.append((x_coor, y_coor))
                elif char_list[y] == 'S':
                    new_block = create_Block(self.shrubBlocks
                                             [random.randint(0, len(self.
                                                             shrubBlocks))-1],
                                             PG.Rect(x_coor, y_coor,
                                                     self.grid_size[0],
                                                     self.grid_size[1]),
                                             char_list[y])
                elif char_list[y] == 'T':
                    randType = random.randint(0, len(self.treeBlocksT))-1
                    treeblockType.append(randType)
                    new_block = create_Block(self.treeBlocksT[randType],
                                             PG.Rect(x_coor, y_coor,
                                                     self.grid_size[0],
                                                     self.grid_size[1]),
                                             char_list[y])
                elif char_list[y] == 'Y':
                    new_block = create_Block(self.treeBlocksB
                                             [treeblockType.popleft()],
                                             PG.Rect(x_coor, y_coor,
                                                     self.grid_size[0],
                                                     self.grid_size[1]),
                                             char_list[y])
                elif char_list[y] == '!':  # readable sign
                    new_block = create_Block(self.signImg,
                                             PG.Rect(x_coor, y_coor,
                                                     self.grid_size[0],
                                                     self.grid_size[1]),
                                             char_list[y], sign_id)
                    sign_id += 1
                # enemies
                elif char_list[y] == 'I':  # icecream
                    self.ic_coord.append((x_coor, y_coor))
                    char_list[y] = '.'
                elif char_list[y] == 'B':  # burger
                    self.br_coord.append((x_coor, y_coor))
                    char_list[y] = '.'
                elif char_list[y] == 'L':  # lettuce
                    self.lr_coord.append((x_coor, y_coor))
                    char_list[y] = '.'
                elif char_list[y] == 'C':  # cupcake
                    self.cc_coord.append((x_coor, y_coor))
                    char_list[y] = '.'
                elif char_list[y] == 'E':  # eg
                    self.eg_coord.append((x_coor, y_coor))
                    char_list[y] = '.'
                elif char_list[y].isdigit():
                    # number, so we put doors here
                    new_block =
                    create_Block(self.doorBlocks[random.randint(0,
                                                 slen(self.doorBlocks))-1],
                                 PG.Rect(x_coor, y_coor,
                                         self.grid_size[0],
                                         self.grid_size[1]),
                                 char_list[y])
                    self.disappearing_blocks.add(new_block)
                    self.spots_to_be_filled.append((x_coor, y_coor))
                # set the block & add to obj group
                new_block.set_rectTop(y_coor)
                new_block.set_rectLeft(x_coor)
                self.object_group.add(new_block)

                # if char_list[y] == '.':
                # add pair of coordinates
                tile_index = random.randint(0, 2)
                self.grass_type.append(tile_index)
                self.grasstiles.append((x_coor, y_coor))

                # added pad tiles##
                # HOT
                if char_list[y] == ',':
                    self.pad_type.append(0)
                    # 0 or 1, type for hot or cold pads
                    self.padtiles.append((x_coor, y_coor))
#                    newPad = Pad.create_Pad(self.pad_array[0],
#                                            self.pad_array[0].get_rect(), 0)
#                    newPad.set_rectLeft(x_coor)
#                    newPad.set_rectTop(y_coor)
#                    self.allPads.add(newPad)
                # COLD
                if char_list[y] == ';':
                    self.pad_type.append(1)
                    # 0 or 1, type for hot or cold pads
                    self.padtiles.append((x_coor, y_coor))
#                    newPad = Pad.create_Pad(self.pad_array[0],
#                                            self.pad_array[0].get_rect(), 1)
#                    newPad.set_rectLeft(x_coor)
#                    newPad.set_rectTop(y_coor)
#                    self.allPads.add(newPad)
                x_coor += self.grid_size[0]

            y_coor += self.grid_size[1]

    def get_enemy_coordx(self, index, enemy_type=1):
        if enemy_type == 1:
            return self.ic_coord[index][0]
        if enemy_type == 2:
            return self.br_coord[index][0]
        if enemy_type == 3:
            return self.lr_coord[index][0]
        if enemy_type == 4:
            return self.cc_coord[index][0]
        if enemy_type == 5:
            return self.eg_coord[index][0]

    def get_enemy_coordy(self, index, enemy_type=1):
        if enemy_type == 1:
            return self.ic_coord[index][1]
        if enemy_type == 2:
            return self.br_coord[index][1]
        if enemy_type == 3:
            return self.lr_coord[index][1]
        if enemy_type == 4:
            return self.cc_coord[index][1]
        if enemy_type == 5:
            return self.eg_coord[index][1]

    def get_num_enemies(self, enemy_type=1):
        if enemy_type == 1:
            return len(self.ic_coord)
        if enemy_type == 2:
            return len(self.br_coord)
        if enemy_type == 3:
            return len(self.lr_coord)
        if enemy_type == 4:
            return len(self.cc_coord)
        if enemy_type == 5:
            return len(self.eg_coord)

    def get_pad_x(self, index):
        return self.padtiles[index][0]

    def get_pad_y(self, index):
        return self.padtiles[index][1]

    def update_background(self):
        background = self.surface
        background = background.convert()
        # for block in self.object_group:
        #   block.draw_block(background)
        # draw grasstiles to the background
        if len(self.grasstiles) == len(self.grass_type):
            for (grasstile, gtype) in zip(self.grasstiles, self.grass_type):
                background.blit(self.grass_array[gtype], grasstile)
        else:
            print "ERROR: grasstile != grass_type. Map.py line 183"

        for block in self.object_group:
            block.draw_block(background)
        # for spot in self.spots_to_be_filled:
        #     background.blit(self.grass_array[0], spot)

        return background

    # called in the setup/game class
    def draw_map(self):

        for block in self.object_group:
            block.draw_block(self.surface)

    def create_background(self):
        background = self.surface
        background = background.convert()
        # for block in self.object_group:
        #   block.draw_block(background)
        # draw grasstiles to the background
        if len(self.grasstiles) == len(self.grass_type):
            for (grasstile, gtype) in zip(self.grasstiles, self.grass_type):
                background.blit(self.grass_array[gtype], grasstile)
        else:
            print "ERROR: grasstile != grass_type. Map.py line 183"

        for block in self.object_group:
            block.draw_block(background)
        return background


# creates a new block sprite
def create_Block(img, rect, t, ID=None):
    new_block = Block(img, rect, t, ID)
    return new_block
