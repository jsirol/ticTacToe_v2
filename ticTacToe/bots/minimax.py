""""
Implements minimax search with alpha-beta pruning using a handcrafted (not very good) heuristic for board
evaluation.

For this to work (better) on bigger board would need:
a) Better heuristic to evaluate game state.
b) Perhaps a more clever way of pruning candidate moves, so can recurse deeper in game tree.
c) Ordering of the candidate moves in order to prune the search tree as much as possible.
"""

import gameLogic as gl
from bots.utils.minimaxUtils import simple_heuristic, heuristic_with_features, prune_possible_moves


class AlphaBetaBot(gl.Player):

    def __init__(self):
        super(AlphaBetaBot, self).__init__()

    def get_move(self, game_state):
        if len(game_state.grid.possible_moves) > 0:
            # Use optimal play under the classic 3x3 tic-tac-toe. Depth 5 = optimal play as it forces draw always.
            if game_state.grid.dimension == 3:
                if game_state.turn == "X":
                    return self.alpha_beta(game_state, 5, True, simple_heuristic)
                else:
                    return self.alpha_beta(game_state, 5, False, simple_heuristic)
            else:
                # For bigger game use smaller depth and more complex heuristic.
                if game_state.turn == "X":
                    return self.alpha_beta(game_state, 0, True, heuristic_with_features)
                else:
                    return self.alpha_beta(game_state, 0, False, heuristic_with_features)
        else:
            raise IndexError("Bot trying to pick move from empty set of free possible moves.")

    # Main alpha-beta routine.
    def alpha_beta(self, node, depth, maximizing_player, h):
        # We actually run alpha-beta on the children of the root node to find optimal action.
        best_move = None
        best = -999 if maximizing_player else 999
        for move in prune_possible_moves(node):
            node.play_turn(move)
            # Returns the final value of the child node.
            value = self.alpha_beta_iter(node, depth, -999, 999, not maximizing_player, h)
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
    def alpha_beta_iter(self, node, depth, alpha, beta, maximizing_player, h):
        value = 999 if not maximizing_player else -999
        if depth == 0 or not node.game_running:
            return h(node)

        for move in prune_possible_moves(node):
            node.play_turn(move)
            if maximizing_player:
                value = max(value, self.alpha_beta_iter(node, depth-1, alpha, beta, False, h))
                alpha = max(alpha, value)
            else:
                value = min(value, self.alpha_beta_iter(node, depth-1, alpha, beta, True, h))
                beta = min(beta, value)
            node.backtrack_move(move)
            if alpha >= beta:
                break
        return value


