from dypy.systems.Map import Map

class LogisticMap(Map):
    def __init__(self):
        Map.__init__(self, 'Logistic Map')

    def iterate(self, x, r):
        return r * x * (1-x)
    
    def derivative(self, x, r):
        return r - 2*r*x
    
    def get_parameter_names(self):
        return 'r'

    def get_state_names(self):
        return 'x'