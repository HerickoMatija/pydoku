def printBoard(board):
    borderLine = "+---+---+---+"

    print(borderLine)

    for row in range(len(board)):
        print("|", end="")
        for column in range(len(board[row])):
            print(board[row][column], end="")
            if (column + 1) % 3 == 0:
                print("|", end="")
        print()
        if (row + 1) % 3 == 0:
            print("+---+---+---+")


def solveSudoku(board):
    solveSudokuHelper(board, 0, 0)


def solveSudokuHelper(board, row, column):
    lastColumn = len(board[row]) - 1
    lastRow = len(board) - 1

    # We check if the cell already has a value
    if board[row][column] != 0:
        # We are at the last cell so return True
        if column == lastColumn and row == lastRow:
            return True
        else:
            # Check if we are at the last cell in a row
            if column == lastColumn:
                return solveSudokuHelper(board, row + 1, 0)
            else:
                return solveSudokuHelper(board, row, column + 1)

    # Cell has no value so try to find a candidate
    for candidateNumber in range(1, 10):
        # Check if the candidate number is valid in this cell
        if isValid(candidateNumber, row, column, board):

            # Set the candidate number
            board[row][column] = candidateNumber

            # Check if we reached the end
            if column == lastColumn and row == lastRow:
                return True
            else:
                # Check if we are at the last cell in a row
                if column == lastColumn:
                    result = solveSudokuHelper(board, row + 1, 0)
                else:
                    result = solveSudokuHelper(board, row, column + 1)

            # If the recursion returns True we found a solution
            if result:
                return True

            # Otherwise reset the cell
            board[row][column] = 0

    return False


def isValid(number, row, column, board):
    # Check if the same number is in the row or column
    for idx in range(9):
        if board[idx][column] == number and idx != row:
            return False
        if board[row][idx] == number and idx != column:
            return False

    # Find the starting cell of the 3x3 square
    squareStartRow = (row // 3) * 3
    squareStartColumn = (column // 3) * 3

    # Check if the same number is in the 3x3 square
    for boardRow in range(squareStartRow, squareStartRow + 3):
        for boardColumn in range(squareStartColumn, squareStartColumn + 3):
            if board[boardRow][boardColumn] == number:
                if boardRow != row or boardColumn != column:
                    return False

    return True


def isSolved(board, solved):
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] != solved[row][column]:
                return False

    return True


# The sudoku puzzle that we are solving
board = [
    [0, 0, 9, 2, 1, 8, 0, 0, 0],
    [1, 7, 0, 0, 9, 6, 8, 0, 0],
    [0, 4, 0, 0, 5, 0, 0, 0, 6],
    [4, 5, 1, 0, 6, 0, 3, 7, 0],
    [0, 0, 0, 0, 0, 5, 0, 0, 9],
    [9, 0, 2, 3, 7, 0, 5, 0, 0],
    [6, 0, 0, 5, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 4, 9, 2, 5, 7],
    [0, 9, 4, 8, 0, 0, 0, 1, 3],
]

# The solution
solved = [
    [3, 6, 9, 2, 1, 8, 7, 4, 5],
    [1, 7, 5, 4, 9, 6, 8, 3, 2],
    [2, 4, 8, 7, 5, 3, 1, 9, 6],
    [4, 5, 1, 9, 6, 2, 3, 7, 8],
    [7, 3, 6, 1, 8, 5, 4, 2, 9],
    [9, 8, 2, 3, 7, 4, 5, 6, 1],
    [6, 2, 7, 5, 3, 1, 9, 8, 4],
    [8, 1, 3, 6, 4, 9, 2, 5, 7],
    [5, 9, 4, 8, 2, 7, 6, 1, 3]
]

# Trigger the algorithm to solve the board
solveSudoku(board)
# Print the board to console
printBoard(board)
# Print the result if the algorithm solved it correctly
print(isSolved(board, solved))
