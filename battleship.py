#battleship
import time #used for delaying output nicely
import random #used for enemy guessing
#import mysql.connector
import re

def greet():
    print("WOULD YOU LIKE TO PLAY A GAME?")
    time.sleep(2)
    print()
    name = input("ENTER NAME: ")
    time.sleep(1)
    print("HELLO "+name.upper()+".")

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
        self.length = height*width
        self.layout = self.generateEmptyBoard()

    def coordRegexCheck(self,message):
        print(message+': ')
        coordinate = input('==> ')
        while not re.search("^[ABCDEFGHIJabcdefghij]([1-9]|10)$",coordinate):
            print(message,'(of the form A1): ')
            coordinate = input('==> ')
        return coordinate

    def directionRegexCheck(self,message):
        print(message+': ')
        direction = input('==> ')
        while not re.search("^left|right|up|down$",direction):
            print(message,'left/right/up/down: ')
            direction = input('==> ')
        return direction

    def showBoard(self): #displays the board nicely
        print('================================')
        print('X  ',end = '')
        for counter in range(self.width):
            print(counter+1,' ',end = '')
        print()
        for y in range(self.height):
            print(['A','B','C','D','E','F','G','H','I','J'][y],' ',end = '')
            for x in range(self.width):
                print(self.layout[y][x],' ',end = '')
            print()
        print('================================')

    def copyBoard(self,source,target):
        for col in range(len(target)):
                for row in range(len(target[0])):
                    target[col][row] = source[col][row]

    def generateEmptyBoard(self): #returns an empty board of the object's dimensions
        board = []
        for counter in range(self.height):
            board.append([0]*self.width)
        return board

    def getPlacement(self,ship):
        print('place your ship of length',ship)
        coordinate = self.coordRegexCheck('enter the coordinate you wish to place the ship head')
        x,y = coordinateParser(coordinate)
        orientation = self.directionRegexCheck('enter the ship orientation')
        return orientation,x,y

    def placeShip(self,ship,orientation,x,y): #modifies the board to have a ship on it
        savedLayout = self.generateEmptyBoard()
        self.copyBoard(self.layout,savedLayout)#saves layout for possible overlaps
        #ship is in range(6)
        #orientation is a direction string
        #x is the x position of the head of the ship
        #y is the y position of the head of the ship
        #self.layout is expected to be a 2D array
        modx,mody = orientationSeparator(orientation)
        #print(x,y)
        for counter in range(ship):
            if y > len(self.layout)-1 or x > len(self.layout[0])-1 or x < 0 or y < 0:
                print('SHIP OFF BOARD: PLACE ELSEWHERE')
                self.copyBoard(savedLayout,self.layout)
                newOrientation,newx,newy = self.getPlacement(ship)
                self.placeShip(ship,newOrientation,newx,newy)
            if self.layout[y][x] == 0: #tests that placement space is empty
                self.layout[y][x] = ship #places ship bit
                x += modx
                y += mody
            else:
                print('SHIP OVERLAP: PLACE ELSEWHERE')

                self.copyBoard(savedLayout,self.layout)

                self.showBoard()

                newOrientation,newx,newy = self.getPlacement(ship)
                self.placeShip(ship,newOrientation,newx,newy)
            #print(x,y)
            #showBoard(board)

    def autoPlaceShip(self,ship,orientation,x,y):
        savedLayout = self.generateEmptyBoard()
        self.copyBoard(self.layout,savedLayout)
        modx,mody = orientationSeparator(orientation)
        for counter in range(ship):
            if y > len(self.layout)-1 or x > len(self.layout[0])-1 or x < 0 or y < 0:
                self.copyBoard(savedLayout,self.layout)
                return False
            if self.layout[y][x] == 0: #tests that placement space is empty
                self.layout[y][x] = ship #places ship
                x += modx
                y += mody
            else:
                self.copyBoard(savedLayout,self.layout)
                return False
        return True

    def playerSetup(self):
        print('The board is blank. Place your ships.')
        self.showBoard()
        for counter in range(1,6):
            orientation,x,y = self.getPlacement(counter)
            self.placeShip(counter,orientation,x,y)
            self.showBoard()

    def enemySetup(self):
        for counter in range(1,6):
            orientation,x,y = ['left','right','up','down'][random.randint(0,3)], random.randint(0,9), random.randint(0,9) #remove when not needed
            result = False
            while not result:
                orientation,x,y = ['left','right','up','down'][random.randint(0,3)], random.randint(0,9), random.randint(0,9) #remove when not needed
                result = self.autoPlaceShip(counter,orientation,x,y)

    def getShipPlaces(self,x,y,board):#returns the coordinates of the ship blocks
        coordinates = [(x,y)]
        for counter in range(1):
            diffX,diffY = orientationSeparator(['left','right','up','down'][counter])
            if board.layout[y+diffY][x+diffX] == board.layout[y][x]:
                coordinates.append((x+diffX,y+diffY))
                counter = 0
                continue
        for counter in range(2,4):
            diffX,diffY = orientationSeparator(['left','right','up','down'][counter])
            if board.layout[y+diffY][x+diffX] == board.layout[y][x]:
                coordinates.append((x+diffX,y+diffY))
                counter = 2
                continue
        return coordinates

    def checkAllHits(self,coordinates):
        place = 0
        hits = []
        for col in range(self.width):
            for row in range(self.height):
                if self.layout[col][row] == 'X':
                    hits.append((col,row))
        while coordinates[place] in hits and place < len(coordinates):
            place+=1
        if place == len(coordinates)-1:
            return True
        return False

    def guess(self,targetBoard,coordinate):
        x,y = coordinateParser(coordinate)
        print(x,y)
        if targetBoard.layout[y][x] > 0: #is there a thing in the coord?
            self.layout[y][x] = 'X' #add hit to guess board
            #if self.checkAllHits(self.getShipPlaces(x,y,targetBoard)):
                #print('Ship sunk!')
            return True
        self.layout[y][x] = 'M' #add miss to guess board
        return False

    def winCheck(self):
        hitCount = 0
        for col in range(self.width):
            for row in range(self.height):
                if self.layout[col][row] == 'X':
                    hitCount+=1
        if hitCount>=15:
            return True
        return False

