from Device import *
import numpy
import OSC
import struct

class WiimoteDevice(Device):
    def __init__(self, tool_server, port=9000):
        Device.__init__(self, device_name="WiiMote", tool_server=tool_server, port=port, speed=180.0)
        self.threshold = 0.001
        self.a = 0
        self.b = 0

    def parse_function(self, data):
        # OSCulator uses big endian, OSC.py uses big endian
        name, rest = OSC.readString(data)
        
        if not name.startswith("/wii"):
            return
        
        type, rest = OSC.readString(rest)
        
        if name.endswith("/pry/0"):
            self.parse_field(rest, 'pitch', 'y')

        if name.endswith("pry/1"):
            self.parse_field(rest, 'roll', 'x')
        
        if name.endswith("pry/2"):
            self.parse_field(rest, 'yaw', 'z')
        
        if name.endswith("button/A"):
            self.a = self.readFloat(rest)[0]
            
        if name.endswith("button/B"):
            b = self.readFloat(rest)[0]
            
            if self.b and not b:
                self.tool_server.on_mouse_release(0, 0, 0, 0)
            elif not self.b and b:
                self.tool_server.on_mouse_press(0, 0, 0, 0)               
            
            self.b = b
    
    def parse_field(self, rest, field, axis):
        # get new value
        value = self.readFloat(rest)[0]
              
        try:
            # get old value and subtract
            value_old = getattr(self, field)
            self.delta = value - value_old
        except AttributeError, detail:
            # if old value wasn't set, don't rotate yet
            self.delta = 0
        
        # update previous with new value
        setattr(self, field, value)
        
        # only rotate when b button is held  
        if self.b:
            # ignore tiny jitters
            if numpy.abs(self.delta) > self.threshold:
                if axis == 'x':
                    self.tool_server.on_mouse_drag(0, 0, self.speed*self.delta, 0, 0, 0)
                elif axis == 'y':
                    self.tool_server.on_mouse_drag(0, 0, 0, -self.speed*self.delta, 0, 0)      
                elif axis == 'z':
                    self.tool_server.on_mouse_scroll(0, 0, 0, -self.speed*self.delta)

    def readFloat(self, data):
        if(len(data)<4):
            rest = data
            float = 0
        else:
            float = struct.unpack(">f", data[0:4])[0]
            rest  = data[4:]
    
        return (float, rest)

if __name__ == '__main__':
    wiimote_server = WiimoteDevice(FakeServer())
    wiimote_server.start()
    wiimote_server.join()