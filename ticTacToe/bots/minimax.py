""""
Implements minimax search with alpha-beta pruning using a handcrafted (not very good) heuristic for board
evaluation.

For this to work (better) on bigger board would need:
a) Better heuristic to evaluate game state.
b) Perhaps a more clever way of pruning candidate moves, so can recurse deeper in game tree.
c) Ordering of the candidate moves in order to prune the search tree as much as possible.
"""

import gameLogic as gl
import numpy as np

MAX_REWARD = 100


class AlphaBetaBot(gl.Player):

    def __init__(self):
        super(AlphaBetaBot, self).__init__()

    def get_move(self, game_state):
        if len(game_state.grid.possible_moves) > 0:
            # Use optimal play under the classic 3x3 tic-tac-toe. Depth 5 = optimal play as it forces draw always.
            if game_state.grid.dimension == 3:
                if game_state.turn == "X":
                    return alpha_beta(game_state, 5, True, simple_heuristic)
                else:
                    return alpha_beta(game_state, 5, False, simple_heuristic)
            else:
                # For bigger game use smaller depth and more complex heuristic.
                if game_state.turn == "X":
                    return alpha_beta(game_state, 0, True, heuristic_with_features)
                else:
                    return alpha_beta(game_state, 0, False, heuristic_with_features)
        else:
            raise IndexError("Bot trying to pick move from empty set of free possible moves.")


# Heuristic(s) to evaluate board position.

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
    x_win = False
    o_win = False
    x_near_win = 0
    o_near_win = 0
    x_improving = 0
    o_improving = 0
    for move in prune_possible_moves(game_state, stride=3):
        if grid.test_coordinate_for_win(move, "X", score, look_ahead=True)[0]:
            x_win = True
        if grid.test_coordinate_for_win(move, "O", score, look_ahead=True)[0]:
            o_win = True
        if (x_win and game_state.turn == "X") or \
                (o_win and game_state.turn == "O"):
            break
        else:
            x_near_win += 1 if grid.test_coordinate_for_win(move, "X", score - 1, look_ahead=True)[0] else 0
            o_near_win += 1 if grid.test_coordinate_for_win(move, "O", score - 1, look_ahead=True)[0] else 0
            x_improving += 1 if grid.test_coordinate_for_win(move, "X", score - 2, look_ahead=True)[0] else 0
            o_improving += 1 if grid.test_coordinate_for_win(move, "O", score - 2, look_ahead=True)[0] else 0

    # Player will win next move or opponent threatens to win.
    if game_state.turn == "X" and x_win is True:
        return MAX_REWARD * 0.9
    elif game_state.turn == "X" and o_win is True:
        return -MAX_REWARD * 0.8
    elif game_state.turn == "O" and o_win is True:
        return -MAX_REWARD * 0.9
    elif game_state.turn == "O" and x_win is True:
        return MAX_REWARD * 0.8
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


# Main alpha-beta routine.
def alpha_beta(node, depth, maximizing_player, h):
    # We actually run alpha-beta on the children of the root node to find optimal action.
    best_move = None
    best = -999 if maximizing_player else 999
    for move in prune_possible_moves(node):
        node.play_turn(move)
        # Returns the final value of the child node.
        value = __alpha_beta_iter(node, depth, -999, 999, not maximizing_player, h)
        node.backtrack_move(move)
        # Update best found value, move tuple.
        if maximizing_player and value >= best:
            best = value
            best_move = move
        elif not maximizing_player and value <= best:
            best = value
            best_move = move
    return best_move


# One iteration of alpha-beta algorithm.
def __alpha_beta_iter(node, depth, alpha, beta, maximizing_player, h):
    value = 999 if not maximizing_player else -999
    if depth == 0 or not node.game_running:
        return h(node)

    for move in prune_possible_moves(node):
        node.play_turn(move)
        if maximizing_player:
            value = max(value, __alpha_beta_iter(node, depth-1, alpha, beta, False, h))
            alpha = max(alpha, value)
        else:
            value = min(value, __alpha_beta_iter(node, depth-1, alpha, beta, True, h))
            beta = min(beta, value)
        node.backtrack_move(move)
        if alpha >= beta:
            break
    return value


