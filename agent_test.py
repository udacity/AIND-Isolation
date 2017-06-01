"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import timeit
import isolation
import game_agent

from importlib import reload
from sample_players import open_move_score

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)


from game_agent import MinimaxPlayer, AlphaBetaPlayer, possible_moves_count, custom_score_3, custom_score, custom_score_2
from sample_players import GreedyPlayer, improved_score

def test1():
    player1 = AlphaBetaPlayer(search_depth=20, name='p1', score_fn=open_move_score)
    player2 = GreedyPlayer()
    game = isolation.Board(player1, player2, height=9, width=9)
    print(game.play(time_limit=500))

def test2():
    player1 = MinimaxPlayer(search_depth=1)
    player2 = MinimaxPlayer(search_depth=0)
    game = isolation.Board(player1, player2, height=4, width=4)
    game.apply_move((2, 0))
    game.apply_move((0, 1))
    game.apply_move((1, 2))
    game.apply_move((2, 2))
    game.apply_move((3, 1))
    print(game.to_string())
    print(player2.score(game, player1))

def test3():
    player1 = MinimaxPlayer(search_depth=1)
    player2 = MinimaxPlayer(search_depth=0)
    game = isolation.Board(player1, player2, height=5, width=5)
    game.apply_move((3,2))
    game.apply_move((4,4))

    print(game.to_string())
    print(game.get_player_location(game.active_player))
    print(possible_moves_count(*game.get_player_location(game.active_player), game))
    print(possible_moves_count(*game.get_player_location(game.inactive_player), game))

def test4():
    player1 = MinimaxPlayer(search_depth=1)
    player2 = MinimaxPlayer(search_depth=0)
    game = isolation.Board(player1, player2, height=5, width=5)
    game.apply_move((0,3))
    game.apply_move((4,4))
    print(game.to_string())

def test5():
    player1 = AlphaBetaPlayer(search_depth=100, score_fn=open_move_score)
    player2 = AlphaBetaPlayer(search_depth=100, score_fn=custom_score_3)
    game = isolation.Board(player1, player2, height=7, width=7)
    game._board_state =[0, 0, 0, 'o13', 0, 0, 0, 'o17', 0, 0, 'x17', ' O ', ' X ', 'o09', 0, 'x19', 'o15', 'x27', 'o11',
                        'x03', 'o27', 0, 'o19', 'x11', 'x01', 'x15', 'o07', 0, 'x21', 0, 'x25', 'o05', 'x05', 'o25',
                        0, 0, 'x09', 'o21', 'x13', 0, 'o03', 0, 0, 'x23', 0, 'x07', 'o23', 0, 0, 1, 11, 12]
    game._active_player, game._inactive_player = game._inactive_player, game._active_player
    print(game.to_string())
    print(game.active_player==game._player_2)
    game_copy = game.copy()
    time_millis = lambda: 1000 * timeit.default_timer()
    move_start = time_millis()
    time_left = lambda: 150000 - (time_millis() - move_start)
    curr_move = game._active_player.get_move(game_copy, time_left)
    return curr_move

def test6():
    player1 = AlphaBetaPlayer(search_depth=1, score_fn=custom_score)
    player2 = AlphaBetaPlayer(search_depth=1, score_fn=custom_score_3)
    game = isolation.Board(player1, player2, height=5, width=5)
    game.apply_move((0, 3))
    print(game.to_string())
    game.apply_move((4, 4))
    print(game.to_string())
    game.apply_move((3, 2))
    print(game.to_string())
    game.apply_move((1, 1))
    game.apply_move((2, 0))
    game.apply_move((3, 0))
    game.apply_move((1, 2))

    print(game.to_string())
    print(custom_score(game, game.active_player))
    print(custom_score(game, game.inactive_player))
    print(custom_score_2(game, game.active_player))
    print(custom_score_2(game, game.inactive_player))
    print(custom_score_3(game, game.active_player))
    print(custom_score_3(game, game.inactive_player))
    print(improved_score(game, game.active_player))
    print(improved_score(game, game.inactive_player))



print(test6())

