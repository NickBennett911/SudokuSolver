from config import *

class Board():
    def __init__(self, board):
        self.board = board
        self.font = pygame.font.SysFont("Times New Roman", cellHeight, True, False)
        self.font2 = pygame.font.SysFont("Times New Roman", cellHeight-10, True, False)

        self.showProcess = False    # boolean to show the algarithim in process or not
        self.cells = []
        for row in range(0, 9):
            for col in range(0, 9):
                self.cells.append(Cell(col*cellWidth+xOffset, row*cellHeight+yOffset, self.board[row][col]))
        self.cells[0].selected = True
        self.count = 0                  #used if wanting to count num times solve function gets ran
        self.solved = False             #when board gets solved

        self.manual = False             # if player manually solving board
        self.rowTotals = []             # contains all the rows totals
        self.colTotals = []             # contains all the col totals
        self.determinTotals()           # function that finds row and col totals

    def displayBoard(self, win):
        """
        handles the display for everything to do with the board, even the side buttons
        :param win: window surface
        :return: nothing
        """
        win.fill((0, 0, 0))
        for row in range(0, 9):         # nested for loop for going through rows and cols of board
            for col in range(0, 9):
                x = col * cellWidth + xOffset
                y = row * cellHeight + yOffset
                pygame.draw.rect(win, white, (x, y, cellWidth, cellHeight), 1)
                if self.board[row][col] != 0:               # blits number of cell if its non-zero
                    text = self.font.render(str(self.board[row][col]), True, white)
                    txt_x = x +  (text.get_width() / 2)
                    win.blit(text, (txt_x, y))
                if col%3 == 0:                          # lines for main 3x3 sections
                    pygame.draw.line(win, white, (x, yOffset), (x, cellHeight*9+yOffset), 7)
                if row%3 == 0:
                    pygame.draw.line(win, white, (xOffset, y), (cellWidth*9+xOffset, y), 7)
        # edge lines for board
        board_bottom_right = (cellWidth*9+xOffset, cellHeight*9+yOffset)
        pygame.draw.line(win, white, (cellWidth*9+xOffset ,yOffset), (board_bottom_right[0], board_bottom_right[1]), 7)
        pygame.draw.line(win, white, (xOffset, cellHeight*9+yOffset), (board_bottom_right[0], board_bottom_right[1]), 7)

        if not self.solved and self.manual: # only draws cells if unsolved and manual selected
            for cell in self.cells:
                cell.drawCell(win)

        self.drawExtra(win)     # draws other non board things

        pygame.display.flip()

    def drawExtra(self, win):
        """
        draws excess screen info so draw board method doesnt get cluttered
        :param win: window surface
        :return: nothing
        """
        # reset button draw
        pygame.draw.rect(win, white, resetRect, 2)
        win.blit(resetText, (resetRect[0] + 4, resetRect[1]))
        # new board draw
        pygame.draw.rect(win, white, newBoardRect, 2)
        win.blit(newBoardText, (newboard_x, newBoardRect[1]))
        # solve button draw
        pygame.draw.rect(win, white, solveRect, 2)
        win.blit(solveText, (solvetext_x, solveRect[1]))
        # show solution toggle button
        if self.showProcess:
            pygame.draw.rect(win, (0, 255, 0), showSolutionRect)
        pygame.draw.rect(win, white, showSolutionRect, 2)
        win.blit(showSolutionText, (showSolutionText_x, showSolutionRect[1] + 5))

        if self.manual:
            pygame.draw.rect(win, (0, 255, 0), manualSolve)
        pygame.draw.rect(win, white, manualSolve, 2)
        win.blit(manualSolveText, (showSolutionText_x, manualSolve[1] + 5))

        # DRAWS THE SIDE VALUES
        #for row in range(0, 9):
        #    x, y = (cellWidth*9+xOffset*2, (row*cellHeight+yOffset))
        #    txt = self.font2.render(str(self.rowTotals[row]), True, white)
        #    win.blit(txt, (x, y))
        #    if 0<row<9:
        #        pygame.draw.line(win, white, (x, y), (x+cellWidth, y))

        #for col in range(0, 9):
        #    x, y = (col*cellWidth+xOffset, cellHeight*9+yOffset*2)
        #    num = self.colTotals[col]
        #    txt = self.font2.render(str(num), True, white)
        #    if num < 10:
        #        win.blit(txt, (x+txt.get_width()/2,y))
        #    else:
        #        win.blit(txt, (x,y))

        #    if 0<col<9:
        #        pygame.draw.line(win, white, (x, y), (x, y+cellHeight))

    def determinTotals(self):
        """
        used to find row and col totals to display on side of board
        :return: nothing
        """

        self.rowTotals = []
        self.colTotals = []
        for row in self.board:      # adding up total in row
            total = 0
            for num in row:
                total += num
            self.rowTotals.append(total)

        for col in range(0, 9):     # adding up total cols
            total = 0
            for curRow in range(0, 9):
                total += self.board[curRow][col]
            self.colTotals.append(total)

    def solve(self, row, col, win):
        """
        function that gets called using recursion to solve board using backtracking algorithm
        :param row: starting row
        :param col: starting col
        :param win: window surface for when the solution process is being shown
        :return: True when able to find a valid spot false when a spot doesnt work and
                 algorithm needs to go back and make changes
        """
        self.count += 1               # will count how many times solve function gets called
        if self.showProcess:           # if showing process then display board every function call
            self.displayBoard(win)
            #time.sleep(0.01)          # add a time.sleep to show process a bit clearer

        if col == len(self.board[row]):     # if at the end of a row then adjust col and row for next row
            row += 1
            col = 0

        if row == len(self.board):  # if at the very end of board then its solved and return true to end recursion
            return True

        if self.board[row][col] != 0:               # if number already given in spot just skip to the next cell
            return self.solve(row, col + 1, win)

        cellValue = 1
        while (cellValue <= 9):  # iterate through all possible choices for #'s
            if self.validSpot(row, col, cellValue):  # determines if cellValue is a good pick
                self.board[row][col] = cellValue
                if self.solve(row, col + 1, win):  # if cell picks is good then move to next col
                    return True

            cellValue += 1

        self.board[row][col] = 0    # if unable to find valid num for spot set back to 0 and return false

        return False

    def validSpot(self, row, col, attemptedValue):
        """
        gets information and tests if the row and col given can allow the attempted value
        while still obeying Sudoku rules
        :param row: row being looked at
        :param col: column being looked at
        :param attemptedValue: value wanting to be added
        :return: true if value fits within game rules fails otherwise
        """
        if attemptedValue in self.board[row]:  # testing no duplicates in row
            return False

        for curRow in range(0, 9):  # testing new num isn't already in column
            if self.board[curRow][col] == attemptedValue:
                return False

        # the [row, col] index for the major section being tested
        sectionIndex = [int(row / 3), int(col / 3)]
        for x in range(0, 3):  # testing if duplicates in current major section
            for y in range(0, 3):
                curCell = self.board[x + sectionIndex[0] * 3][y + sectionIndex[1] * 3]
                if curCell == attemptedValue:       # if the current cell matches our wanted value
                    return False

        return True  # if code has made it to end then all constraints pass and return true

    def input(self, mouseRect, evt):
        """
        handles input for the board, i.e. buttons and board cell selection
        :param mouseRect: the rect at the mouse position
        :param evt: pygame event to handle button presses
        :return: nothing
        """
        index = None
        for cell in self.cells:         # gets index in cells list of the currently selected cell
            if cell.selected:
                index = self.cells.index(cell)

        if evt.type == pygame.KEYDOWN:      # writes the number pressed into the selected cell
            if evt.key in keyList:
                if evt.key == 48:
                    self.cells[index].state = 0
                self.cells[index].state = evt.key - 48
                if not self.cells[index].unchangeable:
                    self.board[int(self.cells[index].pos[1]/cellWidth)][int(self.cells[index].pos[0]/cellHeight)] = evt.key - 48

                # TO DETERMINE SIDE VALUES
                #self.determinTotals()

        if index != None:
            if evt.type == pygame.MOUSEBUTTONDOWN:  # determines if new cell is selected
                if evt.button == 1:
                    for cell in self.cells:
                        if mouseRect.colliderect(cell.cellRect):
                            self.cells[index].selected = False
                            cell.selected = True

