from Device import *
import OSC
import struct

class WiimoteDevice(Device):
    def __init__(self, tool_server, port=9000):
        Device.__init__(self, device_name="WiiMote", tool_server=tool_server, port=port, speed=120.0)
        self.threshold = 0.01

    def parse_function(self, data):
        # OSCulator uses big endian, OSC.py uses big endian
        name, rest = OSC.readString(data)
        
        if not name.startswith("/wii"):
            return
        
        type, rest = OSC.readString(rest)
        
        if name.endswith("/pry/0"):
            pitch = 0
            
            try:
                pitch = self.readFloat(rest)[0]
                self.dx = pitch - self.pitch_old
                
                if self.b and self.dx > self.threshold:
                    self.tool_server.on_mouse_drag(0, 0, self.speed*self.dx, 0, 0, 0)
            except AttributeError:
                pass
            
            self.pitch_old = pitch
            
        if name.endswith("pry/1"):
            roll = 0
            
            try:
                roll = self.readFloat(rest)[0]
                self.dy = roll - self.roll_old
                
                if self.b and self.dy > self.threshold:
                    self.tool_server.on_mouse_drag(0, 0, 0, self.speed*self.dy, 0, 0)
            except AttributeError:
                pass
                        
            self.roll_old = roll
        
        if name.endswith("pry/2"):
            yaw = 0
            
            try:
                yaw = self.readFloat(rest)[0]
                self.dz = yaw - self.yaw_old
                
                if self.b and self.dz > self.threshold:
                    self.tool_server.on_mouse_scroll(0, 0, 0, self.speed*self.dz)
            except AttributeError:
                pass
                            
            self.yaw_old = yaw
        
        if name.endswith("pry/3"):
            accel = self.readFloat(rest)[0]
        
        if name.endswith("button/A"):
            self.a = self.readFloat(rest)[0]
            
        if name.endswith("button/B"):
            self.b = self.readFloat(rest)[0]  

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