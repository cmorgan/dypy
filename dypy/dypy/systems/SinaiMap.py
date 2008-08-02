from dypy.systems.Map import Map
import numpy

class SinaiMap(Map):
    def __init__(self):
        Map.__init__(self, 'Sinai Map', ' ')

    def iterate(self, (x, y), alpha):
        return (x + y + alpha*numpy.cos(2*numpy.pi*y)) % 1, (x + 2*y) % 1
    
    # fix
    def derivative(self, x, r):
        return -r * numpy.sin(x)
    
    def get_parameter_names(self):
        return ['alpha']

    def get_state_names(self):
        return ['x', 'y']