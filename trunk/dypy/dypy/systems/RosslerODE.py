import numpy
from dypy.systems.ODE import ODE

class RosslerODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'Rossler Attractor')
    
    def derivative(self, (x, y, z), (a, b, c)):
        xdot = -y - z
        ydot = x + a*y
        zdot = b + z*(x-c)
        
        return numpy.array([xdot, ydot, zdot])
    
    def get_parameter_names(self):
        return ['a', 'b', 'c']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)']