import random

class SudokuGenerator:
    def __init__(self, row_length=9, removed_cells=30):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]
        self.fill_values()
        self.solution = [row[:] for row in self.board]
        self.remove_cells()

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
               (self.valid_in_col(col, num)) and
               (self.valid_in_box(row - row % 3, col - col % 3, num)))

    def fill_box(self, row_start, col_start):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = nums.pop()

    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self, row=0, col=3):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length:
            return True
        if row < 3:
            if col < 3:
                col = 3
        elif row < 6:
            if col == int(row / 3) * 3:
                col += 3
        else:
            if col == 6:
                return True
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        cells_removed = 0
        cells = [(row, col) for row in range(self.row_length) for col in range(self.row_length)]
        random.shuffle(cells)

        while cells_removed < self.removed_cells:
            row, col = cells.pop()
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_removed += 1


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    return sudoku.get_board()