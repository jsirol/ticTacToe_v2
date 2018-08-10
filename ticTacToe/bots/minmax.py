""""
Implements a min-max search with alpha-beta pruning.
"""

import gameLogic as gl
from copy import deepcopy


class AlphaBetaBot(gl.Player):

    def __init__(self):
        super(AlphaBetaBot, self).__init__()

    def get_move(self, game_state):
        if len(game_state.grid.possible_moves) > 0:
            if game_state.turn == "X":
                return alpha_beta(game_state, 2, True)
            else:
                return alpha_beta(game_state, 2, False)
        else:
            raise IndexError("Bot trying to pick move from empty set of free possible moves.")


# Heuristic to evaluate board position.
def simple_heuristic(game_state):
    if game_state.turn == "X":
        if game_state.winner == "X":
            return 10
        elif game_state.game_running:
            return 0.5
        return 0
    else:
        if game_state.winner == "O":
            return -10
        elif game_state.game_running:
            return -0.5
        return 0


# Main alpha-beta routine.
def alpha_beta(node, depth, maximizing_player):
    best_move = None
    if maximizing_player:
        best = -999
    else:
        best = 999
    for move in node.grid.possible_moves:
        value = alpha_beta_iter(node, depth, -999, 999, maximizing_player, simple_heuristic)
        if maximizing_player and value >= best:
            best = value
            best_move = move
        elif not maximizing_player and value <= best:
            best = value
            best_move = move
    return best_move


# One iteration of alpha-beta algorithm.
def alpha_beta_iter(node, depth, alpha, beta, maximizing_player, h):
    initial_value = 999
    if depth == 0 or not node.game_running:
        return h(node)

    if maximizing_player:
        value = -initial_value
        # iterate over possible moves
        for move in node.grid.possible_moves:
            child = deepcopy(node)
            child.play_turn(move)
            value = max(value, alpha_beta_iter(child, depth-1, alpha, beta, False, h))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
            return value
    else:
        value = initial_value
        for move in node.grid.possible_moves:
            child = deepcopy(node)
            child.play_turn(move)
            value = min(value, alpha_beta_iter(child, depth-1, alpha, beta, True, h))
            beta = min(beta, value)
            if alpha >= beta:
                break
            return value




"""
Code template from wikipedia
function alphabeta(node, depth, α, β, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if α ≥ β then
                break (* β cut-off *)
        return value
    else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if α ≥ β then
                break (* α cut-off *)
        return value
(* Initial call *)
alphabeta(origin, depth, −∞, +∞, TRUE)
"""