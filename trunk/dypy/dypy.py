from dypy.tools.ToolServer import ToolServer
import dypy

dypy.reset_log()
dypy.debug("dypy", "Starting dypy...")

s = ToolServer(width=800, height=800)
s.start()
s.waitUntilStarted()

import os, subprocess

cmd = ['python', 'gui.py']
subprocess.call(cmd, cwd=os.getcwd())