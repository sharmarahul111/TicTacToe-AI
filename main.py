from player import Human, Agent
from game import Game
from random import choices, sample

top_agent_count = 5
opponents = [Agent() for _ in range(100)]
# opponents = [Agent() for _ in range(1000)]
# import pickle
# with open("benchmark_agents.pkl", "wb") as f:
# 	pickle.dump(opponents, f)
# print("Saved 1000 benchmark agents")

# exit()
# takes the best players
# adds some mutations and random players
# makes them compete, returns the best player
def evolve(gen_count, top_agents):
	print(f"Generation: {gen_count}, Last top agent ({top_agents[0].fitness()}): {top_agents[0]}")
	agents = top_agents.copy()
	for top_agent in top_agents:
		agents += top_agent.mutate(6, diversity=.01) + top_agent.mutate(2,diversity=.15)
	# opponents = [Agent() for _ in range(10)]

	for a in agents:
		a.reset_score()

	# matchmaking
	for agent1 in agents:
		for agent2 in opponents + top_agents:
			game.match(agent1, agent2)
			game.match(agent2, agent1)
	
	return sorted(agents, key=lambda a:a.fitness(), reverse=True)[:top_agent_count]


game = Game()

top_agents = [Agent()]*top_agent_count
generations = 20
print("Generation Count:", generations)
for i in range(generations):
	top_agents = evolve(i+1,top_agents)
	# print(f"Agent {top_agent.code} Games: {top_agent.games}, Score: {top_agent.score}")


# play top_agent with benchmark agents

top_agent = max(top_agents, key=lambda a: a.fitness())
top_agent.reset_score()
random_count = 1000
for i in range(random_count):
	random = Agent(f"Random {i}")
	game.match(random, top_agent)
	game.match(top_agent, random)


# for i in range(2):
# 	random = Agent(f"Random {i}")
# 	print("Random (O) v Top Agent (X): ", end="")
# 	game.match(random, top_agent, draw_board=True, print_result=True)
# 	print("Top Agent (O) v Random (X): ", end="")
# 	game.match(top_agent, random, draw_board=True, print_result=True)

print(f"Top agent score for {random_count} random players:")
print(top_agent)
# play the best agent with human
# human_player = Human("Human")
# game.match(top_agent, human_player, draw_board=True)