import numpy as np
from random import choice
class Game:
	def __init__(self, player_A, player_B):
		# 0 = empty
		# 1 = player_A
		# -1 = player_B
		self.grid = np.zeros((3,3), dtype=int)
		self.player_A = player_A
		self.player_B = player_B
	
	def randomize(self):
		for i in range(self.grid.shape[0]):
			for j in range(self.grid.shape[1]):
				self.grid[i][j] = choice([0,1,-1])
				# print(j)
	def draw(self):
		print("-"*13)
		for g in self.grid:
			print("|", end="")
			for cell in g:
				if cell == 0: print("   ", end="")
				elif cell == 1: print(" O ", end="")
				elif cell == -1: print(" X ", end="")
				else: print(cell, end="")
				print("|", end="")
			print()
			print("-"*13)

# pass player class objecs instead of 0 and 1 as players
game = Game(0,1)
game.randomize()
game.draw()