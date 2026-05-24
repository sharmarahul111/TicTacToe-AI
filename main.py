from player import *
from game import Game
from random import choices, sample

top_agent_count = 1
algorithm = Algorithm()
random = RandomPlayer()


def evolve(gen_count, top_agents):
	print(f"Generation: {gen_count}, Last top agent ({top_agents[0].fitness()}): {top_agents[0]}")
	agents = top_agents.copy()
	for top_agent in top_agents:
		agents += top_agent.mutate(8, diversity=.015) + top_agent.mutate(3,diversity=.15)

	for a in agents:
		a.reset_score()

	# matchmaking
	for agent in agents:
		# against self
		for agent2 in top_agents:
			game.match(agent, agent2)
			game.match(agent2, agent)
		# against algorithm
		for i in range(20):
			game.match(agent, algorithm)
			game.match(algorithm, agent)
		#against random
		# for i in range(10):
		# 	game.match(agent, random)
		# 	game.match(random, agent)
		# against agents
		for i in range(20):
			neural_random = Agent()
			game.match(agent, neural_random)
			game.match(neural_random, agent)

	return sorted(agents, key=lambda a:a.fitness(), reverse=True)[:top_agent_count]


game = Game()

top_agents = [Agent() for _ in range(top_agent_count)]
generations = 50
print("Generation Count:", generations)
for i in range(generations):
	top_agents = evolve(i+1,top_agents)
	# print(f"Agent {top_agent.code} Games: {top_agent.games}, Score: {top_agent.score}")


random = RandomPlayer()
count = 2000
top_agent = max(top_agents, key=lambda a: a.fitness())
top_agent.reset_score()
for i in range(count):
	game.match(random, top_agent)
	game.match(top_agent, random)

print("Top agent score:")
print(f"{count} random players:")
print(top_agent)

top_agent.reset_score()
for i in range(count):
	game.match(random, top_agent)
	game.match(top_agent, random)

print(f"{count} algorithm players:")
print(top_agent)
# play the best agent with human
# while(input("Play more? ") == '1'):
# 	human_player = Human("Human")
# 	game.match(top_agent, human_player, draw_board=True)