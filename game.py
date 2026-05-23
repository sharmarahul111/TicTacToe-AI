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

	def play(self, player):
		# it is expected that the players return valid move
		(x,y) = player.move(self.grid)
		self.grid[x][y] = player.code
		# return (x,y)

	def match(self):
		# this method handles the complete start to finish of the match logic
		# logic for game completion and assigning wins/losses
		for i in range(9):
			self.play(self.player_A)
			self.play(self.player_B)
			# for visual purpose
			# (x,y) = self.play(self.player_A)
			# print(f"Player A: {x}, {y}")
			# self.draw()
			# print()
			# (x,y) = self.play(self.player_B)
			# print(f"Player B: {x}, {y}")
			# self.draw()
			# print("--------------------")
