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
		self.turn = True # True = Player A, False = Player B
	
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

	def play(self):
		# turn = True for player A, False for player B
		player = self.player_A
		if not self.turn:
			player = self.player_B
		self.turn = not self.turn # change the turn for next round
		# it is expected that the players return valid move
		(x,y) = player.move(self.grid)
		self.grid[x][y] = player.code
		# return (x,y)

	def check_game_over(self):
		game_over = False
		# check if the cells are filled
		if np.count_nonzero(self.grid) == 9:
			game_over = True
			return game_over
		# check for win/lose condition
		


		return game_over


	def match(self, mode="silent"):
		# this method handles the complete start to finish of the match logic
		# logic for game completion and assigning wins/losses
		while not self.check_game_over():
			self.play()
			# for visual purpose
			if mode != "silent":
				self.draw()
