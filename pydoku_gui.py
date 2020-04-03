# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Create the font that will be used
font = pygame.font.SysFont('Monospace', 32)


class PydokuGUI:

    # colors that are used
    COLOR_BLACK = (0, 0, 0)
    COLOR_GREY = (105, 105, 105)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GREEN = (0, 255, 0)
    COLOR_LIGHT_BLUE = (0, 180, 255)

    WIDTH = 9 * 39 + 6 * 1 + 2 * 3
    cellCenters = [20, 60, 100, 142, 182, 222, 264, 304, 344]

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        pygame.display.set_caption('Pydoku GUI')
        self.selectedCell = None       
        self.board = [
            [(0, True), (0, True), (9, False), (2, False), (1, False), (8,False), (0, True), (0, True), (0, True)],
            [(1, False), (7, False), (0, True), (0, True), (9, False), (6, False), (8, False), (0, True), (0, True)],
            [(0, True), (4, False), (0, True), (0, True), (5, False), (0, True), (0, True), (0, True), (6, False)],
            [(4, False), (5, False), (1, False), (0, True), (6, False), (0, True), (3, False), (7, False), (0, True)],
            [(0, True), (0, True), (0, True), (0, True), (0, True), (5, False), (0, True), (0, True), (9, False)],
            [(9, False), (0, True), (2, False), (3, False), (7, False), (0, True), (5, False), (0, True), (0, True)],
            [(6, False), (0, True), (0, True), (5, False), (0, True), (1, False), (0, True), (0, True), (0, True)],
            [(0, True), (0, True), (0, True), (0, True), (4, False), (9, False), (2, False), (5, False), (7, False)],
            [(0, True), (9, False), (4, False), (8, False), (0, True), (0, True), (0, True), (1, False), (3, False)],
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
                cell = self.board[row][column]
                if cell[0] != 0:
                    color = self.COLOR_GREY if cell[1] else self.COLOR_BLACK
                    self.drawNumber(cell[0],
                                    self.cellCenters[column],
                                    self.cellCenters[row],
                                    color)

    def drawNumber(self, number, centerX, centerY, color):
        text = font.render(str(number),
                           True,
                           color,
                           self.COLOR_WHITE)

        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.center = (centerX, centerY)

        self.screen.blit(text, textRect)

    def drawSelected(self):
        if self.selectedCell is None:
            return

        rowCenter = self.cellCenters[self.selectedCell[0]]
        columnCenter = self.cellCenters[self.selectedCell[1]]

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
        clickedColumn = self.getCellFromCoord(mouseClickPosition[0])
        clickedRow = self.getCellFromCoord(mouseClickPosition[1])

        if clickedRow >= 0 and clickedColumn >= 0:
            self.selectedCell = (clickedRow, clickedColumn)

    def getCellFromCoord(self, coordinate):
        for idx, cellCenter in enumerate(self.cellCenters):
            if cellCenter - 20 < coordinate and coordinate < cellCenter + 20:
                return idx

        return -1

    def setNumber(self, number):
        if self.selectedCell is None:
            return

        cell = self.board[self.selectedCell[0]][self.selectedCell[1]]

        if cell[1]:
            self.board[self.selectedCell[0]][self.selectedCell[1]] = (number, True)

    def delete(self):
        if self.selectedCell is None:
            return

        cell = self.board[self.selectedCell[0]][self.selectedCell[1]]

        if cell[1]:
            self.board[self.selectedCell[0]][self.selectedCell[1]] = (0, True)

    def moveSelectedCell(self, rowMove, columnMove):
        if self.selectedCell is None:
            return

        newRow = self.selectedCell[0] + rowMove
        newColumn = self.selectedCell[1] + columnMove

        if -1 < newRow and newRow < 9 and -1 < newColumn and newColumn < 9:
            self.selectedCell = (newRow, newColumn)


# Create a new Pydoku GUI
pydoku = PydokuGUI()

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
