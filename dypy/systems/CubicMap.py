from dypy.systems.Map import Map

class CubicMap(Map):
    def __init__(self):
        Map.__init__(self, 'Cubic Map', 'One-dimensional iterated map of a cubic function.')

    def iterate(self, x, r):
        return r*x - x**3
    
    def derivative(self, x, r):
        return r - 3*x**2
    
    def get_parameter_names(self):
        return 'r'

    def get_state_names(self):
        return 'x'