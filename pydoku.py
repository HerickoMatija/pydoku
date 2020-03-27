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
    if board[row][column] != 0:
        if column == len(board[row]) - 1 and row == len(board) - 1:
            return True
        else:
            if column == len(board[row]) - 1:
                return solveSudokuHelper(board, row + 1, 0)
            else:
                return solveSudokuHelper(board, row, column + 1)
    
    for candidateNumber in range(1,10):
        if isValid(candidateNumber, row, column, board):
            board[row][column] = candidateNumber

            if column == len(board[row]) - 1 and row == len(board) - 1:
                return True
            else:                
                if column == len(board[row]) - 1:
                    result = solveSudokuHelper(board, row + 1, 0)
                else:
                    result = solveSudokuHelper(board, row, column + 1)

            if result:
                return True
            
            board[row][column] = 0

    return False

def isValid(number, row, column, board):
    for boardRow in range(9):        
        if board[boardRow][column] == number and boardRow != row:
            return False
    
    for boardColumn in range(9):
        if board[row][boardColumn] == number and boardColumn != column:
            return False
    
    squareStartRow = (row // 3) * 3
    squareStartColumn = (column // 3) * 3

    for boardRow in range(squareStartRow, squareStartRow + 3):
        for boardColumn in range(squareStartColumn, squareStartColumn + 3):
            if board[boardRow][boardColumn] == number:
                if boardRow != row or boardColumn != column:
                    return False
    
    return True


board = [
    [0,0,9,2,1,8,0,0,0],
    [1,7,0,0,9,6,8,0,0],
    [0,4,0,0,5,0,0,0,6],
    [4,5,1,0,6,0,3,7,0],
    [0,0,0,0,0,5,0,0,9],
    [9,0,2,3,7,0,5,0,0],
    [6,0,0,5,0,1,0,0,0],
    [0,0,0,0,4,9,2,5,7],
    [0,9,4,8,0,0,0,1,3],
]

solved = [        
    [3,6,9,2,1,8,7,4,5],
    [1,7,5,4,9,6,8,3,2],
    [2,4,8,7,5,3,1,9,6],
    [4,5,1,9,6,2,3,7,8],
    [7,3,6,1,8,5,4,2,9],
    [9,8,2,3,7,4,5,6,1],
    [6,2,7,5,3,1,9,8,4],
    [8,1,3,6,4,9,2,5,7],
    [5,9,4,8,2,7,6,1,3]
]

solveSudoku(board)
printBoard(board)

def isSolved(board, solved):
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] != solved[row][column]:
                return False
    
    return True

print(isSolved(board, solved))
