from game import Game
from player import *
game = Game()

algo = Algorithm()
random = RandomPlayer()
bruteforce = Bruteforce()
for i in range(20):
	game.match(bruteforce, random, draw_board=False, print_result=True)
	game.match(random, bruteforce, draw_board=False, print_result=True)
	game.match(bruteforce, algo, draw_board=False, print_result=True)
	game.match(algo, bruteforce, draw_board=False, print_result=True)