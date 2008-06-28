from dypy.tools.ToolServer import ToolServer
import dypy

dypy.reset_log()
dypy.debug("dypy", "Starting dypy...")

s = ToolServer(width=600, height=600)
s.start()
s.waitUntilStarted()

import os, subprocess

cmd = ['python', 'gui.py']
subprocess.call(cmd, cwd=os.getcwd())