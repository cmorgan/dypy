from dypy.systems.Map import Map
import numpy

class TinkerbellMap(Map):
    def __init__(self):
        Map.__init__(self, 'Tinkerbell Map', ' ')

    def iterate(self, (x, y), (a, b, c, d)):
        return x**2 - y**2 + a*x + b*y, 2*x*y + c*x + d*y
    
    # fix
    def derivative(self, x, r):
        return -r * numpy.sin(x)
    
    def get_parameter_names(self):
        return ['a', 'b', 'c', 'd']

    def get_state_names(self):
        return ['x', 'y']