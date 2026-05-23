import numpy as np
from random import random
class Layer:
	def __init__(self, weights=None, biases=None):
		self.weights = weights
		self.biases = biases

class Network():
	def __init__(self, *args: int):
		self.design = args
		self.layers = []
		for i in range(1,len(args)):
			weights = np.random.randn(args[i-1], args[i])*.2
			biases = np.zeros(args[i])
			self.layers.append(Layer(weights, biases))
	
	def __str__(self):
		s = "\n["
		i=1
		for layer in self.layers:
			s+= f"\n\tlayer[{i}]: "
			# weights
			s+= "\n\t\tWeights ["
			for l in layer.weights:
				s+= "\n\t\t\t"
				s+= str(l)
				s+= " "
			s+= "\n\t\t]"

			# biases
			s+= "\n\t\tBiases ["
			for l in layer.biases:
				s+= "\n\t\t\t"
				s+= str(l)
				s+= " "
			s+= "\n\t\t]"

			i+=1
		s+= "\n]\n"
		return s

	def sigmoid(self, x):
		return 1./(1+np.exp(-x))

	def tanh(self, x):
		return np.tanh(x)

	def forward(self, inp):
		activation = inp
		for i in range(len(self.layers)-1):
			activation = activation @ self.layers[i].weights + self.layers[i].biases
			activation = self.tanh(activation)
		activation = activation @ self.layers[-1].weights + self.layers[-1].biases
		activation = self.sigmoid(activation)
		return activation

	def mutate(self, diversity=.1):
		net = Network(*self.design)
		for i in range(len(self.layers)):
			net.layers[i].weights = self.layers[i].weights + np.random.randn(*self.layers[i].weights.shape)*diversity
			net.layers[i].biases = self.layers[i].biases + np.random.randn(*self.layers[i].biases.shape)*diversity
		return net