def setup():
    enemyBoard = Board(10,10)
    enemyGuesses = Board(10,10)
    playerBoard = Board(10,10)
    playerGuesses = Board(10,10)
    #playerBoard.playerSetup()
    enemyBoard.enemySetup()
    playerBoard.copyBoard(enemyBoard.layout,playerBoard.layout) #temp
    return enemyBoard,enemyGuesses,playerBoard,playerGuesses

def coordinateParser(coordString): #turns A3 into (0,2)
    xy = [coordString[0],coordString[1:]] #separates A3 into ['A','3']
    y = ord(xy[0].lower()) - 97 #turns A > a > 97 > 0, B > b > 97 > 0
    x = int(xy[1])-1
    return x,y

def randomCoordinate():
    letter = ['A','B','C','D','E','F','G','H','I','J'][random.randint(0,9)]
    number = random.randint(1,10)
    return letter+str(number)

def gameLoop(enemyBoard,enemyGuesses,playerBoard,playerGuesses):
    end = False
    while not end:
        if playerGuesses.guess(playerBoard,playerGuesses.coordRegexCheck('enter target')):
            print('hit!')
            print('YOUR GUESSES:')
            playerGuesses.showBoard()
        else:
            print('miss')
        if playerGuesses.winCheck():
            print('You win!')
            return
        if enemyGuesses.guess(enemyBoard,randomCoordinate()):
            print('ship hit!')
            print('ENEMY GUESSES:')
            enemyGuesses.showBoard()
        else:
            print('ships are safe.')
        if enemyGuesses.winCheck():
            print('You lose. Better luck next time!')
            return
    return

def main():
    #greet()
    enemyBoard,enemyGuesses,playerBoard,playerGuesses = setup()
    playerBoard.showBoard()
    gameLoop(enemyBoard,enemyGuesses,playerBoard,playerGuesses)
    print('GAME OVER. PLAY AGAIN?')
    response = input('Y/N: ')
    while not re.search("[YNyn]",(response)):
        response = input('Y/N: ')
    if response in ['Y','y']:
        main()
        print('GOODBYE.')
    elif response in ['N','n']:
        time.sleep(3)
        return
    #PUT SOME DATA IN A FILE HERE FOR THE DB PROGRAM TO EAT

main()
