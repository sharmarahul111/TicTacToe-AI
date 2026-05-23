from player import Human, Agent
from game import Game
from random import choices

# takes the best players
# adds some mutations and random players
# makes them compete, returns the best player
def evolve(gen_count, top_agent):
	print(f"Generation: {gen_count}, Last top agent score: {top_agent.fitness()}")
	top_agent.reset_score()
	agents = top_agent.mutate(10, .1) + [Agent() for _ in range(5)]

	# matchmaking
	for agent1 in agents:
		for agent2 in agents:
			game.match(agent1, agent2)
			game.match(agent2, agent1)
	
	# print agent status
	# for agent in agents:
	# 	print(f"Agent {agent.code} Games: {agent.games}, Score: {agent.score}")
	
	return max(agents, key=lambda agent: agent.fitness())


game = Game()

top_agent = Agent()
generations = 30
print("Generation Count:", generations)
for i in range(generations):
	top_agent = evolve(i+1,top_agent)
	# print(f"Agent {top_agent.code} Games: {top_agent.games}, Score: {top_agent.score}")


# play top_agent with random player
top_agent.reset_score()
random_count = 30
for i in range(random_count):
	random = Agent(f"Random {i}")
	# print("Random (O) v Top Agent (X): ", end="")
	game.match(random, top_agent, draw_board=False, print_result=False)
	# print("Top Agent (O) v Random (X): ", end="")
	game.match(top_agent, random, draw_board=False, print_result=False)

print(f"Top agent score for {random_count} random players:")
print(top_agent)
# play the best agent with human
# human_player = Human("Human")
# game.match(top_agent, human_player, draw_board=True)