from dypy.systems.LogisticMap import LogisticMap
from dypy.tools.ToolServer import ToolServer
import Pyro

s = ToolServer(width=600, height=600)
s.start()
s.waitUntilStarted()

s.tool.set_system(LogisticMap())
s.tool.set_parameter_ranges([(3, 4)])
s.tool.set_state_ranges([(0, 1)])