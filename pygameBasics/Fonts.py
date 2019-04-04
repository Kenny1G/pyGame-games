import pygame,sys
from pygame.locals import *
import time

pygame.init()
HiRez = pygame.display.set_mode((400,300))
pygame.display.set_caption('Fonts')

WHITE = (255,255,255)
GREEN = pygame.Color(0,255,0)
BLUE = (0,0,128)
RED = (255,0,0)

fontObj = pygame.font.Font('freesansbold.ttf',32)
textSurfaceObj = fontObj.render('Hello world!',True,RED)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200,150)
# pygame.mixer.music.load('makingGameszip/Doja Cat - Mooo! (Official Video).mp3')
# pygame.mixer.music.play(-1,0.0)
soundObj = pygame.mixer.Sound('makingGamesZip/beep1.ogg')
while True:
    HiRez.fill(WHITE)
    HiRez.blit(textSurfaceObj,textRectObj)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.music.stop()
            soundObj.play()
            time.sleep(1)
            soundObj.stop()
            pygame.quit()
            sys.exit()
    pygame.display.update()
