from player import Human
from game import Game


human_player = Human(code=1)
human_player2 = Human(code=-1)
game = Game(human_player, human_player2)
game.match()
game.draw()