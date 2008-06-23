from dypy.tools.ToolServer import ToolServer

s = ToolServer(width=600, height=600)
s.start()
s.waitUntilStarted()

import os, subprocess

cmd = ['python', 'gui.py']
subprocess.call(cmd, cwd=os.getcwd())