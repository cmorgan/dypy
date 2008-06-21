import numpy
from dypy.systems.Map import Map

class NeuronMap(Map):
    def __init__(self):
        Map.__init__(self, 'Neuron Map')

    def f(self, x, y, alpha):
        if x <= 0:
            return alpha/(1-x) + y
        elif x < alpha+y:
            return alpha + y
        else:
            return -1
        
    def iterate(self, (x, y), (alpha, mu, sigma)):
          return self.f(x, y, alpha), y - mu*(x+1) + mu*sigma
    
    def get_state_names(self):
        return ['x', 'y']    

    def get_parameter_names(self):
        return 'k'