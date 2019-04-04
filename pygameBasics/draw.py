import pygame, sys
from pygame.locals import *

pygame.init()

#set up the window
HiRez = pygame.display.set_mode((500,400),0,32)
pygame.display.set_caption('Drawing')

#set up colors
BLACK = ( 0, 0, 0)
WHITE =(255, 255, 255)
RED =(255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#draw on the HiRez

HiRez.fill(WHITE)

pygame.draw.polygon(HiRez,GREEN,((146, 0),(291,106),(236,277),(56,277)\
                                 ,(0,106)))
pygame.draw.line(HiRez,BLUE,(60,60),(120,60),4)
pygame.draw.line(HiRez,BLUE,(120,60),(60,120))
pygame.draw.line(HiRez,BLUE,(60,120),(120,120),4)

pygame.draw.circle(HiRez,BLUE,(300,50),20,0)
pygame.draw.ellipse(HiRez,RED,(300,250,40,80),1)

pygame.draw.rect(HiRez,RED,(200,150,100,50))

pix = pygame.PixelArray(HiRez)
pix[480][380] = BLACK
pix[482][382] = BLACK
pix[484][384] = BLACK
pix[486][384] = BLACK
pix[488][388] = BLACK
del pix
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
