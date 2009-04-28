import numpy
from dypy.systems.ODE import ODE

class RabinovichODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'Rabinovich-Fabrikant', 'Models stochasticity due to modulation instability in a non-equilibrium dissipative medium.')
    
    def derivative(self, (x, y, z), (alpha, gamma)):
        xdot = y*(z - 1 + x**2) + gamma*x
        ydot = x*(3*z + 1 - x**2) + gamma*y
        zdot = -2*z*(alpha + x*y)
        
        return numpy.array([xdot, ydot, zdot])
    
    def get_parameter_names(self):
        return ['alpha', 'gamma']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)']