'''import random
import time

def dragonCall():
    print('monkaS, you stand there scared shitless, two caves stare at  you \n \
They look into your soul, you must pick one... Your destiny awaits')
    print()
def choice():
    print('What cave do you choose?\n 1 or 2:',end='')
    cave = input()
    return cave

def dramaticDotEffect():
    for i in range(4):
        print('.',end='')
        time.sleep(2)

def checkCave():
    goodCave = random.randint(1, 2)
    userCave = choice()
    print('Spooky Scary, you step in')
    time.sleep(1)
    print('You hear a sound')
    dramaticDotEffect()
    print()
    print('A HUGE DRAGON COMES RUSHING AT YOU MOUTH WIDE OPEN')
    time.sleep(2)
    if userCave == str(goodCave):
        print('IN HIS MOUTH, a pot of gold?')
        dramaticDotEffect()
        print(Yup, I guess you're rich now? )
        return
    print('you froze, he eats , YOU\'RE DEAD')

again = 'yes'

while again == 'yes' or again == 'y':
    dragonCall()
    checkCave()
    print('wow what a ride, wanna go again? (Y/N)')
    again = input().lower() '''

import random
import time

def displayIntro():
    print('''You are in a land full of dragons. In front of you,
 you see two caves. In one cave, the dragon is friendly
 and will share his treasure with you. The other dragon
 is greedy and hungry, and will eat you on sight.''')
    print()

def chooseCave():
    cave = ''
    while cave != 1 and cave != 2:
        print('Which cave will you go into? (1 or 2)')
        cave = input()

    return cave

def checkCave(chosenCave):
    print('You approach the cave...')
    time.sleep(2)
    print('It is dark and spooky...')
    time.sleep(2)
    print('A large dragon jumps out in front of you! He opens his jaws and...')
    print('\n')
    time.sleep(2)

    friendlyCave = random.randint(1, 2)

    if chosenCave == str(friendlyCave):
        print('Gives you his treasure!')
    else:
        print('Gobbles you down in one bite!')

playAgain = 'yes'
while playAgain == 'yes' or playAgain == 'y':
    displayIntro()
    caveNumber = chooseCave()
    checkCave(caveNumber)

    print('Do you want to play again? (yes or no)')
    playAgain = input()
