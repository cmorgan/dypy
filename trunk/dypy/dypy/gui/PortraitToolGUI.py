from dypy.gui.ToolGUI import ToolGUI

import wx, dypy
import dypy.gui.Widgets as Widgets

class PortraitToolGUI(ToolGUI):
    def __init__(self, parent):
        ToolGUI.__init__(self, parent, 'PortraitTool')
        
        # gui components: labels
        mode_label = Widgets.LabelText(self, "Select Visualization Mode:")        
        
        # gui components: selection
        self.mode_check = Widgets.Checkbox(self, "Draw Lines")

        sizer = wx.BoxSizer(wx.VERTICAL)        
        
        sizer.Add(mode_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        sizer.Add(self.mode_check, 0, wx.LEFT, 30)
        
        sizer.AddStretchSpacer(1)
        
        # register event handling
        wx.EVT_CHECKBOX(self, self.mode_check.GetId(), self.on_mode_selected)
        
        self.SetSizerAndFit(sizer)
        
        dypy.debug("PortraitToolGUI", "Initialized.")        
        
    def update_system(self, system):
        self.tool.set_system(system)
    
    def on_mode_selected(self, event = wx.CommandEvent()):
        mode = self.mode_check.GetValue()
        self.tool.use_lines = mode
        
        dypy.debug("PortraitToolGUI", "Draw lines set to %s." % str(mode))