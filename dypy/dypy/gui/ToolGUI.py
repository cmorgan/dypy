import Pyro.naming

import wx, dypy

class ToolGUI(wx.Panel):
    def __init__(self, parent, name):
        wx.Panel.__init__(self, parent, -1)
        
        # get tool from tool server
        ns = Pyro.naming.NameServerLocator().getNS(host='localhost')
        uri = ns.resolve(name)
        self.tool = uri.getAttrProxy()
        dypy.debug(name + 'GUI', 'Connected to server.')
        
        self.name = self.tool.name
        self.description = self.tool.description
        
        self.set_parameter_ranges = self.tool.set_parameter_ranges
        self.set_state_ranges = self.tool.set_state_ranges
    
    def update_system(self, system):
        assert 0, 'must be defined'      