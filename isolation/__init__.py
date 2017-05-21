"""
This library provides a Python implementation of the game Isolation.
Isolation is a deterministic, two-player game of perfect information in
which the players alternate turns moving between cells on a square grid
(like a checkerboard).  Whenever either player occupies a cell, that
location is blocked for the rest of the game. The first player with no
legal moves loses, and the opponent is declared the winner.
"""

# Make the Board class available at the root of the module for imports
from .isolation import Board
