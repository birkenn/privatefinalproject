import pygame
from cell import Cell
from sudoku_generator import generate_sudoku

BLACK = (0, 0, 0)
class Board:
    def __init__(self, width, height, screen, difficulty, offset_y=0):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.offset_y = offset_y
        self.removed_cells = 18 if difficulty == "easy" else 28 if difficulty == "medium" else 38
        self.board = generate_sudoku(9, self.removed_cells) # Corrected line
        self.cells = [[Cell(self.board[i][j], i, j, screen) for j in range(9)] for i in range(9)]
        self.selected = None

    def draw(self):
        cell_size = self.width // 9

        # Draw grid lines with offset
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, "BLACK",
                             (0, i * cell_size + self.offset_y),
                             (self.width, i * cell_size + self.offset_y), thickness)
            pygame.draw.line(self.screen, BLACK,
                             (i * cell_size, self.offset_y),
                             (i * cell_size, self.height + self.offset_y), thickness)


        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw(j * cell_size, i * cell_size + self.offset_y, cell_size, cell_size)

    def select(self, row, col):
        if self.selected:
            self.cells[self.selected[0]][self.selected[1]].selected = False
        self.selected = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        y_adjusted = y  # Remove offset before calculation
        if 0 <= x < self.width and 0 <= y_adjusted < self.height:
            row = y_adjusted // (self.height // 9)
            col = x // (self.width // 9)
            return (row, col)
        return None

    def clear(self):
        if self.selected:
            row, col = self.selected
            if self.board[row][col] == 0:
                self.cells[row][col].set_cell_value(0)
                self.cells[row][col].set_sketched_value(None)

    def sketch(self, value):
        if self.selected:
            row, col = self.selected
            if self.board[row][col] == 0:
                self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected and value != 0:
            row, col = self.selected
            if self.board[row][col] == 0:
                self.cells[row][col].set_cell_value(value)
                self.cells[row][col].set_sketched_value(None)

    def reset_to_original(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_cell_value(self.board[i][j])
                self.cells[i][j].set_sketched_value(None)

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def check_board(self):

        for row in range(9):
            nums = set()
            for col in range(9):
                num = self.cells[row][col].value
                if num == 0 or num in nums:
                    return False
                nums.add(num)


        for col in range(9):
            nums = set()
            for row in range(9):
                num = self.cells[row][col].value
                if num == 0 or num in nums:
                    return False
                nums.add(num)


        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                nums = set()
                for i in range(3):
                    for j in range(3):
                        num = self.cells[box_row + i][box_col + j].value
                        if num == 0 or num in nums:
                            return False
                        nums.add(num)
        return True