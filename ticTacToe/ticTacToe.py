#!/usr/bin/env python3

"""
Start the game here.
"""

import argparse
import gameLogic as gl

"""
Parse command line arguments.
-d, --dim   Dimension of the game grid.
--turn      Mark of the starting player (X/O).
--score     How many straight marks are needed to win the game.
--display   Type of UI (text/gui).
"""


parser = argparse.ArgumentParser(description='Runs Tic Tac Toe')
parser.add_argument("-d", "--dim", metavar="N", type=int, default=3, help="Create a N by N game board.")
parser.add_argument("--score", metavar="s", type=int, default=3, help="How many marks straight are needed for win.")
parser.add_argument("--display", metavar="dt", type=str, default="text", help="UI type (text/gui).")
parser.add_argument("--bot_x", metavar="bx", type=str, default=None, help="Assign bot player to 'X' (None/random).")
parser.add_argument("--bot_o", metavar="bo", type=str, default=None, help="Assign bot player to 'O' (None/random).")
parser.add_argument("--bot_delay", metavar="s", type=float, default=0.5, help="Bot thinking time before move.")
parser.add_argument("--num_games", metavar="n", type=int, default=1, help="Number of games to play.")
parser.add_argument("--analytics",
                    action='store_true',
                    help="Only print analytics (bot vs bot mode does not print UI).")

args = parser.parse_args()

bot_options = {None: gl.HumanPlayer(),
               "random": gl.RandomBot()
               }

x_player = bot_options[args.bot_x]
o_player = bot_options[args.bot_o]

ticTacToe = gl.Game(
    dimension=args.dim,
    end_condition_length=args.score,
    x_player=x_player,
    o_player=o_player,
    display=args.display,
    bot_move_draw_delay=args.bot_delay,
    num_games=args.num_games,
    analytics=False if args.analytics is None else args.analytics)

ticTacToe.run()
