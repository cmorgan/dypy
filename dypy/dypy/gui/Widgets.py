import wx, os.path, dypy

# module containing various small widget classes

def get_image(name):
	path = os.path.join(dypy.__path__[0], "images", name)
	
	if not os.path.exists(path):
		print "Warning: Unable to find dypy.images package path."
		return wx.Bitmap(0,0)
	
	return wx.Bitmap(path)

class Logo(wx.StaticBitmap):
	def __init__(self, parent):
		wx.StaticBitmap.__init__(self, parent, wx.ID_ANY, \
		get_image("logo_opaque.png"))

class ToolButton(wx.BitmapButton):
	def __init__(self, parent, file):
		wx.BitmapButton.__init__(self, parent, wx.ID_ANY, \
		get_image(file))

class BoldFont(wx.Font):
	def __init__(self, size = 10):
		wx.Font.__init__(self, size, wx.FONTFAMILY_SWISS, \
		wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

class PlainFont(wx.Font):
	def __init__(self, size = 10):
		wx.Font.__init__(self, size, wx.FONTFAMILY_SWISS, \
		wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

class ItalicFont(wx.Font):
	def __init__(self, size = 10):
		wx.Font.__init__(self, size, wx.FONTFAMILY_SWISS, \
		wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)

class FixedFont(wx.Font):
	def __init__(self, size = 10):
		wx.Font.__init__(self, size, wx.FONTFAMILY_TELETYPE, \
		wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

class LabelText(wx.StaticText):
	def __init__(self, parent, label):
		wx.StaticText.__init__(self, parent, wx.ID_ANY, label)
		self.SetFont(BoldFont())

class ChoiceList(wx.Choice):
	def __init__(self, parent):
		wx.Choice.__init__(self, parent, wx.ID_ANY, choices = [])
		self.SetFont(PlainFont(12))

class AboutText(wx.TextCtrl):
	def __init__(self, parent):
		wx.TextCtrl.__init__(self, parent, wx.ID_ANY, value = "", \
		style = wx.TE_READONLY | wx.TE_WORDWRAP | wx.TE_MULTILINE)
		
		self.SetInitialSize(size = (10, 20))
		self.Disable()

class FloatValidator( wx.PyValidator):
	def __init__(self, pyVar = None):
		wx.PyValidator.__init__(self)
		self.charlist = [ str(n) for n in range(0, 10) ]
		self.charlist.append('.')
		self.charlist.append('-')
		self.codelist = [ wx.WXK_SPACE, wx.WXK_DELETE, \
		wx.WXK_BACK, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_TAB]

		self.Bind(wx.EVT_CHAR, self.ProcessKey)
		
	def Clone (self):
		return FloatValidator()

	def ProcessKey(self, event):
		key = event.GetKeyCode()
	
		if key in self.codelist or chr(key) in self.charlist:
			event.Skip()
			return
		
		if not wx.Validator_IsSilent():
			wx.Bell()

class FloatLabel(wx.StaticText):
	def __init__(self, parent, label):
		wx.StaticText.__init__(self, parent, wx.ID_ANY, label)
		self.SetFont(PlainFont(12))

class FloatControl(wx.TextCtrl):
	def __init__(self, parent, value):
		wx.TextCtrl.__init__(self, parent, wx.ID_ANY, str(value), \
		validator = FloatValidator())

		self.SetMinSize((50,-1))
		self.SetMaxSize((100,-1))
		self.SetFont(PlainFont(12))

# because default sliders are ugly
class SimpleSlider(wx.Panel):
	def __init__(self, parent, value, min, max):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		
		min_label = wx.StaticText(self, wx.ID_ANY, "%2s" % str(min))
		min_label.SetFont(FixedFont(10))
		
		max_label = wx.StaticText(self, wx.ID_ANY, "%-4s" % str(max))
		max_label.SetFont(FixedFont(10))
		
		self.slider = wx.Slider(self, wx.ID_ANY, value, min, max, \
		style = wx.SL_HORIZONTAL)

		self.GetId = self.slider.GetId
		self.GetValue = self.slider.GetValue

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(min_label, 0, wx.ALL, 4)
		sizer.Add(self.slider, 1, wx.TOP | wx.BOTTOM, 4)
		sizer.Add(max_label, 0, wx.ALL, 4)
		
		self.SetSizerAndFit(sizer)
	
class Checkbox(wx.CheckBox):
	def __init__(self, parent, label):
		wx.CheckBox.__init__(self, parent, wx.ID_ANY, label)
		self.SetFont(PlainFont(10))

# class for saving demos
# a little big to be in the widgets file...
class SaveDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Save Demo to File", \
		style = wx.DEFAULT_DIALOG_STYLE)
		self.SetSize((400, 300))
		
		self.default_dir  = os.path.join(dypy.__path__[0], "demos")
		self.default_file = "CustomDemo.db"
		
		panel = wx.Panel(self, wx.ID_ANY)
		
		self.name_text = wx.TextCtrl(panel, wx.ID_ANY)
		self.name_text.SetFont(PlainFont(12))
		self.name_text.SetValue("Custom Demo")
		self.name_text.SetInsertionPoint(0)

		self.description_text = wx.TextCtrl(panel, wx.ID_ANY, style = wx.TE_MULTILINE)
		self.description_text.SetFont(PlainFont(12))
		self.description_text.SetValue("Custom demo created by user.")

		self.location_text = wx.TextCtrl(panel, wx.ID_ANY)
		self.location_text.SetFont(PlainFont(12))
		self.location_text.SetValue(os.path.join(self.default_dir, \
		self.default_file))

		browse_button = wx.Button(panel, wx.ID_ANY, "Browse...")
		browse_button.SetFont(BoldFont())
		wx.EVT_BUTTON(self, browse_button.GetId(), self.on_browse)

		location_sizer = wx.BoxSizer(wx.HORIZONTAL)
		location_sizer.Add(self.location_text, 1, wx.RIGHT, 5)
		location_sizer.Add(browse_button, 0)

		save_button = wx.Button(panel, wx.ID_ANY, "Save Demo")
		save_button.SetFont(BoldFont())
		wx.EVT_BUTTON(self, save_button.GetId(), self.on_save)
		
		cancel_button = wx.Button(panel, wx.ID_ANY, "Cancel")
		cancel_button.SetFont(BoldFont())
		wx.EVT_BUTTON(self, cancel_button.GetId(), self.on_cancel)
		
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		button_sizer.Add(save_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 5)
		button_sizer.Add(cancel_button, 0, wx.ALIGN_RIGHT | wx.RIGHT, 5)

		# begin main layout
		vsizer = wx.BoxSizer(wx.VERTICAL)
		
		vsizer.Add(LabelText(panel, "Enter Demo Name:"), 0, wx.ALIGN_LEFT)
		vsizer.AddSpacer(2)

		vsizer.Add(self.name_text, 0, wx.EXPAND)
		vsizer.AddSpacer(10)
		
		vsizer.Add(LabelText(panel, "Enter Demo Description:"), 0, wx.ALIGN_LEFT)
		vsizer.AddSpacer(2)
		
		vsizer.Add(self.description_text, 1, wx.EXPAND)
		vsizer.AddSpacer(10)
		
		vsizer.Add(LabelText(panel, "Save Demo To:"), 0, wx.ALIGN_LEFT)
		vsizer.AddSpacer(2)
		
		vsizer.Add(location_sizer, 0, wx.EXPAND)
		vsizer.AddStretchSpacer(1)

		vsizer.Add(button_sizer, 0, wx.ALIGN_RIGHT)
		
		panel.SetSizer(vsizer)
		
		# make panel stretch to entire dialog size
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(panel, 1, wx.EXPAND | wx.ALL, 10)

		self.SetSizer(hsizer)
	
	def on_save(self, event):		
		self.EndModal(wx.ID_OK)
	
	def on_cancel(self, event):
		self.EndModal(wx.ID_CANCEL)
		
	def on_browse(self, event):
		filter = "dypy Demo files (*.db)|*.db"
		dialog = wx.FileDialog(self, message = "Select Save Location", \
		wildcard = filter, style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, \
		defaultDir = self.default_dir, defaultFile = self.default_file)
		
		if dialog.ShowModal() == wx.ID_OK:
			self.location_text.Clear()
			self.location_text.SetValue(dialog.GetPath())
			
			dypy.debug("SaveDialog", "Save location set to %s." % dialog.GetPath())
		else:
			dypy.debug("SaveDialog", "Location selection canceled.")		