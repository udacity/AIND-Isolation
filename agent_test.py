"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationAlphaBetaTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.AlphaBetaPlayer()
        self.player2 = game_agent.AlphaBetaPlayer()
        self.game = isolation.Board(self.player1, self.player2, 9, 9)
        self.game._board_state = \
            [0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 1, 1, 1, 0, 0,
             0, 0, 0, 1, 1, 1, 1, 0, 0,
             0, 0, 0, 1, 1, 1, 0, 0, 0,
             0, 0, 0, 1, 1, 1, 0, 0, 0,
             0, 0, 0, 1, 0, 1, 1, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57, 41]

    def test_alphabeta(self):
        ab_move = self.player1.get_move(self.game, lambda: 10)

        pass

if __name__ == '__main__':
    unittest.main()
