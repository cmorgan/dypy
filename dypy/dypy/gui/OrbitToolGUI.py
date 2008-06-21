from dypy.tools.OrbitTool import OrbitTool
import dypy.gui.utils as utils
import Pyro.core
import Pyro.naming
import wx

class OrbitToolGUI(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1)
		
		ns = Pyro.naming.NameServerLocator().getNS(host='localhost')
		uri = ns.resolve('OrbitTool')
		self.tool = uri.getAttrProxy()
		utils.debug("OrbitToolGUI: Initialized")
        
		self.tool.set_age_max(1000)
		self.tool.set_density(4)
	
	def update_system(self, system):
		utils.debug("OrbitToolGUI: Updating tool to use %s." % system.name)
		self.tool.set_system(system)
	
	def get_name(self):
		return self.tool.name
	
	def get_description(self):
		return self.tool.description

	def start(self):
		self.tool.start()