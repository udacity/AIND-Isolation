"""This file contains all the classes you must complete for this project.
You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.
You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
from functools import partial

INFINITY_POSITIVE = float('+inf')
INFINITY_NEGATIVE = float('-inf')
NO_LEGAL_MOVES = (-1, -1)


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

    get_legal_moves = game.get_legal_moves
    moves_player = len(get_legal_moves(player))
    moves_opponent = len(get_legal_moves(game.get_opponent(player)))
    total_squares = game.height * game.width
    filled_squares = total_squares - len(game.get_blank_spaces())

    # Return maximum scores if no moves left by either player
    if player is game.inactive_player and moves_opponent == 0:
        return INFINITY_POSITIVE
    elif player is game.active_player and moves_player == 0:
        return INFINITY_NEGATIVE

    # This evaluation function takes into account the relative number of legal moves left to each player
    # as well as the state of the game
    # If the opponent has more moves left then we get a larger negative number
    # filled_squares magnifies this ratio as the game progresses so stakes are higher
    # In addition the 0.75 vs. 0.25 help with controlling how aggressive the player is
    # This strategy somewhat consistently beats ID_Improved in aggregate
    return -(moves_opponent + 0.75) / (moves_player + 0.25) * filled_squares


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
        self.depths = []

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

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        move = NO_LEGAL_MOVES
        if len(legal_moves) == 0:
            return move

        blank_spaces = len(game.get_blank_spaces())
        board_squares = game.width * game.height
        if blank_spaces == board_squares:
            self.depths.append(0)
            return game.height // 2, game.width // 2

        depth = 1

        search_methods = {
            'minimax': partial(self.minimax, game=game),
            'alphabeta': partial(self.alphabeta, game=game)
        }

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                while True:
                    s, move = search_methods[self.method](depth=depth)
                    if s == INFINITY_POSITIVE:
                        return move
                    depth += 1
            else:
                depth = self.search_depth
                return search_methods[self.method](depth=depth)[1]
        except Timeout:
            # Handle any actions required at timeout, if necessary
            self.depths.append(depth)
            return move

    def _search_body(self, game, depth, maximizing_player, alpha=None, beta=None):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        player = game.active_player if maximizing_player else game.inactive_player

        if depth == 0:
            return self.score(game, player), NO_LEGAL_MOVES

        best_score = INFINITY_NEGATIVE if maximizing_player else INFINITY_POSITIVE
        best_move = NO_LEGAL_MOVES

        for move in game.get_legal_moves(game.active_player):
            forecast_move = game.forecast_move(move)
            if isinstance(alpha, float) and isinstance(beta, float):
                s, _ = self.alphabeta(forecast_move, depth - 1, alpha, beta, not maximizing_player)
            else:
                s, _ = self.minimax(forecast_move, depth - 1, not maximizing_player)
            if maximizing_player:
                if s > best_score:
                    best_score = s
                    best_move = move
                    if alpha is not None:
                        alpha = max(alpha, s)

                if beta is not None and s >= beta:
                    break
            else:
                if s < best_score:
                    best_score = s
                    best_move = move
                    if beta is not None:
                        beta = min(beta, s)

                if alpha is not None and s <= alpha:
                    break

        return best_score, best_move

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
        return self._search_body(game, depth, maximizing_player)

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
        return self._search_body(game, depth, maximizing_player, alpha, beta)
