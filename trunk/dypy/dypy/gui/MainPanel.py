import wx, dypy
import dypy.gui.Widgets as Widgets

# main panel for selecting system, demo, and tool
class MainPanel(wx.Panel):
	def __init__(self, main, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		self.main = main
		
		# gui components
		# combo components contain loaded module/class names
		# about components contain description of current selection
		self.nlds_label = Widgets.LabelText(self, "Select a dynamical system:")
		self.nlds_combo = Widgets.ChoiceList(self)
		self.nlds_about = Widgets.AboutText(self)

		self.demo_label = Widgets.LabelText(self, "Select a demo:")
		self.demo_combo = Widgets.ChoiceList(self)
		self.demo_about = Widgets.AboutText(self)

		self.tool_label = Widgets.LabelText(self, "Select a visualization tool:")
		self.tool_combo = Widgets.ChoiceList(self)
		self.tool_about = Widgets.AboutText(self)

		# begin component layout
		sizer = wx.BoxSizer(wx.VERTICAL)

		# add system components (nlds: nonlinear dynamical system)
		sizer.Add(self.nlds_label, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.nlds_combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.nlds_about, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)
		
		# add demo components
		sizer.Add(self.demo_label, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.demo_combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.demo_about, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)

		# add tool components
		sizer.Add(self.tool_label, 0, wx.ALIGN_LEFT | wx.TOP | wx.LEFT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.tool_combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		sizer.Add(self.tool_about, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)
		
		self.SetSizer(sizer)

		# set event handlers for choices
		wx.EVT_CHOICE(self, self.nlds_combo.GetId(), self.update_system)
		wx.EVT_CHOICE(self, self.demo_combo.GetId(), self.update_demo)
		wx.EVT_CHOICE(self, self.tool_combo.GetId(), self.update_tool)

		# populate the system, demo, and tool choices
		# init_systems will populate the demo choices
		self.init_systems()
		self.init_tools()
		
		dypy.debug("MainPanel", "Panel initialized.")

	# disables system, demo, and tool selection
	# called to prevent selection while a tool is running
	def lockdown(self):
		self.nlds_combo.Disable()
		self.demo_combo.Disable()
		self.tool_combo.Disable()
		
		dypy.debug("MainPanel", "Selection disabled.")

	# renables selection
	# called after tool is stopped
	def unlock(self):
		self.nlds_combo.Enable()
		self.demo_combo.Enable()
		self.tool_combo.Enable()
		
		dypy.debug("MainPanel", "Selection enabled.")

	# populate system choices from main window
	def init_systems(self):
		names = [ system.name for system in self.main.systems ]
		self.nlds_combo.SetItems(names)
		self.nlds_combo.SetSelection(0)
		
		dypy.debug("MainPanel", "System selection initialized.")
		self.update_system()

	# updates system description and valid demos
	def update_system(self, event = wx.CommandEvent()):
		nlds_index = self.nlds_combo.GetSelection()
		nlds = self.main.systems[nlds_index]
		self.nlds_about.SetValue(nlds.description)

		dypy.debug("MainPanel", "System is now %s." % nlds.name)
		
		# populate demos for selected system
		self.init_demos()
		
		# let main window update the system panel
		self.main.update_system_panel(nlds)

	# populate demo choices from main window
	def init_demos(self):
		nlds_index = self.nlds_combo.GetSelection()
		nlds = self.main.systems[nlds_index]

		# get system prefix from demo name
		# should be SystemName_DemoName.py
		system_prefix = nlds.__module__.split('.')[-1]
		names = []

		# checks each loaded demo for name match
		for demo in self.main.demos:
			demo_module = demo.__module__.split('.')[-1]
			demo_prefix = demo_module.split('_')[0]
			
			if demo_prefix == system_prefix:
				names.append(demo.name)
			
		names.append("Custom Parameter Settings")
		
		self.demo_combo.SetItems(names)
		self.demo_combo.SetSelection(0)
		
		dypy.debug("MainPanel", "Found %d demos for %s." %(len(names), nlds.name))
		
		# update description of current demo
		self.update_demo()

	# updates demo description and sets system parameter values
	def update_demo(self, event = wx.CommandEvent()):
		demo_name = self.demo_combo.GetStringSelection()
		
		dypy.debug("MainPanel", "Demo is now %s." % demo_name)

		# set custom parameter settings about message
		if demo_name == "Custom Parameter Settings":
			self.demo_about.SetValue("Manually enter custom parameter " + \
			"settings on the %s tab." % self.nlds_combo.GetStringSelection())
			return
		
		# find demo class reference by name
		for demo in self.main.demos:
			if demo.name == demo_name:
				self.demo_about.SetValue(demo.description)
				self.main.update_parameters(demo)
				return

	# populate tool choice from main window
	def init_tools(self):
		names = [ tool.name for tool in self.main.tools ]
		self.tool_combo.SetItems(names)
		self.tool_combo.SetSelection(0)
		
		dypy.debug("MainPanel", "Tool selection initialized.")
		self.update_tool()

	# update tool description and tool panel
	def update_tool(self, event = wx.CommandEvent()):
		tool_index = self.tool_combo.GetSelection()
		tool = self.main.tools[tool_index]
		
		nlds_index = self.nlds_combo.GetSelection()
		nlds = self.main.systems[nlds_index]
		
		self.tool_about.SetValue(tool.description)
		
		dypy.debug("MainPanel", "Tool is now %s" % tool.name)
		
		# let main window update the tool panel
		self.main.update_tool_panel(nlds, tool)
		
		self.main.system_panel.update_state()
		self.main.system_panel.update_param()

	# returns name of currently selected system
	def get_system_name(self):
		nlds_index = self.nlds_combo.GetSelection()
		nlds = self.main.systems[nlds_index]

		return nlds.name
	
	# sets the currently selected system based on name
	def set_system_by_name(self, name):
		for i in range(0, len(self.main.systems)):
			nlds = self.main.systems[i]
			
			if nlds.name == name:
				self.nlds_combo.SetSelection(i)
				self.update_system()
				return

	# returns name of currently selected tool
	def get_tool_name(self):
		tool_index = self.tool_combo.GetSelection()
		tool = self.main.tools[tool_index]
		
		return tool.name

	# sets the currently selected tool based on name
	def set_tool_by_name(self, name):
		for i in range(0, len(self.main.tools)):
			tool = self.main.tools[i]
			
			if tool.name == name:
				self.tool_combo.SetSelection(i)
				self.update_tool()
				return