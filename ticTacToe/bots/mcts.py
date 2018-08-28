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
        self.num_sims = 0
        self.turn = game_state.turn
        self.root = hash(game_state)
        self.states = dict()
        self.states[hash(game_state)] = [0, 0, 0]
        self.explored_sequence = []  # moves for the rollout
        return self.mcts(game_state)

    def computation_resources(self, num_sims=None, computation_time_ms=None, start_time=None):
        if num_sims is None and computation_time_ms is None:
            raise ValueError("num_sims and computation_time_ms cannot both be None.")
        if num_sims is None and start_time is None:
            raise ValueError("start_time not set when using time limit for computation.")
        if num_sims is not None:
            return self.num_sims < num_sims
        else:
            return int(round(time.time() * 1000)) - start_time < computation_time_ms

    def mcts(self, root, computation_time_ms=2000):
        start_time = int(round(time.time() * 1000))
        while self.computation_resources(num_sims=200, computation_time_ms=computation_time_ms, start_time=start_time):
            leaf = self.traverse(deepcopy(root))  # leaf = unvisited node
            simulation_result = self.rollout(deepcopy(leaf))
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
            self.explored_sequence.append(move)
        if node.game_running:
            # pick unvisited child randomly
            moves_list = deepcopy(node.grid.possible_moves)
            candidate = rand.sample(moves_list, 1)[0]  # in case all nodes are already visited
            while True:
                move = rand.sample(moves_list, 1)[0]
                node.play_turn(move)
                if hash(node) in self.states:
                    node.backtrack_move(move)
                    moves_list.remove(move)
                if len(moves_list) == 0:
                    self.explored_sequence.append(candidate)
                    break
                else:
                    self.explored_sequence.append(move)
                    break
        if hash(node) not in self.states:
            self.states[hash(node)] = [0, 0, 0]
        return node

    # rollout function (simulate playout)
    def rollout(self, node):
        while node.game_running:  # non terminal
            move = rand.sample(node.grid.possible_moves, 1)[0]
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
            if key in self.states:
                wins, losses, visits = self.states.get(key)
                current = max(best, self.states.get(key)[2])
                #print(node.grid.grid_to_string())
                #print("win/loss/draw=visits:  {}/{}/{}={}".format(wins, losses, visits - wins - losses, visits))
                if current > best:
                    best = current
                    best_move = move
            node.backtrack_move(move)
        return best_move
