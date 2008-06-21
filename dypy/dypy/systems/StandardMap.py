import numpy
from dypy.systems.Map import Map

class StandardMap(Map):
    def __init__(self):
        Map.__init__(self, 'Standard Map')
        
    def iterate(self, (x, y), k):
        y_new = y + k*numpy.sin(x)
        return (x + y_new) % (2.0*pi), y_new % (2.0*pi)
    
    # 6/08, http://mathworld.wolfram.com/StandardMap.html
    def get_state_names(self):
        return ['x', 'y']

    def get_parameter_names(self):
        return 'k'