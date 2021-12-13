from SudokuBoard import *
from copy import deepcopy

win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

done = False
curBoard = emptySudoku
myBoard = Board(deepcopy(curBoard))


while not done:
    #update
    deltaTime = clock.tick() / 1000.0
    for cell in myBoard.cells:
        if cell.selected:
            cell.update(deltaTime)

    #input
    evt = pygame.event.poll()
    mx, my = pygame.mouse.get_pos()
    mouseRect = pygame.Rect(mx, my, 1, 1)
    if myBoard.manual:
        myBoard.input(mouseRect, evt)
    if evt.type == pygame.QUIT:
        done = True
    elif evt.type == pygame.KEYDOWN:
        if evt.key == pygame.K_ESCAPE:
            done = True
    elif evt.type == pygame.MOUSEBUTTONDOWN:
        if evt.button == 1:
            if mouseRect.colliderect(resetRect):  # reset button pressed
                myBoard = Board(deepcopy(curBoard))
            elif mouseRect.colliderect((newBoardRect)):  # new board button pressed
                curBoard = pickRandomBoard(curBoard)
                myBoard = Board(deepcopy(curBoard))
            elif mouseRect.colliderect(solveRect):  # solve Rect
                myBoard.solve(0, 0, win)
                myBoard.determinTotals()
                myBoard.solved = True
            elif mouseRect.colliderect(showSolutionRect):  # solve Rect
                myBoard.showProcess = not myBoard.showProcess
            elif mouseRect.colliderect(manualSolve):
                myBoard.manual = not myBoard.manual

    print(myBoard.count)
    #draw
    myBoard.displayBoard(win)   # handles window reset and display flip
pygame.quit()