class Cell():               # cell objs are used when board is made playable
    TIMER = 0               # static class variable used to for the flashing dash indicator
    DASH = True             # static class variable used for when dash is on screen
    def __init__(self, x, y, state):        # cells needs a x, y, position and a state for the number it has
        self.pos = [x, y]
        if state != 0:      # if cell already holds a number at start it cant be changed
            self.unchangeable = True
        else:
            self.unchangeable = False
        self.state = state
        self.cellRect = pygame.Rect(self.pos[0], self.pos[1], cellWidth, cellHeight)    #used for collision
        self.selected = False                       # is cell currently selected?
        self.font = pygame.font.SysFont("Times New Roman", cellHeight, True, False)
        self.font2 = pygame.font.SysFont("Times New Roman", cellHeight-10, True, False)
        self.dash = self.font2.render("|", True, (0, 0, 255))


    def update(self, dt):
        """
        updates the flashing cursor
        :param dt: time inbetween frames in seconds
        :return: nothing
        """
        self.TIMER += dt            #updating the toggle for the dash
        if self.TIMER >= 0.75:
            self.DASH = not self.DASH
            self.TIMER = 0.0

    def drawCell(self, win):
        """
        draws everything need for the selected cell and other cells with writen data
        :param win: window surface
        :return: Nothing
        """
        if self.selected:           # draws everything associated with a seleted cell
            pygame.draw.rect(win, (255, 0, 0), self.cellRect, 2)
            if self.state == 0 and self.DASH:               # draws dash when toggle is true
                win.blit(self.dash, ((self.pos[0]+cellWidth/2- self.dash.get_width()/2), self.pos[1]))
        if not self.unchangeable and self.state != 0:               # draws if unchangable and value has been changed
            num = self.font.render(str(self.state), True, (0, 0, 255))
            win.blit(num, (self.pos[0]+(num.get_width()/2), self.pos[1]))

