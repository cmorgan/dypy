from dypy.tools.OrbitTool import OrbitTool

import Pyro.core
import Pyro.naming

import wx, dypy
import dypy.gui.Widgets as Widgets

class OrbitToolGUI(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1)
		
		# get tool from tool server
		ns = Pyro.naming.NameServerLocator().getNS(host='localhost')
		uri = ns.resolve('OrbitTool')
		self.tool = uri.getAttrProxy()
		dypy.debug("OrbitToolGUI", "Connected to server.")
		
		self.name = self.tool.name
		self.description = self.tool.description
		
		self.set_parameter_ranges = self.tool.set_parameter_ranges
		self.set_state_ranges = self.tool.set_state_ranges

		# gui components: labels
		state_label   = Widgets.LabelText(self, "Select State Axis:")
		param_label   = Widgets.LabelText(self, "Select Varying Parameter:")
		density_label = Widgets.LabelText(self, "Select Maximum Point Density:")
		age_label     = Widgets.LabelText(self, "Select Maximum Point Age:")
		mode_label    = Widgets.LabelText(self, "Select Visualization Mode:")
		
		# gui components: selection
		self.state_choice = Widgets.ChoiceList(self)
		self.param_choice = Widgets.ChoiceList(self)
		
		self.density_slider = Widgets.SimpleSlider(self, 4, 1, 10)
		self.age_slider     = Widgets.SimpleSlider(self, 1000, 1, 2000)

		self.mode_check = Widgets.Checkbox(self, "Show History")

		sizer = wx.BoxSizer(wx.VERTICAL)
		
		sizer.Add(state_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
		sizer.Add(self.state_choice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		
		sizer.Add(param_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
		sizer.Add(self.param_choice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)
		
		sizer.Add(density_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
		sizer.Add(self.density_slider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(2)
		
		sizer.Add(age_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
		sizer.Add(self.age_slider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
		sizer.AddSpacer(10)
		
		sizer.Add(mode_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
		sizer.Add(self.mode_check, 0, wx.LEFT, 30)
		
		sizer.AddStretchSpacer(1)
		
		note = wx.StaticText(self, wx.ID_ANY, \
		"* Minimum values used for fixed parameters in orbit display.")
		note.SetFont(Widgets.ItalicFont(8))
		
		sizer.Add(note, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# register event handling
		wx.EVT_CHOICE(self, self.state_choice.GetId(), self.on_state_selected)
		wx.EVT_CHOICE(self, self.param_choice.GetId(), self.on_param_selected)
		
		wx.EVT_COMMAND_SCROLL(self, self.density_slider.GetId(), \
		self.on_density_changed)
		
		wx.EVT_COMMAND_SCROLL(self, self.age_slider.GetId(), \
		self.on_age_changed)
		
		wx.EVT_CHECKBOX(self, self.mode_check.GetId(), self.on_mode_selected)
		
		# trigger event handling for visualization settings
		self.on_density_changed()
		self.on_age_changed()
		self.on_mode_selected()
		
		self.SetSizerAndFit(sizer)
		
		dypy.debug("OrbitToolGUI", "Initialized.")

	def update_system(self, system):
		# update state axis choices
		states = system.get_state_names()
		self.state_choice.SetItems(states)
		self.state_choice.SetSelection(0)
		
		# update parameter choices
		params = system.get_parameter_names()
		self.param_choice.SetItems(params)
		self.param_choice.SetSelection(0)
		
		dypy.debug("OrbitToolGUI", "Updated for system %s." % system.name)
		
		# set system in tool
		self.tool.set_system(system)
		
		# trigger state/param choice event handling
		self.on_state_selected()
		self.on_param_selected()

	def on_state_selected(self, event = wx.CommandEvent()):
		index = self.state_choice.GetSelection()
		self.tool.set_state_index(index)

		dypy.debug("OrbitToolGUI", "State axis is now %s." \
		% self.state_choice.GetStringSelection())

	def on_param_selected(self, event = wx.CommandEvent()):
		index = self.param_choice.GetSelection()
		self.tool.set_parameter_index(index)
		
		dypy.debug("OrbitToolGUI", "Parameter is now %s." \
		% self.param_choice.GetStringSelection())

	def on_density_changed(self, event = wx.CommandEvent()):
		density = self.density_slider.GetValue()
		self.tool.set_density(density)
		
		dypy.debug("OrbitToolGUI", "Density is now %d." % density )

	def on_age_changed(self, event = wx.CommandEvent()):
		age = self.age_slider.GetValue()
		self.tool.set_age_max(age)
		
		dypy.debug("OrbitToolGUI", "Age is now %d." % age )
	
	def on_mode_selected(self, event = wx.CommandEvent()):
		mode = self.mode_check.GetValue()
		self.tool.set_show_history(mode)
		
		dypy.debug("ObritToolGUI", "Show history set to %s." % str(mode))