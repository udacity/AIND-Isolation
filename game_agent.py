"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player: 'IsolationPlayer') ->float:

    own_legal_moves = len(game.get_legal_moves(player=player))
    if own_legal_moves == 0:
        return -float('inf')
    return float(len(game.get_legal_moves(player=player)))

class IsolationPlayer:

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10., name=None):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.name=name


def custom_score_2(game, player):
    own_legal_moves = len(game.get_legal_moves(player=player))
    opponent_legal_moves = len(game.get_legal_moves(player=game.get_opponent(player=player)))
    if opponent_legal_moves == 0:
        return float('inf')
    elif own_legal_moves == 0:
        return float('-inf')
    else:
        return float(own_legal_moves - opponent_legal_moves)


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
    # TODO: finish this function!
    raise NotImplementedError


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
    # TODO: finish this function!
    raise NotImplementedError



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


    def minimax(self, game, depth: int) -> (int, int):

        def max_move(game, max_depth, currdepth=0):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if max_depth > currdepth:
                has_timed_out = False
                max_score = float('-inf')
                legal_moves = game.get_legal_moves()
                for legal_move in legal_moves:
                    try:
                        score, has_timed_out \
                            = min_move(game.forecast_move(move=legal_move), max_depth=max_depth, currdepth=currdepth+1)
                    except SearchTimeout as se:
                        return max_score, True
                    if score > max_score:
                        max_score = score
                return max_score, has_timed_out
            else:
                max_score = self.score(game, self)
                return max_score, False


        def min_move(game, max_depth, currdepth=0):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if max_depth > currdepth:
                has_timed_out = False
                min_score = float('inf')
                legal_moves = game.get_legal_moves()
                for legal_move in legal_moves:
                    try:
                        score, has_timed_out \
                            = max_move(game.forecast_move(move=legal_move), max_depth=max_depth, currdepth=currdepth+1)
                    except SearchTimeout as se:
                        return min_score, True
                    if score < min_score:
                        min_score = score
                return min_score, False
            else:
                min_score = self.score(game, self)
                return min_score, False


        depth = depth - 1
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        max_score = float('-inf')
        recommended_move = None
        try:
            for legal_move in legal_moves:
                score, has_timed_out = min_move(game.forecast_move(move=legal_move), max_depth=depth)
                if score > max_score:
                    recommended_move = legal_move
                    max_score = score
            #print('{} score: {} move: {} \n {}'.format(self.name, max_score, recommended_move, game.to_string()))
        except SearchTimeout as se:
            return recommended_move
        return recommended_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        self.time_left = lambda: time_left() - 10


        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout



        # Return the best move from the last completed search iteration
        return self.alphabeta(game, self.search_depth)


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        search_depth = 1
        return_move = (-1, -1)
        while depth > search_depth:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                selected_move = (-1, -1)
                legal_moves = game.get_legal_moves()
                if not legal_moves:
                    return selected_move
                max_score = float('-inf')
                for legal_move in legal_moves:
                    score = self.recursive_alphabeta(
                        game=game.forecast_move(legal_move),
                        depth=search_depth,
                        alpha=max_score,
                        beta=beta,
                        is_max=False)
                    if score > max_score:
                        max_score = score
                        selected_move = legal_move
                best_move = selected_move

                if best_move == (-1, -1):
                    print('Existential Crisis after {} moves with {}ms left'.format(search_depth, self.time_left()))
                    return return_move
                elif max_score == float('inf'):
                    print("Player {} will win after maximum {} moves ({}ms left ont the clock)"
                          .format(self.name, search_depth, self.time_left()))
                    return return_move
                else:
                    return_move = best_move

                print('Searching at depth {} with {:.2f}ms left, suggesting move: {}'.
                      format(search_depth, self.time_left(), return_move))
                search_depth += 1

            except SearchTimeout:
                print('timeing out at search depth {} at time {}'.format(search_depth-1, self.time_left()))
                # Handle any actions required after timeout as needed
                return return_move

        return return_move

    def recursive_alphabeta(self, game, depth, alpha, beta, is_max):
        if depth <= 1:
            return self.score(game, self)
        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return float('-inf') if is_max else float('inf')
        if is_max:
            running_score = float('-inf')
            for legal_move in legal_moves:
                if self.time_left() < 0:
                    print('Raising SearchTimeout, time left:{}'.format(self.time_left()))
                    raise SearchTimeout
                running_score = max(running_score,
                                    self.recursive_alphabeta( game=game.forecast_move(legal_move),
                                                        depth=depth - 1,
                                                        alpha=alpha,
                                                        beta=beta,
                                                        is_max=(not is_max)))
                alpha = max(alpha, running_score)
                if beta <= alpha:
                    break
            return running_score
        else:
            running_score = float('inf')
            for legal_move in legal_moves:
                if self.time_left() < 0:
                    print('Raising SearchTimeout, time left:{}'.format(self.time_left()))
                    raise SearchTimeout
                running_score = min(running_score,
                                    self.recursive_alphabeta(game=game.forecast_move(legal_move),
                                                        depth=depth - 1,
                                                        alpha=alpha,
                                                        beta=beta,
                                                        is_max=(not is_max)))
                beta = min(beta, running_score)
                if beta <= alpha:
                    break
            return running_score