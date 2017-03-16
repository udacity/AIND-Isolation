"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random, sys
from utils import get_distance

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return diverge(game, player)

# strategies
# diverge
# converge constrict the opposition
# alternate diverge and converge based on number of spaces
# reach a position with access to more blank spaces on the board


def diverge(game, player):
    """
      Checks for moves that have the least common moves with the opposing player
      appropriate for opening move
    :param game:
    :param player:
    :return: Float containing heuristic score
    """

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    return float(len(set(own_moves).difference(set(opp_moves))))


def converge(game, player):
    """
      Checks for moves that have the least common moves with the opposing player
      appropriate for opening move
    :param game:
    :param player:
    :return: Float containing heuristic score
    """

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    return float(len(set(own_moves).intersection(set(opp_moves))))


def alternate(game, player):
    blank_spaces = len(game.get_blank_spaces())
    total_spaces = game.height * game.width
    if blank_spaces > 5:
        return diverge(game, player)
    else:
        return converge(game, player)


def weighted_avg(game, player):
    board_values = {}
    blank_spaces = game.get_blank_spaces()
    moves = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
    for blank_space in blank_spaces:
        board_values[blank_space] = len([position for position in [(blank_space[0]-x, blank_space[1]-y)
                                                                   for x,y in moves] if position in blank_spaces])
    own_score = 0
    opp_score = 0
    max_distance = 72**0.5
    blank_space_count = len(blank_spaces)
    for m in game.get_legal_moves(player):
        for position, value in board_values.items():
            own_score += (max_distance - get_distance(m, position)) * value

    for m in game.get_legal_moves(game.get_opponent(player)):
        for position, value in board_values.items():
            opp_score += (max_distance - get_distance(m, position)) * value

    return (own_score-opp_score)/blank_space_count


def future_moves(game, player):

    blank_spaces = game.get_blank_spaces()
    directions = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
    own_sum = sum([len([p for p in [(m[0]-x, m[1]-y) for x, y in directions] if p in blank_spaces])
                   for m in game.get_legal_moves(player)])
    opp_sum = sum([len([p for p in [(m[0]-x, m[1]-y) for x, y in directions] if p in blank_spaces])
                   for m in game.get_legal_moves(game.get_opponent(player))])
    return own_sum-opp_sum


def knights_tour(game, player):
    """
    Using Warnsdorf's rule for determining the Knight's tour path. This requires finding the path
    with the least possible moves emanating from it (restricting initial movement to the sides)
    and then using the space in the center to move across the board
    :param game:
    :param player:
    :return:
    """

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    move_count = len(set(own_moves).difference(opp_moves))
    # each node should have aleast 2 moves so that the player is able to visit the node and exit it
    if move_count > 1:
        # chose an arbitrary number larger than max possible moves which is 8
        # max distance is between two points (0,0) and (6,6) is 8.48.
        # we choose a factor of 0.1 so as to keep the product below 1 in effect serving to break ties between
        # same move count
        return 10 - len(own_moves) + get_distance(game.get_player_location(player),
                                                  game.get_player_location(game.get_opponent(player)))
    else:
        return 0


def knights_tour_improved(game, player):
    """
    Improved version of the Knight's tour where the player begins with occupying all squares that have
    the least possible moves (greater than 1) and then based on the state of the game switches to occupying
    squares that have max possible moves

    :param game: Board
    :param player:
    :return: Heuristic value based on board configuration and current player and opposition position
    """
    own_moves = game.get_legal_moves(player)
    blank_spaces = game.get_blank_spaces()
    blank_space_count = len(blank_spaces)
    knight_tour_mode = True
    # The value of heuristic function is inversely proportional to the depth
    if knight_tour_mode and blank_space_count < 32:
        #if average_board_score(game) < 1.7:
        knight_tour_mode = False

    # Identifying squares with max possible moves that are not in contention with the opposing player

    # BLOCKING MOVE also need to consider the case where the current forecasted move is in the path of the opponent
    # while the second possible move is not and also follows the previous move

    if knight_tour_mode: #blank_space_count > 32:
        return knights_tour(game, player)
    else:
        #if len(own_moves) > 1:
        #return len(own_moves) + blocking_move_score(game, player)
        #else:
        #return diverge(game, player) + get_max_depth(game.get_player_location(player), blank_spaces)/1000000
        #return diverge(game, player)
        return len(own_moves) + get_max_depth(game.get_player_location(player), blank_spaces)/1000000


