"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class FoundWinningMoveException(Exception):
    def __init__(self, move):
        self.move = move


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def possible_moves_count(row, column, game):
    total_moves = (8
                   - (1 if (column < 2 or row < 1) else 0)  # 10 o'clock blocked
                   - (1 if (column < 1 or row < 2) else 0)  # 11 o'clock blocked
                   - (1 if (column > game.width - 2 or row < 2) else 0)  # 1 o'clock blocked
                   - (1 if (column > game.width - 3 or row < 1) else 0)  # 2 o'clock blocked
                   - (1 if (column > game.width - 3 or row > game.height - 2) else 0)  # 4 o'clock blocked
                   - (1 if (column > game.width - 2 or row > game.height - 3) else 0)  # 5 o'clock bocked
                   - (1 if (column < 1 or row > game.height - 3) else 0)  # 7 o'clock blocked
                   - (1 if (column < 2 or row > game.height - 2) else 0)  # 8 o'clock blocked
                   )
    return total_moves

def legal_move_primary(game, player):
    if len(game.get_legal_moves(game.active_player)) == 0:
        return float('-inf') if player == game.active_player else float('inf')
    else:
        own_legal_moves = len(game.get_legal_moves(player=player))
        opponent_legal_moves = len(game.get_legal_moves(player=game.get_opponent(player=player)))
        return float(own_legal_moves - opponent_legal_moves)

def legal_move_relative(game, player):

        own_legal_moves = len(game.get_legal_moves(player=player))
        own_total_moves = possible_moves_count(*game.get_player_location(player), game)
        opponent_legal_moves = len(game.get_legal_moves(player=game.get_opponent(player=player)))
        opponent_total_moves = possible_moves_count(*game.get_player_location(player=game.get_opponent(player=player)), game)
        return own_legal_moves/own_total_moves - opponent_legal_moves/opponent_total_moves

def can_be_blocked(game, player):
    if game.active_player == player:
        afraid_of_blocking = 1
    else:
        afraid_of_blocking = -1

    r,c = game.player_1_loc()
    color1 = (r+c)%2

    r,c = game.player_2_loc()
    color2 = (r+c)%2

    blocked = float(color1 == color2)
    return afraid_of_blocking * blocked


def norm_center_distance(game, player):
    center_row = (float(game.height) - 1.) / 2.
    center_col = (float(game.width) - 1.) / 2.
    max_distance = center_row ** 2 + center_col ** 2
    player_row, player_col = game.get_player_location(player=player)
    oppo_row, oppo_col = game.get_player_location(player=game.get_opponent(player=player))
    return (
            (oppo_row-center_row) ** 2 + (oppo_col-center_col) ** 2 -
            (player_row-center_row) ** 2 - (player_col-center_col) ** 2
            ) / max_distance


def custom_score(game, player: 'IsolationPlayer') ->float:

    return legal_move_primary(game, player) + can_be_blocked(game, player)


def custom_score_2(game, player):

    return legal_move_primary(game, player) + norm_center_distance(game, player)


def custom_score_3(game, player):

    return legal_move_primary(game, player) # + legal_move_relative(game, player)

class IsolationPlayer:

    def __init__(self, search_depth=100, score_fn=custom_score, timeout=10., name=None):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.name = name


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
                return min_score
            else:
                min_score = self.score(game, self)
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
        self.time_left = lambda: time_left() - self.TIMER_THRESHOLD

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout


        search_depth = 1
        return_move = (-1, -1)
        while self.search_depth >= search_depth:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                move = self.alphabeta(game, search_depth)
                if move == (-1, -1):
                    #print('Existential Crisis after {} moves with {}ms left'.format(search_depth, self.time_left()))
                    break
                    #return return_move
                #elif will_win:
                #    return_move = move
                #    return return_move
                else:
                    return_move = move
                search_depth += 1

            except SearchTimeout:
                #print('timeing out at search depth {} at time {}'.format(search_depth - 1, self.time_left()))
                return return_move
            except FoundWinningMoveException as fwme:
                return fwme.move

        # Return the best move from the last completed search iteration
        return return_move

    def recursive_alphabeta(self, game, depth, alpha, beta, is_max):
        if self.time_left() < 0:
            # print('Raising SearchTimeout, time left:{}'.format(self.time_left()))
            raise SearchTimeout
        if depth <= 1:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float('-inf') if is_max else float('inf')

        running_score = float('inf') * ((-1) ** float(is_max))
        for legal_move in legal_moves:
            recursive_score = self.recursive_alphabeta(game=game.forecast_move(legal_move),
                                                       depth=depth - 1,
                                                       alpha=alpha,
                                                       beta=beta,
                                                       is_max=(not is_max))
            if is_max:
                running_score = max(running_score, recursive_score)
                alpha = max(alpha, running_score)
            else:
                running_score = min(running_score, recursive_score)
                beta = min(beta, running_score)
            if beta <= alpha:
                break
        return running_score


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        #print('Called with depth {}'.format(depth))

        selected_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return selected_move
        max_score = float('-inf')
        for legal_move in legal_moves:
            score = self.recursive_alphabeta(game=game.forecast_move(legal_move),
                                             depth=depth,
                                             alpha=max_score,
                                             beta=beta,
                                             is_max=False)
            if score > max_score or (max_score==float('-inf')):
                max_score = score
                selected_move = legal_move
        if max_score == float('inf'):
            raise FoundWinningMoveException(move=selected_move)
        return selected_move#, max_score == float('inf')



