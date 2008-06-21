import dypy.demos
import dypy.systems
import dypy.tools
import os.path
import wx

def debug(string):
	print string
	#pass

def get_modules(names):
	modules = []
	
	for name in names:
		module = __import__(name)
		packages = name.split('.')
		
		for subpackage in packages[1:]:
			module = getattr(module, subpackage)
		
		modules.append(module)

	return modules

"""def get_classes(modules):
	classes = []
	
	for module in modules:
		class_name = module.__name__.split('.')[-1]
		exec "current = %s.%s()" % (module.__name__, class_name)
		classes.append(current)
	
	return classes"""

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

def get_systems():
	names = dypy.systems.__all__
	names = ["dypy.systems." + name for name in names]
	names.sort()	
	
	return get_classes(get_modules(names))

def get_demos():
	names = dypy.demos.__all__
	names = ["dypy.demos." + name for name in names]
	names.sort()	
	
	return get_classes(get_modules(names))

def get_tools(parent):
	names = dypy.tools.__all__
	names = ["dypy.tools." + name for name in names]
	names.sort()

	return get_classes(get_modules(names), parent)

def get_image(name):
	path = os.path.join(dypy.__path__[0], "images", name)
	
	if not os.path.exists(path):
		print "Warning: Unable to find dypy.images package path."
		return wx.Bitmap(0,0)
	
	return wx.Bitmap(path)

def get_main_window(parent):
	main = parent
	current = parent
		
	while current:
		main = current
		current = current.GetParent()
	
	return main