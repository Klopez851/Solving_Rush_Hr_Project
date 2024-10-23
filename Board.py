import Car
import math


class Board:
    def __init__(self, L: int, W: int, cars: list, goalPos: tuple, goalCarID: int, actionTaken=[], moveMagnitude=[]):
        self.L = L
        self.W = W
        self.cars = cars
        self.board = []
        self.goalPos = goalPos
        self.goalCarID = goalCarID
        self.carMoveCount = None
        self.actionTaken = actionTaken
        self.moveMagnitude = moveMagnitude

    ###########
    # GETTERS #
    ###########

    def getLength(self):
        return self.L

    def getWidth(self):
        return self.W

    def getBoard(self):
        return self.board

    def getCars(self):
        return self.cars

    def getGoalPos(self):
        return self.goalPos

    def getGoalCarID(self):
        return self.goalCarID

    def getMoveCount(self):
        return self.carMoveCount

    def getAction(self):
        return self.actionTaken

    def getMoveMagnitude(self):
        return self.moveMagnitude

    ###########
    # SETTERS #
    ###########

    def setCarMoveCount(self, moves: list):
        self.carMoveCount = moves

    def setActionTaken(self, y: int, x: int, carID: int):
        self.actionTaken.extend((y, x, carID))

    def setMoveMagnitude(self, carID: int, moveMagnitude: int):
        self.moveMagnitude.extend((carID, moveMagnitude))

    #########
    # OTHER #
    #########

    # Purpose:Creates a nested list(board) of specified dimentions with cars at certain indices, stores it w/n the class
    # Input->None
    # Output->None
    def createBoard(self):
        for i in range(self.L):
            self.board.append([0.1 for j in range(self.W)])
        # self.board[self.goalPos[1]][self.goalPos[0]] = "G"

        self.carMoveCount = [0 for j in range(len(self.cars))]

        # add cars to board
        for car in self.cars:
            if car.orientation == "H":
                for i in range(car.length):
                    self.board[car.getY()][car.getX() + i] = car.getID()
            if car.orientation == "V":
                for i in range(car.length):
                    self.board[car.getY() + i][car.getX()] = car.getID()

    # Purpose:Checks if a spot on the board had a value of 0.1
    # Input-> Ints
    # Output->Bool
    def isUnoccupied(self, y: int, x: int):
        if self.board[y][x] == 0.1:
            return True
        else:
            return False

    # Purpose:calculated the heuristic value of board (A.K.A how far away from the goal the goal car is)
    # Input->None
    # Output->Int
    def h(self):
        x1, y1 = self.cars[self.goalCarID].getX(), self.cars[self.goalCarID].getY()
        x2, y2 = self.goalPos[0], self.goalPos[1]
        h = (math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)))
        return math.floor(h)

    # Purpose:Calculates the sum of all the moves the cars on the board have made
    # Input->None
    # Output->Int
    def g(self):
        g = 0
        for num in self.carMoveCount:
            g += num

        return g

    # Purpose:Overides the default == method of object, comparing the cars lists of both boards
    # Input-> Board object
    # Output->Bool
    def __eq__(self, other):
        if other == None:
            return False
        else:
            board1 = self.cars
            board2 = other.cars
            equalValues = 0

        for i in range(len(board1)):
            if board1[i] == board2[i]:
                equalValues += 1
            else:
                continue

        return equalValues == len(board1)
