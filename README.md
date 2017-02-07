
# Build a Game-playing Agent

## Synopsis

In this project, students will develop an adversarial search agent to play the game "Isolation".  Students only need to modify code in the `game_agent.py`, however, code is included for example player and evaluation functions for you to review and test against in the other files.

Isolation is a deterministic, two-player game of perfect information in which the players alternate turns moving a single piece from one cell to another on a board.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.

This project uses a version of Isolation where each agent is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chess or checkerboard).  The agents can move to any open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. Movements are blocked at the edges of the board (the board does not wrap around), however, the player can "jump" blocked or occupied spaces (just like a knight in chess).

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

These rules are implemented in the `isolation.Board` class provided in the repository. 


## Quickstart Guide

The following example creates a game and illustrates the basic API. You can run this example with `python sample_players.py`

    from isolation import Board

    # create an isolation board (by default 7x7)
    player1 = RandomPlayer()
    player2 = GreedyPlayer()
    game = Board(player1, player2)

    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that .apply_move() changes the calling object
    game.apply_move((2, 3))
    game.apply_move((0, 5))
    print(game.to_string())

    # players take turns moving on the board, so player1 should be next to move
    assert(player1 == game.active_player)

    # get a list of the legal moves available to the active player
    print(game.get_legal_moves())

    # get a successor of the current state by making a copy of the board and
    # applying a move. Notice that this does NOT change the calling object
    # (unlike .apply_move()).
    new_game = game.forecast_move((1, 1))
    assert(new_game.to_string() != game.to_string())
    print("\nOld state:\n{}".format(game.to_string()))
    print("\nNew state:\n{}".format(new_game.to_string()))

    # play the remainder of the game automatically -- outcome can be "illegal
    # move" or "timeout"; it should _always_ be "illegal move" in this example
    winner, history, outcome = game.play()
    print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    print(game.to_string())
    print("Move history:\n{!s}".format(history))


## Instructions

Implement the following four functions in `game_agent.py`:

- `CustomPlayer.minimax()`: implement minimax search
- `CustomPlayer.alphabeta()`: implement minimax search with alpha-beta pruning
- `CustomPlayer.get_move()`: implement fixed-depth and iterative deepening search
- `custom_score()`: implement your own position evaluation heuristic

You may write or modify code within each file (as long as you maintain compatibility with the function signatures provided) and you may add other classes, functions, etc., as needed, but it is not required.  


### Coding

The steps below outline one suggested process for completing the project -- however, this is just a suggestion to help you get started.  Unit tests can be executed by running `python agent_test.py -v`.  (See the [unittest](https://docs.python.org/3/library/unittest.html#basic-example) module for details.)

0. Pass the test_get_move_interface and test_minimax_interface unit tests by implementing a fixed-depth call to minimax in `CustomPlayer.get_move()` and implementing a single-level search in `CustomPlayer.minimax()` (the interface checks only tests depth=1)

0. Pass the test_minimax test by extending your `CustomPlayer.minimax()` function with the full recursive search process.  See Also: [AIMA Minimax Decision](https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md)

0. Pass the test_alphabeta_interface test by copying the code from `CustomPlayer.minimax()` into the `CustomPlayer.alphabeta()` function.

0. Pass the test_alphabeta test by extending your `CustomPlayer.alphabeta()` function to include alpha and beta pruning.  See Also: [AIMA Alpha-Beta Search](https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md)

0. Pass the test_get_move test by extending your fixed-depth call in `CustomPlayer.get_move()` to implement Iterative Deepening.  See Also [AIMA Iterative Deepening Search](https://github.com/aimacode/aima-pseudocode/blob/master/md/Iterative-Deepening-Search.md)

0. Finally, pass the test_heuristic test by implementing any heuristic in `custom_score()`.  (This test only validates the return value type -- it does not check for "correctness" of your heuristic.)  You can see example heuristics in the `sample_players.py` file.


### Tournament

The `tournament.py` script is used to evaluate the effectiveness of your custom_score heuristic.  The script measures relative performance of your agent (called "Student") in a round-robin tournament against several other pre-defined agents.  The Student agent uses time-limited Iterative Deepening and the custom_score heuristic you wrote.

The performance of time-limited iterative deepening search is hardware dependent (faster hardware is expected to search deeper than slower hardware in the same amount of time).  The script controls for these effects by also measuring the baseline performance of an agent called "ID_Improved" that uess Iterative Deepening and the improved_score heuristic from `sample_players.py`.  Your goal is to develop a heuristic such that Student outperforms ID_Improved.

The tournament opponents are listed below. (See also: sample heuristics and players defined in sample_players.py)

- Random: An agent that randomly chooses a move each turn.
- MM_Null: CustomPlayer agent using fixed-depth minimax search and the null_score heuristic
- MM_Open: CustomPlayer agent using fixed-depth minimax search and the open_move_score heuristic
- MM_Improved: CustomPlayer agent using fixed-depth minimax search and the improved_score heuristic
- AB_Null: CustomPlayer agent using fixed-depth alpha-beta search and the null_score heuristic
- AB_Open: CustomPlayer agent using fixed-depth alpha-beta search and the open_move_score heuristic
- AB_Improved: CustomPlayer agent using fixed-depth alpha-beta search and the improved_score heuristic


## Submitting

Your project is ready for submission when it meets all requirements of the project rubric.  Your code is finished when it passes all unit tests, and you have successfully implemented a suitable heuristic function.
