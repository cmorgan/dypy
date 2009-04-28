from dypy.gui.ToolGUI import ToolGUI

import wx, dypy
import dypy.gui.Widgets as Widgets

class CobwebToolGUI(ToolGUI):
    def __init__(self, parent):
        ToolGUI.__init__(self, parent, 'CobwebTool')
        
    def update_system(self, system):
        self.tool.set_system(system)