import OSC
from Device import *

class WiiDevice(Device):
    def __init__(self, tool_server, port=9000):
        Device.__init__(self, name="WiiMote", tool_server=tool_server, port=port, speed=0.2)

    def parse_function(self, data):
        OSC.hexDump(data)
        print

if __name__ == '__main__':
    wiimote_server = WiiDevice(FakeServer())
    wiimote_server.start()
    wiimote_server.join()