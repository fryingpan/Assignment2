import pygame
import random
import sys
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)




#Map Array
mapList = []





#
#Block class's
#
class Block(pygame.sprite.Sprite):

   
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
      
        pygame.sprite.Sprite.__init__(self)
        self.list = 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
       
        self.rect = self.image.get_rect()
        self

class Player(pygame.sprite.Sprite):

   
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
      
        pygame.sprite.Sprite.__init__(self)
        selfList = [
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
       
        self.rect = self.image.get_rect()
        self
        
class Enemy(pygame.sprite.Sprite):

   
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
      
        pygame.sprite.Sprite.__init__(self)
        selfList = [
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
       
        self.rect = self.image.get_rect()
        self

class Wall(pygame.sprite.Sprite):

   
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
      
        pygame.sprite.Sprite.__init__(self)
        selfList = [
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
       
        self.rect = self.image.get_rect()
        self




#Array for handling previous positions of moveable entities
entityPrePosList=[]

#Collision Handling Method
        def handle_collisions(sprite_dict)
        #given sprite dict, removes group1 from group2's rect
            for p in sprite_dict:
                for o in sprite_dict[p]:
                    

















        
    
# Initialize Pygame
pygame.init()
# Set the height and width of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])


enemy_sprites_list = pygame.sprite.Group()
wall_sprites_list = pygame.sprite.Group()
player_sprites_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


for i in range(10):
    # This represents a enemy block
    block = Block(BLACK, 20, 15)
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
    # Add the block to the list of objects
    enemy_sprites_list.add(block)
    all_sprites_list.add(block)

for i in range(5):
    # This represents a wall
    block = Block(BLUE, 20, 15)
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
    # Add the block to the list of objects
    wall_sprites_list.add(block)
    all_sprites_list.add(block)
    
# Create a RED player block
player = Block(RED, 20, 15)
all_sprites_list.add(player)
player_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Clear the screen
    screen.fill(WHITE)
    
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    #pos = pygame.mouse.get_pos()
    
    # Collision lists, fix these variables to be in order with call
    player_enemy_collide = pygame.sprite.spritecollide(player,enemy_sprites_list, True)
    player_wall_collide = pygame.sprite.spritecollide(player, wall_sprites_list, False)
    enemy_wall_collide = pygame.sprite.groupcollide(enemy_sprites_list, wall_sprites_list,False,False)


    #Preposition Var
    oldX=player.rect.x
    oldY=player.rect.y


    if player_wall_collide != 1:
    
        #Movement
        keys=pygame.key.get_pressed()
        
        if keys[pygame.K_DOWN]!=0:
            player.rect.y += 10
        elif keys[pygame.K_RIGHT]!=0:
            player.rect.x += 10
        elif keys[pygame.K_LEFT]!=0:
            player.rect.x -= 10
        elif keys[pygame.K_UP]!=0:
            player.rect.y -= 10
            
    # Check the list of collisions.
    for block in player_enemy_collide:
        score += 1
        print(score)
        #destroy block, find method for this
        
    # Collision Correction for enemies
        # for block in wall_enemy_list:
        #Collision correction for enemies, array of old values? Dirty Rects?
    
    # Draw all the spites
    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()
