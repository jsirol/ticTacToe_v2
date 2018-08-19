"""
Implements a Monte-Carlo Tree Search.
"""

import gameLogic as gl
import numpy as np

class MCTSBot(gl.Player):

    def __init__(self):
        super(MCTSBot, self).__init__()
        self.states = {}
        self.num_sims = 0

    def get_move(self, game_state):
        return self.mcts(game_state)


    def mcts(self, root):
        while resources_left(time, computational power):
            leaf = self.traverse(root) # leaf = unvisited node
            simulation_result = rollout(leaf)
            backpropagate(leaf, simulation_result)
        return best_child(root)


    def fully_expanded(self, node):
        expanded = 0
        for move in node.grid.possible_moves:
            node.play_turn(move)
            if hash(node) in self.states:
                expanded += 1
            node.backtrack_move(move)
        return expanded == len(node.grid.possible_moves)


    def best_uct(self, node, c = np.sqrt(2)):
        wins, visits = self.states[hash(node)]
        return wins / visits + c * np.sqrt(np.log(self.num_sims) / visits)

    @staticmethod
    def pick_node(node):
        if len(node.grid.possible_moves) > 0
            move = np.rand.sample(node.grid.possible_moves, 1)[0]
            return node.play_turn(move)
        else:
            return node

    def traverse(self, node):
        while self.fully_expanded(node):
            node = self.best_uct(node)
        return self.pick_node(node)

    def rollout(self, node):
        while node.game_running: # non terminal
            node = self.rollout_policy(node)
        return node.winner


    def rollout_policy(self, node):
        # random rollout policy
        return np.rand.sample(node.grid.possible_moves, 1)[0]

    def backpropagate(self, node, result):
        if is_root(node) return
        node.stats = update_stats(node, result)
        backpropagate(node.parent)

    def best_child(self, node):
        pick child with highest number of visits