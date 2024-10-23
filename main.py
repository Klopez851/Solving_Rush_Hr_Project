# Filename: main.py
# Name: Keidy Lopez
# Purpose: main file for the project

import copy
import csv  # found this useful class through a youtube video (https://youtu.be/q5uM4VKywbA?si=4oL_h5OMOtHug1iB)
import math
import time
from logging import exception
from operator import truediv
from queue import PriorityQueue, Queue
from tabnanny import check
from timeit import Timer

import Car
from Board import Board


# Purpose: Determines whether the car of any given board is at the goal position
# Input-> Board object
# Output-> Bool
def isAtGoal(board: Board):
    carList = board.getCars()
    goalCarID = board.getGoalCarID()
    goalPos = board.getGoalPos()

    if carList[goalCarID].getX() == goalPos[0] and carList[goalCarID].getY() == goalPos[1]:
        return True
    else:
        return False


# Purpose: Generates all the possible board states of the current board (A.K.A. All the possible moves the cars can make)
# Input-> Board Object
# Output->List
def genAllPosBoardS(board: Board):
    posMoves = []
    boardStates = []
    moves = None
    for car in board.getCars():  # get all the possible moves a car can make on the current board and put them in a list
        posMoves.append(car.genAllPosMoves(board))

        # make a separate board for all possible moves
    for i in range(len(posMoves)):  # carID
        if len(posMoves[i]) != 0:
            for j in range(len(posMoves[i])):
                boardN = Board(board.getLength(), board.getWidth(), copy.deepcopy(board.getCars()), board.getGoalPos(),
                               board.getGoalCarID(), list(board.getAction()), list(board.getMoveMagnitude()))
                # Found deepcopy method in this website https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
                # while trying to find all my options for coping a list

                boardN.createBoard()

                newCars = boardN.getCars()
                newCars[i].move(posMoves[i][j][0], posMoves[i][j][1], posMoves[i][j][2], boardN.getBoard())

                moves = list(board.getMoveCount())  # keep track of the number of moves each car has made
                moves[i] += 1

                match posMoves[i][j][2]:
                    case "B":
                        boardN.setActionTaken(posMoves[i][j][0], posMoves[i][j][1], newCars[i].getOldID())
                        boardN.setMoveMagnitude(newCars[i].getOldID(), 1)
                    case "T":
                        boardN.setActionTaken(posMoves[i][j][0], posMoves[i][j][1], newCars[i].getOldID())
                        boardN.setMoveMagnitude(newCars[i].getOldID(), -1)

                boardN.setCarMoveCount(moves)
                boardStates.append(boardN)
        else:
            continue
    return boardStates


# Purpose: Stores all the information extracted from the csv and generates Car objects
# Input->List
# Output->List
def extractInfo(csvInfo: list):
    L = 0
    W = 0
    goalPos = None
    goalCarID = 0
    cars = []
    for i in range(len(csvInfo)):
        if i == 0:
            L = int(csvInfo[i][0])
            W = int(csvInfo[i][1])
        elif i == 1:
            goalPos = (int(csvInfo[i][0]), int(csvInfo[i][1]))
        else:
            car = Car.createCar(int(csvInfo[i][0]), int(csvInfo[i][1]), int(csvInfo[i][2]), csvInfo[i][3],
                                int(csvInfo[i][4]), csvInfo[i][5])

            if car.getID() != (i - 2):
                car.setID(i - 2)
            if car.getIsGoalCar():  # gets ID of goal car while in loop
                goalCarID = car.getID()
            cars.append(car)
    return L, W, goalPos, goalCarID, cars


def main():
    # get board file and extract its information
    boardFile = input("Please enter the name of your board file: ")  # Here im assuming the board file will be within
    # project folder, which is why im not asking for a
    # relative file path
    csvInfo = []
    with open(boardFile) as boardCSV:
        boardReader = csv.reader(boardCSV)
        for line in boardReader:
            csvInfo.append(line)
    print("extracting information from file...")
    time.sleep(.5)  # timer to improve the flow of the program and make the user experience better

    # create board
    L, W, goalPos, goalCarID, cars = extractInfo(csvInfo)
    board = Board(L, W, cars, goalPos, goalCarID)
    board.createBoard()
    print("creating board..")
    time.sleep(.5)

    print("Generating a solution...")
    # A* algorithm
    pQueue = PriorityQueue()
    moveMagnitude = None  # for solution file
    visitedBoards = []  # keeps track of all the expanded/visited board states
    solved = False
    counter = 0  # for the purpose of giving each board a unique value and keeping track of how many states where expanded

    # CURRENT PROBLEM: Can solve simple boards, but cant solve more complex boards
    while solved != True:
        # generate all possible board states
        boardList = genAllPosBoardS(board)

        # check if board states have been previously expanded
        for i in range(len(boardList)):
            for j in range(len(visitedBoards)):
                if boardList[i] == visitedBoards[j]:
                    boardList[i] = None
                    break

        # add boards not in visited to pQueue
        for i in range(len(boardList)):
            if boardList[i] == None:
                continue
            else:
                f = boardList[i].g() + boardList[i].h()
                pQueue.put((f, counter, boardList[i]))
                counter += 1

        # swap boards
        temp = pQueue.get()

        # check if new board is in visited

        checking = True
        while checking:
            if len(visitedBoards) == 0:
                checking = False

            for i in range(len(visitedBoards)):
                if temp[2] == visitedBoards[i]:
                    temp = pQueue.get()
                    break
                elif temp[2] != visitedBoards[j] and i == len(visitedBoards) - 1:
                    checking = False
                    break
                else:
                    continue

        board = temp[2]
        visitedBoards.append(board)

        # check if car is at the goal position
        if isAtGoal(board):
            moveMagnitude = board.getMoveMagnitude()
            solved = True

    # Let user know solution has been found
    time.sleep(.5)
    print("Solution found!")
    time.sleep(.5)

    # #write moves to csv
    solutionFile = input("Where would you like to store the solution? (File name): ")
    with open(solutionFile, 'w', newline='') as file:
        boardWriter = csv.writer(file)
        for i in range(0, len(moveMagnitude), 2):
            boardWriter.writerow([moveMagnitude[i], moveMagnitude[i + 1]])

    time.sleep(.5)
    print("Solution stored!")
    time.sleep(.5)
    print("Closing program...")
    time.sleep(.5)

    # end of program


if __name__ == '__main__':
    main()
