"""
Include game logic here.
"""

import numpy as np

"""
This encodes the play area, aka grid.
Assume all coordinates are given as (row, col) tuples.
"""


class Grid:
    def __init__(self, dimension):
        self.dimension = dimension
        self.grid = np.array([str(x) for x in range(0, dimension**2)]).reshape((dimension, dimension))

    def is_free(self, coord):
        if self.grid[coord[0], coord[1]] not in ["X", "O"]:
            return True
        else:
            return False

    def is_valid_coord(self, coord):
        return (0 <= coord[0] < self.dimension) and (0 <= coord[1] < self.dimension)

    def get_mark(self, coord):
        return self.grid[coord[0], coord[1]]

    def place_mark(self, coord, mark):
        # free square
        if self.is_free(coord):
            self.grid[coord[0], coord[1]] = mark

    def clear_grid(self):
        self.grid = np.array([str(x) for x in range(0, self.dimension**2)]).reshape((self.dimension, self.dimension))

    def grid_to_string(self):
        s = ""
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                if j < self.dimension - 1:
                    s += "{:3s} | ".format(self.grid[i, j])
                else:
                    s += "{:3s}\n".format(self.grid[i, j])
        return s

    def test_coordinate_for_win(self, coord, test_mark, end_condition_length):

        row = coord[0]
        col = coord[1]

        if not self.is_valid_coord(coord):
            return False
        # check if move was a winning move
        counter = 0
        # horizontal
        for h in range(col - end_condition_length + 1, col + end_condition_length):
            if self.is_valid_coord((row, h)):
                if self.get_mark((row, h)) == test_mark:
                    counter += 1
                else:
                    counter = 0
            if counter == end_condition_length:
                return True

        counter = 0
        # vertical
        for v in range(row - end_condition_length + 1, row + end_condition_length):
            if self.is_valid_coord((v, col)):
                if self.get_mark((v, col)) == test_mark:
                    counter += 1
                else:
                    counter = 0
                if counter == end_condition_length:
                    return True

        counter = 0
        # diagonal left-right top-down
        v = range(row - end_condition_length + 1, row + end_condition_length)
        h = range(col - end_condition_length + 1, col + end_condition_length)
        for ii in range(0, len(v)):
            if self.is_valid_coord((v[ii], h[ii])):
                if self.get_mark((v[ii], h[ii])) == test_mark:
                    counter += 1
                else:
                    counter = 0
                if counter == end_condition_length:
                    return True

        counter = 0
        # diagonal right-left top-down
        h = range(col + end_condition_length - 1, col - end_condition_length, -1)
        v = range(row - end_condition_length + 1, row + end_condition_length)
        for ii in range(0, len(h)):
            if self.is_valid_coord((v[ii], h[ii])):
                if self.get_mark((v[ii], h[ii])) == test_mark:
                    counter += 1
                else:
                    counter = 0
                if counter == end_condition_length:
                    return True
        return False


"""
This encodes the player behavior.
"""


class Player:

    def __init__(self, mark):
        self.mark = mark

    def get_mark(self):
        return self.mark

    def get_move(self, game_state):
        raise NotImplementedError("Will be implemented by subclasses!")


class HumanPlayer(Player):
    def __init__(self, mark):
        super(HumanPlayer, self).__init__(mark)

    def get_move(self, game_state):
        # row = int(input("Give the row {}-{}: ".format(0, game_state.grid.dimension - 1)))
        # col = int(input("Give the column {}-{}: ".format(0, game_state.grid.dimension - 1)))
        index = int(input("Give a free square index for move: "))
        row, col = index // game_state.grid.dimension, index % game_state.grid.dimension
        print("({},{})".format(row, col))
        return row, col


"""
This encodes the player behavior.
"""


class GameState:
    def __init__(self, dimension, turn, end_condition_length):
        self.grid = Grid(dimension)
        self.turn = turn
        self.x = HumanPlayer("X")
        self.o = HumanPlayer("O")
        self.end_condition_length = end_condition_length
        self.game_running = True
        self.turn_count = 0

    def get_grid(self):
        return self.grid

    def get_turn(self):
        return self.turn

    def get_x(self):
        return self.x

    def get_o(self):
        return self.o

    def get_end_condition_length(self):
        return self.end_condition_length

    def get_game_running(self):
        return self.game_running

    def set_turn(self, turn):
        self.turn = turn

    def set_game_running(self, state):
        self.game_running = state


"""
This contains the main game logic
"""


class Game:
    def __init__(self, dimension, turn, end_condition_length, display="text"):
        self.gameState = GameState(dimension, turn, end_condition_length)
        if display == "text":
            import textDisplay as td
            self.display = td.TextDisplay(self.gameState)

    def run(self):
        gs = self.gameState
        self.display.update_board()

        while self.gameState.game_running:
            self.display.print_turn()

            next_coord = (-1, -1)
            while not (gs.grid.is_valid_coord(next_coord) and gs.grid.is_free(next_coord)):
                if gs.turn == "X":
                    next_coord = gs.get_x().get_move(gs)
                else:
                    next_coord = gs.get_o().get_move(gs)

            # do the move and update game state
            gs.grid.place_mark(next_coord, gs.turn)
            move_won = gs.grid.test_coordinate_for_win(next_coord, gs.turn, gs.end_condition_length)
            gs.turn_count += 1
            self.display.update_board()

            if move_won:
                gs.set_game_running(False)
                self.display.update_winner()
            elif gs.turn_count + 1 == gs.grid.grid.size:
                gs.set_game_running(False)
                self.display.update_draw()

            if gs.turn == "O":
                gs.set_turn("X")
            else:
                gs.set_turn("O")


if __name__ == "__main__":
    ticTacToe = Game(
        dimension=3,
        turn="X",
        end_condition_length=3)
    ticTacToe.run()
