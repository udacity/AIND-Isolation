"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import numpy as np

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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
    # amount of moves minus 2 x the opponent moves, as hinted in the lecture
    if game.is_loser(player):
        return -np.inf

    if game.is_winner(player):
        return np.inf

    own_moves = len(game.get_legal_moves(player))
    opp_moves = 2 * len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


def custom_score_2(game, player):
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
        return -np.inf

    if game.is_winner(player):
        return np.inf
    
    # tries to play in the geometric oposite of the opponent in the board,
    # or the closest possible based on simple euclidean distance,
    # as hinted by the student in the lecture

    opponent_position = game.get_player_location(game.get_opponent(player))
    best_position = (opponent_position[1], opponent_position[0]) #invert coordinates
    player_position = game.get_player_location(player)

    catet_1 = best_position[0] - player_position[0] + 1
    catet_2 = best_position[1] - player_position[1] + 1
    return 1.0 / max(0.1, (catet_1**2 + catet_2**2))


def custom_score_3(game, player):
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
        return -np.inf

    if game.is_winner(player):
        return np.inf

    # gets the amount of possible moves for both players and reduce the amount of
    # intersection between them. The idea is to do an heuristics around the concept of
    # separation, when both players are isolated from each other in the board, the one with the biggest
    # amount of movements will win inevitably
    opponent = game.get_opponent(player)    
    player_moves = set(game.get_legal_moves(player))
    opponent_moves = set(game.get_legal_moves(opponent))    
    intersection_moves = player_moves & opponent_moves
    
    return (len(player_moves) - len(opponent_moves))/float(len(intersection_moves)+1)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=50.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        def terminal_test(game_):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            return not bool(game_.get_legal_moves())  # by Assumption 1
        
        def max_value(game_, depth_remaining):
            if terminal_test(game_) \
                or depth_remaining == 0:
                return self.score(game_, self)

            v = -np.inf
            for m in game_.get_legal_moves():
                v = max(v, min_value(game_.forecast_move(m), depth_remaining-1))
            return v
        
        def min_value(game_, depth_remaining):
            if terminal_test(game_) \
                or depth_remaining == 0:
                return self.score(game_, self)
            
            v = np.inf
            for m in game_.get_legal_moves():
                v = min(v, max_value(game_.forecast_move(m), depth_remaining-1))
            return v        
        
        moves = game.get_legal_moves()
        utility = -np.inf
        best_move = (-1,-1)
        for move in moves:
            pred = min_value(game.forecast_move(move), depth-1)
            if pred > utility:
                utility = pred
                best_move = move
        
        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if legal_moves:
            best_move = legal_moves[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.            
            depth = 0
            while True:
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()

                depth += 1
                best_move = self.alphabeta(game, depth)
                # once we run out of time, this loop will end
                # due to the exception raised in the alphabeta function
            
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def alphabeta(self, game, depth, alpha=-np.inf, beta=np.inf):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

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

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
                        
        def terminal_test(game_):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            return not bool(game_.get_legal_moves())  # by Assumption 1

        def max_value(game_, alpha_, beta_, depth_remaining):
            if terminal_test(game_) \
                or depth_remaining == 0:
                return self.score(game_, self)

            v = -np.inf
            for m in game_.get_legal_moves():
                v = max(v, min_value(game_.forecast_move(m), alpha_, beta_, depth_remaining-1))
                if v >= beta_:
                    return v
                alpha_ = max(alpha_, v)
            return v

        def min_value(game_, alpha_, beta_, depth_remaining):
            if terminal_test(game_) \
                or depth_remaining == 0: 
                return self.score(game_, self)
            
            v = np.inf
            for m in game_.get_legal_moves():
                v = min(v, max_value(game_.forecast_move(m), alpha_, beta_, depth_remaining-1))
                if v <= alpha_:
                    return v
                beta_ = min(beta_, v)
            return v               
        
        moves = game.get_legal_moves()
        utility = -np.inf
        best_move = (-1,-1)
        for move in moves:
            pred = min_value(game.forecast_move(move), alpha, beta, depth-1)
            if pred > utility:
                utility = pred
                best_move = move
            alpha = max(alpha, utility)
        
        return best_move

        

