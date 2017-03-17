"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import math

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


def diverge(game, player):
    """
    Checks for squares with max moves giving preferences those which have
    least common moves with the opposing player.

    :param game: `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: Float
        containing move score determined by the heuristic
    """

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    return float(len(set(own_moves).difference(set(opp_moves))))


def converge(game, player):
    """
    Checks for squares with the most common moves with the opposing player

    :param game: `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: Float
        containing move score determined by the heuristic
    """

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    return float(own_moves + len(set(own_moves).intersection(set(opp_moves))))


def alternate(game, player):
    """
    This function switches from diverge and converge based on the game state
    :param game: `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: Float
        containing move score determined by the heuristic
    """

    blank_spaces = len(game.get_blank_spaces())
    if blank_spaces > 15:
        return diverge(game, player)
    else:
        return converge(game, player)


def knights_tour(game, player):
    """
    Using Warnsdorf's rule for determining the Knight's tour path. This requires finding the path
    with the least possible moves emanating from it (restricting initial movement to the sides)
    and then using the space in the center to move across the board
    :param game: `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: Float
        containing move score determined by the heuristic
    """
    # Number larger than 8 which is the max possible moves. Nodes with lesser moves are traversed first
    MOVES_CONSTANT = 10
    # This constant should be large enough to keep the distance factor < 1. We choose 10 since max distance is 8.48
    DISTANCE_CONSTANT = 10
    opponent = game.get_opponent(player)
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)
    move_count = len(set(own_moves).difference(opp_moves))
    own_loc = game.get_player_location(player)
    opp_loc = game.get_player_location(opponent)
    # Each node should have at least 2 moves so that the player is not blocked by the opponent
    if move_count > 1:
        # Distance between opponent location and current move to break the tie
        return MOVES_CONSTANT - len(own_moves) + get_distance(own_loc, opp_loc)/DISTANCE_CONSTANT
    else:
        return 0


def get_distance(point1, point2):
    """
    Distance formula to find the distance between two points x1, y1 and x2, y2
    :param point1: (int, int)
        tuple containing the player's cell position
    :param point2: (int, int)
        tuple containing the opponent's cell position
    :return: Float
        Distance between the two points
    """

    x1, y1 = point1
    x2, y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5


def knights_tour_improved(game, player):
    """
    Improved version of the Knight's tour where the player begins with occupying all squares that have
    the least possible moves (greater than 1) and then based on the state of the game switches to occupying
    squares that have max possible moves

    :param game: `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    :param player: object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    :return: Float
        containing move score determined by the heuristic
    """
    opponent = game.get_opponent(player)
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)
    own_loc = game.get_player_location(player)
    blank_spaces = game.get_blank_spaces()
    blank_space_count = len(blank_spaces)
    # Number larger than 8 which is the max possible moves. Nodes with lesser moves are traversed first
    MOVES_CONSTANT = 10
    # This constant should be large enough to keep the distance factor < 1. We choose 10 since max distance is 8.48
    DISTANCE_CONSTANT = 10
    knight_tour_mode = True

    if knight_tour_mode and blank_space_count < 34:
        knight_tour_mode = False

    if knight_tour_mode:
        opp_loc = game.get_player_location(opponent)
        move_count = len(set(own_moves).difference(opp_moves))
        # Each node should have at least 2 moves so that the player is not blocked by the opponent
        if move_count > 1:
            # Distance between opponent location and current move to break the tie
            return MOVES_CONSTANT - len(own_moves) + get_distance(own_loc, opp_loc)/DISTANCE_CONSTANT
        else:
            return 0
    else:
        depth_factor = compute_depth_factor(own_loc, blank_spaces)/1000000.
        #assert depth_factor < 1, "Depth factor {} is greater than 1".format(depth_factor)
        return depth_factor


def compute_depth_factor(position, blank_spaces, depth=0):
    """
    Traverses the partial game tree to obtain the move with the greatest depth and spread
    :param position: (int, int)
        Tuple containing location of the player
    :param [(int,int), (int,int)..]
        Array of tuples containing the current blank spaces in the board
    :return: Int
        containing move score
    """
    directions = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, -1), (-2, 1), (2, -1), (2, 1)]
    x, y = position
    moves = [(x - p, y - q) for p, q in directions
             if x-p >= 0 and y-q >= 0 and (x-p, y-q) in blank_spaces]
    if moves:
        updated_blank_spaces = [blank_space for blank_space in blank_spaces if blank_space != position]
        return sum([compute_depth_factor(move, updated_blank_spaces, depth+1) for move in moves])
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
            return -1, -1
        move = None
        try:
            depth = 1
            # Iterative deepening starting from depth = 1 until the terminal node or cutoff is reached
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
            # In case the no move is returned before cutoff then we get the heuristic value from the root
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
