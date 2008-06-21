import dypy.gui.utils as utils
import wx

class MainPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		self.main = utils.get_main_window(parent)

		utils.debug("MainPanel: Panel initialized.")
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.nlds_label = wx.StaticText(self, wx.ID_ANY, "Select a dynamical system:")
		self.nlds_combo = wx.Choice(self, wx.ID_ANY, choices = [])
		self.nlds_about = wx.TextCtrl(self, wx.ID_ANY, value = "", style = wx.TE_READONLY | wx.TE_WORDWRAP | wx.TE_MULTILINE)
		self.nlds_about.SetInitialSize(size = (10, 20))
		self.nlds_about.Disable()
		
		self.demo_label = wx.StaticText(self, wx.ID_ANY, "Select a demo:")
		self.demo_combo = wx.Choice(self, wx.ID_ANY, choices = [])
		self.demo_about = wx.TextCtrl(self, wx.ID_ANY, value = "", style = wx.TE_READONLY | wx.TE_WORDWRAP | wx.TE_MULTILINE)
		self.demo_about.SetInitialSize(size = (10, 20))
		self.demo_about.Disable()

		self.tool_label = wx.StaticText(self, wx.ID_ANY, "Select a visualization tool:")
		self.tool_combo = wx.Choice(self, wx.ID_ANY, choices = [])
		self.tool_about = wx.TextCtrl(self, wx.ID_ANY, value = "", style = wx.TE_READONLY | wx.TE_WORDWRAP | wx.TE_MULTILINE, size = (10, 10))
		self.tool_about.SetInitialSize(size = (10, 20))
		self.tool_about.Disable()
				
		sizer.Add(self.nlds_label, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.nlds_combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.nlds_about, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)
		
		sizer.Add(self.demo_label, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.demo_combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.demo_about, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)

		sizer.Add(self.tool_label, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.tool_combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.tool_about, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)
		
		self.SetSizer(sizer)
		
		utils.debug("MainPanel: Initializing event triggers.")
		wx.EVT_CHOICE(self, self.nlds_combo.GetId(), self.update_system_about)
		wx.EVT_CHOICE(self, self.demo_combo.GetId(), self.update_demo_about)
		wx.EVT_CHOICE(self, self.tool_combo.GetId(), self.update_tool_about)

		self.update_system_combo()
		self.update_tool_combo()
	
	def update_system_combo(self, event = wx.CommandEvent()):
		utils.debug("MainPanel: Updating system choice box.")
		names = [ system.name for system in self.main.systems ]
		self.nlds_combo.SetItems(names)
		self.nlds_combo.SetSelection(0)
		self.update_system_about()

	def update_system_about(self, event = wx.CommandEvent()):
		nlds_index = self.nlds_combo.GetSelection()
		nlds = self.main.systems[nlds_index]
		
		utils.debug("MainPanel: Updating system description for %s." % nlds.name)
		
		self.nlds_about.SetValue(nlds.description)
		self.update_demo_combo()
		self.main.update_system_panel(nlds)
		#self.main.update_tool_panel(nlds, self.main.active_tool)
	
	def update_demo_combo(self, event = wx.CommandEvent()):
		nlds_index = self.nlds_combo.GetSelection()
		nlds = self.main.systems[nlds_index]
		
		utils.debug("MainPanel: Updating demo choice box for %s." % nlds.name)
		
		system_prefix = nlds.__module__.split('.')[-1]
		names  = []

		for demo in self.main.demos:
			demo_module = demo.__module__.split('.')[-1]
			demo_prefix = demo_module.split('_')[0]
			
			if demo_prefix == system_prefix:
				names.append(demo.name)

		names.append("Custom Parameter Settings")
		
		self.demo_combo.SetItems(names)
		self.demo_combo.SetSelection(0)
		self.update_demo_about()
	
	def update_demo_about(self, event = wx.CommandEvent()):
		demo_name = self.demo_combo.GetStringSelection()

		utils.debug("MainPanel: Updating demo description for %s." % demo_name)
		
		if demo_name == "Custom Parameter Settings":
			self.demo_about.SetValue("Manually enter custom parameter settings on the %s tab." % self.nlds_combo.GetStringSelection())
			return
		
		for demo in self.main.demos:
			if demo.name == demo_name:
				self.demo_about.SetValue(demo.description)
				return	

	def update_tool_combo(self, event = wx.CommandEvent()):
		utils.debug("MainPanel: Updating tool choice box.")
		#names = [ tool.get_name() for tool in self.main.tools ]
		#self.tool_combo.SetItems(names)
		#self.tool_combo.SetSelection(0)
		#self.update_tool_about()
		pass
		
	def update_tool_about(self, event = wx.CommandEvent()):
		tool_index = self.tool_combo.GetSelection()
		tool = self.main.tools[tool_index]

		nlds_index = self.nlds_combo.GetSelection()
		nlds = self.main.systems[nlds_index]
		
		utils.debug("MainPanel: Updating tool description for %s." % tool.get_name())
		
		self.tool_about.SetValue(tool.get_description())
		self.update_demo_combo()
		self.main.update_tool_panel(nlds, tool)	