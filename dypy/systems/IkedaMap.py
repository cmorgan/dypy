from dypy.systems.Map import Map
import numpy

class IkedaMap(Map):
    def __init__(self):
        Map.__init__(self, 'Ikeda Map', 'Plane-wave model of a bistable ring cavity introduced by Ikeda in 1979.')
        
    def iterate(self, (x, y), (a, b, mu)):
        theta = a - b/(x**2 + y**2 + 1)
        return 1 + mu*(x*numpy.cos(theta) - y*numpy.sin(theta)), \
            mu*(x*numpy.sin(theta) - y*numpy.cos(theta))   

    def get_state_names(self):
        return ['x', 'y']

    def get_parameter_names(self):
        return ['a', 'b', 'mu']