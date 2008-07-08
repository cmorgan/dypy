from dypy.gui.MainPanel import MainPanel
from dypy.gui.SystemPanel import SystemPanel
from dypy.gui.OrbitToolGUI import OrbitToolGUI
from dypy.gui.PortraitToolGUI import PortraitToolGUI
from dypy.gui.CobwebToolGUI import CobwebToolGUI

import wx, shelve, os.path
import dypy, dypy.systems, dypy.demos
import dypy.gui.Widgets as Widgets

import Pyro.naming

# main window for dypy gui
class MainWindow(wx.Frame):
	def __init__(self):
		dypy.debug("MainWindow", "Initializing window.")
		
		self.gui_title  = "dypy: Dynamical Systems in Python"
		self.gui_width  = 360
		self.gui_height = 650
		
		wx.Frame.__init__(self, None, wx.ID_ANY, self.gui_title)
		self.SetSize((self.gui_width, self.gui_height))
		self.SetBackgroundColour("#f0f0f0")
		
		# connect to tool server
		ns = Pyro.naming.NameServerLocator().getNS(host='localhost')
		uri = ns.resolve('ToolServer')
		self.server = uri.getAttrProxy()
		dypy.debug("MainWindow", "Connected to server.")

		panel = wx.Panel(self, wx.ID_ANY)
		panel.SetBackgroundColour("#f0f0f0")
		
		self.toolbar = self.init_toolbar(panel)	
		logo = Widgets.Logo(panel)
		
		self.notebook = wx.Notebook(panel, wx.ID_ANY, style = wx.NB_BOTTOM)
		self.notebook.SetFont(Widgets.PlainFont())
		self.notebook.AddPage(wx.Panel(self.notebook, wx.ID_ANY), "(Main Tab)")
		self.notebook.AddPage(wx.Panel(self.notebook, wx.ID_ANY), "(System Tab)")
		self.notebook.AddPage(wx.Panel(self.notebook, wx.ID_ANY), "(Tool Tab)")
		
		self.start_button = wx.Button(panel, wx.ID_ANY, "Start Visualization")
		self.start_button.SetFont(Widgets.BoldFont())
		wx.EVT_BUTTON(self, self.start_button.GetId(), self.on_start)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar, 0, wx.ALL | wx.EXPAND, 3)
		sizer.Add(wx.StaticLine(panel, wx.ID_ANY), 0, wx.EXPAND)
		sizer.Add(logo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
		sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)
		sizer.Add(self.start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 10)
		
		self.systems = get_systems()
		dypy.debug("MainWindow", "Loaded %d systems." % len(self.systems))
		
		self.demos = get_demos()
		dypy.debug("MainWindow", "Loaded %d demos." % len(self.demos))
		
		# define tools
		self.tools = [OrbitToolGUI(self.notebook), PortraitToolGUI(self.notebook), \
					  CobwebToolGUI(self.notebook)]
		self.active_tool = self.tools[0]
		dypy.debug("MainWindow", "Loaded %d tools." % len(self.tools))
	
		dypy.debug("MainWindow", "Setting up main panel.")
		self.main_panel = MainPanel(self, self.notebook)
		self.notebook.RemovePage(0)
		self.notebook.InsertPage(0, self.main_panel, "Main", True)

		# make sure to close server when window closed
		self.Bind(wx.EVT_CLOSE, self.on_exit_dypy)

		panel.SetSizerAndFit(sizer)
		self.Show()
		
		dypy.debug("MainWindow", "Initialization complete.")
	
	# note: due to display inconsistencies, toolbar has been converted
	# to a normal panel with bitmap buttons.
	def init_toolbar(self, parent):		
		toolbar = wx.Panel(parent, wx.ID_ANY)
		toolbar.SetBackgroundColour("#f0f0f0")

		load_nlds = Widgets.ToolButton(toolbar, "icon_nlds.png")
		load_demo = Widgets.ToolButton(toolbar, "icon_demo.png")
		save_demo = Widgets.ToolButton(toolbar, "icon_save.png")
		view_help = Widgets.ToolButton(toolbar, "icon_help.png")
		exit_dypy = Widgets.ToolButton(toolbar, "icon_exit.png")

		wx.EVT_BUTTON(self, load_nlds.GetId(), self.on_load_system)
		wx.EVT_BUTTON(self, load_demo.GetId(), self.on_load_demo)
		wx.EVT_BUTTON(self, save_demo.GetId(), self.on_save_demo)
		wx.EVT_BUTTON(self, view_help.GetId(), self.on_view_help)
		wx.EVT_BUTTON(self, exit_dypy.GetId(), self.on_exit_dypy)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(load_nlds, 0, wx.RIGHT, 3)
		sizer.Add(load_demo, 0, wx.RIGHT, 3)
		sizer.Add(save_demo, 0, wx.RIGHT, 0)
		sizer.AddStretchSpacer(wx.EXPAND)
		sizer.Add(view_help, 0, wx.RIGHT, 3)
		sizer.Add(exit_dypy, 0, wx.RIGHT, 0)
		
		toolbar.SetSizerAndFit(sizer)
		return toolbar
	
	# called when start visualization clicked
	def on_start(self, event):
		# disable changing system and tool
		self.main_panel.lockdown()
		
		# change start button text and event handling
		self.start_button.SetLabel("Stop Visualization")
		self.start_button.SetFont(Widgets.ItalicFont())
		wx.EVT_BUTTON(self, self.start_button.GetId(), self.on_stop)
		
		# make tool panel active
		self.notebook.SetSelection(2)
		
		self.server.unpause()
		dypy.debug("MainWindow", "Visualization started.\n")

	# called when stop visualization clicked
	def on_stop(self, event):
		# enable selecting system and tool
		self.main_panel.unlock()
		
		# change stop button text and event handling
		self.start_button.SetLabel("Start Visualization")
		self.start_button.SetFont(Widgets.BoldFont())
		wx.EVT_BUTTON(self, self.start_button.GetId(), self.on_start)
		
		# make system panel active
		self.notebook.SetSelection(0)
		
		self.server.pause()
		dypy.debug("MainWindow", "Visualization stopped.\n")

	def on_load_system(self, event):
		dypy.debug("MainWindow", "Loading system from file.")

	def on_load_demo(self, event):
		dypy.debug("MainWindow", "Loading demo from file.")

		filter = "dypy Demo files (*.db)|*.db"
		dialog = wx.FileDialog(self, message = "Choose demo file", \
		wildcard = filter, style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, \
		defaultDir = os.path.join(dypy.__path__[0], "demos"))
		
		# open dialog and get file name
		if dialog.ShowModal() == wx.ID_OK:
			dypy.debug("MainWindow", "Loading demo from file %s." % dialog.GetPath())

			shelf = shelve.open(dialog.GetPath())
			
			demo_system = shelf["demo system"]
			demo_name = shelf["demo name"]
			demo_description = shelf["demo description"]
			
			dypy.debug("MainWindow", "Updating system to %s." % demo_system)
			self.main_panel.set_system_by_name(demo_system)
			
			dypy.debug("MainWindow", "Loading demo controls." )
			self.load_control(shelf, 'state minimum controls', \
				self.system_panel.state_min_controls)
			
			self.load_control(shelf, 'state maximum controls', \
				self.system_panel.state_max_controls)
			
			self.load_control(shelf, 'parameter minimum controls', \
				self.system_panel.param_min_controls)
			
			self.load_control(shelf, 'parameter maximum controls', \
				self.system_panel.param_max_controls)
			
			shelf.close()
			
			self.system_panel.update_param()
			self.system_panel.update_state()
			
		else:
			dypy.debug("MainWindow", "Loading demo canceled by user.")
		
		dialog.Destroy()

	def on_save_demo(self, event):
		dypy.debug("MainWindow", "Saving demo to file.")
			
		dialog = Widgets.SaveDialog(self)
		
		if dialog.ShowModal() == wx.ID_OK:
			demo_name = dialog.name_text.GetValue()
			demo_description = dialog.description_text.GetValue()
			demo_location = dialog.location_text.GetValue()
			
			shelf = shelve.open(demo_location)
			
			shelf["demo system"] = self.main_panel.get_system_name()
			shelf["demo name"] = demo_name
			shelf["demo description"] = demo_description
			
			self.save_control(shelf, "state minimum controls", \
				self.system_panel.state_min_controls)

			self.save_control(shelf, "state maximum controls", \
				self.system_panel.state_max_controls)
			
			self.save_control(shelf, "parameter minimum controls", \
				self.system_panel.param_min_controls)

			self.save_control(shelf, "parameter maximum controls", \
				self.system_panel.param_max_controls)

			shelf.close()

			dypy.debug("MainWindow", "Saving demo as file %s." % demo_location)
		else:
			dypy.debug("MainWindow", "Saving demo canceled by user.")
		
		dialog.Destroy()
		
	def load_control(self, shelf, key, controls):
		values = shelf[key]
		
		for i in xrange(0, len(controls)):
			controls[i].SetValue(values[i])
	
	def save_control(self, shelf, key, controls):
		values = []
		
		for i in xrange(0, len(controls)):
			values.append(controls[i].GetValue())
				
		shelf[key] = values	
	
	def on_view_help(self, event):
		dypy.debug("MainWindow", "Displaying help.")
	
	# called when exit button clicked on toolbar
	def on_exit_dypy(self, event):
		dypy.debug("MainWindow", "Exiting dypy.")
	
		try:
			# signal server to close visualization window
			# THIS BREAKS WHEN THE SERVER IS ALREADY CLOSED
			self.server.on_close()
		finally:
			#close gui window
			self.Destroy()

	# updates system panel for currently selected system
	def update_system_panel(self, system):
		# create system panel and trigger layout
		self.system_panel = SystemPanel(self, self.notebook, system)
		self.system_panel.Layout()
		
		# reinsert system panel into notebook display
		self.notebook.RemovePage(1)
		self.notebook.InsertPage(1, self.system_panel, system.name)
		
		dypy.debug("MainWindow", "System panel changed to %s." % system.name)
		
		# update active tool's system
		self.active_tool.update_system(system)

	# updates tool panel for currently selected tool and system
	def update_tool_panel(self, system, tool):
		# set active tool
		self.active_tool = tool
		
		# set system for active tool
		self.active_tool.update_system(system)
		
		# insert tool gui into notebook display
		self.notebook.RemovePage(2)
		self.notebook.InsertPage(2, self.active_tool, self.active_tool.name)
		
		dypy.debug("MainWindow", "Tool panel changed to %s." % tool.name)

	# updates parameter values when new demo is selected
	def update_parameters(self, demo):
		dypy.debug("MainWindow", "System parameters updated for %s." % demo.name)

