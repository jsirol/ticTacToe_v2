from tkinter import Tk, Canvas, Frame, font
import numpy as np
from gameLogic import HumanPlayer
from time import sleep


class GraphicsDisplay(Frame):

    def __init__(self, root, game_state, canvas_size=(1200, 800), analytics=False):
        self.root = root
        self.game_state = game_state
        self.analytics = analytics
        self.spacing_x = canvas_size[0] / game_state.grid.dimension
        self.spacing_y = canvas_size[1] / game_state.grid.dimension
        self.canvas_size = canvas_size
        self.highlighted_square = None
        Frame.__init__(self, root)
        self.__init_ui()

    def __init_ui(self):
        self.canvas = Canvas(self.root, width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.bind("<Button-1>", self.__process_click)
        self.canvas.pack()
        self.root.title("Tic Tac Toe")
        self.__draw_grid()

    def __redraw_ui(self):
        self.canvas.delete("all")
        self.__draw_grid()

    def __draw_grid(self):
        # create grid lines on canvas
        for i in range(0, self.game_state.grid.dimension - 1):
            # vertical
            self.canvas.create_line((i + 1) * self.spacing_x, 0, (i + 1) * self.spacing_x, self.canvas_size[1])
            # horizontal
            self.canvas.create_line(0, (i + 1) * self.spacing_y, self.canvas_size[0], (i + 1) * self.spacing_y)

    def __game_coordinate_to_canvas_coordinate(self, game_coord, center=False):
        if not center:
            return game_coord[1] * self.spacing_x, game_coord[0] * self.spacing_y
        else:
            return game_coord[1] * self.spacing_x + self.spacing_x / 2, \
                   game_coord[0] * self.spacing_y + self.spacing_y / 2

    def __canvas_coordinate_to_game_coordinate(self, canvas_coord):
        return canvas_coord[1] // self.spacing_x, canvas_coord[0] // self.spacing_y

    def __draw_mark(self, mark, coord):
        # top left corner on the drawn board
        location_on_canvas = self.__game_coordinate_to_canvas_coordinate(coord)

        if mark == "X":
            self.canvas.create_line(
                location_on_canvas[0],
                location_on_canvas[1],
                location_on_canvas[0] + self.spacing_x,
                location_on_canvas[1] + self.spacing_y,
                fill="red",
                width=2)
            self.canvas.create_line(
                location_on_canvas[0],
                location_on_canvas[1] + self.spacing_y,
                location_on_canvas[0] + self.spacing_x,
                location_on_canvas[1],
                fill="red",
                width=2)

        elif mark == "O":
            self.canvas.create_oval(
                location_on_canvas[0],
                location_on_canvas[1],
                location_on_canvas[0] + self.spacing_x,
                location_on_canvas[1] + self.spacing_y,
                fill="",
                width=2)

        self.highlighted_square = self.canvas.create_rectangle(
            location_on_canvas[0],
            location_on_canvas[1],
            location_on_canvas[0] + self.spacing_x,
            location_on_canvas[1] + self.spacing_y,
            outline="green",
            width=2
        )

    def __remove_highlight(self):
        self.canvas.delete(self.highlighted_square)

    def __draw_streak(self, start_coord, end_coord):
        start = self.__game_coordinate_to_canvas_coordinate(start_coord, center=True)
        end = self.__game_coordinate_to_canvas_coordinate(end_coord, center=True)
        self.canvas.create_line(
            start[0],
            start[1],
            end[0],
            end[1],
            fill="green",
            width=3
        )
        self.canvas.create_text(
            self.canvas_size[0] / 2,
            self.canvas_size[1] / 2,
            text="{:s} wins!".format(self.game_state.winner),
            fill="green",
            font=font.Font(size=44)
        )

    def __draw_draw(self):
        self.canvas.create_text(
            self.canvas_size[0] / 2,
            self.canvas_size[1] / 2,
            text="Draw!",
            fill="green",
            font=font.Font(size=44)
        )

    def __print_analytics(self):
        cg = self.game_state.game_counter
        if self.analytics and self.game_state.NUM_GAMES == cg:
                print("{:6d}/{:6d} games played, X won {:1.2f}%, O won {:1.2f}%, draw {:1.2f}%".format(
                    cg,
                    self.game_state.NUM_GAMES,
                    100.0 * self.game_state.x_won / cg,
                    100.0 * self.game_state.o_won / cg,
                    100.0 - 100.0 * (self.game_state.x_won + self.game_state.o_won) / cg)
                )

    def __process_click(self, event):

        def __play_bot():
            turn, move, move_won, winning_streak = self.game_state.play_turn(None)
            sleep(self.game_state.bot_move_draw_delay)
            if self.last_coordinate is not None:
                self.__remove_highlight()
            self.__draw_mark(turn, move)
            self.last_coordinate = move
            self.update()
            return winning_streak

        def __play_human():
            # This is the coordinate on the game board (note in game board we have order row,col
            # on canvas, x,y (i.e. order is reversed)
            coord = int(np.floor(event.y / self.spacing_y)), int(np.floor(event.x / self.spacing_x))
            if gs.grid.is_valid_coord(coord) and gs.grid.is_free(coord):
                turn, move, move_won, winning_streak = gs.play_turn(coord)
                if self.highlighted_square is not None:
                    self.__remove_highlight()
                self.__draw_mark(turn, move)
                self.last_coordinate = move
                self.update()  # needed to draw before bot starts thinking
                return winning_streak

        gs = self.game_state
        if gs.NUM_GAMES == gs.game_counter:
            self.__print_analytics()
            print("All games finished!")
            exit(0)
        streak = None
        if not gs.game_running:
            # re-initialize game and re-draw board
            gs.initialize_game_state(
                turn="X",
                x_player=gs.x,
                o_player=gs.o,
                game_running=True,
                turn_count=0)
            self.__redraw_ui()
            self.update()
            # initial bot move in case it has first move
            if (gs.turn == "X" and not isinstance(gs.x, HumanPlayer)) or \
                    (gs.turn == "O" and not isinstance(gs.o, HumanPlayer)):
                __play_bot()
        else:
            # place mark on board an update game state
            # case 1. human player turn
            if (gs.turn == "X" and isinstance(gs.x, HumanPlayer)) or \
                    (gs.turn == "O" and isinstance(gs.o, HumanPlayer)):
                streak = __play_human()
        # play bot move(s) if game is still running
        if gs.game_running:
            while (gs.turn == "X" and not isinstance(gs.x, HumanPlayer)) or \
                    (gs.turn == "O" and not isinstance(gs.o, HumanPlayer)):
                streak = __play_bot()
                if not gs.game_running:
                    break

        # announce game has ended (draw streak)
        if not gs.game_running and gs.winner is not None:
            self.__draw_streak(streak[0], streak[1])
            self.update()
        elif not gs.game_running:
            self.__draw_draw()
            self.update()


def begin_graphics(game_state, analytics=False):
    root = Tk()
    root.resizable(False, False)
    gui = GraphicsDisplay(root=root, game_state=game_state, canvas_size=(1200, 800), analytics=analytics)
    root.mainloop()


if __name__ == "__main__":
    import gameLogic as gl
    #gs = gl.GameState(3, "X", 3, num_games=2, x_player=gl.RandomBot(), o_player=gl.RandomBot())
    gs = gl.GameState(3, "X", 3, num_games=2, x_player=gl.HumanPlayer(), o_player=gl.HumanPlayer())
    begin_graphics(gs)