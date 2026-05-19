import unittest

from recursive_abc_sudoku_demo import Sudoku4x4Solver


class Sudoku4x4SolverTests(unittest.TestCase):
    def test_solves_expected_puzzle(self):
        puzzle = [
            [1, 0, 0, 4],
            [0, 4, 0, 2],
            [2, 0, 4, 0],
            [4, 3, 0, 1],
        ]
        expected = [
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            [2, 1, 4, 3],
            [4, 3, 2, 1],
        ]

        solution = Sudoku4x4Solver(puzzle).solve()

        self.assertEqual(solution, expected)

    def test_returns_none_for_invalid_puzzle(self):
        invalid_puzzle = [
            [1, 1, 0, 4],
            [0, 4, 0, 2],
            [2, 0, 4, 0],
            [4, 3, 0, 1],
        ]

        solution = Sudoku4x4Solver(invalid_puzzle).solve()

        self.assertIsNone(solution)


if __name__ == "__main__":
    unittest.main()
