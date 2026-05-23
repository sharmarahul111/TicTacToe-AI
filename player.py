from numpy import argmax
from network import Network
from random import choices

def generate_id():
	return ''.join(choices("0123456789ABCDEF", k=8))
# Acts as a base class / interface for all kinds of players (agents, human)
class Player:
	def __init__(self, code):
		self.code = code # for identifying O and X
		self.games = 0
		self.score = [0,0,0] # [win, draw, lose]
		# self.score = 0 # 3-win,2-draw,1-lose
		pass

	# will return (x,y) in the grid as a choice
	# has to return legal move
	def move(self, grid):
		pass

	def reset_score(self):
		self.games = 0 # maybe not needed
		self.score = [0,0,0]
	
	def __str__(self):
		s = "Player: "+self.code
		s+= f", Games = {self.games}"
		s+= f", Wins = {self.score[0]}"
		s+= f", Draws = {self.score[1]}"
		s+= f", Loss = {self.score[2]}"
		return s
	
	def fitness(self):
		win = 10
		draw = 3
		loss = -10
		if self.games == 0: return 0
		return (self.score[0]*win +self.score[1]*draw +self.score[2]*loss)/self.games


class Human(Player):
	def __init__(self, code):
		super().__init__(code)
	
	def move(self, grid):
		(y,x) = (int(input("x:")), int(input("y:")))
		return (x-1, y-1)

class Agent(Player):
	def __init__(self, code=None):
		super().__init__(code or generate_id())
		# 9 inputs for each cell having (-1,0,1)
		# 9 outputs as probabilities
		self.network = Network(9,18,9)
	
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
	
	def mutate(self, copies, diversity=.1):
		agents = []
		for i in range(copies):
			agent = Agent()
			agent.network = self.network.mutate(diversity)
			agents.append(agent)
		return agents


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