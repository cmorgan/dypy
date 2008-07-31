from dypy.gui.ToolGUI import ToolGUI

import wx, dypy
import dypy.gui.Widgets as Widgets

class PortraitToolGUI(ToolGUI):
    def __init__(self, parent):
        ToolGUI.__init__(self, parent, 'PortraitTool')
        
        # gui components: labels
        state_x_label   = Widgets.LabelText(self, "Select State for x-Axis:")
        state_y_label   = Widgets.LabelText(self, "Select State for y-Axis:")
        state_z_label   = Widgets.LabelText(self, "Select State for z-Axis:")        
        mode_label      = Widgets.LabelText(self, "Select Visualization Mode:")        
       
        # gui components: selection
        self.state_x_choice = Widgets.ChoiceList(self)
        self.state_y_choice = Widgets.ChoiceList(self)
        self.state_z_choice = Widgets.ChoiceList(self)
        self.mode_check = Widgets.Checkbox(self, "Draw Lines")
        
        sizer = wx.BoxSizer(wx.VERTICAL)        
        
        sizer.Add(state_x_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        sizer.Add(self.state_x_choice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer.AddSpacer(2)
        
        sizer.Add(state_y_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        sizer.Add(self.state_y_choice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer.AddSpacer(2)
        
        sizer.Add(state_z_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        sizer.Add(self.state_z_choice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        sizer.AddSpacer(2)   
        
        sizer.Add(mode_label, 0, wx.ALIGN_LEFT | wx.ALL, 4)
        sizer.Add(self.mode_check, 0, wx.LEFT, 30)
        
        sizer.AddStretchSpacer(1)
        
        # register event handling
        wx.EVT_CHOICE(self, self.state_x_choice.GetId(), self.on_state_x_selected)
        wx.EVT_CHOICE(self, self.state_y_choice.GetId(), self.on_state_y_selected)
        wx.EVT_CHOICE(self, self.state_z_choice.GetId(), self.on_state_z_selected)      
        wx.EVT_CHECKBOX(self, self.mode_check.GetId(), self.on_mode_selected)
        
        self.SetSizerAndFit(sizer)
        
        dypy.debug("PortraitToolGUI", "Initialized.")        

    def on_state_x_selected(self, event = wx.CommandEvent()):
        index = self.state_x_choice.GetSelection()
        self.tool.set_state_index(0, index)

        dypy.debug("PortraitToolGUI", "State x-axis is now %s." \
        % self.state_x_choice.GetStringSelection())
        
    def on_state_y_selected(self, event = wx.CommandEvent()):
        index = self.state_y_choice.GetSelection()
        self.tool.set_state_index(1, index)

        dypy.debug("PortraitToolGUI", "State y-axis is now %s." \
        % self.state_y_choice.GetStringSelection())
        
    def on_state_z_selected(self, event = wx.CommandEvent()):
        index = self.state_z_choice.GetSelection()
        self.tool.set_state_index(2, index)

        dypy.debug("PortraitToolGUI", "State z-axis is now %s." \
        % self.state_z_choice.GetStringSelection())
     
    def update_system(self, system):
        # update state axis choices
        self.state_x_choice.SetItems(system.get_state_names())
        self.state_x_choice.SetSelection(0)
        
        self.state_y_choice.SetItems(system.get_state_names())
        self.state_y_choice.SetSelection(0)
        
        self.state_z_choice.SetItems(system.get_state_names())
        self.state_z_choice.SetSelection(0)
        
        dypy.debug("PortraitToolGUI", "Updated for system %s." % system.name)

        # set system in tool        
        self.tool.set_system(system)
        
        # trigger state/param choice event handling
        self.on_state_x_selected()
        self.on_state_y_selected()
        self.on_state_z_selected() 
    
    def on_mode_selected(self, event = wx.CommandEvent()):
        mode = self.mode_check.GetValue()
        self.tool.use_lines = mode
        
        dypy.debug("PortraitToolGUI", "Draw lines set to %s." % str(mode))