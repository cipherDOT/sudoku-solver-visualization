
# -------------------------------------------------------imports------------------------------------------------------------ #

import pygame
from pygame.draw import line, rect
pygame.font.init()

# ---------------------------------------------------global variables------------------------------------------------------ #

width = 720
height = 720
rez = 80
white = (255, 255, 255)
black = (0, 0, 0)

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sudoku solver')
font = pygame.font.SysFont("comicsans", 25)

board = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0]
]

# -----------------------------------------------------Cell class----------------------------------------------------------- #


class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0
        self.solved = False

    def draw(self):
        rect(display, (black), (self.x, self.y, rez, rez))
        if self.value > 0:
            value_text = font.render(str(self.value), 1, (255, 255, 255))
            display.blit(value_text, (self.x + 34, self.y + 34))

# -----------------------------------------------------Board class----------------------------------------------------------- #


class Board(object):
    def __init__(self):
        self.grid = []
        for i in range(9):
            self.grid.append([])
            for j in range(9):
                self.grid[i].append(Cell(i * rez, j * rez))
                self.grid[i][j].value = board[j][i]

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def solved(self):
        for row in self.grid:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

# ----------------------------------------------------draw functions--------------------------------------------------------- #


def draw_grid():
    for i in range(rez, width, rez):
        thick = 1
        if i % 3 == 0:
            thick = 3
        line(display, (white), (i, 0), (i, height), thick)
    for j in range(rez, height, rez):
        thick = 1
        if j % 3 == 0:
            thick = 3
        line(display, (white), (0, j), (width, j), thick)


def draw(b):
    b.draw()
    draw_grid()
    pygame.display.flip()

# ---------------------------------------------------solver functions--------------------------------------------------------- #


def possible(board, y, x, n):
    for i in range(len(board)):
        if board[y][i].value == n:
            return False
    for j in range(len(board[0])):
        if board[j][x].value == n:
            return False

    xoff = (x // 3) * 3
    yoff = (y // 3) * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if board[yoff + i][xoff + j].value == n:
                return False

    return True


def print_matrix(m):
    if m == None or m == []:
        print('No solution')
        return
    line = '----------------------'
    cols = len(m)
    rows = len(m[0])

    for i in range(rows):
        if i % 3 == 0:
            print(line)

        row_to_print = ""
        for j in range(cols):
            if j % 3 == 0:
                row_to_print += '|'
            value = str(m[j][i].value) if m[j][i].value > 0 else ' '
            row_to_print += value + " "
        row_to_print += '|'
        print(row_to_print)
    print(line)

# ------------------------------------------------Backtracking algorithm----------------------------------------------------- #


def solve(board):
    if board.solved():
        print_matrix(board.grid)
        quit()
    for y in range(9):
        for x in range(9):
            draw(board)
            if board.grid[y][x].value == 0:
                for n in range(1, 10):
                    if possible(board.grid, y, x, n):
                        board.grid[y][x].value = n
                        solve(board)
                        board.grid[y][x].value = 0
                return


# ----------------------------------------------------main function------------------------------------------------------------ #

def main():
    run = True
    sboard = Board()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solve(sboard)

                if event.key == pygame.K_q:
                    run = False
                    quit()

        draw(sboard)

# -------------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    main()
