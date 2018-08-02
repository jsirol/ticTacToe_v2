from tkinter import Tk, Label, Button, Canvas, Frame
import numpy as np


class GraphicsDisplay:

    def __init__(self, root, game_state, canvas_size=(1200, 800)):
        self.root = root
        self.gameState = game_state
        self.spacing_x = canvas_size[0] / game_state.grid.dimension
        self.spacing_y = canvas_size[1] / game_state.grid.dimension
        self.canvas_size = canvas_size
        self.canvas = Canvas(root, width=canvas_size[0], height=canvas_size[1])
        self.canvas.bind("<Button-1>", self.register_click)
        self.canvas.pack()
        root.title("Tic Tac Toe")

    def draw_grid(self):
        # create grid lines on canvas
        for i in range(0, self.gameState.grid.dimension - 1):
            # vertical
            self.canvas.create_line((i + 1) * self.spacing_x, 0, (i + 1) * self.spacing_x, self.canvas_size[1])
            # horizontal
            self.canvas.create_line(0, (i + 1) * self.spacing_y, self.canvas_size[0], (i + 1) * self.spacing_y)

    def draw_mark(self, mark, coord):
        # top left corner on the drawn board
        location_on_canvas = (coord[0] * self.spacing_x, coord[1] * self.spacing_y)

        if mark == "X":
            self.canvas.create_line(
                location_on_canvas[0],
                location_on_canvas[1],
                location_on_canvas[0] + self.spacing_x,
                location_on_canvas[1] + self.spacing_y,
                fill="red")
            self.canvas.create_line(
                location_on_canvas[0],
                location_on_canvas[1] + self.spacing_y,
                location_on_canvas[0] + self.spacing_x,
                location_on_canvas[1],
                fill="red")

        elif mark == "O":
            self.canvas.create_oval(
                location_on_canvas[0],
                location_on_canvas[1],
                location_on_canvas[0] + self.spacing_x,
                location_on_canvas[1] + self.spacing_y,
                fill="blue")

    def register_click(self, event):
        return np.floor(event.x / self.spacing_x), np.floor(event.y / self.spacing_y)

    def update_board(self, coord):
        self.draw_mark(self.gameState.turn, coord)

    @staticmethod
    def update_draw():
        raise NotImplementedError

    def update_winner(self):
        raise NotImplementedError


def initialize_graphics(game_state):
    root = Tk()
    root.resizable(False, False)
    return root, GraphicsDisplay(root=root, game_state=game_state, canvas_size=(1200, 800))


def begin_graphics(root, gui):
    gui.draw_grid()
    root.mainloop()
