import unittest
from puzzle.tile_puzzle import TilePuzzle, create_tile_puzzle

class TestTilePuzzle(unittest.TestCase):
    def test_tile_puzzle_get_board(self):
        p = TilePuzzle([[1, 2], [3, 0]])
        self.assertEqual(p.get_board(), [[1, 2], [3, 0]])

        p = TilePuzzle([[0, 1], [3, 2]])
        self.assertEqual(p.get_board(), [[0, 1], [3, 2]])

        p = create_tile_puzzle(3, 3)
        self.assertEqual(p.get_board(), [[1, 2, 3], [4, 5, 6], [7, 8, 0]])

        p = create_tile_puzzle(2, 4)
        self.assertEqual(p.get_board(), [[1, 2, 3, 4], [5, 6, 7, 0]])

    def test_tile_puzzle_perform_move(self):
        p = create_tile_puzzle(3, 3)
        self.assertTrue(p.perform_move("up"))
        self.assertEqual(p.get_board(), [[1, 2, 3], [4, 5, 0], [7, 8, 6]])

        p = create_tile_puzzle(3, 3)
        self.assertFalse(p.perform_move("down"))
        self.assertEqual(p.get_board(), [[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    def test_tile_puzzle_is_solved(self):
        p = TilePuzzle([[1, 2], [3, 0]])
        self.assertTrue(p.is_solved())

        p = TilePuzzle([[0, 1], [3, 2]])
        self.assertFalse(p.is_solved())

    def test_tile_puzzle_copy(self):
        p = create_tile_puzzle(3, 3)
        p2 = p.copy()
        self.assertEqual(p.get_board(), p2.get_board())

        p.perform_move("left")
        self.assertNotEqual(p.get_board(), p2.get_board())

    def test_tile_puzzle_successors(self):
        p = create_tile_puzzle(3, 3)
        successors = list(p.successors())
        self.assertIn("up", [move for move, _ in successors])
        self.assertIn("left", [move for move, _ in successors])

        b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        p = TilePuzzle(b)
        successors = list(p.successors())
        expected_moves = ["up", "down", "left", "right"]
        self.assertEqual(sorted([move for move, _ in successors]), sorted(expected_moves))

    def test_tile_puzzle_find_solutions_iddfs(self):
        b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
        p = TilePuzzle(b)
        solutions = p.find_solutions_iddfs()
        self.assertEqual(next(solutions), ['up', 'right', 'right', 'down', 'down'])

        b = [[1, 2, 3], [4, 0, 8], [7, 6, 5]]
        p = TilePuzzle(b)
        solutions = list(p.find_solutions_iddfs())
        self.assertIn(['down', 'right', 'up', 'left', 'down', 'right'], solutions)
        self.assertIn(['right', 'down', 'left', 'up', 'right', 'down'], solutions)

    def test_tile_puzzle_find_solution_a_star(self):
        b = [[4, 1, 2], [0, 5, 3], [7, 8, 6]]
        p = TilePuzzle(b)
        self.assertEqual(p.find_solution_a_star(), ['up', 'right', 'right', 'down', 'down'])

        b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        p = TilePuzzle(b)
        self.assertTrue(len(p.find_solution_a_star()) > 0)

if __name__ == '__main__':
    unittest.main()