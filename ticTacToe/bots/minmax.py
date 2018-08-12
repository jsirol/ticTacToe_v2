""""
Implements min-max search with alpha-beta pruning.
This only works for 3x3 game board as of now.

For this to work on bigger board would likely need:
a) Good heuristic to evaluate game state.
b) Clever pruning of candidate moves.
c) Some sort of ordering of the candidate moves in order to prune the search tree as much as possible.
TL;DR sounds like lot of feature engineering and work to figure out what are good metrics to rate a position, unless
there is sufficient computing power available to increase search depth to some reasonable number (e.g. 5?) which would
catch most obvious winning/losing scenarios.
"""

import gameLogic as gl
import numpy as np

MAX_REWARD = 1


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
                raise NotImplementedError("Only supported size for min-max bot is dim=3.")
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
    # 1st move
    if len(taken) == 0:
        return game_state.grid.possible_moves.pop()
    else:
        # 2nd move onwards
        pruned_moves = set()
        for move in game_state.grid.possible_moves:
            for coord in taken:
                if dist(move, coord) < stride:
                    pruned_moves.add(move)
                    break
        return pruned_moves


"""
New version that backtracks.
"""


# Main alpha-beta routine.
def alpha_beta(node, depth, maximizing_player, h, debug=False):
    # We actually run alpha-beta on the children of the root node to find optimal action.
    best_move = None
    if maximizing_player:
        best = -999
    else:
        best = 999
    for move in prune_possible_moves(node):
        """
        used to do (which though is too expensive for bigger board)...
        child = deepcopy(node)
        child.play_turn(move)
        __alpha_beta_iter(child, depth, -999, 999, not maximizing_player, h)
        now changed to backtracking on just one instance of the game.
        """
        node.play_turn(move)
        # Returns the final value of the child node.
        value = __alpha_beta_iter(node, depth, -999, 999, not maximizing_player, h)
        node.backtrack_move(move)
        if debug:
            print("move: " + str(move) + " with value: " + str(value))
            print("\n")
        # Update best found value, move tuple.
        if maximizing_player and value >= best:
            best = value
            best_move = move
            # shortcut if best possible path found
            if value == MAX_REWARD:
                break
        elif not maximizing_player and value <= best:
            best = value
            best_move = move
            # shortcut if best possible path found
            if value == -MAX_REWARD:
                break
    return best_move


# One iteration of alpha-beta algorithm.
def __alpha_beta_iter(node, depth, alpha, beta, maximizing_player, h):
    initial_value = 999
    if depth == 0 or not node.game_running:
        return h(node)

    if maximizing_player:
        value = -initial_value
        # iterate over possible moves
        for move in prune_possible_moves(node):
            node.play_turn(move)
            value = max(value, __alpha_beta_iter(node, depth-1, alpha, beta, False, h))
            node.backtrack_move(move)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = initial_value
        for move in prune_possible_moves(node):
            node.play_turn(move)
            value = min(value, __alpha_beta_iter(node, depth-1, alpha, beta, True, h))
            node.backtrack_move(move)
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

