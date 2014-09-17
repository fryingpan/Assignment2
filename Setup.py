# Assignment 2
# Frying Pan

import pygame
import sys
import Player
import Enemy
import Wall

screen = pygame.display.set_mode((800, 600))

character = Player.Player()
# bad = Enemy()
charrect = character.image.get_rect()
# badrect = bad.image.get_rect()
wall = Wall.Wall()
wall_list = pygame.sprite.Group()

pygame.init()

running = True
while running:
    # handle every event since the last frame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # quit the screen
            running = False

    character.handle_keys() # handle the keys

    screen.fill((255,255,255)) # fill the screen with white
    character.draw(screen) # draw the bird to the screen
    i = 0
    j = 0
    for x in range(10):
        wall_list.add(wall)
    pygame.display.update() # update the screen

    # clock.tick(40)

