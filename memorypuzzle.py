#Memory game
import random, pygame,sys
from pygame.locals import *

FPS = 30

WINDOWWIDTH = 640#windows width
WINDOWHEIGHT = 480#windows height

REVEALSPEED = 8 #Speed boxes' sliding reveals and covers
BOXSIZE = 40 #size of box height & width in pixels
GAPSIZE = 10 #size of gap between boxes in pixels
BOARDWIDTH = 10 #number of columns of icons
BOARDHEIGHT = 7 #number of rows of icons

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Baoard needs to have an even  \
number of boxes for pairs of matches.'
# the length of one of the blank spaces over on the left or right
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
# the length of one of the blank spaces over at the top or bottom
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE)))/2)

#               R    G    B
GRAY        = (100, 100, 100)
NAVYBLUE    = ( 60,  60, 100)
WHITE       = (255, 255, 255)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
BLUE        = (  0,   0, 255)
YELLOW      = (255, 255,   0)
ORANGE      = (255, 128,   0)
PURPLE      = (255,   0, 255)
CYAN        = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

#we dont hardcode strings in this house
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'


#tuple with all the colors
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)



def main():
    global FPSCLOCK, HiRez
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    HiRez = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 #used to store x coordinate of mouse event
    mousey = 0 #ditto for y
    pygame.display.set_caption('MEMBER?')

    mainBoard = getRandomizedBoard()
    #we create a list that represents the the revealed state of every cell of our board.we set every cell to false cause every cell starts out unrevealed
    revealedBoxes = generateRevealedBoxesData(False)
    #revealedBoxes2 = generateRevealedBoxesData(True) <used for testing>

    firstSelection = None # stores the (x,y) of the first box clicked

    HiRez.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: #main game loop
        mouseClicked = False

        HiRez.fill(BGCOLOR)#drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #always have the position our mouse is in saved as mousex and mouse y
            elif event.type == MOUSEMOTION:
                mousex,mousey = event.pos
            #if someone holds m1 and then moves the mouse we register the position they let go as were they clicked
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos
                mouseClicked = True
            elif event.type == KEYUP  and event.key == K_f:
                 startGameAnimation(mainBoard)

        boxx,boxy = getBoxAtPixel(mousex, mousey)#boxx is the box our mouse is on
        if boxx != None and boxy != None:
            #mouse is over a box
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:#box hasnt been revealed and we click on it
                revealBoxesAnimation(mainBoard, [(boxx,boxy)])
                revealedBoxes[boxx][boxy] = True #set the box as "revealed"
                if firstSelection == None:#current box is first boxed clicked out of 2
                    firstSelection = (boxx,boxy)
                else: #the current box was the second box clicked so now we
                    #check if there is a match between the two icons:
                    icon1shape,icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape,icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                         #Icons didint match so cover both
                         pygame.time.wait(1000)#wait 1 second(1000milisecond)
                         coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx,boxy)])
                         revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                         revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):#check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)#2 seconda

                        #Reset le Board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        #Show the fully unrevealed board for a second
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        #Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None #reset firstSelection variable

        #Redraw the screen and wait a clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)



#this function creates a list that contains 10, 7 value lists each inner list represents the revealed states of a single column of the board.
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


#The icon data structure is a list of tuples in each tuple there are two
#values one for the icons shape and one for the icons color
#we need to be sure we have exactly as many icons as the boxes on the board
#and we need to make sure there are exactly 2 of each
def getRandomizedBoard():
    #start by getting a list of every possible shape in every possible color
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            #icons list containing every possible shape color combination
            icons.append( (shape,color) )

    random.shuffle(icons)#randomize the order of the icons list
    # the total number of boxes divided by 2 (cause we'll have two of each)
    #the number of combinations we'll need
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT /2 )
    #start from the first item in the list all the way to the number
    #in the numsIconsUsed and duplicate everysingle tuple
    #icons now represents exactly what we want to see on our board,
    #the needed number of shape color combination and their duplicate
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons) #shuffle again

    #the board data structure is a list of lists,each inner list represents
    # a column on the board
    #board[x][y] is the syntax we use were x is column and y row and the result
    #is the box where these two meet
    #board[x][y][0] represents shape and board[x][y][1] represents color
    board = []
    #iterate over every column
    for x in range(BOARDWIDTH):
        #make a new list for every column
        column = []
        #and for every box in each column add an icon tuple from the icons
        #list to the column list
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            #delete the icon we added in order to iterate through every icon
            del icons[0]
        #add the column to the board
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    #splits a list into a list of lists, where the inner lists have at most
    #groupSize number of items
    result = []
    for i in range(0,len(theList),groupSize):
        result.append(theList[i:i+groupSize])
    return result


