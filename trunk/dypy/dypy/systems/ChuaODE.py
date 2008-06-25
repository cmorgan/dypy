import numpy
from dypy.systems.ODE import ODE

class ChuaODE(ODE):
    def __init__(self):
        ODE.__init__(self, 'Chua\'s Circuit')
    
    def f(self, x, m0, m1):
        if x >= 1:
            return m1*x + (m0 - m1)
        elif numpy.abs(x) <= 1:
            return m0*x
        else:
            return m1*x - (m0 - m1)
    
    def derivative(self, (x, y, z), (alpha, beta, m0, m1)):
        xdot = alpha * (y - x - self.f(x, m0, m1))
        ydot = x - y + z
        zdot = -beta * y
        
        return numpy.array([xdot, ydot, zdot])
    
    def get_parameter_names(self):
        return ['alpha', 'beta', 'm0', 'm1']
    
    def get_state_names(self):
        return ['f(x)', 'f(y)', 'f(z)']