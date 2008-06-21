import numpy
from dypy.systems.Map import Map

class CosineMap(Map):
    def __init__(self):
        Map.__init__(self, 'Cosine Map')

    def iterate(self, x, r):
        return r * numpy.cos(x)
    
    def derivative(self, x, r):
        return -r * numpy.sin(x)
    
    def get_parameter_names(self):
        return 'r'

    def get_state_names(self):
        return 'x'