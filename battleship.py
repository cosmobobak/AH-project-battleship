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
        self.length = height*width
        self.layout = self.generateEmptyBoard()

    def coordRegexCheck(self,message):
        print(message+': ')
        coordinate = input('==> ')
        while not re.search("[ABCDEFGHIJ]\d+",coordinate):
            print(message,'(of the form A1): ')
            coordinate = input('==> ')

    def showBoard(self): #displays the board nicely
        print('X  ',end = '')
        for counter in range(self.width):
            print(counter+1,' ',end = '')
        print()
        for y in range(self.height):
            print(['A','B','C','D','E','F','G','H','I','J'][y],' ',end = '')
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
        coordinate = input('enter the coordinate you wish to place the ship head: ')
        while not re.search("[ABCDEFGHIJ]\d+",coordinate):
            coordinate = input('enter the coordinate you wish to place the ship head (of the form A1): ')
        x,y = coordinateParser(coordinate)
        orientation = input('enter the ship orientation: ')
        while not re.search("left|right|up|down",orientation):
            orientation = input('enter right/left/up/down: ')
        return orientation,x,y

    def placeShip(self,ship,orientation,x,y): #modifies the board to have a ship on it
        savedLayout = self.layout #saves layout for possible overlaps
        #ship is in range(6)
        #orientation is a direction string
        #x is the x position of the head of the ship
        #y is the y position of the head of the ship
        #self.layout is expected to be a 2D array
        modx,mody = orientationSeparator(orientation)
        #print(x,y)
        for counter in range(0,ship):
            if y > len(self.layout)-1 or x > len(self.layout[0])-1 or x < 0 or y < 0:
                print('SHIP OFF BOARD: PLACE ELSEWHERE')
                self.layout = savedLayout
                newOrientation,newx,newy = self.getPlacement(ship)
                self.placeShip(ship,newOrientation,newx,newy)
            if self.layout[y][x] == 0: #tests that placement space is empty
                self.layout[y][x] = ship #places ship
                x += modx
                y += mody
            else:
                print('SHIP OVERLAP: PLACE ELSEWHERE')
                self.layout = savedLayout
                newOrientation,newx,newy = self.getPlacement(ship)
                self.placeShip(ship,newOrientation,newx,newy)
            #print(x,y)
            #showBoard(board)

    def autoPlaceShip(self,ship,orientation,x,y):
        savedLayout = self.layout
        modx,mody = orientationSeparator(orientation)
        for counter in range(0,ship):
            if y > len(self.layout)-1 or x > len(self.layout[0])-1 or x < 0 or y < 0:
                self.layout = savedLayout
                return False
            if self.layout[y][x] == 0: #tests that placement space is empty
                self.layout[y][x] = ship #places ship
                x += modx
                y += mody
            else:
                self.layout = savedLayout
                return False
        return True

    def playerSetup(self):
        print('The board is blank. Place your ships.')
        self.showBoard()
        for counter in range(1,6):
            orientation,x,y = self.getPlacement(counter)
            self.placeShip(counter,orientation,x,y)
            self.showBoard()

    def databaseInterface():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="enemyBoards"
            )
        except:
            print("Database connection error")
        else:
            stuff = []
            mycursor = conn.cursor()
            mycursor.execute('SELECT * FROM enemyBoards WHERE enemyid = "X"')
            myresult = mycursor.fetchall()
            '''then put those ships on the board procedurally
            probably use parallel arrays'''
            for x in myresult:
                stuff.append(x)



            print(stuff)
            return stuff

    def enemySetup(self):
        for counter in range(1,6):
            '''[
            PUT THE DATABASE INTERFACING HERE
            ]'''
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
                if self.layout[y][x] == 'X':
                    hits.append((x,y))
        while coordinates[place] in hits and place < len(coordinates):
            place+=1
        if place == len(coordinates)-1:
            return True
        return False

    def guess(self,targetBoard,coordinate):
        x,y = coordinateParser(coordinate)
        if targetBoard.layout[y][x] > 0: #is there a thing in the coord?
            self.layout[y][x] = 'X' #add hit to guess board
            print('Hit!')
            if self.checkAllHits(self.getShipPlaces(x,y,targetBoard)):
                print('Ship sunk!')
            return True
        self.layout[y][x] = '・' #add miss to guess board
        return False

def setup():
    enemyBoard = Board(10,10)
    enemyGuesses = Board(10,10)
    playerBoard = Board(10,10)
    playerGuesses = Board(10,10)
    playerBoard.playerSetup()
    enemyBoard.enemySetup()
    return enemyBoard,enemyGuesses,playerBoard,playerGuesses

def coordinateParser(coordString): #turns A3 into (0,2)
    xy = [coordString[0],coordString[1:]] #separates A3 into ['A','3']
    y = ord(xy[0].lower()) - 97 #turns A > a > 97 > 0, B > b > 97 > 0
    x = int(xy[1])-1
    return x,y

def winCheck(self):
    pass
    #count hits, if enough, win!

def gameLoop():
    end = False
    while not end:
        playerGuesses.guess(playerBoard,input('enter target'))
        #check if won
        if end:
            print('You win!')
            return
        enemyGuesses.guess()
        #check if won
    print('You lose. Better luck next time!')

def main():
    greet()
    enemyBoard,enemyGuesses,playerBoard,playerGuesses = setup()
    gameLoop()
    print('GAME OVER. PLAY AGAIN?')
    while not re.search("[YN]",(response := input('Y/N: '))): #the walrus op is unlikely to work here, keep an eye.
        pass
    if response == 'Y':
        main()
    else:
        print('GOODBYE.')
        time.sleep(3)
        return

#main()
setup()
