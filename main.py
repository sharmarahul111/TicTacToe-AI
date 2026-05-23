from player import Human, Agent
from game import Game


# human_player = Human(code=1)
agent1 = Agent(code=1)
agent2 = Agent(code=-1)
game = Game(agent1, agent2)
for i in range(50):
	game.match()
# game.draw()
print(f"Agent 1: {agent1.score}")
print(f"Agent 2: {agent2.score}")