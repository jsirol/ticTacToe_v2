#!/usr/bin/env python3


"""
Start the game here.
"""

import argparse
import gameLogic as Gl

parser = argparse.ArgumentParser(description='Runs Tic Tac Toe')
parser.add_argument("-d", "--dim", metavar="N", type=int, default=3, help="Create a N by N game board.")
parser.add_argument("--turn", metavar="c", type=str, default="X", help="Starting player (X/O).")
parser.add_argument("--score", metavar="s", type=int, default=3, help="How many marks straight are needed for win.")

args = parser.parse_args()

ticTacToe = Gl.Game(
    dimension=args.dim,
    turn=args.turn,
    end_condition_length=args.score,
    display="text")

ticTacToe.run()
