from network import Network
# Acts as a base class / interface for all kinds of players (agents, human)
class Player:
	def __init__(self, code):
		self.code = code # for identifying O and X
		pass

	# will return (x,y) in the grid as a choice
	# has to return legal move
	def move(self, grid):
		pass

class Human(Player):
	def __init__(self, code):
		super().__init__(code)
	
	def move(self, grid):
		return (int(input("x:")), int(input("y:")))

class Agent(Player):
	def __init__(self, code):
		super().__init__(code)
		# self.network = Network()
	
	def move(self, grid):
		# move logic
		return (0,0)
