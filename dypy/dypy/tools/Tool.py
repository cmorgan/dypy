import Pyro.core
import threading
import dypy

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
        
        self.points_lock = threading.Lock()
        
    def set_system(self, system):
        dypy.debug("DynamicsTool", "Attempting to update system.")
        self.points_lock.acquire()
        
        try:
            self.server.window.set_caption(system.name)
            self.system = system
            self.server.update_tool(self)
            dypy.debug("DynamicsTool", "System set to %s." % system.name)
        finally:
            self.points_lock.release()
    
    def set_parameter_index(self, parameter_index):
        self.points_lock.acquire()
        
        try:
            self.parameter_index = parameter_index
            self.server.update_tool(self)
            dypy.debug("DynamicsTool", "Parameter index updated.")
        finally:
            self.points_lock.release()
    
    def set_state_index(self, state_index):
        self.points_lock.acquire()
        
        try:
            self.state_index = state_index
            self.server.update_tool(self)
            dypy.debug("DynamicsTool", "State index updated.")
        finally:
            self.points_lock.release()
    
    def set_parameter_ranges(self, parameter_ranges):
        self.points_lock.acquire()
        
        try:
            self.parameter_ranges = parameter_ranges
            self.server.update_tool(self)
            dypy.debug("DynamicsTool", "Parameter ranges updated.")
        finally:
            self.points_lock.release()        
    
    def set_state_ranges(self, state_ranges):
        self.points_lock.acquire()
        
        try:
            self.state_ranges = state_ranges
            self.server.update_tool(self)
            dypy.debug("DynamicsTool", "State ranges updated.")
        finally:
            self.points_lock.release()
    
    def init_points(self):
        assert 0, 'must be defined'
    
    def draw_points(self):
        assert 0, 'must be defined'