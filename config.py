import pygame
import random
import time
pygame.init()

# GLOBALS
width = 1300
height = 750
cellWidth = 70
cellHeight = 70
white = (255, 255, 255)
yOffset = 20
xOffset = 50

mouseRect = pygame.Rect(0, 0, 1, 1)     # rectangle for where the mouse is in window

# RESETS BOARD TO ORIGONAL
FONT = pygame.font.SysFont("Times New Roman", 40)
resetText = FONT.render("Reset Board", True, white)
rect_w = 200
rect_x = (cellWidth*9) + (((width - (cellWidth*9))/2) - (rect_w/2)) + xOffset
resetRect = pygame.Rect(rect_x, 50, 200, 50)

# GIVES A RANDOM NEW BOARD
newBoardText = FONT.render("New Board", True, white)
newboard_x = rect_x+(rect_w/2) - (newBoardText.get_width()/2)
newBoardRect = pygame.Rect(rect_x, 150, 200, 50)

# USE ALGORITHM AND SOLVE BOARD
solveText = FONT.render("Solve", True, white)
solvetext_x = rect_x+(rect_w/2) - (solveText.get_width()/2)
solveRect = pygame.Rect(rect_x, 250, 200, 50)

# sHOW ALGORITHM RECTANGLE AND TEXT
tinyfont = pygame.font.SysFont("Times New Roman", 15)
showSolutionText = tinyfont.render("Show Algorithm", True, white)
showSolutionRect = pygame.Rect(rect_x + 25, 325, 30, 30)
showSolutionText_x = showSolutionRect[0]+showSolutionRect[3]+10

# SOLVE MANUALLY RECTANGLE
manualSolve = pygame.Rect(rect_x+25, 375, 30, 30)
manualSolveText = tinyfont.render("Solve Manually", True, white)

# KEY CODES FOR NUMBERS 1-9
keyList = [49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 13, 271]


# PRESET SUDOKU BOARDS
emptySudoku =  [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

presetSudoku1 = [[0, 0, 8, 0, 0, 0, 2, 3, 0],
                [3, 0, 0, 7, 0, 0, 0, 0, 5],
                [4, 0, 0, 3, 0, 0, 0, 6, 0],
                [6, 0, 0, 8, 0, 1, 0, 0, 0],
                [0, 1, 2, 0, 0, 0, 9, 0, 0],
                [0, 0, 0, 2, 0, 5, 0, 0, 4],
                [0, 3, 0, 0, 0, 6, 0, 0, 9],
                [2, 0, 0, 0, 0, 0, 0, 0, 7],
                [0, 4, 7, 0, 0, 0, 0, 0, 0]]


presetSudoku2 =  [[0,0,0,0,4,9,0,0,0],
                  [0,4,0,0,0,0,0,7,3],
                  [8,0,0,6,7,0,0,2,0],
                  [0,0,0,3,0,0,8,5,0],
                  [6,0,0,0,2,0,0,0,7],
                  [0,3,1,0,0,8,0,0,0],
                  [0,9,0,0,8,2,0,0,1],
                  [4,7,0,0,0,0,0,8,0],
                  [0,0,0,5,9,0,0,0,0]]

presetSudoku3 =  [[0,0,8,0,3,0,2,0,0],
                  [0,4,0,0,0,0,0,9,0],
                  [2,0,0,6,0,1,0,0,7],
                  [0,0,9,0,0,0,7,0,0],
                  [4,0,0,0,2,0,0,0,8],
                  [0,0,5,0,0,0,3,0,0],
                  [3,0,0,5,0,8,0,0,1],
                  [0,7,0,0,0,0,0,5,0],
                  [0,0,4,0,6,0,8,0,0]]

presetSudoku4 =  [[0,8,0,0,0,1,0,0,0],
                  [7,5,0,0,0,0,0,0,3],
                  [0,0,0,9,0,7,0,5,4],
                  [0,2,0,0,0,8,0,0,0],
                  [0,1,0,7,5,6,0,3,0],
                  [0,0,0,2,0,0,0,9,0],
                  [6,7,0,0,0,2,0,0,0],
                  [2,0,0,0,0,0,0,7,8],
                  [0,0,0,8,0,0,0,4,0]]

def pickRandomBoard(currentBoard):      # some nice extra recursion on the side :)
    boards = [presetSudoku1,
              presetSudoku2,
              presetSudoku3,
              presetSudoku4]
    choice = random.randint(0, len(boards)-1)
    if boards[choice] == currentBoard:
        return pickRandomBoard(currentBoard) # if random selected board is current board then try function again

    return boards[choice]