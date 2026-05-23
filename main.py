from player import Human, Agent
from game import Game


human_player = Human(code=1)
agent = Agent(code=-1)
game = Game(human_player, agent)
game.match()
game.draw()