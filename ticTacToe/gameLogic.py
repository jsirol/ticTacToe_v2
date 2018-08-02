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
        self.grid = np.array([" " for x in range(0, dimension**2)]).reshape((dimension, dimension))

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
        self.grid = np.array([" " for x in range(0, self.dimension**2)]).reshape((self.dimension, self.dimension))

    def grid_to_string(self):
        s = "    " + " | ".join(map(lambda x: "{:2s}".format(str(x)), range(0, self.dimension))) + "\n"
        s += "--" + "-----" * self.dimension + "\n"
        for i in range(0, self.dimension):
            s += "{:2s}".format(str(i)) + "   "
            for j in range(0, self.dimension):
                if j < self.dimension - 1:
                    s += "{:1s} |  ".format(self.grid[i, j])
                else:
                    s += "{:1s}\n".format(self.grid[i, j])
        return s

    def test_coordinate_for_win(self, coord, test_mark, end_condition_length):

        row = coord[0]
        col = coord[1]
        winning_streak = None  # on canvas ((y0, x0), (y1, x1))

        if not self.is_valid_coord(coord):
            return False, winning_streak
        # check if move was a winning move
        counter = 0
        # horizontal
        for c in range(col - end_condition_length + 1, col + end_condition_length):
            if self.is_valid_coord((row, c)):
                if self.get_mark((row, c)) == test_mark:
                    counter += 1
                else:
                    counter = 0
            if counter == end_condition_length:
                winning_streak = ((row, c - end_condition_length + 1), (row, c))
                return True, winning_streak

        counter = 0
        # vertical
        for r in range(row - end_condition_length + 1, row + end_condition_length):
            if self.is_valid_coord((r, col)):
                if self.get_mark((r, col)) == test_mark:
                    counter += 1
                else:
                    counter = 0
                if counter == end_condition_length:
                    winning_streak = (r, col), (r - end_condition_length + 1, col)
                    return True, winning_streak

        counter = 0
        # diagonal left-right top-down
        r = range(row - end_condition_length + 1, row + end_condition_length)
        c = range(col - end_condition_length + 1, col + end_condition_length)
        for ii in range(0, len(r)):
            if self.is_valid_coord((r[ii], c[ii])):
                if self.get_mark((r[ii], c[ii])) == test_mark:
                    counter += 1
                else:
                    counter = 0
                if counter == end_condition_length:
                    winning_streak = (r[ii] - end_condition_length + 1, c[ii] - end_condition_length + 1), (r[ii], c[ii])
                    return True, winning_streak

        counter = 0
        # diagonal right-left top-down
        c = range(col + end_condition_length - 1, col - end_condition_length, -1)
        r = range(row - end_condition_length + 1, row + end_condition_length)
        for ii in range(0, len(c)):
            if self.is_valid_coord((r[ii], c[ii])):
                if self.get_mark((r[ii], c[ii])) == test_mark:
                    counter += 1
                else:
                    counter = 0
                if counter == end_condition_length:
                    winning_streak = (r[ii] - end_condition_length + 1, c[ii] + end_condition_length - 1), (r[ii], c[ii])
                    return True, winning_streak

        return False, winning_streak


"""
This encodes the player behavior.
"""


class Player:

    def __init__(self, mark):
        self.mark = mark

    def get_move(self, game_state):
        raise NotImplementedError("Will be implemented by subclasses!")


class HumanPlayer(Player):
    def __init__(self, mark):
        super(HumanPlayer, self).__init__(mark)

    def get_move(self, game_state):
        row = int(input("Give the row {}-{}: ".format(0, game_state.grid.dimension - 1)))
        col = int(input("Give the column {}-{}: ".format(0, game_state.grid.dimension - 1)))
        # index = int(input("Give a free square index for move: "))
        # row, col = index // game_state.grid.dimension, index % game_state.grid.dimension
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

    def initialize_game_state(self, turn, x_player, o_player, game_running, turn_count):
        self.turn = turn
        self.x = x_player
        self.o = o_player
        self.game_running = game_running
        self.turn_count = turn_count
        self.grid.clear_grid()

    def play_turn(self, next_coord):
        if next_coord is None:
            next_coord = (-1, -1)
        while not (self.grid.is_valid_coord(next_coord) and self.grid.is_free(next_coord)):
            if self.turn == "X":
                next_coord = self.x.get_move(self)
            else:
                next_coord = self.o.get_move(self)

        # do the move and update game state
        self.grid.place_mark(next_coord, self.turn)
        move_won, winning_streak = self.grid.test_coordinate_for_win(next_coord, self.turn, self.end_condition_length)
        self.turn_count += 1

        if move_won:
            self.game_running = False
        elif self.turn_count + 1 == self.grid.grid.size:
            self.game_running = False

        if not move_won:
            if self.turn == "O":
                self.turn = "X"
            else:
                self.turn = "O"

        return move_won, winning_streak


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
            self.display.print_turn_info()

            move_won, winning_streak = gs.play_turn()

            self.display.update_board()

            if move_won:
                self.display.update_winner()
            elif gs.turn_count + 1 == gs.grid.grid.size:
                self.display.update_draw()


if __name__ == "__main__":
    ticTacToe = Game(
        dimension=3,
        turn="X",
        end_condition_length=3)
    ticTacToe.run()
