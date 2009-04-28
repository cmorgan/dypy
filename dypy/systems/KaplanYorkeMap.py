from dypy.systems.Map import Map
import numpy

class KaplanYorkeMap(Map):
    def __init__(self):
        Map.__init__(self, 'Kaplan-Yorke Map', 'A classically chaotic discrete map with a strange attractor introduced by Kaplan and Yorke in 1979.')
        
    def iterate(self, (x, y), (alpha)):
        return 2*x - numpy.floor(2*x), alpha*y + numpy.cos(4*numpy.pi*x) 

    def get_state_names(self):
        return ['x', 'y']

    def get_parameter_names(self):
        return ['alpha']