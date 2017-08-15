"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationMinimaxTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = game_agent.MinimaxPlayer()
        self.game = isolation.Board(self.player1, self.player2, 3, 2)

    def test_first_move(self):
        best_moves = {(0, 0), (2, 0), (0, 1)}
        minimax_move = self.player1.get_move(self.game, lambda: 10)

        print('Best move choices: {}'.format(list(best_moves)))
        print('Your code chose: {}'.format(minimax_move))

        assert minimax_move in best_moves, 'Move choice was not in best moves'

if __name__ == '__main__':
    unittest.main()
