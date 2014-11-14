import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
from Player import Player
from Enemy import Enemy

class Projectile(PS.DirtySprite):
    side = 7 # small side of Projectile rectangle
    vel = 180 # velocity
    mass = 50
    maxlifetime = 10.0 # seconds
    IMAGE_LENGTH = 4  # all Projectile sprite has 12 frames

    def __init__(self, boss, surface, rect, thetype, user, num_frames, pass_through = 0, lifetime=8000, image=None, speed = 1):
        PS.DirtySprite.__init__(self)
        #draw variables
        self.rect = rect
        if image is not None:
            self.image = image
        self.num_frames = num_frames #num frames of animation
        self.surface = surface
        #update variables
        #0 = passes nothing; 1 = passes enemies; 2 = passes walls AWESOME
        self.pass_through = pass_through 
        self.lifetime = lifetime #time proj lives
        self.boss = boss #boss is the sprite the projectile is fired from
        self.speed = speed
        self.frame = 0
        self.lifetime = lifetime
        self.calculate_origin()
        self.update() # to avoid ghost sprite in upper left corner, 
                      # force position calculation.

    def load_images_helper(self, imageArray, sheet):
            # key = sheet.get_at((0,0))
            # hereeeeee
            alphabg = (23, 23, 23)
            for i in range(0, 4):
                surface = PG.Surface((100, 100))
                surface.set_colorkey(alphabg)
                surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
                imageArray.append(surface)
            return imageArray

    # this will all end up in the key handler
    def update_image(self, imageArray):
        try:
            self.image = imageArray[self.frame].convert_alpha()
        except IndexError:
            self.image = self.errorImg
            self.face = list(self.face)[0]

    def calculate_origin(self):
        #add option for offsets for multiple projectiles
        self.rect.x = self.boss.rect.centerx
        self.rect.y = self.boss.rect.centery

    def handle_player(self, player):
        collisions = PS.spritecollide(self, player, False)
        if(len(collisions) == 1 and isinstance(collisions[0], Player)):
            if(self.invincibility_count == 0):
                self.attacked_player = True
                self.invincibility_count = 200

    def handle_collision(self, bg):
        collisions = PS.spritecollide(self, bg, False)
        #if collide, disappear

    def handle_enemies(self, enemies):
        collisions = PS.spritecollide(self, bg, False)

    def update(self):
        # ---- kill if too old ---
        self.lifetime += Globals.DELTA
        if self.lifetime > Projectile.maxlifetime:
            self.kill()
        # ----- !!!!TODO kill if out of screen
        if self.pos[0] < 0:
            self.kill()
        # elif self.pos[0] > Config.width:
        #     self.kill()
        if self.pos[1] < 0:
            self.kill()
        # elif self.pos[1] > Config.height:
        #     self.kill()
        #------- move -------
        self.move(bg, player, Globals.DELTA)
        if(isinstance(self.boss, Player)):
            self.handle_enemies()
        if(isinstance(self.boss, Enemy)):
            self.handle_player()
        #####MAKE PLAYER INVINCIBILITY GLOBAL!!!!!
        # if(self.invincibility_count > 0):
        #     self.invincibility_count -= 1

        # update time
        self.time = self.time + Globals.DELTA
        if self.time > Projectile.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Projectile.CYCLE / Projectile.IMAGE_LENGTH))
        if frame != self.frame:
                self.frame = frame
                self.update_image(self.image)
        self.dirty = 1

class LettuceCutter(Projectile):
    CYCLE = .6

    def __init__(self, xlocation, ylocation, fps=1):
        ######unique attributes parent class doesn't have
        self.image = PI.load("FPGraphics/burger/burgerFront.png") \
            .convert_alpha()
        self.front_image = self.image
        self.bound_factor = 2
        #######
        #attributes to be passed to parent for parent function use
        self.health = 3
        self.speed = 1
        self.rect = self.image.get_rect()
        self.rect.x = xlocation
        self.rect.y = ylocation
        self.xboundl = xlocation - self.rect.width*self.bound_factor
        self.yboundt = ylocation - self.rect.width*self.bound_factor
        self.xboundr = xlocation + self.rect.width*self.bound_factor
        self.yboundb = ylocation + self.rect.width*self.bound_factor

        self.IMAGES_RIGHT = []
        self.IMAGES_LEFT = []
        self.IMAGES_FRONT = []
        self.IMAGES_BACK = []
        self.load_images()
        Enemy.__init__(self, self.rect, self.IMAGES_RIGHT,
                       self.IMAGES_LEFT, self.IMAGES_FRONT,
                       self.IMAGES_BACK, self.health, self.speed)
        self.drop_num = 3

    def attack(self, surface):
        ###
        pass

    def move(self, player, interval):

        ran = random.randint(0, 10)
        move_dist = 0
        if(ran < 3):  # slow him down cuz he hella scary when he's fast
            dist = int(self.speed)
            # distance moved in 1 frame, try changing it to 5
            move_dist = math.ceil(dist*interval)
            if player.sprites()[0].rect.y > self.rect.y and self.rect.y <= self.yboundb:
                self.rect.y += move_dist  # move down
                self.face = 'd'
            elif player.sprites()[0].rect.y < self.rect.y and self.rect.y >= self.yboundt:
                self.rect.y -= move_dist  # move up
                self.face = 'u'
            if player.sprites()[0].rect.x > self.rect.x and self.rect.x <= self.xboundr:
                self.rect.x += move_dist  # move right
                self.face = 'r'
            elif player.sprites()[0].rect.x < self.rect.x and self.rect.x >= self.xboundl:
                self.rect.x -= move_dist  # move left
                self.face = 'l'

    def drop_item(self, surface):
            d = random.randint(0, 9)
            if(d == 0):
                return BurgerDrop(self.rect.x, self.rect.y, surface)
            if(d > 0 and d < 4):
                return MeatDrop(self.rect.x, self.rect.y, surface)
            if(d >= 4 and d < 7):
                return LettuceDrop(self.rect.x, self.rect.y, surface)
            if(d >= 7):
                return BreadDrop(self.rect.x, self.rect.y, surface)

    def get_face(self):
        return self.face

    def get_ID(self):
        return self.enemy_ID

    def is_alive(self):
        if self.health == 0:
            #then the enemy is dead
            pass

    def load_images(self):
        sheetR = PI.load("FPGraphics/burger/burgerrightWalk.png") \
            .convert_alpha()
        sheetL = PI.load("FPGraphics/burger/burgerleftWalk.png") \
            .convert_alpha()
        sheetF = PI.load("FPGraphics/burger/burgerFrontWalk.png") \
            .convert_alpha()
        sheetB = PI.load("FPGraphics/burger/burgerbackWalk.png") \
            .convert_alpha()
        self.IMAGES_RIGHT = self.load_images_helper(self.IMAGES_RIGHT,
                                                    sheetR)
        self.IMAGES_LEFT = self.load_images_helper(self.IMAGES_LEFT,
                                                   sheetL)
        self.IMAGES_FRONT = self.load_images_helper(self.IMAGES_FRONT,
                                                    sheetF)
        self.IMAGES_BACK = self.load_images_helper(self.IMAGES_BACK,
                                                   sheetB)