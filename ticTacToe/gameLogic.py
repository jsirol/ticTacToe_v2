"""
Include game logic here.
"""

import numpy as np

"""
This encodes the play area, aka grid.
"""
class grid:

	def __init__(self, dimension):
		self.dimension = dimension
		self.grid = np.array([[" " for l in range(0, dimension)] for x in range(0, dimension)])

	def isFree(self, coord):
		return self.grid[coord[1], coord[0]] == " "

	def isValidCoord(self, coord):
		return (0 <= coord[0] < self.dimension) and (0 <= coord[1] < self.dimension)

	def getMark(self, coord):
		return self.grid[coord[1], coord[0]]

	def placeMark(self, coord, mark):
		# free square
		if	self.isFree(coord):
			self.grid[coord[1], coord[0]] = mark
		else:
			print("Error: position ({0}, {1}) is not free!".format(coord[1], coord[0]))

	def clearGrid(self):
		self.grid = np.array([[" " for l in range(0, self.dimension)] for x in range(0, self.dimension)])


"""
This encodes the player behavior.
"""
class player:
	def __init__(self, name, winner):
		self.name = name
		self.winner = False

	def getWinner(self):
		return self.winner

	def getName(self):
		return self.name

"""
This contains the game state.
"""
class gameState:

	def __init__(self, dimension, turn, endConditionLength):
		self.grid = grid(dimension)
		self.turn = turn
		self.x = player("X", False)
		self.o = player("O", False)
		self.endConditionLength = endConditionLength
		self.gameRunning = True
		self.turnCount = 0


	def getGrid(self):
		return self.grid

	def getTurn(self):
		return self.turn

	def getX(self):
		return self.x

	def getO(self):
		return self.o

	def getEndConditionLength(self):
		return self.endConditionLength

	def getGameRunning(self):
		return self.gameRunning

	def setTurn(self, turn):
		self.turn = turn

	def setGameRunning(self, state):
		self.gameRunning = state

	def testCoordinateForWin(self, coord, testTurn):

		row = coord[0]
		col = coord[1]

		if not self.grid.isValidCoord(coord):
			return False
		# check if move was a winning move			
		counter = 0
		# horizontal
		for xx in range(row - self.endConditionLength + 1, row + self.endConditionLength):
			if (self.grid.isValidCoord((xx, col))):
				if (self.grid.getMark((xx, col)) == testTurn):
					counter += 1
				else: counter = 0
			if (counter == self.endConditionLength - 1): 
				return True
			elif (abs(xx - row) < self.endConditionLength - counter): 
				counter = 0
				break

		# vertical
		for yy in range(col - self.endConditionLength + 1, col + self.endConditionLength):
			if (self.grid.isValidCoord((row, yy))):
				if (self.grid.getMark((row, yy)) == testTurn): 
					counter += 1
				else: counter = 0
				if (counter == self.endConditionLength - 1): 
					return True
				elif (abs(yy - col) < self.endConditionLength - counter):
					counter = 0
					break

		# diagonal left-right top-down
		xx = [z for z in range(row - self.endConditionLength + 1, row + self.endConditionLength)]
		yy = [z for z in range(col - self.endConditionLength + 1, col + self.endConditionLength)]
		for ii in range(0, len(xx)):
			if (self.grid.isValidCoord((xx[ii], yy[ii]))):
				if (self.grid.getMark((xx[ii], yy[ii])) == testTurn):
					counter += 1
				else: 
					counter = 0
				if (counter == self.endConditionLength - 1):
					return True
		# diagonal right-left top-down
		xx = [z for z in range(row + self.endConditionLength, row - self.endConditionLength + 1, -1)]
		yy = [z for z in range(col - self.endConditionLength + 1, col + self.endConditionLength)]
		for ii in range(0, len(xx)):
			if (self.grid.isValidCoord((xx[ii], yy[ii]))):
				if (self.grid.getMark((xx[ii], yy[ii])) == testTurn):
					counter += 1
				else: 
					counter = 0
				if (counter == self.endConditionLength - 1):
					return True
		return False


"""
This contains the main game logic
"""
class game:

	def __init__(self, dimension, turn, endConditionLength, display = "text"):
		import textDisplay as td
		self.gameState = gameState(dimension, turn, endConditionLength)

		if display == "text":
			self.display = td.textDisplay(self.gameState)

	def run(self):
		self.display.printBoard()
		while (self.gameState.gameRunning):

			user_coord = (-1, -1)
			# text based game
			while (not self.gameState.grid.isValidCoord(user_coord)):
				print("Move #{}. It's {}'s turn.".format(self.gameState.turnCount + 1, self.gameState.turn))
				row = int(input("Give the column {}-{}: ".format(0, self.gameState.grid.dimension - 1)))
				col = int(input("Give the row: {}-{}: ".format(0, self.gameState.grid.dimension - 1)))
				user_coord = (row, col)


			move_wins = self.gameState.testCoordinateForWin(user_coord, self.gameState.turn)
			# do the move and update game state
			self.gameState.grid.placeMark(user_coord, self.gameState.turn)
			self.gameState.turnCount += 1

			self.display.printBoard()

			if (self.gameState.turn == "O"):
				self.gameState.setTurn("X")
			else: 
				self.gameState.setTurn("O")

			if (move_wins):
				self.gameState.setGameRunning(False)
				print("winner!")
			elif self.gameState.turnCount + 1 == self.gameState.grid.grid.size:
				print("draw!")
				self.gameState.setGameRunning(False)
