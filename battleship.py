#battleship
import time

def greet():
    print("WOULD YOU LIKE TO PLAY A GAME?")
    time.sleep(3)
    print()
    name = input("ENTER NAME: ")
    name = name.upper()
    time.sleep(1)
    print("HELLO "+name+".")

def orientationSeparator(orientation):
    if orientation == 1:
        modx = 1
        mody = 0
    elif orientation == 2:
        modx = 0
        mody = -1
    elif orientation == 3:
        modx = -1
        mody = 0
    else:
        modx = 0
        mody = 1
    return modx, mody

class Board:
    def __init__(self,height,width):
        self.height = height
        self.width = width
        self.layout = self.generateEmptyBoard()

    def showBoard(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.layout[y][x],' ',end = '')
            print()

    def generateEmptyBoard(self):
        board = []
        for counter in range(self.height):
            board.append([0]*self.width)
        return board

    def placeShip(self,ship,orientation,x,y):
        #ship is an integer from 1-5
        #orientation is an integer from 1-4
        #x is the x position of the head of the ship
        #y is the y position of the head of the ship
        #self.layout is expected to be a 10x10 2D array
        modx,mody = orientationSeparator(orientation)
        #print(x,y)
        for counter in range(0,ship):
            self.layout[y][x] = ship
            x += modx
            y += mody
            #print(x,y)
            #showBoard(board)

def setup():
    enemyBoard = Board(10,10)
    enemyGuesses = Board(10,10)
    playerBoard = Board(10,10)
    playerGuesses = Board(10,10)
    print('The board is blank. Place your ships.')
    playerBoard.showBoard()
    for counter in range(1,6):
        print('place your ship of length',counter)
        x = int(input('enter the row you wish to place the ship'))-1
        y = int(input('enter the column you wish to place the ship'))-1
        orientation = int(input('enter the ship orientation.'))
        playerBoard = placeShip(counter,orientation,x,y,playerBoard)

        showBoard(playerBoard)

def main():
    greet()

setup()

time.sleep(20)
