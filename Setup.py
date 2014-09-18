# Assignment 2
# Frying Pan

import pygame
import sys
import Player
import Enemy

screen = pygame.display.set_mode((800, 600))

character = Player.Player()
# bad = Enemy()
charrect = character.image.get_rect()
# badrect = bad.image.get_rect()

pygame.init()

running = True
while running:
    # handle every event since the last frame.

    character.handle_keys() # handle the keys

    screen.fill((255,255,255)) # fill the screen with white
    character.draw(screen) # draw the bird to the screen
    i = 0
    j = 0
    pygame.display.update() # update the screen
    
    # handle every event since the last frame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit() # quit the screen
    # clock.tick(40)


