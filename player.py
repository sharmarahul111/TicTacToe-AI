from numpy import argmax
from network import Network
# Acts as a base class / interface for all kinds of players (agents, human)
class Player:
	def __init__(self, code):
		self.code = code # for identifying O and X
		self.games = 0
		# self.score = [0,0,0] # [win, draw, lose]
		self.score = 0 # 3-win,2-draw,1-lose
		pass

	# will return (x,y) in the grid as a choice
	# has to return legal move
	def move(self, grid):
		pass

class Human(Player):
	def __init__(self, code):
		super().__init__(code)
	
	def move(self, grid):
		return (int(input("x:")), int(input("y:")))

class Agent(Player):
	def __init__(self, code):
		super().__init__(code)
		# 9 inputs for each cell having (-1,0,1)
		# 9 outputs as probabilities
		self.network = Network(9,2,9)
	
	def move(self, grid):
		# move logic
		# convert grid to 1D vector
		inp = grid.reshape(1,9)
		probabilities = self.network.forward(inp).reshape(3,3)
		# mask the probabilities for not giving illegal moves
		for i in range(3):
			for j in range(3):
				# set non clear cells probability to 0 or -inf
				if grid[i][j] != 0:
					probabilities[i][j] = 0 # -inf for non sigmoid outputs
		# probability matrix
		# print(probabilities)
		# getting the highest probability index
		index = argmax(probabilities) # returns flat array index
		(x,y) = (index//3, index%3) # convert flat index to 2D
		# print(index)
		# print(f"p[{x}][{y}] = {probabilities[x][y]}")
		return (x,y)

if __name__ == "__main__":
	import numpy as np
	from random import choice
	agent = Agent(code=-1)
	grid = np.zeros((3,3), dtype=int)
	for i in range(grid.shape[0]):
			for j in range(grid.shape[1]):
				grid[i][j] = choice([0,1,-1])
	
	print(grid)
	agent.move(grid)