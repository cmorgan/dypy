import OSC
from Device import *

class WiimoteDevice(Device):
    def __init__(self, tool_server, port=9000):
        Device.__init__(self, name="WiiMote", tool_server=tool_server, port=port, speed=0.2)

    def parse_function(self, data):
        print 'parse'
        OSC.hexDump(data)

if __name__ == '__main__':
    wiimote_server = WiimoteDevice(FakeServer())
    wiimote_server.start()
    wiimote_server.join()