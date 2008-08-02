from dypy.systems.Map import Map
import numpy

class GingerbreadMap(Map):
    def __init__(self):
        Map.__init__(self, 'Gingerbread Map', ' ')

    def iterate(self, (x, y), none):
        return 1 - y + numpy.abs(x), x
    
    # fix
    def derivative(self, x, r):
        return -r * numpy.sin(x)
    
    def get_parameter_names(self):
        return ['none']

    def get_state_names(self):
        return ['x', 'y']