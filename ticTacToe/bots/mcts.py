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
        self.explored_sequence = []  # moves for the rollout

    def get_move(self, game_state):
        return self.mcts(game_state)

    def mcts(self, root, computation_time_ms=2000):
        self.turn = root.turn
        self.root = hash(root)
        self.states = dict()
        self.states[hash(root)] = [0, 0, 0]
        start_time = int(round(time.time() * 1000))
        while int(round(time.time() * 1000)) - start_time < computation_time_ms:
            leaf = self.traverse(root)  # leaf = unvisited node
            simulation_result = self.rollout(leaf)
            self.backpropagate(leaf, simulation_result)
            self.num_sims += 1
            self.explored_sequence = []
        return self.best_child(root)

    def fully_expanded(self, node):
        expanded = 0
        for move in node.grid.possible_moves:
            node.play_turn(move)
            if hash(node) in self.states:
                expanded += 1
            node.backtrack_move(move)
        return expanded == len(node.grid.possible_moves)

    def best_ucb1(self, node, c=np.sqrt(2)):
        best = -999999999
        best_node = deepcopy(node)
        best_move = None
        for move in node.grid.possible_moves:
            candidate = deepcopy(node)
            candidate.play_turn(move)
            if hash(candidate) in self.states:
                wins, losses, visits = self.states.get(hash(candidate))
                uct = wins / visits - losses / visits + c * np.sqrt(np.log(self.num_sims) / visits)
                if uct > best:
                    best = uct
                    best_node = candidate
                    best_move = move
        return best_node, best_move

    # traverse to leaf node
    def traverse(self, node):
        while self.fully_expanded(node) and len(node.grid.possible_moves) > 0:
            # pick from children
            node, move = self.best_ucb1(node)
            self.explored_sequence.append(move)
        if len(node.grid.possible_moves) > 0 and node.game_running:
            move = rand.sample(node.grid.possible_moves, 1)[0]
            self.explored_sequence.append(move)
            node.play_turn(move)
        if hash(node) not in self.states:
            self.states[hash(node)] = [0, 0, 0]
        return node

    # rollout function (simulate playout)
    def rollout(self, node):
        while node.game_running:  # non terminal
            move = self.rollout_policy(node)
            self.explored_sequence.append(move)
            node.play_turn(move)
            # adding a node to visited states list
            if hash(node) not in self.states:
                self.states[hash(node)] = [0, 0, 0]

        #print(node.grid.grid_to_string())

        return node.winner

    # default rollout policy (simulation policy)
    def rollout_policy(self, node):
        # random rollout policy
        return rand.sample(node.grid.possible_moves, 1)[0]

    # update statistics of node
    def update_node_stats(self, node, winner):
        key = hash(node)
        # if not node.game_running:
        #     print("winner: " + str(winner) + " add to losses: " + str((1 if winner is not None and self.turn != winner else 0)))
        self.states.get(key)[0] += (1 if self.turn == winner else 0)
        self.states.get(key)[1] += (1 if winner is not None and self.turn != winner else 0)
        self.states.get(key)[2] += 1

    # test for root
    def is_root(self, node):
        return hash(node) == self.root

    # backpropagate playout result
    def backpropagate(self, node, result):
        self.update_node_stats(node, result)
        if self.is_root(node):
            return
        last_move = self.explored_sequence.pop()
        node.backtrack_move(last_move)
        self.backpropagate(node, result)

    # final evaluation
    def best_child(self, node):
        best = -1
        best_move = None
        for move in node.grid.possible_moves:
            node.play_turn(move)
            key = hash(node)
            print(node.grid.grid_to_string())
            visits = self.states.get(key)[2]
            losses = self.states.get(key)[1]
            wins = self.states.get(key)[0]
            print("key: " + str(key) + " wins/losses/simulations: " + str(wins) + "/" + str(losses) + "/" + str(visits))
            current = max(best, self.states.get(key)[2])
            if current > best:
                best = current
                best_move = move
            node.backtrack_move(move)
        return best_move
