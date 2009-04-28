import numpy
from dypy.systems.ODE import ODE

class ElNinoODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'El Nino', ' ')
        self.t = 0
    
    def f(self, a0, a1):
        return a0 + a1*numpy.sin(2 * numpy.pi * self.t)
    
    def derivative(self, (x, y, z), (mu, a0, a1, b, c)):
        xdot = mu*(y - z) - b*(x - self.f(a0, a1))
        ydot = x*z - y + c
        zdot = -x*y - z + c
        self.t += 1
        
        return numpy.array([xdot, ydot, zdot])
    
    def get_parameter_names(self):
        return ['mu', 'a0', 'a1', 'b', 'c']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)']