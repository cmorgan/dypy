from dypy.systems.Map import Map
import numpy

class ExponentialMap(Map):
    def __init__(self):
        Map.__init__(self, 'Exponential Map', 'One-dimensional iterated map of an exponential function.')

    def iterate(self, x, r):
        return r * numpy.exp(x)
    
    def derivative(self, x, r):
        return r * numpy.exp(x)
    
    def get_parameter_names(self):
        return 'r'
    
    def get_state_names(self):
        return 'x'