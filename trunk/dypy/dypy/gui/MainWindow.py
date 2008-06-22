from dypy.gui.MainPanel import MainPanel
from dypy.gui.OrbitToolGUI import OrbitToolGUI
from dypy.gui.SystemPanel import SystemPanel
import dypy.gui.utils as utils
import Pyro.naming
import wx

class MainWindow(wx.Frame):
	def __init__(self):
		self.gui_title  = "dypy: Dynamical Systems in Python"
		self.gui_width  = 350
		self.gui_height = 700
		
		wx.Frame.__init__(self, None, wx.ID_ANY, self.gui_title)
		self.SetSize((self.gui_width, self.gui_height))
		
		ns = Pyro.naming.NameServerLocator().getNS(host='localhost')
		uri = ns.resolve('ToolServer')
		self.server = uri.getAttrProxy()

		utils.debug("MainWindow: Frame initialized")

		self.SetBackgroundColour("#f0f0f0")
				
		self.status = self.CreateStatusBar()
		self.status.SetStatusText("Welcome to dypy! Click \"Start Visualization\" to begin.")
		
		self.add_toolbar()
		
		panel = wx.Panel(self, wx.ID_ANY)
		panel.SetBackgroundColour("#f0f0f0")
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		logo_bitmap = utils.get_image("logo_opaque.png")
		logo = wx.StaticBitmap(panel, wx.ID_ANY, logo_bitmap)
		
		self.notebook = wx.Notebook(panel, wx.ID_ANY, style = wx.NB_BOTTOM)
		self.notebook.AddPage(wx.Panel(self.notebook, wx.ID_ANY), "Main")
		self.notebook.AddPage(wx.Panel(self.notebook, wx.ID_ANY), "System")
		self.notebook.AddPage(wx.Panel(self.notebook, wx.ID_ANY), "Tool")
		
		start_button = wx.Button(panel, wx.ID_ANY, "Start Visualization")
		wx.EVT_BUTTON(self, start_button.GetId(), self.on_start)

		sizer.Add(logo, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)
		sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)
		sizer.Add(start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 10)
	
		utils.debug("MainWindow: Dynamically loading systems, demos, and tools.")
		self.systems = utils.get_systems()
		self.demos = utils.get_demos()
		self.tools = [OrbitToolGUI(self)]
		self.active_tool = self.tools[0]
		
		utils.debug("MainWindow: Setting up gui panels.")
		main_panel = MainPanel(self.notebook)
		self.notebook.RemovePage(0)
		self.notebook.InsertPage(0, main_panel, "Main", True)

		panel.SetSizerAndFit(sizer)		
		self.Show()
	
	def add_toolbar(self):
		return
		utils.debug("MainWindow: Creating tool bar.")
		toolbar = self.CreateToolBar()
		toolbar.SetToolBitmapSize(size = (40, 40))
		toolbar.SetBackgroundColour("#f0f0f0")
		toolbar.SetBackgroundStyle(wx.BG_STYLE_COLOUR)	
		
		load_nlds = wx.BitmapButton(toolbar, wx.ID_ANY, utils.get_image("icon_nlds.png") )
		load_demo = wx.BitmapButton(toolbar, wx.ID_ANY, utils.get_image("icon_demo.png"), style = wx.NO_BORDER)
		load_tool = wx.BitmapButton(toolbar, wx.ID_ANY, utils.get_image("icon_tool.png"), style = wx.NO_BORDER)
		save_demo = wx.BitmapButton(toolbar, wx.ID_ANY, utils.get_image("icon_save.png"), style = wx.NO_BORDER)
		view_help = wx.BitmapButton(toolbar, wx.ID_ANY, utils.get_image("icon_help.png"), style = wx.NO_BORDER)
		exit_dypy = wx.BitmapButton(toolbar, wx.ID_ANY, utils.get_image("icon_exit.png"), style = wx.NO_BORDER)

		wx.EVT_BUTTON(self, load_nlds.GetId(), self.on_load_system)
		wx.EVT_BUTTON(self, load_demo.GetId(), self.on_load_demo)
		wx.EVT_BUTTON(self, load_tool.GetId(), self.on_load_tool)
		wx.EVT_BUTTON(self, save_demo.GetId(), self.on_save_demo)
		wx.EVT_BUTTON(self, view_help.GetId(), self.on_view_help)
		wx.EVT_BUTTON(self, exit_dypy.GetId(), self.on_exit_dypy)
		
		toolbar.AddControl(load_nlds)
		toolbar.AddControl(load_demo)
		toolbar.AddControl(load_tool)
		toolbar.AddControl(save_demo)
		toolbar.AddSeparator()
		toolbar.AddControl(view_help)
		toolbar.AddControl(exit_dypy)

		toolbar.Realize()
	
	def on_start(self, event):
		self.active_tool.start()
	
	def on_load_system(self, event):
		self.status.SetStatusText("Loads a system from a Python file. (Not yet implemented)")

	def on_load_demo(self, event):
		self.status.SetStatusText("Loads parameter settings from a Python file. (Not yet implemented)")

	def on_load_tool(self, event):
		self.status.SetStatusText("Loads a visualization tool. (Not yet implemented)")
	
	def on_save_demo(self, event):
		self.status.SetStatusText("Saves current parameter settings to a file. (Not yet implemented)")
	
	def on_view_help(self, event):
		self.status.SetStatusText("Opens the help window. (Not yet implemented)")
	
	def on_exit_dypy(self, event):
		self.status.SetStatusText("Closing dypy...")
		utils.get_main_window(self).Close()

	def update_system_panel(self, system):
		utils.debug("MainWindow: Updating system panel.")
		self.notebook.RemovePage(1)
		self.notebook.InsertPage(1, SystemPanel(self.notebook, system), system.name)

	def update_tool_panel(self, system, tool):
		utils.debug("MainWindow: Updating tool panel.")
		self.active_tool = tool
		self.active_tool.update_system(system)
		self.notebook.RemovePage(2)
		self.notebook.InsertPage(2, self.active_tool, self.active_tool.get_name())

def show():
	gui   = wx.PySimpleApp()
	frame = MainWindow()
	
	gui.MainLoop()