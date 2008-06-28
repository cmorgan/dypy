import wx, dypy
import dypy.gui.Widgets as Widgets

# panel for setting system parameters
class SystemPanel(wx.Panel):
	def __init__(self, main, parent, system):
		wx.Panel.__init__(self, parent, wx.ID_ANY)

		self.system = system
		self.main = main

		self.state_names = self.system.get_state_names()
		self.param_names = self.system.get_parameter_names()
		
		# store an array of controls for state and parameter ranges
		self.state_min_controls = []
		self.state_max_controls = []
		
		self.param_min_controls = []
		self.param_max_controls = []
				
		sizer = wx.GridBagSizer(2, 5)
		sizer.SetEmptyCellSize((3, 3))
		
		# track current row
		row = 0	
	
		# add label for state range settings
		sizer.Add(Widgets.LabelText(self, "Select State Range:"), \
		(row,0), (1,4), wx.ALL, 4)	
	
		# make columns for text areas growable
		sizer.AddGrowableCol(1)
		sizer.AddGrowableCol(3)

		# add min, max controls for each state dimension
		for i in range(len(self.state_names)):
			row = row + 1
			
			min_control = Widgets.FloatControl(self, -1)
			max_control = Widgets.FloatControl(self,  1)
			
			# add controls to array
			self.state_min_controls.append(min_control)
			self.state_max_controls.append(max_control)
			
			# bind controls
			min_control.Bind(wx.EVT_KILL_FOCUS, self.update_state)
			max_control.Bind(wx.EVT_KILL_FOCUS, self.update_state)

			# add controls to sizer
			sizer.Add(Widgets.FloatLabel(self, self.state_names[i] + ":"), \
			(row, 0), (1, 1), \
			wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
			
			sizer.Add(min_control, (row, 1), (1, 1), wx.EXPAND)
			
			sizer.Add(Widgets.FloatLabel(self, "to"), \
			(row, 2), (1, 1), wx.ALIGN_CENTER )
			
			sizer.Add(max_control, (row, 3), (1,1), \
			wx.EXPAND | wx.RIGHT, 10)
			
			# skip a row before next
			row = row + 1

		# skip some rows before next section
		row = row + 2

		# add label for parameter range settings
		sizer.Add(Widgets.LabelText(self, "Select Parameter Range:"), \
		(row,0), (1,4), wx.ALL, 4)	
	
		# add min, max controls for each parameter
		for i in range(len(self.param_names)):
			row = row + 1
			
			min_control = Widgets.FloatControl(self, -1)
			max_control = Widgets.FloatControl(self,  1)
			
			# add controls to array
			self.param_min_controls.append(min_control)
			self.param_max_controls.append(max_control)
			
			# bind controls
			min_control.Bind(wx.EVT_KILL_FOCUS, self.update_param)
			max_control.Bind(wx.EVT_KILL_FOCUS, self.update_param)

			# add controls to sizer
			sizer.Add(Widgets.FloatLabel(self, self.param_names[i] + ":"), \
			(row, 0), (1, 1), \
			wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
			
			sizer.Add(min_control, (row, 1), (1, 1), wx.EXPAND)
			
			sizer.Add(Widgets.FloatLabel(self, "to"), \
			(row, 2), (1, 1), wx.ALIGN_CENTER )
			
			sizer.Add(max_control, (row, 3), (1,1), \
			wx.EXPAND | wx.RIGHT, 10)
			
			row = row + 1

		self.update_state()
		self.update_param()
		
		self.SetSizer(sizer)
		dypy.debug("SystemPanel", "Initialized for %s." % system.name)
	
	# update state ranges whenever lose focus
	def update_state(self, event = wx.CommandEvent()):
		ranges = []
		
		# get range strings and convert to floating point numbers
		for i in range(len(self.state_names)):
			min = float(self.state_min_controls[i].GetValue())
			max = float(self.state_max_controls[i].GetValue())
			
			ranges.append((min, max))		

		dypy.debug("SystemPanel", "State ranges updated.")

		# update ranges for the active tool
		self.main.active_tool.set_state_ranges(ranges)

	# update param ranges whenever lose focus
	def update_param(self, event = wx.CommandEvent()):
		ranges = []

		# get range strings and convert to floating point numbers
		for i in range(len(self.param_names)):
			min = float(self.param_min_controls[i].GetValue())
			max = float(self.param_max_controls[i].GetValue())
			
			ranges.append((min, max))		

		dypy.debug("SystemPanel", "Parameter ranges updated.")
		
		# update ranges for the active tool
		self.main.active_tool.set_parameter_ranges(ranges)