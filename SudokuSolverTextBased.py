# Nick Bennett
# Using Recursion to solve Sudoku


sudoku = [[0, 0, 8, 0, 0, 0, 2, 3, 0],
          [3, 0, 0, 7, 0, 0, 0, 0, 5],
          [4, 0, 0, 3, 0, 0, 0, 6, 0],
          [6, 0, 0, 8, 0, 1, 0, 0, 0],
          [0, 1, 2, 0, 0, 0, 9, 0, 0],
          [0, 0, 0, 2, 0, 5, 0, 0, 4],
          [0, 3, 0, 0, 0, 6, 0, 0, 9],
          [2, 0, 0, 0, 0, 0, 0, 0, 7],
          [0, 4, 7, 0, 0, 0, 0, 0, 0]]

def printBoard(board):
    """
    prints the board passed to it
    :param board: board passed
    :return: nothing
    """
    print("")
    for row in board:
        print(row)
    print("")

def validSpot(row, col, board, newNum):
    """
    checks all 3 constraints for sudoku, non-repeating #'s in row/col
    and not # duplicates in current major section
    :param row: current cell being looked at
    :param col: current col being looked at
    :param board: the sudoku board
    :param newNum: number attempting to be placed
    :return: true if all constraints pass, false if even one fails
    """
    if newNum in board[row]:  # testing no duplicates in row
        return False

    for curRow in range(0, 9):              # testing new num isnt already in column
        if board[curRow][col] == newNum:
            return False

    sectionIndex = [int(row/3), int(col/3)]
    for x in range(0, 3):           # testing if duplicates in current major section
        for y in range(0, 3):
            curCell = board[x+sectionIndex[0]*3][y+sectionIndex[1]*3]
            if curCell == newNum:
                return False

    return True         # if code has made it to end then all constraints pass and return true


def solve(row, col, board):
    """
    this function uses backtracking algorithm to solve the entire given
    sudoku board
    :param row: current row being solved
    :param col: current col being solve
    :param board: the passed sudoku board
    :return: true if cellValue is valid
    """
    if col == len(board[row]):  # if at the end of row go to next row
        col = 0
        row += 1
    if row == len(board):     # if at the end of board return true because solved
        return True

    if board[row][col] != 0:        # if current cell is already solved move to the next
        return solve(row, col+1, board)

    cellValue = 1
    while (cellValue <= 9):             # iterate through all possible choices for #'s
        if validSpot(row, col, board, cellValue):  #determins if cellValue is a good pick
            board[row][col] = cellValue
            if solve(row, col + 1, board):          # if cell picks is good then move to next col
                return True

        cellValue += 1

    board[row][col] = 0

    return False

solve(0, 0, sudoku)
printBoard(sudoku)