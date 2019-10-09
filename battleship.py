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

def orientationSeparator(orientation): #converts string directions into coordinate steps
    if orientation == 'right':
        modx,mody = 1,0
    elif orientation == 'up':
        modx,mody = 0,-1
    elif orientation == 'left':
        modx,mody = -1,0
    else: #down
        modx,mody = 0,1
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

    def getPlacement(self,ship):
        print('place your ship of length',ship)
        x,y = coordinateParser(input('enter the coordinate you wish to place the ship head: '))
        orientation = input('enter the ship orientation: ')
        while orientation not in ['left','right','up','down']:
            orientation = input('enter right/left/up/down: ')
        return orientation,x,y

    def placeShip(self,ship,orientation,x,y): #modifies the board to have a ship on it
        savedLayout = self.layout #saves layout for possible overlaps
        #ship is in range(6)
        #orientation is a direction string
        #x is the x position of the head of the ship
        #y is the y position of the head of the ship
        #self.layout is expected to be a 10x10 2D array
        modx,mody = orientationSeparator(orientation)
        #print(x,y)
        for counter in range(0,ship):
            if y > len(self.layout)-1 or x > len(self.layout[0])-1 or x < 0 or y < 0:
                print('SHIP OFF BOARD: PLACE ELSEWHERE')
                self.layout = savedLayout
                '''print('place your ship of length',ship)
                newX,newY = coordinateParser(input('enter the coordinate you wish to place the ship head: '))
                newOrientation = input('enter the ship orientation: ')
                while newOrientation not in ['left','right','up','down']:
                    newOrientation = input('enter right/left/up/down: ')''' #SLATED FOR REMOVAL
                orientation,x,y = self.getPlacement(ship)
                self.placeShip(ship,newOrientation,newX,newY)
            if self.layout[y][x] == 0: #tests that placement space is empty
                self.layout[y][x] = ship #places ship
                x += modx
                y += mody
            else:
                print('SHIP OVERLAP: PLACE ELSEWHERE')
                self.layout = savedLayout
                '''print('place your ship of length',ship)
                newX,newY = coordinateParser(input('enter the coordinate you wish to place the ship head: '))
                newOrientation = input('enter the ship orientation: ')
                while newOrientation not in ['left','right','up','down']:
                    newOrientation = input('enter right/left/up/down: ')''' #SLATED FOR REMOVAL
                orientation,x,y = self.getPlacement(ship)
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
        '''print('place your ship of length',counter)
        x,y = coordinateParser(input('enter the coordinate you wish to place the ship head: '))
        orientation = input('enter the ship orientation: ')
        while orientation not in ['left','right','up','down']:
            orientation = input('enter right/left/up/down: ')''' #SLATED FOR REMOVAL
        orientation,x,y = playerBoard.getPlacement(counter)
        playerBoard.placeShip(counter,orientation,x,y)

        playerBoard.showBoard()

    return enemyBoard,enemyGuesses,playerBoard,playerGuesses

def coordinateParser(coordString): #turns A3 into (0,2)
    xy = [coordString[0],coordString[1:]] #separates A3 into ['A','3']
    y = ord(xy[0].lower()) - 97 #turns A > a > 97 > 0, B > b > 97 > 0
    x = int(xy[1])-1
    return x,y

def guess():
    guess = input('enter bombing coordinates: ')
    guessCol,guessRow = coordinateParser(guess)
    if enemyGuesses[guessRow][guessCol] != 0:
        playerGuesses[guessRow][guessCol] = 'X'
        print('hit!')
        playerGuesses.showBoard()
    else:
        playerGuesses[guessRow][guessCol] = 'M'
        print('miss.')
        playerGuesses.showBoard()
    return

def main():
    greet()
    enemyBoard,enemyGuesses,playerBoard,playerGuesses = setup()

main()
