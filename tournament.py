"""
Estimate the strength rating of student-agent with iterative deepening and
a custom heuristic evaluation function against fixed-depth minimax and
alpha-beta search agents by running a round-robin tournament for the student
agent. Note that all agents are constructed from the student CustomPlayer
implementation, so any errors present in that class will affect the outcome
here.

The student agent plays a fixed number of "fair" matches against each test
agent. The matches are fair because the board is initialized randomly for both
players, and the players play each match twice -- switching the player order
between games. This helps to correct for imbalances in the game due to both
starting position and initiative.

For example, if the random moves chosen for initialization are (5, 2) and
(1, 3), then the first match will place agentA at (5, 2) as player 1 and
agentB at (1, 3) as player 2 then play to conclusion; the agents swap
initiative in the second match with agentB at (5, 2) as player 1 and agentA at
(1, 3) as player 2.
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
from game_agent import CustomPlayer
from game_agent import custom_score

NUM_MATCHES = 20  # number of matches against each opponent
TIME_LIMIT = 100  # number of milliseconds before timeout

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


def play_match(agent1, test_agents, win_counts, num_matches):
    """Play a "fair" set of matches between two agents by playing two games
    between the players, forcing each agent to play from randomly selected
    positions. This should control for differences in outcome resulting from
    advantage due to starting position on the board.
    """
    timeout_count = 0

    for _ in range(num_matches):

        games = [Board(agent1.player, test_agents[0].player),
                 Board(test_agents[0].player, agent1.player),
                 Board(agent1.player, test_agents[1].player),
                 Board(test_agents[1].player, agent1.player)]

        # initialize both games with a random move and response
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)

        # play both games and tally the results
        for game in games:
            winner, _, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1

        if termination == "timeout":
            timeout_count += 1

    return timeout_count


def play_round(agents, test_agents, num_matches):
    """Play one round (i.e., a single match between each pair of opponents)"""
    total_wins = [0, 0]
    total_timeouts = 0.
    total_matches = 2 * num_matches * len(agents)

    print("\n{:^11}{:^13}{:^25}{:^25}".format(
        "Match #", "Opponent", test_agents[0].name, test_agents[1].name))
    print("{:^11}{:^13} {:^11}|{:^11}  {:^11}|{:^11}".format(
        "", "", "Won", "Lost", "Won", "Lost"))

    for idx, agent_2 in enumerate(agents):
        wins = {test_agents[0].player: 0,
                test_agents[1].player: 0,
                agent_2.player: 0}

        print("{!s:^11}{:^13}".format(idx + 1, agent_2.name),
              end=" ", flush=True)

        total_timeouts += play_match(agent_2, test_agents, wins, num_matches)
        ta1_wins = wins[test_agents[0].player]
        ta2_wins = wins[test_agents[1].player]
        total_wins[0] += ta1_wins
        total_wins[1] += ta2_wins
        print("{:^11}|{:^11}  {:^11}|{:^11}".format(
            ta1_wins, 2 * num_matches - ta1_wins,
            ta2_wins, 2 * num_matches - ta2_wins))

    print("-" * 74)
    print("{:^11}{:^13}{:^25}{:^25}\n".format(
        "", "Win Rate:", "{:.1f}%".format(100 * total_wins[0] / total_matches),
        "{:.1f}%".format(100 * total_wins[1] / total_matches)))

    if total_timeouts:
        print("\nThere were {} timeouts during play -- make sure your agent " +
              "handles search timeout correctly, and consider increasing " +
              "the timeout margin for your agent.\n")


def main():

    HEURISTICS = [#("Null", null_score),
                  ("Open", open_move_score),
                  ("Improved", improved_score)]
    AB_ARGS = {"search_depth": 5, "method": 'alphabeta', "iterative": False}
    MM_ARGS = {"search_depth": 3, "method": 'minimax', "iterative": False}
    CUSTOM_ARGS = {"method": 'alphabeta', 'iterative': True}

    # Create a collection of CPU agents using fixed-depth minimax or alpha beta
    # search, or random selection.  The agent names encode the search method
    # (MM=minimax, AB=alpha-beta) and the heuristic function (Null=null_score,
    # Open=open_move_score, Improved=improved_score). For example, MM_Open is
    # an agent using minimax search with the open moves heuristic.
    mm_agents = [Agent(CustomPlayer(score_fn=h, **MM_ARGS),
                       "MM_" + name) for name, h in HEURISTICS]
    ab_agents = [Agent(CustomPlayer(score_fn=h, **AB_ARGS),
                       "AB_" + name) for name, h in HEURISTICS]
    random_agents = [Agent(RandomPlayer(), "Random")]

    # ID_Improved agent is used for comparison to the performance of the
    # submitted agent for calibration on the performance across different
    # systems; i.e., the performance of the student agent is considered
    # relative to the performance of the ID_Improved agent to account for
    # faster or slower computers.
    test_agents = [Agent(CustomPlayer(score_fn=improved_score, **CUSTOM_ARGS), "ID_Improved"),
                   Agent(CustomPlayer(score_fn=custom_score, **CUSTOM_ARGS), "ID_Custom")]

    print(DESCRIPTION)
    print("{:^74}".format("*************************"))
    print("{:^74}".format("Playing Matches"))
    print("{:^74}".format("*************************"))

    agents = random_agents + mm_agents + ab_agents
    play_round(agents, test_agents, NUM_MATCHES)

if __name__ == "__main__":
    main()
