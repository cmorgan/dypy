import OSC
from Device import *

class P5Device(Device):
    def __init__(self, tool_server, port=7000):
        Device.__init__(self, name='P5Glove', tool_server=tool_server, port=port, speed=0.2)

    def parse_function(self, data):
        # OSC.py used > (big endian) in struct.unpack,
        # which is incorrect for mac
        address, rest   = OSC.readString(data)
        time, rest      = OSC.readLong(rest)
        length, rest    = OSC.readInt(rest)
        name, rest      = OSC.readString(rest)
        
        if name != "/p5glove_data":
            return
        
        junk, rest      = OSC.readString(rest)         
        a, rest         = OSC.readInt(rest)
        b, rest         = OSC.readInt(rest)
        c, rest         = OSC.readInt(rest)
        thumb, rest     = OSC.readInt(rest)
        index, rest     = OSC.readInt(rest)
        middle, rest    = OSC.readInt(rest)
        ring, rest      = OSC.readInt(rest)
        pinky, rest     = OSC.readInt(rest)
        x, rest         = OSC.readInt(rest)
        y, rest         = OSC.readInt(rest)
        z, rest         = OSC.readInt(rest)
        
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

if __name__ == '__main__':
    glove_server = P5Device(FakeServer())
    glove_server.start()
    glove_server.join()