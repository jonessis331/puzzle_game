import unittest
from puzzle.dominoes_game import DominoesGame, create_dominoes_game

class TestDominoesGame(unittest.TestCase):
    def test_dominoes_game_initialization(self):
        b = [[False, False], [False, False]]
        g = DominoesGame(b)
        self.assertEqual(g.get_board(), [[False, False], [False, False]])

        b = [[True, False], [True, False]]
        g = DominoesGame(b)
        self.assertEqual(g.get_board(), [[True, False], [True, False]])

        g = create_dominoes_game(2, 2)
        self.assertEqual(g.get_board(), [[False, False], [False, False]])

    def test_dominoes_game_reset(self):
        b = [[True, False], [True, False]]
        g = DominoesGame(b)
        g.reset()
        self.assertEqual(g.get_board(), [[False, False], [False, False]])

    def test_dominoes_game_legal_moves(self):
        g = create_dominoes_game(3, 3)
        self.assertEqual(len(list(g.legal_moves(True))), 6)
        self.assertEqual(len(list(g.legal_moves(False))), 6)

        b = [[True, False], [True, False]]
        g = DominoesGame(b)
        self.assertEqual(list(g.legal_moves(True)), [(0, 1)])
        self.assertEqual(list(g.legal_moves(False)), [])

    def test_dominoes_game_perform_move(self):
        g = create_dominoes_game(3, 3)
        g.perform_move(0, 1, True)
        self.assertEqual(g.get_board(), [[False, True, False], [False, True, False], [False, False, False]])

        g = create_dominoes_game(3, 3)
        g.perform_move(1, 0, False)
        self.assertEqual(g.get_board(), [[False, False, False], [True, True, False], [False, False, False]])

    def test_dominoes_game_over(self):
        b = [[False, False], [False, False]]
        g = DominoesGame(b)
        self.assertFalse(g.game_over(True))
        self.assertFalse(g.game_over(False))

        b = [[True, False], [True, False]]
        g = DominoesGame(b)
        self.assertFalse(g.game_over(True))
        self.assertTrue(g.game_over(False))

    def test_dominoes_game_copy(self):
        g = create_dominoes_game(4, 4)
        g2 = g.copy()
        self.assertEqual(g.get_board(), g2.get_board())

        g.perform_move(0, 0, True)
        self.assertNotEqual(g.get_board(), g2.get_board())

if __name__ == '__main__':
    unittest.main()