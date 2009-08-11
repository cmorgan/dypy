from Device import *
import OSC

class SpaceNavigatorDevice(Device):
    def __init__(self, tool_server, port=9001):
        Device.__init__(self, device_name='SpaceNavigator', tool_server=tool_server, port=port, speed=150)

    def parse_function(self, data):
        # OSC.py uses big endian, OSC.readInt changed to little endian for p5osc
        name, rest = OSC.readString(data)
        
        if not name.startswith("/sp"):
            return    
        
        type, rest = OSC.readString(rest)
        
        if name.endswith("rot/xyz/0"):
            self.parse_field(rest, 'pitch', 'y')

        if name.endswith("rot/xyz/1"):
            self.parse_field(rest, 'roll', 'x')
        
        if name.endswith("rot/xyz/2"):
            self.parse_field(rest, 'yaw', 'z')        
            
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
        
        if axis == 'x':
            self.tool_server.on_mouse_drag(0, 0, self.speed*self.delta, 0, 0, 0)
        elif axis == 'y':
            self.tool_server.on_mouse_drag(0, 0, 0, self.speed*self.delta, 0, 0)      
        elif axis == 'z':
            self.tool_server.on_mouse_scroll(0, 0, 0, -self.speed*self.delta)            
    
if __name__ == '__main__':
    sn_server = SpaceNavigatorDevice(FakeServer())
    sn_server.start()
    sn_server.join()