from player import Human, Agent
from game import Game
from random import choices, sample

top_agent_count = 3
opponents = [Agent() for _ in range(50)]
# opponents = [Agent() for _ in range(3000)]
# import pickle
# with open("benchmark_agents.pkl", "wb") as f:
# 	pickle.dump(opponents, f)
# print("Saved 3000 benchmark agents")

# exit()
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
		for agent2 in opponents + top_agents + [Agent() for _ in range(5)]:
			game.match(agent1, agent2)
			game.match(agent2, agent1)
	
	return sorted(agents, key=lambda a:a.fitness(), reverse=True)[:top_agent_count]


game = Game()

top_agents = [Agent() for _ in range(top_agent_count)]
generations = 100
print("Generation Count:", generations)
for i in range(generations):
	top_agents = evolve(i+1,top_agents)
	# print(f"Agent {top_agent.code} Games: {top_agent.games}, Score: {top_agent.score}")


# play top_agent with benchmark agents
import pickle
benchmark_agents = None
with open("benchmark_agents.pkl", "rb") as f:
	benchmark_agents = pickle.load(f)
print(f"[INFO] Loaded {len(benchmark_agents)} agents.")
top_agent = max(top_agents, key=lambda a: a.fitness())
top_agent.reset_score()
for agent in benchmark_agents:
	game.match(agent, top_agent)
	game.match(top_agent, agent)


# for i in range(2):
# 	random = Agent(f"Random {i}")
# 	print(f"Top Agent 1 (O) v random {i} (X): ", end="")
# 	game.match(top_agents[0], random, draw_board=True, print_result=True)
# 	print(f"random {i} (O) v Top Agent 1 (X): ", end="")
# 	game.match(random, top_agents[0], draw_board=True, print_result=True)

print(f"Top agent score for {len(benchmark_agents)} random players:")
print(top_agent)
# play the best agent with human
# while(input("Play more? ") == '1'):
# 	human_player = Human("Human")
# 	game.match(top_agent, human_player, draw_board=True)