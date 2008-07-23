from Device import *
import OSC
import struct

class P5Device(Device):
    def __init__(self, tool_server, port=7000):
        Device.__init__(self, device_name='P5Glove', tool_server=tool_server, port=port, speed=0.2)

    def parse_function(self, data):
        # OSC.py uses big endian, OSC.readInt changed to little endian for p5osc
        address, rest   = OSC.readString(data)
        time, rest      = OSC.readLong(rest)
        length, rest    = self.readInt(rest)
        name, rest      = OSC.readString(rest)
        
        if name != "/p5glove_data":
            return
        
        junk, rest      = OSC.readString(rest)         
        a, rest         = self.readInt(rest)
        b, rest         = self.readInt(rest)
        c, rest         = self.readInt(rest)
        thumb, rest     = self.readInt(rest)
        index, rest     = self.readInt(rest)
        middle, rest    = self.readInt(rest)
        ring, rest      = self.readInt(rest)
        pinky, rest     = self.readInt(rest)
        x, rest         = self.readInt(rest)
        y, rest         = self.readInt(rest)
        z, rest         = self.readInt(rest)
        
        if self.initialized:
            self.dx = self.speed * (x - self.x_old)
            self.dy = self.speed * (y - self.y_old)
            self.dz = self.speed * (z - self.z_old)    
            
            self.tool_server.on_mouse_drag(0, 0, self.dx, self.dy, 0, 0)
            self.tool_server.on_mouse_scroll(0, 0, 0, self.dz)  
        else:
            self.initialized = True
            
        self.x_old = x
        self.y_old = y
        self.z_old = z

    def readInt(self, data):
        if(len(data)<4):
            rest = data
            integer = 0
        else:
            integer = struct.unpack("i", data[0:4])[0]
            rest    = data[4:]
            
        return (integer, rest)

if __name__ == '__main__':
    glove_server = P5Device(FakeServer())
    glove_server.start()
    glove_server.join()