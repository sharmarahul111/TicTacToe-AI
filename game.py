import numpy as np
from random import choice
class Game:
	def __init__(self):
		# 0 = empty
		# 1 = player_A
		# -1 = player_B
		self.grid = np.zeros((3,3), dtype=int)
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

	def play(self, player, code):
		# it is expected that the players return valid move
		(x,y) = player.move(self.grid)
		self.grid[x][y] = code

	def check_game_over(self):
		# print(np.count_nonzero(self.grid))
		# check if the cells are filled
		if np.count_nonzero(self.grid) == 9:
			return True
		if self.check_match_three():
			game_over = True
		return False # the game isn't over
	
	def check_match_three(self):
		winner = 0
		# check for win/lose condition
		# check matching rows
		for i in range(3):
			if (self.grid[i][0] != 0) and np.all(self.grid[i] == self.grid[i][0]):
				winner = self.grid[i][0]

		# check matching columns
		for i in range(3):
			if (self.grid[:,i][0] != 0) and np.all(self.grid[:, i] == self.grid[:,i][0]):
				winner = self.grid[:,i][0]
		
		# check diagonals
		# major
		arr = np.zeros(3, dtype=int)
		for i in range(3):
			arr[i] = self.grid[i][i]
		if (arr[0] != 0) and np.all(arr == arr[0]):
			winner = arr[0]
		
		# minor
		for i in range(3):
			arr[i] = self.grid[i][-i-1]
		if (arr[0] != 0) and np.all(arr == arr[0]):
			winner = arr[0]

		return winner


	def match(self, player1, player2, draw_board=False):
		# this method handles the complete start to finish of the match logic
		# logic for game completion and assigning wins/losses
		while not self.check_game_over():
			if self.turn:
				self.play(player1, 1) # player1 = 1
			else:
				self.play(player2, -1) # player2 = -1
			self.turn = not self.turn # change the turn for next round

			if draw_board:
				self.draw()

		score = self.check_match_three()
		# print("Game score: ", self.check_match_three())
		# assuming player_A = 1, player_B = -1
		# TODO: play with different scoring system
		player1.games += 1
		player2.games += 1
		if score == 1:
			player1.score += 3
			player2.score += 0
		elif score == -1:
			player1.score += 1
			player2.score += 0
		else:
			player1.score += 1
			player2.score += 1
		
		if draw_board:
			if score==1:
				print("Winner: ", player1.code)
			elif score==-1:
				print("Winner: ", player1.code)
			else:
				print("Draw")

		self.reset() # reset the board for new games

	def reset(self):
		self.turn = True
		self.grid = np.zeros((3,3), dtype=int)