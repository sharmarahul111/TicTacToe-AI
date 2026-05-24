from numpy import argmax
from network import Network
from random import random, choice, choices
import numpy as np

def generate_id():
	return ''.join(choices("0123456789ABCDEF", k=8))
# Acts as a base class / interface for all kinds of players (agents, human)
class Player:
	def __init__(self, code):
		self.code = code # for identifying O and X
		self.games = 0
		self.bias = 0
		self.score = [0,0,0] # [win, draw, lose]
		# self.score = 0 # 3-win,2-draw,1-lose
		pass

	# will return (x,y) in the grid as a choice
	# has to return legal move
	def move(self, grid):
		pass

	def reset_score(self):
		self.games = 0 # maybe not needed
		self.bias = 0 # good behaviour shouldn't be reset?
		self.score = [0,0,0]
	
	def __str__(self):
		s = "Player: "+self.code
		s+= f", Games = {self.games}"
		s+= f", Wins = {self.score[0]}"
		s+= f", Draws = {self.score[1]}"
		s+= f", Loss = {self.score[2]}"
		return s
	
	def fitness(self):
		# factors
		win = 10
		draw = 5
		loss = -20
		bias = 5 # comes from good/bad behaviour rewards
		if self.games == 0: return 0
		return (self.score[0]*win +self.score[1]*draw +self.score[2]*loss+self.bias*bias)/self.games


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
		self.network = Network(9,9,9,9)

	def reward(self, grid, chosen):
		(x,y) = chosen
		# if makes third matching move
		# rows and columns
		if np.sum(grid[x]) == 2 or np.sum(grid[:,y]) == 2:
			self.bias += 1
		else:
			self.bias -= 1
		# major diagonal
		if x==y and grid[0][0]+grid[1][1]+grid[2][2] == 2:
			self.bias += 1
		else:
			self.bias -= 1
		#minor diagonal
		if x+y==2 and grid[0][2]+grid[1][1]+grid[2][0] == 2:
			self.bias += 1
		else:
			self.bias -= 1

		# if blocks third matching move
		# rows and columns
		if np.sum(grid[x]) == -2 or np.sum(grid[:,y]) == -2:
			self.bias += 1
		else:
			self.bias -= 1
		# major diagonal
		if x==y and grid[0][0]+grid[1][1]+grid[2][2] == -2:
			self.bias += 1
		else:
			self.bias -= 1
		#minor diagonal
		if x+y==2 and grid[0][2]+grid[1][1]+grid[2][0] == -2:
			self.bias += 1
		else:
			self.bias -= 1

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
					probabilities[i][j] = -np.inf # -inf for non sigmoid outputs
		# getting the highest probability index
		index = argmax(probabilities) # returns flat array index
		(x,y) = (index//3, index%3) # convert flat index to 2D

		# check if it was a good move
		self.reward(grid, (x,y))
		# add some variation in play (pick second best move)
		# if random()>.99:
		# 	print("randomized")
		# 	probabilities[x][y] = 0
		# 	index = argmax(probabilities) # returns flat array index
		# 	(x,y) = (index//3, index%3)

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

class RandomPlayer(Player):
	def __init__(self):
		super().__init__("RANDOM")

	def move(self, grid):
		choice = np.random.rand(3,3)
		for i in range(3):
			for j in range(3):
				# set non clear cells probability to 0 or -inf
				if grid[i][j] != 0:
					choice[i][j] = -np.inf
		index = argmax(choice) # returns flat array index
		(x,y) = (index//3, index%3)
		return (x,y)

class Algorithm(Player):
	def __init__(self):
		super().__init__("Algorithm")

	def move(self, grid):
		legals = np.argwhere(grid == 0)
		move_pool = []
		for (x,y) in legals:
			# print(f"x={x} y={y} Row:", grid[x], end=", ")
			# print("Col:", grid[:,y])
			# winning
			# rows and columns
			if np.sum(grid[x]) == 2 or np.sum(grid[:,y]) == 2:
				move_pool.append((x,y))
			# major diagonal
			if x==y and grid[0][0]+grid[1][1]+grid[2][2] == 2:
				move_pool.append((x,y))
			#minor diagonal
			if x+y==2 and grid[0][2]+grid[1][1]+grid[2][0] == 2:
				move_pool.append((x,y))

		if len(move_pool):
			return choice(move_pool)
		
		for (x,y) in legals:
			# if no winning moves, then check blocking
			# rows and columns
			if np.sum(grid[x]) == -2 or np.sum(grid[:,y]) == -2:
				move_pool.append((x,y))
			# major diagonal
			if x==y and grid[0][0]+grid[1][1]+grid[2][2] == -2:
				move_pool.append((x,y))
			#minor diagonal
			if x+y==2 and grid[0][2]+grid[1][1]+grid[2][0] == -2:
				move_pool.append((x,y))

		if len(move_pool):
			return choice(move_pool)

			# if there is only one move by self in that diagonal and no opponent move
			# sum is 1 only if there is one move by self, otherwise +1+1-1 won't give any legal moves there
			# rows and columns
		for (x,y) in legals:
			if np.sum(grid[x]) == 1 or np.sum(grid[:,y]) == 1:
				move_pool.append((x,y))
			# major diagonal
			if x==y and (grid[0][0]+grid[1][1]+grid[2][2] == 1):
				move_pool.append((x,y))
			#minor diagonal
			if x+y==2 and (grid[0][2]+grid[1][1]+grid[2][0] == 1):
				move_pool.append((x,y))
		
		if len(move_pool):
			return choice(move_pool)

		# print("Row sum:", np.sum(grid[x]))
		# print("Col sum:", np.sum(grid[:,y]))
		# if above strategies don't work, return a random choice
		(x,y) = choice(legals)
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