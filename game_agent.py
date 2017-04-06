"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


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

    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    if game.move_count > 12:
        player_reachable = get_reachable_spaces(game, player)
        opponent_reachable = get_reachable_spaces(game, game.get_opponent(player))
        return float(player_reachable - opponent_reachable)

    else:
        opponent = game.get_opponent(player)
        player_moves = game.get_legal_moves(player)
        opponent_moves = game.get_legal_moves(opponent)

        player_moves_sum = len(player_moves)
        opponent_moves_sum = len(opponent_moves)

        if player == game.active_player:
            for (x, y) in opponent_moves:
                if game.move_is_legal((x, y)):
                    opponent_moves_sum -= 1
        else:
            for (x, y) in player_moves:
                if game.move_is_legal((x, y)):
                    player_moves_sum -= 1

        return float(player_moves_sum - opponent_moves_sum)



def get_reachable_spaces(game, player):
    """Calculate the number of reachable spaces for the provided player.

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
    int
        The number of reachable spaces
    """
    movements = [(1, 2), (1, -2), (-1, 2), (-1, -2)]
    avail_spaces = game.get_blank_spaces()
    legal_moves = game.get_legal_moves(player)
    opponent_moves = []

    reachable_count = len(legal_moves)
    moves_to_search = legal_moves[:]
    searched_moves = legal_moves[:]
    searched_moves.append(game.get_player_location(player))

    if player != game.active_player:
        opponent_moves = game.get_legal_moves(game.active_player)

    def checkmove(new_move, reachable_count):
        if avail_spaces.count(new_move) and not searched_moves.count(new_move):
            reachable_count += 1
            searched_moves.append(new_move)
            moves_to_search.append(new_move)
        return reachable_count

    while len(moves_to_search):
        move = moves_to_search.pop(0)
        (x, y) = move
        for (i, j) in movements:
            if not opponent_moves.count((x, y)):
                reachable_count = checkmove((x + i, y + j), reachable_count)
                reachable_count = checkmove((x + j, y + i), reachable_count)

    return reachable_count


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning.

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
                 iterative=True, method='minimax', timeout=12.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

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

        if len(legal_moves) == 0:
            return (-1, -1)

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if self.method == 'minimax':
            method = self.minimax
        else:
            method = self.alphabeta
        try:
            best_move = legal_moves[0]
            if not self.iterative:
                score, move = method(game, self.search_depth)
                return move
            else:
                for depth in range(len(game.get_blank_spaces())):
                    _, best_move = method(game, depth + 1)

        except Timeout:
            return best_move
        return best_move


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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()


        move_scores = []
        moves = game.get_legal_moves() # get all possible moves for the active player (determine child nodes)

        if len(moves) == 0:
            return (float("-inf"), (-1, -1))

        for move in moves:
            next_state = game.forecast_move(move) # create a new state as if we made this move

            if depth == 1: # base case (last game tree level to search)
                move_scores.append(self.score(next_state, self))

            else: # still want to search deeper down the game tree
                next_score, _ = self.minimax(next_state, depth - 1)
                move_scores.append(next_score)

        if maximizing_player: # return highest score
            score = max(move_scores)
            best_move = moves[move_scores.index(score)]
        else: # return lowest score
            score = min(move_scores)
            best_move = moves[move_scores.index(score)]


        return (score, best_move)

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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        move_scores = []
        moves = game.get_legal_moves() # get all possible moves for the active player (determine child nodes)

        if len(moves) == 0:
            return (float("-inf"), (-1, -1))

        for move in moves:
            next_state = game.forecast_move(move) # create a new state as if we made this move

            if depth == 1: # base case (last game tree level to search)
                next_score = self.score(next_state, self)

            else: # still want to search deeper down the game tree
                next_score, _ = self.alphabeta(next_state, depth - 1, alpha, beta, not maximizing_player)

            if not maximizing_player:
                if next_score <= alpha: # should be pruned
                    return (next_score, move)
                if next_score < beta: # new upper bound
                    beta = next_score
            elif maximizing_player:
                if next_score >= beta: # should be pruned
                    return (next_score, move)
                if next_score > alpha: # new lower bound
                    alpha = next_score
            move_scores.append(next_score)

        if maximizing_player: # return highest score
            score = max(move_scores)
            best_move = moves[move_scores.index(score)]
        else: # return lowest score
            score = min(move_scores)
            best_move = moves[move_scores.index(score)]


        return (score, best_move)
