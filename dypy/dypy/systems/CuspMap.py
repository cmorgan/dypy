from dypy.systems.Map import Map
import numpy

class CuspMap(Map):
    def __init__(self):
        Map.__init__(self, 'Cusp Map')

    def iterate(self, x, r):
        return 1 - 2*numpy.sqrt(numpy.abs(x/r))
    
    def derivative(self, x, r):
        return -1 / numpy.sqrt(numpy.abs(x/r))
    
    def get_parameter_names(self):
        return 'r'

    def get_state_names(self):
        return 'x'