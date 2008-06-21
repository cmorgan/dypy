import numpy
from dypy.systems.ODE import ODE

class LorenzODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'Lorenz Attractor')
    
    def derivative(self, (x, y, z), (sigma, rho, beta)):
        xdot = sigma * (y-x)
        ydot = rho*x - x*z - y
        zdot = beta*z + x*y
        
        return numpy.array([xdot, ydot, zdot])
    
    def get_parameter_names(self):
        return ['sigma', 'rho', 'beta']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)']