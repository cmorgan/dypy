from dypy.systems.Map import Map

class ExponentialMap(Map):
    def __init__(self):
        Map.__init__(self, 'Exponential Map')

    def iterate(self, x, r):
        return r * exp(x)
    
    def derivative(self, x, r):
        return r * exp(x)
    
    def get_parameter_names(self):
        return 'r'
    
    def get_state_names(self):
        return 'x'