from dypy.systems.Map import Map

class HenonMap(Map):
    def __init__(self):
        Map.__init__(self, 'Henon Map')
        
    def iterate(self, (x, y), (a, b)):
        return y + 1 - a*x**2, b*x       

    def get_state_names(self):
        return ['x', 'y']

    def get_parameter_names(self):
        return ['a', 'b']