import pygame
import random
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)


class Block(pygame.sprite.Sprite):
    """
    This class represents physicalobjects
    It derives from the "Sprite" class in Pygame.
    """
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
    
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


for i in range(50):
    # This represents a enemy block
    block = Block(BLACK, 20, 15)
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
    # Add the block to the list of objects
    enemy_sprites_list.add(block)
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
    pos = pygame.mouse.get_pos()
    # Collision lists, fix these variables to be in order with call
    player_enemy_collide = pygame.sprite.spritecollide(player,
    enemy_sprites_list, True)
    player_wall_collide =
    pygame.sprite.spritecollide(player, wall_sprites_list, True)
    enemy_wall_collide =
    pygame.sprite.spritecollide(enemy_sprites_list, wall_sprites_list, True)


    #Preposition Var
    oldX=player.rect.x
    oldY=player.rect.y


    #Movement
    if pygame.key.get_pressed(w):
        player.rect.y += 10
    or if pygame.key.get_pressed(a):
        player.rect.x -= 10
    or if pygame.key.get_pressed(s):
        player.rect.y -= 10
    or if pygame.key.get_pressed(d):
        player.rect.x += 10
        
    # Check the list of collisions.
    for block in enemy_player_list:
        score += 1
        print(score)
        #destroy block, find method for this
        
    # Collision Correction for enemies
    for block in wall_enemy_list:
        #Collision correction for enemies, array of old values? Dirty Rects?
    # Collision correction for player
    if player in wall_player_list:
        player.rect.x=oldX
        player.rect.y=oldY
    # Draw all the spites
    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()
