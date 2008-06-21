from dypy.gui.FloatValidator import FloatValidator
import dypy.gui.utils as utils
import wx

class SystemPanel(wx.Panel):
	def __init__(self, parent, system):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		
		self.system = system
		self.main = utils.get_main_window(parent)

		utils.debug("SystemPanel: Initialized for %s." % system.name)
		
		self.state_names = self.system.get_state_names()
		self.param_names = self.system.get_parameter_names()
		
		self.state_min_controls = []
		self.state_max_controls = []
		
		self.param_min_controls = []
		self.param_max_controls = []
				
		sizer = wx.GridBagSizer(2, 5)
		row = 0		
		
		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Select State Range:"), (row,0), (1,4), wx.ALL, 4)
	
		utils.debug("SystemPanel: Creating state range controls.")
		for i in range(len(self.state_names)):
			row = row + 1
			
			min_control = wx.TextCtrl(self, wx.ID_ANY, "-1", validator = FloatValidator())
			max_control = wx.TextCtrl(self, wx.ID_ANY,  "1", validator = FloatValidator())
			
			self.state_min_controls.append(min_control)
			self.state_max_controls.append(max_control)
			
			min_control.Bind(wx.EVT_KILL_FOCUS, self.on_update_state)
			max_control.Bind(wx.EVT_KILL_FOCUS, self.on_update_state)

			sizer.Add(wx.StaticText(self, wx.ID_ANY, self.state_names[i] + ":"), (row, 0), (1, 1), wx.ALIGN_RIGHT | wx.LEFT, 20)
			
			sizer.Add(min_control, (row, 1), (1, 1), wx.EXPAND | wx.BOTTOM, 4)
			sizer.Add(wx.StaticText(self, wx.ID_ANY, "to"), (row, 2), (1, 1), wx.ALIGN_CENTER | wx.BOTTOM, 4)
			sizer.Add(max_control, (row, 3), (1,1), wx.EXPAND | wx.BOTTOM | wx.RIGHT, 4)

		row = row + 2
	
		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Select Parameter Range:"), (row, 0), (1, 4), wx.ALL, 4)
		
		utils.debug("SystemPanel: Creating parameter range controls.")
		for i in range(len(self.param_names)):
			row = row + 1
			
			min_control = wx.TextCtrl(self, wx.ID_ANY, "-1", validator = FloatValidator())
			max_control = wx.TextCtrl(self, wx.ID_ANY,  "1", validator = FloatValidator())
			
			self.param_min_controls.append(min_control)
			self.param_max_controls.append(max_control)
			
			min_control.Bind(wx.EVT_KILL_FOCUS, self.on_update_param)
			max_control.Bind(wx.EVT_KILL_FOCUS, self.on_update_param)

			sizer.Add(wx.StaticText(self, wx.ID_ANY, self.param_names[i] + ":"), (row, 0), (1, 1), wx.ALIGN_RIGHT | wx.LEFT, 20)
			
			sizer.Add(min_control, (row, 1), (1, 1), wx.EXPAND | wx.BOTTOM, 4)
			sizer.Add(wx.StaticText(self, wx.ID_ANY, "to"), (row, 2), (1, 1), wx.ALIGN_CENTER | wx.BOTTOM, 4)
			sizer.Add(max_control, (row, 3), (1,1), wx.EXPAND | wx.BOTTOM | wx.RIGHT, 4)
		
		row = row + 2
		
		self.SetSizer(sizer)
		
		self.on_update_state()
		self.on_update_param()
	
	def on_update_state(self, event = wx.CommandEvent()):
		utils.debug("SystemPanel: Updating state range.")

		ranges = []
		
		for i in range(len(self.state_names)):
			min = float(self.state_min_controls[i].GetValue())
			max = float(self.state_max_controls[i].GetValue())
			
			ranges.append((min, max))		

		#if self.main.active_tool:
	#		self.main.active_tool.tool.set_state_ranges(ranges)
		#else:
		#	utils.debug("SystemPanel: Unable to update state range.")
	
	def on_update_param(self, event = wx.CommandEvent()):
		utils.debug("SystemPanel: Updating parameter range.")
		
		ranges = []
		
		for i in range(len(self.param_names)):
			min = float(self.param_min_controls[i].GetValue())
			max = float(self.param_max_controls[i].GetValue())
			
			ranges.append((min, max))		

		#if self.main.active_tool:
	#		self.main.active_tool.tool.set_parameter_ranges(ranges)
	#	else:
	#		utils.debug("SystemPanel: Unable to update parameter range.")	