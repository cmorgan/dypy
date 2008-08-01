from dypy.systems.Map import Map
import numpy

class CircleMap(Map):
    def __init__(self):
        Map.__init__(self, 'Circle Map', 'A simplified model of the phase-locked loop in electronics.')

    def iterate(self, theta, (k, omega)):
        return theta + omega - k/(2*numpy.pi) * numpy.sin(2*numpy.pi*theta)
    
    # fix
    def derivative(self, x, r):
        return -r * numpy.sin(x)
    
    def get_parameter_names(self):
        return ['k', 'omega']

    def get_state_names(self):
        return ['theta']