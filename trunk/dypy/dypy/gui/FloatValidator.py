import wx

class FloatValidator( wx.PyValidator ):
	def __init__(self, pyVar = None):
		wx.PyValidator.__init__(self)
		self.charlist = [ str(n) for n in range(0, 10) ]
		self.charlist.append('.')
		self.charlist.append('-')
		self.codelist = [ wx.WXK_SPACE, wx.WXK_DELETE, wx.WXK_BACK, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_TAB]

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