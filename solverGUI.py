
# todo
# [ ] what the hell is happening with cell (1, 4)
# [ ] fix bugs like:
#       - [ ] what the hell is happening with the cell (1, 4)
#       - [ ] optimization ?!
#       - [ ] structure the sboard and the grid!
#       - [ ] find whether there is a bug in a possible() function
# [ ] tweak the solve() function to work with user inputs, or find if tweaks are needed
# [ ] write some cleaner code for god's sake!!!

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
    [5, 0, 1, 0, 6, 0, 0, 2, 4],
    [0, 6, 0, 4, 0, 0, 0, 7, 3],
    [0, 7, 0, 0, 0, 0, 1, 0, 5],
    [0, 0, 0, 0, 0, 7, 2, 0, 8],
    [8, 0, 2, 3, 9, 0, 5, 4, 7],
    [3, 0, 0, 2, 8, 4, 0, 9, 0],
    [0, 0, 5, 6, 0, 0, 4, 0, 0],
    [0, 2, 0, 0, 0, 0, 3, 1, 0],
    [9, 4, 6, 0, 0, 1, 7, 0, 0]
]

# -----------------------------------------------------Cell class----------------------------------------------------------- #


class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0
        self.mutable = True

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
                self.grid[i][j].mutable = (self.grid[i][j].value == 0)

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


def draw(b, s):
    b.draw()
    draw_grid()
    if s != None:
        rect(display, (white), (s.x, s.y, rez, rez), 3)
    pygame.display.flip()

# ---------------------------------------------------solver functions--------------------------------------------------------- #


def possible(board, y, x, n):
    for i in range(len(board)):
        if board[y][i].value == n:
            print(f'error for {n} at {y, x}')
            return False
    for j in range(len(board[0])):
        if board[j][x].value == n:
            print(f'error for {n} at {y, x}')
            return False

    xoff = (x // 3) * 3
    yoff = (y // 3) * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if board[yoff + i][xoff + j].value == n:
                print(
                    f'error for {n} due to cell mismatch at ({yoff + i},{xoff + j})')
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
            draw(board, None)
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
    selected = None

    while run:
        # setting up the [ selected_pos ] variable.
        if selected != None:
            selected_pos = selected.x // rez, selected.y // rez

        # ------------------------Event Handler----------------------------- #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                (i, j) = pygame.mouse.get_pos()
                i = i // rez
                j = j // rez
                selected = sboard.grid[i][j]

            if event.type == pygame.KEYDOWN:
                # setting key = event.key for convenience
                key = event.key

                if key == pygame.K_SPACE:
                    solve(sboard)

                if key == pygame.K_q:
                    run = False
                    quit()

                if key == pygame.K_0:
                    selected.value = 0

                elif key == pygame.K_1:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 1):
                        selected.value = 1

                elif key == pygame.K_2:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 2):
                        selected.value = 2

                elif key == pygame.K_3:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 3):
                        selected.value = 3

                elif key == pygame.K_4:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 4):
                        selected.value = 4

                elif key == pygame.K_5:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 5):
                        selected.value = 5

                elif key == pygame.K_6:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 6):
                        selected.value = 6

                elif key == pygame.K_7:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 7):
                        selected.value = 7

                elif key == pygame.K_8:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 8):
                        selected.value = 8

                elif key == pygame.K_9:
                    if possible(sboard.grid, selected_pos[1], selected_pos[0], 9):
                        selected.value = 9

        # ------------------------Event Handler----------------------------- #
        draw(sboard, selected)

# -------------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    main()


# else:
#     print(
#         f'error at cell {selected_pos} for value 7')
