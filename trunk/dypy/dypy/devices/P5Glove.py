import dypy
import OSC
import socket
import threading

class P5Glove(threading.Thread):
    def __init__(self, tool_server, port=7000):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', port))
        
        self.scale = 0.2
        self.initialized = False
        self.stopped = False
        self.tool_server = tool_server

    def run(self):
        dypy.debug("P5Glove", "Started server")
                
        while not self.stopped:
            data, address = self.s.recvfrom(128)
            
            # OSC.py used > (big endian) in struct.unpack,
            # which is incorrect for mac
            address, rest   = OSC.readString(data)
            time, rest      = OSC.readLong(rest)
            length, rest    = OSC.readInt(rest)
            name, rest      = OSC.readString(rest)
            
            if name != "/p5glove_data":
                continue
            
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
                self.dx = self.scale * (x - self.x_old)
                self.dy = self.scale * (y - self.y_old)
                self.dz = self.scale * (z - self.z_old)    
                
                self.tool_server.on_mouse_drag(0, 0, self.dx, self.dy, 0, 0)
                self.tool_server.on_mouse_scroll(0, 0, 0, self.dz)  
            else:
                self.initialized = True
                
            self.x_old = x
            self.y_old = y
            self.z_old = z
        
        dypy.debug("P5Glove", "Stopped server") 
    
    def stop(self):
        self.stopped = True
        self.s.close()

class FakeServer():
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):    
        print "rotating [x] by", dx, ", [y] by", dy
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        print "rotating [z] by", scroll_y

if __name__ == '__main__':
    glove_server = P5Glove(FakeServer())
    glove_server.start()
    glove_server.join()