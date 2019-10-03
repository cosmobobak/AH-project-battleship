#battleship
import time #used for delaying output nicely

def greet():
    print("WOULD YOU LIKE TO PLAY A GAME?")
    time.sleep(3)
    print()
    name = input("ENTER NAME: ")
    name = name.upper()
    time.sleep(1)
    print("HELLO "+name+".")

def orientationSeparator(orientation): #converts 4 integer directions into coordinate steps
    if orientation == 1: #right
        modx = 1
        mody = 0
    elif orientation == 2: #up
        modx = 0
        mody = -1
    elif orientation == 3: #left
        modx = -1
        mody = 0
    else: #(4) down
        modx = 0
        mody = 1
    return modx, mody

class Board: #the board for ships and the board for guesses
    def __init__(self,height,width): #instantiates a board
        self.height = height
        self.width = width
        self.layout = self.generateEmptyBoard()

    def showBoard(self): #displays the board nicely
        for y in range(self.height):
            for x in range(self.width):
                print(self.layout[y][x],' ',end = '')
            print()

    def generateEmptyBoard(self): #returns an empty board of the object's dimensions
        board = []
        for counter in range(self.height):
            board.append([0]*self.width)
        return board

    def placeShip(self,ship,orientation,x,y): #modifies the board to have a ship on it
        savedLayout = self.layout
        #ship is an integer from 1-5
        #orientation is an integer from 1-4
        #x is the x position of the head of the ship
        #y is the y position of the head of the ship
        #self.layout is expected to be a 10x10 2D array
        modx,mody = orientationSeparator(orientation)
        #print(x,y)
        for counter in range(0,ship):
            if self.layout[y][x] == 0:
                self.layout[y][x] = ship
                x += modx
                y += mody
            else:
                print('SHIP OVERLAP: PLACE ELSEWHERE')
                self.layout = savedLayout
                print('place your ship of length',ship)
                newX = int(input('enter the column you wish to place the ship'))-1
                newY = int(input('enter the row you wish to place the ship'))-1
                newOrientation = int(input('enter the ship orientation.'))
                self.placeShip(ship,newOrientation,newX,newY)
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
        x = int(input('enter the column you wish to place the ship'))-1
        y = int(input('enter the row you wish to place the ship'))-1
        orientation = int(input('enter the ship orientation.'))
        playerBoard.placeShip(counter,orientation,x,y)

        playerBoard.showBoard()

    return enemyBoard,enemyGuesses,playerBoard,playerGuesses

def coordinateParser(coordString): #turns A3 into (0,2)
    xy = coordString.split() #separates A3 into ['A','3']
    x = ord(xy[0].lower()) - 97 #turns A > a > 97 > 0, B > b > 98 > 1
    y = xy[1]-1
    return x,y

def guess():
    guess = input('enter bombing coordinates: ')
    guessCol,guessRow = coordinateParser(guess)
    return

def main():
    greet()
    enemyBoard,enemyGuesses,playerBoard,playerGuesses = setup()

main()
