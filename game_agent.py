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

    def minimax(self, game, depth):
        v, move = self.my_minimax(game, depth, True)
        return move


    def my_minimax(self, game, depth, maximizer):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self), (-1, -1)

        available_my_moves = game.get_legal_moves()
        if len(available_my_moves) == 0:
            return self.score(game, self), (-1, -1)

        next_move = (-1, -1)
        if maximizer == True:  # Maximizing player
            maximizer = False
            utility_score = float("-inf")
            for move in available_my_moves:
                new_game = game.forecast_move(move)
                next_score, _ = self.my_minimax(new_game, depth - 1, maximizer)
                if utility_score < next_score:
                    utility_score = next_score
                    next_move = move
            return utility_score, next_move

        else:
            maximizer = True
            utility_score = float("inf")
            for move in available_my_moves:
                new_game = game.forecast_move(move)
                next_score, _ = self.my_minimax(new_game, depth - 1, maximizer)
                if utility_score > next_score:
                    utility_score = next_score
                    next_move = move
            return utility_score, next_move

    def minimax2(self, game, depth: int) -> (int, int):

        def max_move(game, max_depth, currdepth=0):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if max_depth > currdepth:
                min_score = float('-inf')
                legal_moves = game.get_legal_moves()
                for legal_move in legal_moves:
                    score = min_move(game.forecast_move(move=legal_move), max_depth=max_depth, currdepth=currdepth+1)
                    if score > min_score:
                        min_score = score
                #print('{} {}:\n{}'.format(game._active_player == game._player_1, min_score,game.to_string()))
                return min_score
            else:
                min_score = self.score(game, self)
                #print('{} {}:\n{}'.format(game._active_player == game._player_1, min_score, game.to_string()))
                return min_score


        def min_move(game, max_depth, currdepth=0):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if max_depth > currdepth:
                max_score = float('inf')
                legal_moves = game.get_legal_moves()
                for legal_move in legal_moves:
                    score = max_move(game.forecast_move(move=legal_move), max_depth=max_depth, currdepth=currdepth+1)
                    if score < max_score:
                        max_score = score
                #print('{} {}:\n{}'.format(game._active_player == game._player_1, max_score, game.to_string()))
                return max_score
            else:
                max_score = self.score(game, self)
                #print('{} {}:\n{}'.format(game._active_player == game._player_1, max_score, game.to_string()))
                return max_score


        depth = depth - 1
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        max_score = float('-inf')
        recommended_move = None
        try:
            for legal_move in legal_moves:
                score = min_move(game.forecast_move(move=legal_move), max_depth=depth)
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
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        def recursive_alphabeta(player, game, depth, alpha, beta, is_max):
            if depth <= 1:
                return player.score(game, player)
            legal_moves = game.get_legal_moves()
            if not legal_moves:
                return float('-inf') if is_max else float('inf')
            if is_max:
                running_score = float('-inf')
                for legal_move in legal_moves:
                    running_score = max(running_score,
                                        recursive_alphabeta(player=player,
                                                            game=game.forecast_move(legal_move),
                                                            depth=depth-1,
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
                    running_score = min(running_score,
                                        recursive_alphabeta(player=player,
                                                            game=game.forecast_move(legal_move),
                                                            depth=depth-1,
                                                            alpha=alpha,
                                                            beta=beta,
                                                            is_max=(not is_max)))
                    beta = min(beta, running_score)
                    if beta <= alpha:
                        break
                return running_score

        selected_move = (-1,1)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return selected_move
        max_score = float('-inf')
        for legal_move in legal_moves:
            score = recursive_alphabeta(player=self,
                                        game=game.forecast_move(legal_move),
                                        depth=depth,
                                        alpha=max_score,
                                        beta=beta,
                                        is_max=False)
            if score > max_score:
                max_score = score
                selected_move = legal_move
        return selected_move