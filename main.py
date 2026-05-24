from player import Human, Agent, RandomPlayer
from game import Game
from random import choices, sample

top_agent_count = 3
random = RandomPlayer()

def evolve(gen_count, top_agents):
	print(f"Generation: {gen_count}, Last top agent ({top_agents[0].fitness()}): {top_agents[0]}")
	agents = top_agents.copy()
	for top_agent in top_agents:
		agents += top_agent.mutate(6, diversity=.014) + top_agent.mutate(2,diversity=.15)
	# opponents = [Agent() for _ in range(30)]

	for a in agents:
		a.reset_score()

	# matchmaking
	for agent1 in agents:
		# for agent2 in opponents + top_agents + [Agent() for _ in range(5)]:
		for agent2 in top_agents:
			game.match(agent1, agent2)
			game.match(agent2, agent1)
	for agent in agents:
		for i in range(300):
			game.match(agent, random)
			game.match(random, agent)
	
	return sorted(agents, key=lambda a:a.fitness(), reverse=True)[:top_agent_count]


game = Game()

top_agents = [Agent() for _ in range(top_agent_count)]
generations = 40
print("Generation Count:", generations)
for i in range(generations):
	top_agents = evolve(i+1,top_agents)
	# print(f"Agent {top_agent.code} Games: {top_agent.games}, Score: {top_agent.score}")


random = RandomPlayer()
random_count = 3000
top_agent = max(top_agents, key=lambda a: a.fitness())
top_agent.reset_score()
for i in range(random_count):
	game.match(random, top_agent)
	game.match(top_agent, random)


print(f"Top agent score for {random_count} random players:")
print(top_agent)
# play the best agent with human
# while(input("Play more? ") == '1'):
# 	human_player = Human("Human")
# 	game.match(top_agent, human_player, draw_board=True)