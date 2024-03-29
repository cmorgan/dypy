from dypy.gui.ToolGUI import ToolGUI

import wx, dypy
import dypy.gui.Widgets as Widgets

class OrbitToolGUI(ToolGUI):
	def __init__(self, parent):
		ToolGUI.__init__(self, parent, 'OrbitTool')

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
		self.age_slider     = Widgets.SimpleSlider(self, 1000, 1, 10000)

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
		
		wx.EVT_COMMAND_SCROLL(self, self.density_slider.GetId(), self.on_density_changed)
		wx.EVT_COMMAND_SCROLL(self, self.age_slider.GetId(), self.on_age_changed)
		
		wx.EVT_CHECKBOX(self, self.mode_check.GetId(), self.on_mode_selected)
		
		# trigger event handling for visualization settings
		self.on_density_changed()
		self.on_age_changed()
		self.on_mode_selected()
		
		self.SetSizerAndFit(sizer)
		
		dypy.debug("OrbitToolGUI", "Initialized.")

	def update_system(self, system):
		# update state axis choices
		self.state_choice.SetItems(system.get_state_names())
		self.state_choice.SetSelection(0)
		
		# update parameter choices
		self.param_choice.SetItems(system.get_parameter_names())
		self.param_choice.SetSelection(0)
		
		dypy.debug("OrbitToolGUI", "Updated for system %s." % system.name)
		
		# set system in tool
		self.tool.set_system(system)
		
		# trigger state/param choice event handling
		self.on_state_selected()
		self.on_param_selected()

	def on_state_selected(self, event = wx.CommandEvent()):
		index = self.state_choice.GetSelection()
		self.tool.set_state_index(0, index)

		dypy.debug("OrbitToolGUI", "State axis is now %s." \
		% self.state_choice.GetStringSelection())

	def on_param_selected(self, event = wx.CommandEvent()):
		index = self.param_choice.GetSelection()
		self.tool.set_parameter_index(0, index)
		
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