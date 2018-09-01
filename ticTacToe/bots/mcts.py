"""
Implements a Monte-Carlo Tree Search.
"""

import gameLogic as gl
import numpy as np
import random as rand
import time
from copy import deepcopy


class MCTSBot(gl.Player):

    def __init__(self):
        super(MCTSBot, self).__init__()
        self.states = {}  # holds tuples (wins, losses, visits)
        self.num_sims = 0
        self.root = None
        self.turn = None

    def reset_state(self, game_state):
        self.num_sims = 0
        self.turn = game_state.turn
        self.root = hash(game_state)
        self.states = dict()
        self.states[hash(game_state)] = [0, 0, 0]

    def get_move(self, game_state):
        self.reset_state(game_state)
        return self.mcts(game_state)

    def mcts(self, root, computation_time_ms=2000, max_sims=1000):
        start_time = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - start_time < computation_time_ms and self.num_sims < max_sims:
            leaf = self.traverse(deepcopy(root))  # leaf = unvisited node
            simulation_result = self.rollout(deepcopy(leaf))
            self.backpropagate(leaf, simulation_result)
            self.num_sims += 1
        return self.best_child(root)

    # check if node is fully expanded
    def fully_expanded(self, node):
        expanded = 0
        for move in node.grid.possible_moves:
            node.play_turn(move)
            if hash(node) in self.states:
                expanded += 1
            node.backtrack_move(move)
        return expanded == len(node.grid.possible_moves)

    # calculate utc scores
    def best_uct(self, node, c=np.sqrt(2)):
        best = -999999999
        best_node = deepcopy(node)
        best_move = None
        parent_visits = self.states.get(hash(node))[2]
        for move in node.grid.possible_moves:
            candidate = deepcopy(node)
            candidate.play_turn(move)
            if hash(candidate) in self.states:
                wins, losses, visits = self.states.get(hash(candidate))
                uct = (wins - losses) / visits + c * np.sqrt(np.log(parent_visits) / visits)
                if uct > best:
                    best = uct
                    best_node = candidate
                    best_move = move
        return best_node, best_move

    # traverse to leaf node
    def traverse(self, node):
        while node.game_running and self.fully_expanded(node) and len(node.grid.possible_moves) > 0:
            # pick from children
            node, move = self.best_uct(node)
        if node.game_running:
            # pick unvisited child randomly
            moves_list = deepcopy(node.grid.possible_moves)
            while len(moves_list) > 0:
                move = rand.sample(moves_list, 1)[0]
                node.play_turn(move)
                if hash(node) in self.states:
                    node.backtrack_move(move)
                    moves_list.remove(move)
                else:
                    break
        if hash(node) not in self.states:
            self.states[hash(node)] = [0, 0, 0]
        return node

    @staticmethod
    def rollout_policy(node):
        return rand.sample(node.grid.possible_moves, 1)[0]

    @staticmethod
    def rollout_policy_minimax(node):
        from bots.minimax import AlphaBetaBot
        return AlphaBetaBot().get_move(node)

    # rollout function (simulate playout)
    def rollout(self, node):
        while node.game_running:  # non terminal
            move = self.rollout_policy(node)
            # move = self.rollout_policy_minimax(deepcopy(node))
            node.play_turn(move)
        return node.winner

    # update statistics of node
    def update_node_stats(self, node, winner):
        key = hash(node)
        self.states.get(key)[0] += 1 if self.turn == winner else 0
        self.states.get(key)[1] += 1 if winner is not None and self.turn != winner else 0
        self.states.get(key)[2] += 1

    # backpropagate playout result
    def backpropagate(self, node, result):
        self.update_node_stats(node, result)
        if hash(node) == self.root:
            return
        last_move = node.moves[len(node.moves) - 1]
        node.backtrack_move(last_move)
        self.backpropagate(node, result)

    # final evaluation
    def best_child(self, node):
        best = -1
        best_move = None
        for move in node.grid.possible_moves:
            node.play_turn(move)
            key = hash(node)
            if key in self.states:
                current = max(best, self.states.get(key)[2])
                if current > best:
                    best = current
                    best_move = move
            node.backtrack_move(move)
        return best_move
