from tkinter import Tk, Canvas, Frame
import numpy as np


class GraphicsDisplay(Frame):

    def __init__(self, root, game_state, canvas_size=(1200, 800)):
        self.root = root
        self.game_state = game_state
        self.spacing_x = canvas_size[0] / game_state.grid.dimension
        self.spacing_y = canvas_size[1] / game_state.grid.dimension
        self.canvas_size = canvas_size
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

    def __process_click(self, event):
        gs = self.game_state

        if not gs.game_running:
            # re-initialize game and re-draw board
            gs.initialize_game_state(
                turn="X" if gs.turn is "X" else "O",
                x_player=gs.o,
                o_player=gs.x,
                game_running=True,
                turn_count=0)
            self.__redraw_ui()
        else:
            # this is the coordinate on the game board (note in game board we have order row,col
            # on canvas, x,y (i.e. order is reversed)
            coord_game = int(np.floor(event.y / self.spacing_y)), int(np.floor(event.x / self.spacing_x))
            # place mark on board an update game state
            if gs.grid.is_valid_coord(coord_game) and gs.grid.is_free(coord_game):
                self.__draw_mark(gs.turn, coord_game)
                move_won, winning_streak = gs.play_turn(coord_game)
                if not gs.game_running and winning_streak is not None:
                    self.__draw_streak(winning_streak[0], winning_streak[1])


def begin_graphics(game_state):
    root = Tk()
    root.resizable(False, False)
    gui = GraphicsDisplay(root=root, game_state=game_state, canvas_size=(1200, 800))
    root.mainloop()


if __name__ == "__main__":
    import gameLogic as gl
    gs = gl.GameState(15, "X", 5)
    begin_graphics(gs)