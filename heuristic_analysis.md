# Heuristic Analysis

## Heuristic functions

### 1rst
The first function in the one given in the lectures. It measures the number of the legal moves for the player in his current position
```python
player_moves
```

### 2nd
This function calculates the difference between the number of legal moves for the player and his oponent. It doens't use the absolute value because if it's negative, it means that the oponent
has more moves than the player and that is something to take into account
```python
player_moves - opponent_moves
```

### 3rd
As the second one, it calculates the difference but squaring the oponent moves giving a penalty to the oponent moves.
```python
player_moves - opponent_moves ** 2
```

### 4th
As the third one, it calculates the difference but squaring the player moves
```python
(player_moves ** 2) - opponent_moves
```

## Results

### 1st
![](https://i.imgur.com/EIhxPwG.png)

### 2nd
![](https://i.imgur.com/BfSHYSU.png)

### 3rd
![](https://i.imgur.com/1UKTjen.png)

### 4th
![](https://i.imgur.com/61ovnIL.png)

## Conclussion
The best performance is given by the 3rd option `player_moves - opponent_moves ** 2`. Looks like givin penalty to the opponent moves is working.
But we cannot conclude that that is the best option because all the results are really close to each other. The minimum is `74.52%` and the maximum is `77.38%`.

We would need to run much more games in order to be more confident about the results, but the improvement looks minimum though. I wanted to try another heuristic
but given the constrain of the `Board` it wouldn't have a lot of difference with the player moves. I wanted to try the liberty degrees of the player. I mean, the
directions where a player can move. If the player is in the center, it can move up, down, right, left, and in 4 diagonals. That's a total of 8 degrees of liberty.
If it is in a corner it would have only 3. It sound like a really good feature to introduce in the heuristic, but our game is constrained to only L moves, so it
doesn't have a lot of sense with this constrain given that it will be a multiple of the available moves (In the center, a player would have 8 Ls moves and 4 liberty
degrees).

