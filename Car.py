# Filename: Car.py
# Name: Keidy Lopez
# Purpose: class used to create cars from a CSV

import Board


# Purpose: This method creates car objects
# Input-> Ints & Str
# Output-> Car object
def createCar(ID: int, x: int, y: int, orientation: str, length: int, goalCar: str):
    car = Car(ID, x, y, orientation, length, goalCar)
    return car


class Car:
    def __init__(self, ID: int, x: int, y: int, orientation: str, length: int, goalCar: str):
        self.ID = ID
        self.oldID = ID
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        if goalCar == "T":
            self.isGoalCar = True
        else:
            self.isGoalCar = False

    ###########
    # GETTERS #
    ###########

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getID(self):
        return self.ID

    def getOldID(self):
        return self.oldID

    def getIsGoalCar(self):
        return self.isGoalCar

    ###########
    # SETTERS #
    ###########

    def setX(self, x: int):
        self.x = x

    def setY(self, y: int):
        self.y = y

    def setID(self, ID):
        self.ID = ID

    def setOldID(self, ID):
        self.oldID = ID

    #########
    # OTHER #
    #########

    # Purpose:Moves a car on any given board to a specified location
    # Input-> Ints, Str, Board object
    # Output-> None
    def move(self, upperY: int, upperX: int, moveFrom: str, board: list):
        if self.orientation == "H":
            if moveFrom == "T":
                for i in range(self.length):
                    board[upperY][upperX + i] = self.getID()
                    board[self.getY()][self.getX() + i] = 0.1
                self.setY(upperY)
                self.setX(upperX)
            if moveFrom == "B":
                board[self.getY()][self.getX()] = 0.1
                board[upperY][upperX] = self.getID()
                self.setY(upperY)
                self.setX(upperX - (self.length - 1))
        if self.orientation == "V":
            if moveFrom == "T":
                for i in range(self.length):
                    board[upperY + i][upperX] = self.getID()
                    board[self.getY() + i][self.getX()] = 0.1
                self.setY(upperY)
                self.setX(upperX)
            if moveFrom == "B":
                board[upperY][upperX] = self.getID()
                board[self.getY()][self.getX()] = 0.1
                self.setY(upperY - (self.length - 1))
                self.setX(upperX)

    # Purpose: Generates all the possible moves a car can make on a board, checks for boundaries.
    # Input->Board Object
    # Output->List
    def genAllPosMoves(self, board: Board):
        posMoves = []  # in y,x order cuz board is formatted that way i.e. [y][x]
        if self.orientation == "H":
            if self.x != 0:
                if board.isUnoccupied(self.y, self.x - 1):
                    posMoves.append(
                        [self.y, self.x - 1, "T"])  # T = top side, so it tell me the car is supposed to move up/left
            if not ((self.x + self.length) >= board.getWidth()):  # negate
                if board.isUnoccupied(self.y, (self.x + self.length)):
                    posMoves.append([self.y, (self.x + self.length),
                                     "B"])  # B = bottom side, so it tell me the car is supposed to move down/right
        if self.orientation == "V":
            if self.y != 0:
                if board.isUnoccupied(self.y - 1, self.x):
                    posMoves.append([self.y - 1, self.x, "T"])
            if not ((self.y + self.length) >= board.getLength()):
                if board.isUnoccupied((self.y + self.length), self.x):
                    posMoves.append([(self.y + self.length), self.x, "B"])
        return posMoves

    # Purpose:Overides the default == object, comparing the location and ID of cars
    # Input-> Car object
    # Output->Bool
    def __eq__(self, other):
        return (self.y, self.x, self.ID) == (other.y, other.x, other.ID)
