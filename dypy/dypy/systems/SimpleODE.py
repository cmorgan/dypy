import numpy
from dypy.systems.ODE import ODE

class SimpleODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'Simple System', ' ')
    
    # list with one element is not unpacked like it should be
    def derivative(self, (x, y, z), (mu)):
        xdot = 1 + mu[0]*y*z
        ydot = x - y
        zdot = 1 - x*y
        
        return numpy.array([xdot, ydot, zdot])
    
    def get_parameter_names(self):
        return ['mu']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)']