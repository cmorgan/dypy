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