def average_board_score(game):
    """

    :param game:
    :return:
    """
    directions = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
    blank_spaces = game.get_blank_spaces()
    result = sum([len([(x-p, y-q) for p, q in directions if x-p >= 0 and y-q >= 0 and (x-p, y-q) in blank_spaces])
                  for x, y in blank_spaces])/len(blank_spaces)
    return result


def blocking_move_score(game, player):
    """

    :param game:
    :param player:
    :return:
    """
    opponent = game.get_opponent(player)
    directions = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
    own_position = game.get_player_location(player)
    opp_position = game.get_player_location(opponent)
    own_move_count = len(game.get_legal_moves(player))
    opp_all_moves = [(opp_position[0]-x, opp_position[1]-y) for x, y in directions
                 if opp_position[0]-x > 0 and opp_position[1]-y > 0]
    opp_moves = game.get_legal_moves(opponent)
    if opp_moves and own_position in opp_all_moves:
        max_opp_move_count = max([len(game.forecast_move(m).get_legal_moves(opponent))
                                  for m in opp_moves])
        if max_opp_move_count < own_move_count:
            return 1
    return 0


def get_max_depth(position, blank_spaces, depth=0):
    directions = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
    x, y = position
    moves = [(x - p, y - q) for p, q in directions
             if x-p >= 0 and y-q >= 0 and (x-p, y-q) in blank_spaces]
    if moves:
        updated_blank_spaces = [blank_space for blank_space in blank_spaces if blank_space != position]
        return sum([get_max_depth(move, updated_blank_spaces, depth+1) for move in moves])
    else:
        return depth



class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        if self.time_left() == 99:
            score, move = self.minimax(game, 1)
            return move

        if not legal_moves:
            return(-1, -1)
        move = None
        try:
            depth = 1
            while 1:
                if self.time_left() < self.TIMER_THRESHOLD+15.:
                    break
                if self.method == "minimax":
                    score, m = self.minimax(game, depth)
                    if m is not None:
                        move = m
                    else:
                        break

                else:
                    score, m = self.alphabeta(game, depth)
                    if m is not None:
                        move = m
                    else:
                        break
                depth += 1
        except Timeout:
            # Handle any actions required at timeout, if necessary
            #if move is None:
            if move is None:
                score, move = self.minimax(game, 1)

        if move in legal_moves:
            return move
        else:
            return legal_moves[0]



    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD+30. and depth > 1:
            raise Timeout()

        possible_moves = game.get_legal_moves()
        v = -1. if maximizing_player else float("inf")
        best_move = None

        if possible_moves:
            for move in possible_moves:
                new_game = game.forecast_move(move)
                move_value = None
                if maximizing_player:
                    if depth == 1 or self.time_left() < self.TIMER_THRESHOLD+30.:
                        move_value = self.score(new_game, new_game.inactive_player)
                    else:
                        move_value, temp = self.minimax(new_game, depth-1, False)
                    if move_value > v:
                        v = move_value
                        best_move = move
                else:
                    if depth == 1 or self.time_left() < self.TIMER_THRESHOLD+30.:
                        move_value = self.score(new_game, new_game.active_player)
                    else:
                        move_value, temp = self.minimax(new_game, depth-1, True)
                    if move_value < v:
                        v = move_value
                        best_move = move
            return v, best_move
        else:
            return game.utility(game.active_player), (-1, -1)


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD+30. and depth > 1:
            raise Timeout()

        possible_moves = game.get_legal_moves()
        v = -1. if maximizing_player else float("inf")
        best_move = None
        if possible_moves:
            for move in possible_moves:
                move_value = None
                new_game = game.forecast_move(move)
                if maximizing_player:
                    if depth == 1 or self.time_left() < self.TIMER_THRESHOLD+30.:
                        move_value = self.score(new_game, new_game.inactive_player)
                    else:
                        move_value, temp = self.alphabeta(new_game, depth-1, alpha, beta, False)
                    if move_value > v:
                        v = move_value
                        best_move = move
                        if v >= beta:
                            return v, move
                        alpha = max([alpha, v])
                else:
                    if depth == 1 or self.time_left() < self.TIMER_THRESHOLD+30.:
                        move_value = self.score(new_game, new_game.active_player)
                    else:
                        move_value, temp = self.alphabeta(new_game, depth-1, alpha, beta, True)
                    if move_value < v:
                        v = move_value
                        best_move = move
                        if v <= alpha:
                            return v, move
                        beta = min([beta, v])
            return v, best_move
        else:
            return game.utility(game.active_player), (-1, -1)
