from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from math import isqrt
from typing import Iterable, Optional


Board = list[list[int]]


class RecursiveSolver(ABC):
    """Generic recursive backtracking solver."""

    def solve(self) -> Optional[Board]:
        if self.is_complete():
            return self.current_state()

        for _ in self.next_states():
            result = self.solve()
            if result is not None:
                return result
            self.undo_last_move()
        return None

    @abstractmethod
    def is_complete(self) -> bool: ...

    @abstractmethod
    def current_state(self) -> Board: ...

    @abstractmethod
    def next_states(self) -> Iterable[None]: ...

    @abstractmethod
    def undo_last_move(self) -> None: ...


class SudokuSolver(RecursiveSolver):
    def __init__(self, board: Board):
        self.board = deepcopy(board)
        self._size = len(self.board)
        self._box_size = isqrt(self._size)
        self._move_stack: list[tuple[int, int]] = []
        self._validate_initial_board()

    def is_complete(self) -> bool:
        return self._find_empty() is None

    def current_state(self) -> Board:
        return deepcopy(self.board)

    def next_states(self) -> Iterable[None]:
        empty = self._find_empty()
        if empty is None:
            return

        row, col = empty
        for num in range(1, self._size + 1):
            if self._is_valid(row, col, num):
                self.board[row][col] = num
                self._move_stack.append((row, col))
                yield

    def undo_last_move(self) -> None:
        row, col = self._move_stack.pop()
        self.board[row][col] = 0

    def _find_empty(self) -> Optional[tuple[int, int]]:
        # MRV heuristic: pick the empty cell with the fewest legal candidates.
        best_cell: Optional[tuple[int, int]] = None
        best_count: Optional[int] = None

        for r in range(self._size):
            for c in range(self._size):
                if self.board[r][c] != 0:
                    continue

                count = self._count_candidates(r, c)
                if count == 0:
                    return r, c
                if best_count is None or count < best_count:
                    best_cell = (r, c)
                    best_count = count
                    if count == 1:
                        return best_cell
        return best_cell

    def _count_candidates(self, row: int, col: int) -> int:
        return sum(
            1 for num in range(1, self._size + 1) if self._is_valid(row, col, num)
        )

    def _is_valid(self, row: int, col: int, num: int) -> bool:
        if num in self.board[row]:
            return False
        if any(self.board[r][col] == num for r in range(self._size)):
            return False

        start_row = (row // self._box_size) * self._box_size
        start_col = (col // self._box_size) * self._box_size
        for r in range(start_row, start_row + self._box_size):
            for c in range(start_col, start_col + self._box_size):
                if self.board[r][c] == num:
                    return False
        return True

    def _validate_initial_board(self) -> None:
        if self._size == 0:
            raise ValueError("Board must not be empty.")
        if any(len(row) != self._size for row in self.board):
            raise ValueError("Board must be square.")
        if self._box_size * self._box_size != self._size:
            raise ValueError("Board size must have an integer square root.")

        for r in range(self._size):
            for c in range(self._size):
                value = self.board[r][c]
                if value < 0 or value > self._size:
                    raise ValueError("Board values must be in range 0..size.")

                if value == 0:
                    continue

                self.board[r][c] = 0
                if not self._is_valid(r, c, value):
                    self.board[r][c] = value
                    raise ValueError("Initial board violates Sudoku constraints.")
                self.board[r][c] = value


def _format_board(board: Board) -> str:
    return "\n".join(" ".join(str(cell) for cell in row) for row in board)


if __name__ == "__main__":
    # convert this to a 2D list of ints
    puzzle = [
        [0, 0, 5, 0, 9, 0, 6, 0, 0],
        [0, 0, 4, 6, 3, 5, 1, 0, 0],
        [0, 6, 0, 0, 0, 7, 0, 0, 8],
        [3, 8, 0, 0, 0, 9, 0, 1, 0],
        [0, 1, 0, 8, 0, 6, 0, 2, 0],
        [0, 9, 0, 7, 0, 0, 0, 6, 5],
        [2, 0, 0, 9, 0, 0, 0, 5, 0],
        [0, 0, 1, 3, 6, 4, 2, 0, 0],
        [0, 0, 8, 0, 7, 0, 3, 0, 0]]
    
    solver = SudokuSolver(puzzle)
    solution = solver.solve()
    if solution is None:
        print("No solution found.")
    else:
        print("Solved 9x9 Sudoku:\n")
        print(_format_board(solution))
