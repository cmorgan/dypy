import gui.MainWindow
show = gui.MainWindow.show

# use to toggle debug messages
# warning: very verbose
DEBUG_FLAG = True
LOG_FLAG = False

def reset_log():
	if(LOG_FLAG):
		logfile = open("dypylog.txt", "w")
		logfile.write("")
		logfile.close()

def debug(name, message):
	if(LOG_FLAG):
		logfile = open("dypylog.txt", "a")
		logfile.write("%13s: %s\n" % (name, message))
		logfile.close()

	if(DEBUG_FLAG):
		print "%13s: %s" % (name, message)