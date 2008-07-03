import numpy
from dypy.systems.ODE import ODE

class RikitakiODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'Rikitaki Dynamo', 'Model for the dynamics of magnetic pole variation, introduced by Rikitaki in 1958.')

    def derivative(self, (x, y, z, u), (mu, b, c)):
        xdot = -mu*x + y*z
        ydot = -mu*y + x*u
        zdot = 1 - x*y - b*z
        udot = 1 - x*y - c*u
        
        return numpy.array([xdot, ydot, zdot, udot])

    def get_parameter_names(self):
        return ['mu', 'b', 'c']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)', 'f(u)']