# dynamically loads modules from a list of names
def get_modules(names):
	modules = []
	
	for name in names:
		module = __import__(name)
		packages = name.split('.')
		
		for subpackage in packages[1:]:
			module = getattr(module, subpackage)
		
		modules.append(module)

	return modules

# dynamically loads classes from a list of modules
def get_classes(modules, parent = ""):
	classes = []
	param = 'parent' 
	
	if parent == "":
		param = parent
	
	for module in modules:
		class_name = module.__name__.split('.')[-1]
		exec "current = %s.%s(%s)" % (module.__name__, class_name, param)
		classes.append(current)
	
	return classes

# dynamically loads all systems in dypy.systems subpackage
# uses dynamically set __all__ variable
def get_systems():
	names = dypy.systems.__all__
	names = ["dypy.systems." + name for name in names]
	names.sort()	
	
	return get_classes(get_modules(names))

# dynamically loads all systems in dypy.demos subpackage
# uses dynamically set __all__ variable
def get_demos():
	names = dypy.demos.__all__
	names = ["dypy.demos." + name for name in names]
	names.sort()	
	
	return get_classes(get_modules(names))

# creates main gui window and begins event loop
def show():
	gui   = wx.PySimpleApp()
	frame = MainWindow()
	
	dypy.debug("MainWindow", "Starting event loop.\n")
	gui.MainLoop()
	dypy.debug("MainWindow", "Exiting event loop.")