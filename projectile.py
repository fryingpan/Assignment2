import random
import pygame as PG
import pygame.display as PD
import pygame.sprite as PS
import sys
import math
import pygame.image as PI
from Player import Player
from Enemy import Enemy
import Globals

class Projectile(PS.DirtySprite):
    side = 7 # small side of Projectile rectangle
    vel = 180 # velocity
    mass = 50
    maxlifetime = 5.0 # seconds
    deltaScaleFactor = 8000
    IMAGE_LENGTH = 4  # all Projectile sprite has 12 frames
    CYCLE = .6

    def __init__(self, boss, rect, num_frames, pass_through = 0, lifetime=8000, image=None, speed = 1, dmg = 1):
        PS.DirtySprite.__init__(self)
        #draw variables
        self.rect = rect
        if image is not None:
            self.image = image
        self.num_frames = num_frames #num frames of animation
        #update variables
        #0 = passes nothing; 1 = passes enemies; 2 = passes walls AWESOME
        self.pass_through = pass_through 
        self.lifetime = lifetime #time proj lives
        self.boss = boss #boss is the sprite the projectile is fired from
        self.speed = speed
        self.dmg = dmg
        self.attacked_player = False
        self.frame = 0
        self.lifetime = 0
        self.time = 0.0 #animations
        self.calculate_origin()

        self.projectile_attack_player = False
        self.projectile_attack_enemy = False
        self.enemies_attacked = []

        #load images from sprite sheet
    def load_images_helper(self, imageArray, sheet):
        # key = sheet.get_at((0,0))
        # hereeeeee
        alphabg = (23, 23, 23)
        for i in range(0, 4):
            surface = PG.Surface((50,50))
            surface.set_colorkey(alphabg)
            surface.blit(sheet, (0, 0), (i*100, 0, 100, 100))
            imageArray.append(surface)
        return imageArray

    # change img depending on self.frame
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
            if(Globals.PLAYER_INVINCIBILITY == 0):
                print("hit player")
                self.attacked_player = True
                # self.invincibility_count = 200

    def handle_collision(self, bg):
        collisions = PS.spritecollide(self, bg, False)
        #if collide, disappear
        if(pass_through == 0):
            if(len(collisions) > 0):
                self.kill()

    def handle_enemies(self, enemies):
        collisions = self.handle_collisions(self.enemy_list)
        if len(collisions) > 0:
            self.projectile_attack_enemy = True
        for collision in collisions:
            self.enemies_attacked.append(collision)
        # collisions = PS.spritecollide(self, enemies, False)
        # for col in collisions:
        #     col.decrement_health(self.dmg)
        #     if(self.pass_through == 0):
        #         self.kill()

    def get_enemies_attacked(self):
        if len(self.enemies_attacked) > 0:
            return self.enemies_attacked

    def update(self, bg, player):
        # ---- kill if too old ---
        self.lifetime += (Globals.DELTA)
        if self.lifetime > Projectile.maxlifetime:
            print("KILL")
            self.kill()
        # ----- !!!!TODO kill if out of screen
        if self.rect.x < 0:
            self.kill()
        # elif self.pos[0] > Config.width:
        #     self.kill()
        if self.rect.y < 0:
            self.kill()
        # elif self.pos[1] > Config.height:
        #     self.kill()

        #------- move -------
        self.move(Globals.DELTA, self.boss.pdx, self.boss.pdy)
        if(isinstance(self.boss, Player)):
            self.handle_enemies()
        if(isinstance(self.boss, Enemy)):
            self.handle_player(player)

        # images
        self.time = self.time + Globals.DELTA
        if self.time > Projectile.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Projectile.CYCLE / Projectile.IMAGE_LENGTH))
        if frame != self.frame:
                self.frame = frame
                self.update_image(self.IMAGES)
        self.dirty = 1

class LettuceCutter(Projectile):
    CYCLE = .6

    def __init__(self, boss, fps=1):
        ######unique attributes parent class doesn't have
        self.image = PI.load("FPGraphics/lettuce/lCStart.png").convert_alpha()
        #######
        #attributes to be passed to parent for parent function use
        self.speed = 1
        self.rect = self.image.get_rect()

        self.IMAGES = []
        self.load_images()
        Projectile.__init__(self, boss, self.rect, 4, 0, 8000, self.image, 1, 1)
#(self, boss, rect, num_frames, pass_through = 0, lifetime=8000, image=None, speed = 1, dmg = 1):
    def move(self, interval, pdx, pdy): #pd = projection direction
        ran = random.randint(0, 10)
        move_dist = 0
        if(ran < 3):  # slow him down cuz he hella scary when he's fast
            # distance moved in 1 frame, try changing it to 5
            move_dist = math.ceil(self.speed*interval)
            self.rect.centerx += pdx
            self.rect.centery += pdy

    def get_face(self):
        return self.face

    def load_images(self):
        sheet = PI.load("FPGraphics/lettuce/lC.png").convert_alpha()
        self.IMAGES = self.load_images_helper(self.IMAGES,sheet)