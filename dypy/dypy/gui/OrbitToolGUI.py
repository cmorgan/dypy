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
        
		#self.tool.set_age_max(1000)
		#self.tool.set_density(4)

		sizer = wx.BoxSizer(wx.VERTICAL)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Select State Axis:"), 0, wx.ALIGN_LEFT)
		self.state_choice = wx.ComboBox(self, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN | wx.CB_READONLY)
		sizer.Add(self.state_choice, 0, wx.EXPAND | wx.BOTTOM, 10)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Select Parameter:"), 0, wx.ALIGN_LEFT)
		self.param_choice = wx.ComboBox(self, wx.ID_ANY, choices=[""], style=wx.CB_DROPDOWN | wx.CB_READONLY)
		sizer.Add(self.param_choice, 0, wx.EXPAND | wx.BOTTOM, 10)
		
		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Select Maximum Point Density:"), 0, wx.ALIGN_LEFT)
		self.density_slider = wx.Slider(self, 1, 10, 4)
		sizer.Add(self.density_slider, 0, wx.EXPAND)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Select Maximum Point Age:"), 0, wx.ALIGN_LEFT)
		self.age_slider = wx.Slider(self, 1, 2000, 1000)
		sizer.Add(self.age_slider, 0, wx.EXPAND)

		sizer.Add(wx.StaticText(self, wx.ID_ANY, "Select Visualization Mode:"), 0, wx.ALIGN_LEFT | wx.BOTTOM, 5)

		self.mode_checkbox = wx.CheckBox(self, wx.ID_ANY, 'Show History')
		sizer.Add(self.mode_checkbox, 0, wx.ALIGN_LEFT | wx.LEFT, 20)

		wx.EVT_CHOICE(self, self.state_choice.GetId(), self.on_state_selected)
		wx.EVT_CHOICE(self, self.param_choice.GetId(), self.on_param_selected)
		wx.EVT_COMMAND_SCROLL(self, self.density_slider.GetId(), self.on_density_selected)
		wx.EVT_COMMAND_SCROLL(self, self.age_slider.GetId(), self.on_age_selected)
		wx.EVT_CHECKBOX(self, self.mode_checkbox.GetId(), self.on_mode_selected)

		utils.debug("OrbitToolGUI: Trigger control updates.")
		self.trigger(self.density_slider)
		self.trigger(self.age_slider)
		self.trigger(self.mode_checkbox)
		self.SetSizerAndFit(sizer)	

	def trigger(self, obj):
		event = wx.CommandEvent(wx.wxEVT_SCROLL_THUMBRELEASE)
		event.SetEventObject(obj)
		event.SetId(obj.GetId())
		obj.GetEventHandler().ProcessEvent(event)
		
	def update_system(self, system):
		utils.debug("ObitToolGUI: Update system.")
		self.param_choice.update(system.get_parameter_names())
		self.state_choice.update(system.get_state_names())

	def on_state_selected(self, event):
		utils.debug("OrbitToolGUI: State axis selected.")
		self.tool.set_state_index(self.state_choice.GetSelection())
		
	def on_param_selected(self, event):
		utils.debug("OrbitToolGUI: Parameter axis selected.")
		self.tool.set_parameter_index(self.param_choice.GetSelection())

	def on_density_selected(self, event):
		utils.debug("OrbitToolGUI: Density selected.")
		self.tool.set_density(self.density_slider.GetValue())

	def on_age_selected(self, event):
		utils.debug("OrbitToolGUI: Age selected.")
		self.tool.set_age_max(self.age_slider.GetValue())

	def on_mode_selected(self, event):
		utils.debug("OrbitToolGUI: Mode selected.")
		self.tool.set_show_history(self.mode_checkbox.GetValue())		
	"""
	def update_system(self, system):
		utils.debug("OrbitToolGUI: Updating tool to use %s." % system.name)
		self.tool.set_system(system)
	
	def get_name(self):
		return self.tool.name
	
	def get_description(self):
		return self.tool.description

	def start(self):
		self.tool.start()
	"""