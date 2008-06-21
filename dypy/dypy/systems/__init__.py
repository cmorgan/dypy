import dypy
import os, os.path

def getall():
	path = os.path.join(dypy.__path__[0], "systems")
	excludes = [ "__init__", "Map", "ODE" ]	

	if not os.path.exists(path):
		print "Warning: Unable to find dypy.systems package path."
		return [ "" ]
	
	names = [f[0:-3] for f in os.listdir(path) if f[-3:] == ".py"]
	
	for e in excludes:
		if e in names:
			names.remove(e)

	return names

__all__  = getall()