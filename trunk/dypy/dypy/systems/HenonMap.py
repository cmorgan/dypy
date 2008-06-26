from dypy.systems.Map import Map

class HenonMap(Map):
    def __init__(self):
        Map.__init__(self, 'Henon Map', '2-D iterated map modeling the Poincare section of the Lorenz model, introduced by Michel Henon in 1976.')
        
    def iterate(self, (x, y), (a, b)):
        return y + 1 - a*x**2, b*x       

    def get_state_names(self):
        return ['x', 'y']

    def get_parameter_names(self):
        return ['a', 'b']