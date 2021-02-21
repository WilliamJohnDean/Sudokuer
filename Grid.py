import pygame, random, json
from Solvers import Backtracker, DLXsudoku
solvers = {
    'Backtrack': Backtracker,
    'DLX': DLXsudoku,
    # Placeholder for the linear programming and/or graph 9-colouring algorithms
}
class Grid:
    def __init__(self, rows, cols, width, height, win, solverstr: str, animate: bool):
        with open('games.json') as file:
            game = json.load(file)
            self.board = random.choice(game['board'][str(rows)])
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height, rows) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.win = win
        self.gap = round(self.width / self.rows)
        self.gamesize = self.rows # Provided for clarity
        self.solver = solvers[solverstr](self)
        self.animate = animate
 
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        from numpy import sqrt
        boxsize = int(sqrt(self.gamesize))

        for i in range(self.rows+1):
            if i % boxsize == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i * self.gap), (self.width, i * self.gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * self.gap, 0), (i * self.gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

class Cube:
    def __init__(self, value, row, col, width, height, gamesize):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.gap = round(self.width / gamesize)

    def draw(self, win):
        fnt = pygame.font.SysFont("monospace", 18)
        x = self.col * self.gap
        y = self.row * self.gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x + 5, y + 5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (self.gap / 2 - text.get_width() / 2), y + (self.gap / 2 - text.get_height() / 2)))

    def draw_change(self, win, g = True):
        fnt = pygame.font.SysFont("monospace", 18)
        x = self.col * self.gap
        y = self.row * self.gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, self.gap, self.gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (self.gap / 2 - text.get_width() / 2), y + (self.gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, self.gap, self.gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, self.gap, self.gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # row, col

    return None


def valid(bo, num, pos, gamesize):
    from numpy import sqrt
    boxsize = int(sqrt(gamesize))
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // boxsize
    box_y = pos[0] // boxsize

    for i in range(box_y * boxsize, box_y * (boxsize + 1)):
        for j in range(box_x * boxsize, box_x * (boxsize + 1)):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True
