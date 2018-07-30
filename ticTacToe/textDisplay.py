class textDisplay:

	def __init__(self, gameState):
		self.gameState = gameState

	def printBoard(self):
		grid_ref = self.gameState.grid
		for i in range(0, grid_ref.dimension):
			#print(self.board[i])
			for j in range(0, grid_ref.dimension):
				if (j < grid_ref.dimension - 1):
					print("{} | ".format(grid_ref.grid[i, j]), end = "")
				else:
					print("{}\n".format(grid_ref.grid[i, j]))
