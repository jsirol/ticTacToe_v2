#!/usr/bin/env python3


"""
Start the game here.
"""

import gameLogic as gl

ticTacToe = gl.game(dimension = 3, turn = "X", endConditionLength = 3, display = "text")

ticTacToe.run()