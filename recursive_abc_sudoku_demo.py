from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
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


class Sudoku4x4Solver(RecursiveSolver):
    def __init__(self, board: Board):
        self.board = deepcopy(board)
        self._move_stack: list[tuple[int, int]] = []

    def is_complete(self) -> bool:
        return self._find_empty() is None

    def current_state(self) -> Board:
        return deepcopy(self.board)

    def next_states(self) -> Iterable[None]:
        empty = self._find_empty()
        if empty is None:
            return

        row, col = empty
        for num in range(1, 5):
            if self._is_valid(row, col, num):
                self.board[row][col] = num
                self._move_stack.append((row, col))
                yield

    def undo_last_move(self) -> None:
        row, col = self._move_stack.pop()
        self.board[row][col] = 0

    def _find_empty(self) -> Optional[tuple[int, int]]:
        for r in range(4):
            for c in range(4):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def _is_valid(self, row: int, col: int, num: int) -> bool:
        if num in self.board[row]:
            return False
        if any(self.board[r][col] == num for r in range(4)):
            return False

        start_row = (row // 2) * 2
        start_col = (col // 2) * 2
        for r in range(start_row, start_row + 2):
            for c in range(start_col, start_col + 2):
                if self.board[r][c] == num:
                    return False
        return True


def _format_board(board: Board) -> str:
    return "\n".join(" ".join(str(cell) for cell in row) for row in board)


if __name__ == "__main__":
    puzzle = [
        [1, 0, 0, 4],
        [0, 4, 0, 2],
        [2, 0, 4, 0],
        [4, 3, 0, 1],
    ]
    solver = Sudoku4x4Solver(puzzle)
    solution = solver.solve()
    if solution is None:
        print("No solution found.")
    else:
        print("Solved 4x4 Sudoku:\n")
        print(_format_board(solution))
