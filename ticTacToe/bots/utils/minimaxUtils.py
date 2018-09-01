"""
Put some utility functions here.
"""

import numpy as np

MAX_REWARD = 100


# This is only for small 3x3 tic-tac-toe.
def simple_heuristic(game_state):
    if game_state.winner == "X":
        return MAX_REWARD
    elif game_state.winner == "O":
        return -MAX_REWARD
    else:
        return 0


def winning_features(game_state):
    grid = game_state.grid
    score = game_state.end_condition_length
    x_win = 0
    o_win = 0
    x_near_win = 0
    o_near_win = 0
    x_improving = 0
    o_improving = 0
    for move in prune_possible_moves(game_state, stride=3):
        x_win += 1 if grid.test_coordinate_for_win(move, "X", score, look_ahead=True)[0] else 0
        o_win += 1 if grid.test_coordinate_for_win(move, "O", score, look_ahead=True)[0] else 0
        x_near_win += 1 if grid.test_coordinate_for_win(move, "X", score - 1, look_ahead=True)[0] else 0
        o_near_win += 1 if grid.test_coordinate_for_win(move, "O", score - 1, look_ahead=True)[0] else 0
        x_improving += 1 if grid.test_coordinate_for_win(move, "X", score - 2, look_ahead=True)[0] else 0
        o_improving += 1 if grid.test_coordinate_for_win(move, "O", score - 2, look_ahead=True)[0] else 0

    if x_win > 0 and game_state.turn == "X":
        return MAX_REWARD * 0.9 + (0.01 if x_win > 1 else 0)
    elif o_win > 0 and game_state.turn == "X":
        return -(MAX_REWARD * 0.8 + (0.01 if o_win > 1 else 0))
    elif o_win > 0 and game_state.turn == "O":
        return -(MAX_REWARD * 0.9 + (0.01 if o_win > 1 else 0))
    elif x_win > 0 and game_state.turn == "O":
        return MAX_REWARD * 0.8 + (0.01 if x_win > 1 else 0)

    # Player can win next move if it was his turn.
    elif x_near_win > 0 or o_near_win > 0:
        x_score = x_near_win * MAX_REWARD * 0.025
        o_score = o_near_win * MAX_REWARD * 0.025
        if game_state.turn == "X":
            x_score = min(4 * x_score, MAX_REWARD * 0.7)
        else:
            o_score = min(4 * o_score, MAX_REWARD * 0.7)
    # Scoring of other positions.
    else:
        x_score = x_improving * MAX_REWARD * 0.001
        o_score = o_improving * MAX_REWARD * 0.001
        if game_state.turn == "X":
            x_score = min(2 * x_score, MAX_REWARD * 0.1)
        else:
            o_score = min(2 * o_score, MAX_REWARD * 0.1)
    return x_score - o_score


def heuristic_with_features(game_state):
    # Terminal positions
    if game_state.winner == "X":
        return MAX_REWARD
    elif game_state.winner == "O":
        return -MAX_REWARD
    elif not game_state.game_running:
        return 0
    else:
        return winning_features(game_state)


"""
Prunes moves so that they are max stride points away from the last move coordinate.
This was meant to be used with bigger game board.
"""


def prune_possible_moves(game_state, stride=2):

    def dist(x, y):
        return np.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

    def taken_coordinates():
        return {(x, y)
                for x in range(0, game_state.grid.dimension)
                for y in range(0, game_state.grid.dimension)
                if game_state.grid.grid[x, y] in ["X", "O"]}

    taken = taken_coordinates()
    pruned_moves = set()
    # 1st move
    if len(taken) == 0:
        pruned_moves.add(game_state.grid.possible_moves.pop())
    else:
        # 2nd move onwards
        for move in game_state.grid.possible_moves:
            for coord in taken:
                if dist(move, coord) < stride:
                    pruned_moves.add(move)
                    break
    return pruned_moves
