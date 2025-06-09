import random
from dataclasses import dataclass
from typing import List

@dataclass
class Cell:
    mine: bool = False
    revealed: bool = False
    adjacent_mines: int = 0

class Board:
    def __init__(self, rows: int = 9, cols: int = 9, mines: int = 10):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.grid: List[List[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self._place_mines()
        self._calculate_adjacent_counts()

    def _place_mines(self) -> None:
        positions = random.sample(range(self.rows * self.cols), self.mines_count)
        for pos in positions:
            r = pos // self.cols
            c = pos % self.cols
            self.grid[r][c].mine = True

    def _calculate_adjacent_counts(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].mine:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].mine:
                                count += 1
                self.grid[r][c].adjacent_mines = count

    def is_valid(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def reveal(self, r: int, c: int) -> None:
        if not self.is_valid(r, c):
            return
        cell = self.grid[r][c]
        if cell.revealed:
            return
        cell.revealed = True
        if cell.adjacent_mines == 0 and not cell.mine:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if self.is_valid(nr, nc):
                        self.reveal(nr, nc)

    def all_safe_revealed(self) -> bool:
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.mine and not cell.revealed:
                    return False
        return True

    def display(self, reveal_all: bool = False) -> None:
        print('   ' + ' '.join(str(c) for c in range(self.cols)))
        for r in range(self.rows):
            row_display = []
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.revealed or reveal_all:
                    if cell.mine:
                        row_display.append('*')
                    else:
                        row_display.append(str(cell.adjacent_mines) if cell.adjacent_mines > 0 else ' ')
                else:
                    row_display.append('#')
            print(f"{r:2} " + ' '.join(row_display))


def play() -> None:
    board = Board()
    while True:
        board.display()
        try:
            user_input = input("Enter row and column (e.g. '0 1'): ")
            r_str, c_str = user_input.strip().split()
            r, c = int(r_str), int(c_str)
        except ValueError:
            print("Invalid input. Please enter two numbers.")
            continue

        if not board.is_valid(r, c):
            print("Coordinates out of range.")
            continue

        cell = board.grid[r][c]
        if cell.mine:
            print("BOOM! You hit a mine.")
            board.display(reveal_all=True)
            break
        board.reveal(r, c)
        if board.all_safe_revealed():
            print("Congratulations! You cleared the board.")
            board.display(reveal_all=True)
            break

if __name__ == '__main__':
    play()
