import pygame, sys
from pygame.locals import *

pygame.init()
#the window that we see. 400 wide 400 tall
DISPLAYSURF = pygame.display.set_mode((400,300))
#the thing that appears at the top left bar of the window
pygame.display.set_caption('Hello World')
while True: #main game loop
    #event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
