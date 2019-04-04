import random, sys, time, pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4
BEEP1PATH = 'beep1.ogg'
BEEP2PATH = 'beep2.ogg'
BEEP3PATH = 'beep2.ogg'
BEEP4PATH = 'beep4.ogg'
#                R    G    B

WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2* BUTTONSIZE) - BUTTONGAPSIZE) / 2)

YELLOWRECT  = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT    = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN,
                          BUTTONSIZE, BUTTONSIZE)
REDRECT     = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE,
                          BUTTONSIZE, BUTTONSIZE)
GREENRECT   = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN +
                          BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main():
    global FPSCLOCK, HiRez, BASICFONT, BEEP1, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    HiRez = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Click as I click')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

    infoSurf = BASICFONT.render('Match the pattern by clicking on the button \
or using the Q, W, A, S keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    BEEP1 = pygame.mixer.Sound(BEEP1PATH)
    BEEP2 = pygame.mixer.Sound(BEEP2PATH)
    BEEP3 = pygame.mixer.Sound(BEEP3PATH)
    BEEP4 = pygame.mixer.Sound(BEEP4PATH)

    ColorPattern = []
    currentStep = 0
    lastClickTime = 0
    score = 0

    waitingForInput = False

    while True: #main game loop
        clickedButton = None

        HiRez.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        #                           x         ,  y
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        HiRez.blit(scoreSurf, scoreRect)

        HiRez.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key   == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN


        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            ColorPattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in ColorPattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            if clickedButton and clickedButton == ColorPattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(ColorPattern):
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0
            elif (clickedButton and clickedButton != ColorPattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                gameOverAnimation()
                ColorPattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()


        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def flashButtonAnimation(color, animationSpeed = 50):
    if color == YELLOW:
        sound       = BEEP1
        flashColor  = BRIGHTYELLOW
        rectangle   = YELLOWRECT
    elif color == BLUE:
        sound       = BEEP2
        flashColor  = BRIGHTBLUE
        rectangle   = BLUERECT
    elif color == RED:
        sound       = BEEP3
        flashColor  = BRIGHTRED
        rectangle   = REDRECT
    elif color == GREEN:
        sound       = BEEP4
        flashColor  = BRIGHTGREEN
        rectangle   = GREENRECT

    origSurf    = HiRez.copy()
    flashSurf   = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf   = flashSurf.convert_alpha()
    r, g, b     = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            HiRez.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            HiRez.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    HiRez.blit(origSurf,(0, 0))


def drawButtons():
    pygame.draw.rect(HiRez, YELLOW, YELLOWRECT)
    pygame.draw.rect(HiRez, BLUE,   BLUERECT)
    pygame.draw.rect(HiRez, RED,    REDRECT)
    pygame.draw.rect(HiRez, GREEN,  GREENRECT)


def changeBackgroundAnimation(animationSpeed = 40):
    global bgColor
    newBgColor = (random.randint(0,255), random.randint(0,255),
                  random.randint(0,255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b   = newBgColor
    for alpha in range(0, 255, animationSpeed):
        checkForQuit()
        HiRez.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        HiRez.blit(newBgSurf, (0, 0))

        drawButtons()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(color = WHITE, animationSpeed = 50):
    origSurf = HiRez.copy()
    flashSurf = pygame.Surface(HiRez.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3):
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step):
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                HiRez.blit(origSurf, (0, 0))
                HiRez.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    return None


if __name__ == '__main__':
    main()
