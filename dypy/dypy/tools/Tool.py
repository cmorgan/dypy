import Pyro.core

class Tool(Pyro.core.ObjBase):      
    def __init__(self, **kwds):
        Pyro.core.ObjBase.__init__(self)
        self.name = kwds['name']
        self.description = kwds['description']
        self.server = kwds['server']
 
        self.parameter_index = 0
        self.state_index = 0
        self.parameter_ranges = [(0, 0)]
        self.state_ranges = [(0, 0)]
        
    def set_system(self, system):
        print 'DynamicsTool: Set system to', system
        self.system = system
    
    def set_parameter_index(self, parameter_index):
        self.parameter_index = parameter_index
        self.server.update_tool(self)
    
    def set_state_index(self, state_index):
        self.state_index = state_index
        self.server.update_tool(self)  
    
    def set_parameter_ranges(self, parameter_ranges):
        self.parameter_ranges = parameter_ranges
        self.server.update_tool(self)
    
    def set_state_ranges(self, state_ranges):
        self.state_ranges = state_ranges
        self.server.update_tool(self)
    
    def init_points(self):
        assert 0, 'must be defined'
    
    def draw_points(self):
        assert 0, 'must be defined'