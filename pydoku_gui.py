# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Create the font that will be used
font = pygame.font.SysFont('Monospace', 32)


class PydokuGUI:

    # colors that are used
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GREEN = (0, 255, 0)
    COLOR_LIGHT_BLUE = (0, 180, 255)

    WIDTH = 9 * 39 + 6 * 1 + 2 * 3
    cellCenters = [20, 60, 100, 142, 182, 222, 264, 304, 344]

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        pygame.display.set_caption('Pydoku GUI')
        self.selectedCellRowAndColumn = None
        self.board = [
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

    def drawBoard(self):
        self.drawLines()
        self.drawNumbers()
        self.drawSelected()

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
                if self.board[row][column] != 0:
                    self.drawNumber(self.board[row][column],
                                    self.cellCenters[column],
                                    self.cellCenters[row])

    def drawNumber(self, number, centerX, centerY):
        text = font.render(str(number),
                           True,
                           self.COLOR_BLACK,
                           self.COLOR_WHITE)

        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.center = (centerX, centerY)

        self.screen.blit(text, textRect)

    def drawSelected(self):
        if self.selectedCell is None:
            return

        columnCenter = self.cellCenters[self.selectedCellRowAndColumn[0]]
        rowCenter = self.cellCenters[self.selectedCellRowAndColumn[1]]

        self.markSquare(columnCenter, rowCenter, self.COLOR_LIGHT_BLUE)

    def markSquare(self, columnCenter, rowCenter, color):
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
        clickedRow = self.getCellFromCoord(mouseClickPosition[1])
        clickedColumn = self.getCellFromCoord(mouseClickPosition[0])

        if clickedRow >= 0 and clickedColumn >= 0:
            self.selectedCellRowAndColumn = (clickedColumn, clickedRow)

    def getCellFromCoord(self, coordinate):
        for idx, cellCenter in enumerate(self.cellCenters):
            if cellCenter - 20 < coordinate and coordinate < cellCenter + 20:
                return idx

        return -1


# Create a new Pydoku GUI
pydoku = PydokuGUI()

# Run until the user asks to quit
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            pydoku.setSelectedCell(pos)

        if event.type == pygame.QUIT:
            running = False

    # Draw the actual board
    pydoku.drawBoard()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
