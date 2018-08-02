class TextDisplay:
    def __init__(self, game_state):
        self.gameState = game_state

    def print_turn_info(self):
        print("Move #{}. It's {}'s turn.".format(self.gameState.turn_count + 1, self.gameState.turn))

    def update_board(self):
        grid = self.gameState.grid
        print(grid.grid_to_string())

    @staticmethod
    def update_draw():
        print("Draw!")

    def update_winner(self):
        print(self.gameState.get_turn() + " wins!")
