"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import numpy as np


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player, agressiveness=3):
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
    number_of_moves = game.get_legal_moves(player)
    oponent_moves = game.get_legal_moves(game.get_opponent(player))
    score = float(len(number_of_moves) - (agressiveness * len(oponent_moves)))
    return score


def custom_score_generator(agressiveness=1):
    def custom(game, player):
        return custom_score(game, player, agressiveness)

    return custom


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
        current state.)  This parameter should be ignored when iterative = True.

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10., agressiveness=None):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.move_history = []
        self.open_moves = []
        self.agressiveness = agressiveness

    def get_fill_square_sequence(self, game):
        # TODO may be interesting open book
        j = np.array([0, 2, 1, 0, 2, 0, 1, 2, 0, 1])
        i = np.array([0, 1, -1, 1, 0, -1, 1, -1, -2, 0])
        offsets = [np.array((i, j)), np.array((i, -j)), np.array((-i, j)),
                   np.array((-j, i)), np.array((j, i)), np.array((-j, -i)), np.array((j, -i))]
        location = np.resize(np.array(game.get_player_location()), (2, 1))
        sequence = [location + offset for offset in offsets]
        [[(seq[0, i], seq[1, i]) for i in range(np.shape(seq)[1])] for seq in sequence]

    def has_moved_to(self, move):
        '''
        Add a move to the move history for the player
        '''
        self.move_history.append(list(move))

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
            DEPRECATED -- This argument will be removed in the next release

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
        # TODOs
        # -----
        # Perform any required initializations, including selecting an initial CHANGED
        # move from the game board (i.e., an opening book) TODO finish square sequence
        # returning immediately if there are no legal moves CHANGED
        self.time_left = time_left

        if game.get_player_location(self) == game.NOT_MOVED:
            # print('NOT MOVED !')
            # this is the first move
            center_position = (int(np.ceil(game.width / 2)), int(np.ceil(game.height / 2)))
            if game.get_player_location(game.get_opponent(self)) == game.NOT_MOVED or game.move_is_legal(center_position):
                # We are player one or center is free : pick center
                # print('CENTER POSITION ', center_position)
                return center_position
            else:
                return tuple(np.add(center_position, (1, 0)))

        # TODO implement the open book
        '''
        elif len(self.move_history) < 2 and not len(self.open_moves):
            # first moves, try to fit a square sequence
            # if possible
            self.open_moves = self.get_fill_square_sequence()

        if len(self.open_moves):
            # we are currently attempting to perform open book sequence do not perform search until blocked
            # check if next position on sequence is possible
            # if yes perform and increment sequence index
            next_open_position = self.open_moves.pop(0)
            if game.move_is_legal(next_open_position):
                return next_open_position
            else:
                # stop the open sequence
                self.open_moves = []
        '''
        # Not at the beggining, not doing the open -- start performing the search
        legal_moves = game.get_legal_moves(self)

        if not legal_moves:
            return (-1, -1)

        score = float('-inf')
        move = (-1, -1)
        try:
            maximizing_player = True

            if self.iterative:
                depth = 1
                while True:
                    if self.method == 'minimax':
                        score, move = self.minimax(game, depth, maximizing_player)
                    elif self.method == 'alphabeta':
                        score, move = self.alphabeta(game, depth, float("-inf"), float("inf"), maximizing_player)

                    depth += 1
            else:
                if self.method == 'minimax':
                    score, move = self.minimax(game, self.search_depth, maximizing_player)
                elif self.method == 'alphabeta':
                    score, move = self.alphabeta(game, self.search_depth, float("-inf"), float("inf"), maximizing_player)

        except Timeout:
            return move

        return move

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


                function MINIMAX-DECISION(state) returns an action
                 return arg max a ∈ ACTIONS(s) MIN-VALUE(RESULT(state, a))

                function MAX-VALUE(state) returns a utility value
                 if TERMINAL-TEST(state) the return UTILITY(state)
                 v ← −∞
                 for each a in ACTIONS(state) do
                   v ← MAX(v, MIN-VALUE(RESULT(state, a)))
                 return v

                function MIN-VALUE(state) returns a utility value
                 if TERMINAL-TEST(state) the return UTILITY(state)
                 v ← ∞
                 for each a in ACTIONS(state) do
                   v ← MIN(v, MAX-VALUE(RESULT(state, a)))
                 return v
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        player = game.active_player
        # print("At depth ", depth, " ---- ", player, " -- last move p1", self.move_history[-1])
        legal_moves = game.get_legal_moves(player)

        # if no legal moves return utility
        if not legal_moves:
            if player == self:
                utility = float("-inf")
            else:
                utility = float("+inf")
            return utility, (-1, -1)

        # check if we are at a leaf (depth == 0)
        if depth == 0:
            # we are at a leaf return the board score
            return self.score(game, self), (-1, -1)
        else:
            # not at a leaf - use recursion alternating min and max to search the tree
            if maximizing_player:
                results = [(self.minimax(game.forecast_move(m), depth - 1, not maximizing_player)[0], m) for m in legal_moves]
                # print('RESULTS : ', results)
                # print('MAX : ', max(results))
                return max(results)
            else:
                return min([(self.minimax(game.forecast_move(m), depth - 1, not maximizing_player)[0], m) for m in legal_moves])

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

        player = game.active_player
        # print("At depth ", depth, " ---- ", player, " -- last move p1", self.move_history[-1])
        legal_moves = game.get_legal_moves(player)

        if not legal_moves:
            if player == self:
                utility = float("-inf")
            else:
                utility = float("+inf")
            return utility, (-1, -1)

        if depth == 0:
            # we are at a leaf - return board score
            return self.score(game, self), (-1, -1)
        else:
            if maximizing_player:
                best_score = float('-inf')
                best_move = (-1, -1)
                # print(' beta ', beta)

                # go through all the moves but this time using a for loop in order to prune
                for m in legal_moves:
                    score, move = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, not maximizing_player)

                    # check if the score is above beta for pruning
                    if score >= beta:
                        # score is above beta, this branch will not be selected 2 levels above
                        # can be prunned
                        # print('Score : ', score)
                        # print('move : ', move)
                        return score, m
                    else:
                        alpha = max(alpha, score)
                        if score > best_score:
                            best_score = score
                            best_move = m
                return best_score, best_move

            else:
                best_score = float('+inf')
                best_move = (-1, -1)
                # print(' alpha ', alpha)
                for m in legal_moves:
                    score, move = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, not maximizing_player)
                    # print('Score : ', score, ' alpha ', alpha)
                    if score <= alpha:
                        # print('PRUNED!')
                        return score, m
                    else:
                        beta = min(beta, score)
                        if score < best_score:
                            best_score = score
                            best_move = m
                return best_score, best_move
