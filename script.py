from game import Game
from player import Human, Algorithm
game = Game()

algo = Algorithm()
game.match(algo, algo, draw_board=True, print_result=True)