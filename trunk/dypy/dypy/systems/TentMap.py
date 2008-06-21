import numpy
from dypy.systems.Map import Map

class TentMap(Map):
    def __init__(self):
        Map.__init__(self, "Tent Map")

    def iterate(self, x, r):
        if x > 0 and x < 0.5:
            return r*x
        else:
            return r - r*x
    
    def derivative(self, x, r):
        if x > 0 and x < 0.5:
            return r
        else:
            return -r
    
    def get_parameter_names(self):
        return 'r'
    
    def get_state_names(self):
        return 'x'