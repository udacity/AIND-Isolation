"""
Slight modification to the original code to allow for export of match data
"""

import itertools
import random
import warnings

from collections import namedtuple

from isolation import Board
from sample_players import RandomPlayer
from sample_players import null_score
from sample_players import open_move_score
from sample_players import improved_score
from game_agent import CustomPlayer, custom_score, custom_score_generator

NUM_MATCHES = 5  # number of matches against each opponent
TIME_LIMIT = 150  # number of milliseconds before timeout

TIMEOUT_WARNING = "One or more agents lost a match this round due to " + \
                  "timeout. The get_move() function must return before " + \
                  "time_left() reaches 0 ms. You will need to leave some " + \
                  "time for the function to return, and may need to " + \
                  "increase this margin to avoid timeouts during  " + \
                  "tournament play."

DESCRIPTION = """
This script evaluates the performance of the custom heuristic function by
comparing the strength of an agent using iterative deepening (ID) search with
alpha-beta pruning against the strength rating of agents using other heuristic
functions.  The `ID_Improved` agent provides a baseline by measuring the
performance of a basic agent using Iterative Deepening and the "improved"
heuristic (from lecture) on your hardware.  The `Student` agent then measures
the performance of Iterative Deepening and the custom heuristic against the
same opponents.
"""

Agent = namedtuple("Agent", ["player", "name"])


def play_match(player1, player2):
    """
    Play a "fair" set of matches between two agents by playing two games
    between the players, forcing each agent to play from randomly selected
    positions. This should control for differences in outcome resulting from
    advantage due to starting position on the board.
    """
    num_wins = {player1: 0, player2: 0}
    num_timeouts = {player1: 0, player2: 0}
    num_invalid_moves = {player1: 0, player2: 0}
    games = [Board(player1, player2), Board(player2, player1)]

    # initialize both games with a random move and response
    for _ in range(2):
        move = random.choice(games[0].get_legal_moves())
        games[0].apply_move(move)
        games[1].apply_move(move)

    # play both games and tally the results
    for game in games:
        winner, _, termination = game.play(time_limit=TIME_LIMIT)

        if player1 == winner:
            num_wins[player1] += 1

            if termination == "timeout":
                num_timeouts[player2] += 1
            else:
                num_invalid_moves[player2] += 1

        elif player2 == winner:

            num_wins[player2] += 1

            if termination == "timeout":
                num_timeouts[player1] += 1
            else:
                num_invalid_moves[player1] += 1

    if sum(num_timeouts.values()) != 0:
        warnings.warn(TIMEOUT_WARNING)

    return num_wins[player1], num_wins[player2]


def play_round(agents, num_matches, data_frame):
    """
    Play one round (i.e., a single match between each pair of opponents)
    """
    agent_1 = agents[-1]
    wins = 0.
    total = 0.

    print("\nPlaying Matches:")
    print("----------")

    for idx, agent_2 in enumerate(agents[:-1]):

        counts = {agent_1.player: 0., agent_2.player: 0.}
        names = [agent_1.name, agent_2.name]
        print("  Match {}: {!s:^11} vs {!s:^11}".format(idx + 1, *names), end=' ')

        # Each player takes a turn going first
        for p1, p2 in itertools.permutations((agent_1.player, agent_2.player)):
            for _ in range(num_matches):
                score_1, score_2 = play_match(p1, p2)
                counts[p1] += score_1
                counts[p2] += score_2
                total += score_1 + score_2
                winsA1 = range(score_1)
                lossesA1 = range(score_2)
                if p1 == agent_2.player:
                    winsA1 = range(score_2)
                    lossesA1 = range(score_1)

                data_frame = data_frame \
                    + [[1, names[0], names[1], agent_1.player.agressiveness, agent_1.player.search_depth, agent_1.player.iterative] for _ in winsA1] \
                    + [[0, names[0], names[1], agent_1.player.agressiveness, agent_1.player.search_depth, agent_1.player.iterative] for _ in lossesA1]

        wins += counts[agent_1.player]

        print("\tResult: {} to {}".format(int(counts[agent_1.player]),
                                          int(counts[agent_2.player])))

    return (100. * wins / total, data_frame)


def main():

    HEURISTICS = [("Null", null_score),
                  ("Open", open_move_score),
                  ("Improved", improved_score)]
    AB_ARGS = {"search_depth": 5, "method": 'alphabeta', "iterative": False}
    MM_ARGS = {"search_depth": 3, "method": 'minimax', "iterative": False}
    CUSTOM_ARGS = {"method": 'alphabeta', 'iterative': True}

    # We compare ID_Improved to our custom heuristic with varying amount of agressivenes
    id_op = [Agent(CustomPlayer(score_fn=improved_score, **CUSTOM_ARGS), "ID_Improved")]

    test_agents = [
        Agent(CustomPlayer(score_fn=custom_score_generator(2), method='alphabeta', iterative=True, agressiveness=2), "Student iterative ag2"),
        Agent(CustomPlayer(score_fn=custom_score_generator(3), method='alphabeta', iterative=True, agressiveness=3), "Student iterative ag3"),
        Agent(CustomPlayer(score_fn=custom_score_generator(4), method='alphabeta', iterative=True, agressiveness=4), "Student iterative ag4"),
        Agent(CustomPlayer(score_fn=custom_score_generator(5), method='alphabeta', iterative=True, agressiveness=5), "Student iterative ag5"),
        Agent(CustomPlayer(score_fn=custom_score_generator(6), method='alphabeta', iterative=True, agressiveness=6), "Student iterative ag6"),
    ]

    print(DESCRIPTION)
    NUM_MATCHES = 10
    data_frame = []
    for agentUT in test_agents:
        print("")
        print("*************************")
        print("{:^25}".format("Evaluating: " + agentUT.name))
        print("*************************")

        # agents = random_agents + mm_agents + ab_agents + [agentUT]

        agents = id_op + [agentUT]
        win_ratio, data_frame = play_round(agents, NUM_MATCHES, data_frame)

        print("\n\nResults:")
        print("----------")
        print("{!s:<15}{:>10.2f}%".format(agentUT.name, win_ratio))

    print(data_frame)


if __name__ == "__main__":
    main()
