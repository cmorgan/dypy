import numpy
from dypy.systems.ODE import ODE

class VallisODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'Vallis System', 'Model of temperature fluctuations in the equatorial ocean, introduced by Vallis in 1986.')

    def derivative(self, (x, y, z), (mu, a)):
        xdot = mu*y - a*x
        ydot = x*z - y
        zdot = 1 - x*y - z
        
        return numpy.array([xdot, ydot, zdot])
    
    def get_parameter_names(self):
        return ['mu', 'a']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)']    