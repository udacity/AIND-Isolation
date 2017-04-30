import isolation
import sample_players
import game_agent

def get_object(name):
    """Get the named object from either the sample_players or game_agent module
    """
    return getattr(game_agent, name, getattr(sample_players, name, None))

def main(args):
    if not args:
        print("""\
Usage:
  python play_human.py score_fn [PlayerClass]
Lets you (the human) play against PlayerClass, using the given score_fn.
score_fn can be the name of any function in game_agent or sample_players.
PlayerClass defaults to AlphaBetaPlayer, but can be any class in those
modules that takes a score_fn
""")
        return
    score_fn = get_object(args[0])
    if not score_fn:
        print("Could not find game_agent.{0} or sample_players.{0}".format(args[0]))
        return
    if (args[1:]):
        PlayerClass = get_object(args[1])
        if not PlayerClass:
            print("Could not find game_agent.{0} or sample_players.{0}".format(args[1]))
            return
    else:
        PlayerClass = game_agent.AlphaBetaPlayer
    run_against_human(score_fn, PlayerClass)

def run_against_human(score_fn, PlayerClass):
    """Play a game against the human, given a PlayerClass (such as MinmaxPlayer)
    and a score_fn function"""
    human = sample_players.HumanPlayer()
    board = isolation.Board(
        PlayerClass(score_fn=score_fn),
        human)
    winner, moves, reason = board.play()
    print("Game finished due to:", reason)
    if winner is human:
        print("YOU WON!")
    else:
        print("you lost :(")
    print("Moves:", moves)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
