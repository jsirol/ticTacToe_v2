from gameLogic import HumanPlayer
from time import sleep


class TextDisplay:

    def __init__(self, game_state, analytics):
        self.game_state = game_state
        self.analytics = analytics

    def __print_turn_info(self):
        if not self.analytics:
            print("Move #{}. It's {}'s turn.".format(self.game_state.turn_count + 1, self.game_state.turn))

    def __print_board(self):
        grid = self.game_state.grid
        if not self.analytics:
            print(grid.grid_to_string())

    def __print_game_end(self, move_won, turn):
        if not self.analytics:
            if move_won:
                print(turn + " wins!")
            elif not self.game_state.game_running and self.game_state.winner is not None:
                print("Draw!")

    def __print_analytics(self):
        if self.analytics:
            cg = self.game_state.game_counter
            if self.game_state.game_counter % 100 == 0:
                print("{:6d}/{:6d} games played, X won {:1.2f}%, O won {:1.2f}%, draw {:1.2f}%".format(
                    cg,
                    self.game_state.NUM_GAMES,
                    100.0 * self.game_state.x_won / cg,
                    100.0 * self.game_state.o_won / cg,
                    100.0 - 100.0 * (self.game_state.x_won + self.game_state.o_won) / cg)
                )

    def mainloop(self):
        gs = self.game_state
        while gs.game_counter < gs.NUM_GAMES:
            self.__print_board()
            while gs.game_running:
                self.__print_turn_info()
                turn, move, move_won, winning_streak = gs.play_turn(None)
                if (gs.turn == "X" and not isinstance(gs.x, HumanPlayer)) or \
                        (gs.turn == "O" and not isinstance(gs.o, HumanPlayer)):
                    sleep(gs.bot_move_draw_delay)

                self.__print_board()
                self.__print_game_end(move_won, turn)

                # initialize new game
                if not gs.game_running:
                    self.__print_analytics()
                    if gs.game_counter < gs.NUM_GAMES:
                        gs.initialize_game_state(
                            turn="X",
                            x_player=gs.o,
                            o_player=gs.x,
                            game_running=True,
                            turn_count=0
                        )

        print("All games finished!")
        exit(0)


def begin_graphics(game_state, analytics=False):
        td = TextDisplay(game_state, analytics)
        td.mainloop()


if __name__ == "__main__":
    import gameLogic as gl
    gs = gl.GameState(3, "X", 3)
    begin_graphics(gs)
