
# isolation.Board class

## Constructor

    Board.__init__(self, player_1, player_2, width=7, height=7)

## Attributes

### BLANK : 0 (constant)

### NOT_MOVED : None (constant)

### width : 7 (constant)

Board width

### height : 7 (constant)

Board height

### active_player : hashable

Reference to a hashable object registered as a player with the initiative to move on the current board

### inactive_player : hashable

Reference to a hashable object registered as a player awaiting initiative to move on the current board

### move_count : int

Counter indicating the number of moves that have been applied to the game

## Public Methods

### apply_move(self, move)
    
Modify the game object by moving the active player on the game board and disabling the vacated square (if any). The forecast_move method performs the same function, but returns a copy of the board, rather than modifying the state in-place.

### copy(self)

Return a new Board object that is a copy of the current game state

### forecast_move(self, move)

Equivalent to apply_move, but returns a copy of the board rather than modifying the state in-place.

### get_blank_spaces(self)

Returns a list of tuples identifying the blank squares on the current board

### get_legal_moves(self, player=None)

Returns a list of tuples identifying the legal moves for the specified player

### get_opponent(self, player)

Returns the opponent of the specified player

### get_player_location(self, player)

Returns a tuple (x, y) identifying the location of the specified player on the game board, or None of the player is a registered agent in the game but has not yet been placed on the board. Raises a RuntimeError if the specified player is not registered on the board.

### hash(self)

Return a hash of the current state (public alias of __hash__ method). The hashed state includes occupied cells, current player locations, and which player has initiative on the board. An equivalent hash function can be added to the isolation.Board class from the isolation project:

### is_loser(self, player)

Returns True if the specified player has lost the game in the current state, and False otherwise

### is_winner(self, player)

Returns True if the specified player has won the game in the current state, and False otherwise

### move_is_legal(self, move)

Returns True if the active player can legally make the specified move and False otherwise

### to_string(self, symbols=['1', '2'])

Return a string representation of the current board position

### utility(self, player)

Returns a floating point value: +inf if the specified player has won the game, -inf if the specified player has lost the game, and 0 otherwise.