#this converts board coordinates (3,2), (0,0) to pixel coordinates (100,65), (639,479)
def leftTopCoordsOfBox(boxx,boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN#(70)
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN#(65)
    return (left, top)


#the pixel coordinate is the coordinate that our mouse click and mouse
# movement events use and the board coordinate is how we know which box
# the mouse event happened on.
#pixel coordinates represent the top left of the box while board coordinates
# are like excel spreadsheet cell representations

#this function uses collide point to check if the mouse coordinates provided
#collide with the pixel coordinates of any box. it then returns the
# corresponding board coordinates of said pixel coordinate
def getBoxAtPixel(x, y):
    # iterate every single cell in the board
    for  boxx in range (BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx,boxy)
            #draw a rectangle at the pixel coordinates
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            #then use collide point to see if the board coordinates are on the
            # pixel coordinates.
            # collide point returns true if x, y is in the rectangle
            if boxRect.collidepoint(x, y):
                return (boxx,boxy)
    return (None,None)


def drawIcon(shape,color,boxx,boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half = int(BOXSIZE * 0.5) #moar syntactic sugar

    #gets pixel coordinates of the box
    left, top = leftTopCoordsOfBox(boxx,boxy)

    #draws the shape at pixel coordinates
    if shape  == DONUT:
        pygame.draw.circle(HiRez, color,(left  + half, top + half),half - 5)
        pygame.draw.circle(HiRez,BGCOLOR, (left + half, top + half), quarter - 5)

    elif shape == SQUARE:
        pygame.draw.rect(HiRez, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))

    elif shape == DIAMOND:
        pygame.draw.polygon(HiRez,color, (( left + half, top),
            (left + BOXSIZE - 1, top + half), (left+half, top + BOXSIZE - 1 ), (left, top + half)))

    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(HiRez, color, (left, top + i), (left + i , top))
            pygame.draw.line(HiRez,color,(left + i, top + BOXSIZE - 1),(left + BOXSIZE - 1, top + i))

    elif shape == OVAL:
        pygame.draw.ellipse(HiRez, color, (left, top + quarter,BOXSIZE ,half))


#returns the shape and color in board coodinates boxx,boxy
def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # x is column y is icons 0 is the shape value of icon
    #color value for x,y is stored in board[x][y][1]
    return board[boxx][boxy][0],board[boxx][boxy][1]
    #   shape in x, y           color of shape in x y

def drawBoxCovers(board,boxes, coverage):
    #draw boxes being covered / revealed.
    #<boxes> is a list of two-item lists, which have the x & y spot of the box
    for box in boxes:
        #the top left of the box we want to draw on in pixel coordinates
        left, top = leftTopCoordsOfBox(box[0], box[1])
        #the rectangle we will draw over the box
        pygame.draw.rect(HiRez,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
        #we also draw a shape but if there is coverage. i.e the box is
        #being covered then we draw a white box over this shape
        shape,color = getShapeAndColor(board, box[0],box[1])
        drawIcon(shape, color, box[0],box[1])
        if coverage > 0: #only draw the cover if there is an coverage
            pygame.draw.rect(HiRez, BOXCOLOR, (left, top, coverage, BOXSIZE))

    #this function is gonna be called from a seperate loop than the game loop
    #so we need to call pygame.update and fpsclock.tick
    pygame.display.update()
    FPSCLOCK.tick(FPS)


#uses the draw box covers loop to repeatedly draw boxes that are decreasing
#in width in order to get the illusion of an opening box
def revealBoxesAnimation(board, boxesToReveal):
    #Do the " box reveal " animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) -1, - REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


#uses draw box covers to repeatedly draw boxes that are increasing in width
#in order to to make the illusion of a closing box
def coverBoxesAnimation(board, boxesToCover):
    #Do the 'box cover' animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover , coverage)


def drawBoard(board, revealed):#revealed is the list of lists that generate...
    #revealedBoxesData() returns
    #Draws all of the boxes in their covered or revealed state.
    for boxx in range (BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                #Draw a covered box.
                pygame.draw.rect(HiRez, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                #Draw the (revealed) icon
                shape, color = getShapeAndColor(board,boxx,boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx,boxy):
    #get the  pixel coordinates of the box our mouse is hovering over
    left,top = leftTopCoordsOfBox(boxx,boxy)
    #draw a rectangle around the box at the given pixel coordinate
    pygame.draw.rect(HiRez, HIGHLIGHTCOLOR, (left - 5,top - 5, BOXSIZE + 10,BOXSIZE + 10),4)


#this function draws the board as all coverred then reveals the board 8 cells at a time
def startGameAnimation(board):
    #Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range (BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8,boxes)
    a=1
    print(a)
    drawBoard(board,coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board,boxGroup)
        pygame.time.wait(1000)
        coverBoxesAnimation(board,boxGroup)


def gameWonAnimation(board):
    #flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1,color2 = color2, color1 #swap colors
        HiRez.fill(color1)
        drawBoard(board,coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    #Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any Boxes are covered
    return True




if __name__ == '__main__':
    main()
