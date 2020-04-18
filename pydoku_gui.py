# Simple pygame program

import time

# Import and initialize the pygame library
import pygame
pygame.init()

# Create the font that will be used
font = pygame.font.SysFont('Monospace', 32)


class PydokuCell:

    def __init__(self, number):
        self.number = number
        self.editable = number == 0
        self.invalid = False
        self.selected = False
        self.underConsideration = False


class PydokuGUI:

    # colors that are used
    COLOR_BLACK = (0, 0, 0)
    COLOR_RED = (255, 0, 0)
    COLOR_ORANGE = (255, 165, 0)
    COLOR_GREY = (105, 105, 105)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GREEN = (0, 255, 0)
    COLOR_LIGHT_BLUE = (0, 180, 255)

    # Static width calculation based on 9 cells, 6 normal lines and 2 thicker lines
    WIDTH = 9 * 39 + 6 * 1 + 2 * 3
    # Helper array to have access to the center of the cells
    cellCenters = [20, 60, 100, 142, 182, 222, 264, 304, 344]

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        pygame.display.set_caption('Pydoku GUI')
        self.selectedCell = None
        self.board = self.getBoard()

    def getBoard(self):
        return [
            [
                PydokuCell(0), PydokuCell(0), PydokuCell(9),
                PydokuCell(2), PydokuCell(1), PydokuCell(8),
                PydokuCell(0), PydokuCell(0), PydokuCell(0)
            ],
            [
                PydokuCell(1), PydokuCell(7), PydokuCell(0),
                PydokuCell(0), PydokuCell(9), PydokuCell(6),
                PydokuCell(8), PydokuCell(0), PydokuCell(0)
            ],
            [
                PydokuCell(0), PydokuCell(4), PydokuCell(0),
                PydokuCell(0), PydokuCell(5), PydokuCell(0),
                PydokuCell(0), PydokuCell(0), PydokuCell(6)
            ],
            [
                PydokuCell(4), PydokuCell(5), PydokuCell(1),
                PydokuCell(0), PydokuCell(6), PydokuCell(0),
                PydokuCell(3), PydokuCell(7), PydokuCell(0)
            ],
            [
                PydokuCell(0), PydokuCell(0), PydokuCell(0),
                PydokuCell(0), PydokuCell(0), PydokuCell(5),
                PydokuCell(0), PydokuCell(0), PydokuCell(9)
            ],
            [
                PydokuCell(9), PydokuCell(0), PydokuCell(2),
                PydokuCell(3), PydokuCell(7), PydokuCell(0),
                PydokuCell(5), PydokuCell(0), PydokuCell(0)
            ],
            [
                PydokuCell(6), PydokuCell(0), PydokuCell(0),
                PydokuCell(5), PydokuCell(0), PydokuCell(1),
                PydokuCell(0), PydokuCell(0), PydokuCell(0)
            ],
            [
                PydokuCell(0), PydokuCell(0), PydokuCell(0),
                PydokuCell(0), PydokuCell(4), PydokuCell(9),
                PydokuCell(2), PydokuCell(5), PydokuCell(7)
            ],
            [
                PydokuCell(0), PydokuCell(9), PydokuCell(4),
                PydokuCell(8), PydokuCell(0), PydokuCell(0),
                PydokuCell(0), PydokuCell(1), PydokuCell(3)
            ]
        ]

    def drawBoard(self):
        self.drawLines()
        self.drawNumbers()
        pygame.display.flip()

    def drawLines(self):
        # Fill the background
        self.screen.fill(self.COLOR_WHITE)

        # Draw the lines for the Sudoku board
        x = 40
        for i in range(1, 10):
            self.drawLine((x, 0), (x, self.WIDTH), self.COLOR_BLACK)
            self.drawLine((0, x), (self.WIDTH, x), self.COLOR_BLACK)

            # If its the third line we want to make it appear thicker,
            # so we draw three consecutive lines
            if i % 3 == 0:
                x += 1
                self.drawLine((x, 0), (x, self.WIDTH), self.COLOR_BLACK)
                self.drawLine((0, x), (self.WIDTH, x), self.COLOR_BLACK)
                x += 1
                self.drawLine((x, 0), (x, self.WIDTH), self.COLOR_BLACK)
                self.drawLine((0, x), (self.WIDTH, x), self.COLOR_BLACK)

            x += 40

    def drawLine(self, startPoint, endPoint, color):
        pygame.draw.line(self.screen, color, startPoint, endPoint)

    def drawNumbers(self):
        # Go through the board and draw the numbers into the cells
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):

                cell = self.board[row][column]

                if cell.number != 0:
                    color = self.COLOR_GREY if cell.editable else self.COLOR_BLACK
                    self.drawNumber(cell.number, row, column, color)

                if cell.selected or cell.invalid:
                    color = self.COLOR_RED if cell.invalid else self.COLOR_LIGHT_BLUE
                    self.colorCellBorder(row, column, color)

                if cell.underConsideration:
                    self.colorCellBorder(row, column, self.COLOR_ORANGE)

    def drawNumber(self, number, row, column, color):
        text = font.render(str(number),
                           True,
                           color,
                           self.COLOR_WHITE)

        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.center = (self.cellCenters[column], self.cellCenters[row])

        self.screen.blit(text, textRect)

    def colorCellBorder(self, row, column, color):
        rowCenter = self.cellCenters[row]
        columnCenter = self.cellCenters[column]

        self.drawLine((columnCenter - 20, rowCenter - 20),
                      (columnCenter + 20, rowCenter - 20),
                      color)

        self.drawLine((columnCenter - 20, rowCenter + 20),
                      (columnCenter + 20, rowCenter + 20),
                      color)

        self.drawLine((columnCenter - 20, rowCenter - 20),
                      (columnCenter - 20, rowCenter + 20),
                      color)

        self.drawLine((columnCenter + 20, rowCenter - 20),
                      (columnCenter + 20, rowCenter + 20),
                      color)

    def setSelectedCell(self, mouseClickPosition):
        clickedColumn = self.getCellFromCoord(mouseClickPosition[0])
        clickedRow = self.getCellFromCoord(mouseClickPosition[1])

        if self.selectedCell is not None:
            row, column = self.selectedCell
            self.board[row][column].selected = False

        self.selectedCell = (clickedRow, clickedColumn)
        self.board[clickedRow][clickedColumn].selected = True

    def getCellFromCoord(self, coordinate):
        for idx, cellCenter in enumerate(self.cellCenters):
            if cellCenter - 20 < coordinate and coordinate < cellCenter + 20:
                return idx

        return -1

    def setNumber(self, number):
        if self.selectedCell is None:
            return

        row, column = self.selectedCell
        cell = self.board[row][column]

        if cell.editable:
            self.resetValidation()
            cell.number = number
            if number != 0:
                self.validateSelectedCellNumber()

    def delete(self):
        if self.selectedCell is None:
            return
        self.setNumber(0)

    def moveSelectedCell(self, rowMove, columnMove):
        if self.selectedCell is None:
            return

        oldRow, oldColumn = self.selectedCell

        newRow = oldRow + rowMove
        newColumn = oldColumn + columnMove

        if -1 < newRow and newRow < 9 and -1 < newColumn and newColumn < 9:
            self.selectedCell = (newRow, newColumn)
            self.board[oldRow][oldColumn].selected = False
            self.board[newRow][newColumn].selected = True

    def validateSelectedCellNumber(self):
        if self.selectedCell is None:
            return

        selectedRow, selectedColumn = self.selectedCell
        self.traverseSignificantCellsAndSetInvalidTo(selectedRow,
                                                     selectedColumn,
                                                     True)

    def resetValidation(self):
        if self.selectedCell is None:
            return

        selectedRow, selectedColumn = self.selectedCell
        self.traverseSignificantCellsAndSetInvalidTo(selectedRow,
                                                     selectedColumn,
                                                     False)

    def traverseSignificantCellsAndSetInvalidTo(self, row, column, invalid):
        cell = self.board[row][column]

        for idx in range(9):
            currentCell = self.board[idx][column]

            if currentCell.number == cell.number and row != idx:
                cell.invalid = invalid
                currentCell.invalid = invalid

            currentCell = self.board[row][idx]

            if currentCell.number == cell.number and column != idx:
                cell.invalid = invalid
                currentCell.invalid = invalid

        startingRow = (row // 3) * 3
        startingColumn = (column // 3) * 3

        for currentRow in range(startingRow, startingRow + 3):
            for currentColumn in range(startingColumn, startingColumn + 3):

                currentCell = self.board[currentRow][currentColumn]

                if currentCell.number == cell.number and row != currentRow and column != currentColumn:
                    cell.invalid = invalid
                    currentCell.invalid = invalid

    def solveSudoku(self):
        self.board = self.getBoard()
        self.solveSudokuHelper(0, 0)

    def solveSudokuHelper(self, row, column):
        lastColumn = len(self.board[row]) - 1
        lastRow = len(self.board) - 1

        currentCell = self.board[row][column]
        cellCenterY = self.cellCenters[row]
        cellCenterX = self.cellCenters[column]

        if currentCell.number != 0:

            if column == lastColumn and row == lastRow:
                currentCell.underConsideration = False
                return True

            if column == lastColumn:
                currentCell.underConsideration = False
                return self.solveSudokuHelper(row + 1, 0)
            else:
                currentCell.underConsideration = False
                return self.solveSudokuHelper(row, column + 1)

        currentCell.underConsideration = True

        for candidateNumber in range(1, 10):
            currentCell.number = candidateNumber
            self.drawBoard()
            time.sleep(0.02)
            if self.isValid(candidateNumber, row, column):

                if column == lastColumn and row == lastRow:
                    currentCell.underConsideration = False
                    return True

                if column == lastColumn:
                    currentCell.underConsideration = False
                    result = self.solveSudokuHelper(row + 1, 0)
                else:
                    currentCell.underConsideration = False
                    result = self.solveSudokuHelper(row, column + 1)

                if result:
                    currentCell.underConsideration = False
                    return True

            currentCell.underConsideration = True
            self.drawBoard()
            time.sleep(0.02)
            currentCell.number = 0

        currentCell.underConsideration = False
        return False

    def isValid(self, number, row, column):
        for idx in range(9):
            if self.board[idx][column].number == number and idx != row:
                return False
            if self.board[row][idx].number == number and idx != column:
                return False

        squareStartRow = (row // 3) * 3
        squareStartColumn = (column // 3) * 3

        for boardRow in range(squareStartRow, squareStartRow + 3):
            for boardColumn in range(squareStartColumn, squareStartColumn + 3):
                if boardRow == row and boardColumn == column:
                    continue

                if self.board[boardRow][boardColumn].number == number:
                    return False

        return True


def main():
    # Create a new Pydoku GUI
    pydoku = PydokuGUI()
    pydoku.drawBoard()

    # Set containing the allowed inputs
    ALLOWED_INPUTS = {pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                      pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9}

    # Run until the user asks to quit
    running = True
    while running:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in ALLOWED_INPUTS:
                    number = int(chr(event.key))
                    pydoku.setNumber(number)
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    pydoku.delete()
                elif event.key == pygame.K_UP:
                    pydoku.moveSelectedCell(-1, 0)
                elif event.key == pygame.K_DOWN:
                    pydoku.moveSelectedCell(1, 0)
                elif event.key == pygame.K_RIGHT:
                    pydoku.moveSelectedCell(0, 1)
                elif event.key == pygame.K_LEFT:
                    pydoku.moveSelectedCell(0, -1)
                elif event.key == pygame.K_SPACE:
                    pydoku.solveSudoku()
                # Draw the actual board
                pydoku.drawBoard()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pydoku.setSelectedCell(pos)
                # Draw the actual board
                pydoku.drawBoard()

            if event.type == pygame.QUIT:
                running = False

    # Done! Time to quit.
    pygame.quit()


main()
