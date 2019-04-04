import pygame,sys
from pygame.locals import *

pygame.init()

HiRez = pygame.display.set_mode((400,300),0,32)
pygame.display.set_caption('Just messing around')

fpsObj = pygame.time.Clock()
FPS = 30 #fps

WHITE = (255,255,255)
cat = pygame.image.load('makingGamesZip/cat.png')
catX = 10
catY = 10
position = 'right'
# pygame.mixer.music.load('makingGamesZip/Doja Cat - Mooo! (Official Video).mp3')
# pygame.mixer.music.play(-1,0.0)
# soundObj = pygame.mixer.Sound('makingGamesZip/beep2.ogg')

while True:
    HiRez.fill(WHITE)

    if position == 'right':
        catX += 5
        if catX == 280:
            position = 'down'
    elif position == 'down':
        catY += 5
        if catY == 220:
            position = 'left'
    elif position == 'left':
        catX -= 5
        if catX == 10:
            position = 'up'
    elif position == 'up':
        catY -= 5
        if catY == 10:
            position = 'right'

    HiRez.blit(cat,(catX, catY))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.music.stop()
            # soundObj.play()
            # import time
            # time.sleep(1)
            # soundObj.stop()
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsObj.tick(FPS)
