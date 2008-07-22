import dypy
import OSC
import socket
import threading

class P5Glove(threading.Thread):
    def __init__(self, **kwds):
        threading.Thread.__init__(self)
        
        port = 7000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', port))
        
        self.initialized = False
        self.stopped = False
        self.tool_server = kwds['tool_server']

    def run(self):
        dypy.debug("P5Glove", "Started server")
                
        while not self.stopped:
            data, address = self.s.recvfrom(1024)
            
            # OSC.py used > (big endian) in struct.unpack,
            # which is incorrect for mac
            address, rest   = OSC.readString(data)
            time, rest      = OSC.readLong(rest)
            length, rest    = OSC.readInt(rest)
            name, rest      = OSC.readString(rest)
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
                self.dx = x - self.x_old
                self.dy = y - self.y_old
                self.dz = z - self.z_old               
                
                self.tool_server.on_mouse_drag(0, 0, self.dx, self.dy, 0, 0)
                self.tool_server.on_mouse_scroll(0, 0, 0, self.dz)  
            else:
                self.initialized = True
                
            self.x_old = x
            self.y_old = y
            self.z_old = z         
    
    def stop(self):
        self.stopped = True
        self.s.close()
        dypy.debug("P5Glove", "Stopped server")

if __name__ == 'main':
    glove_server = P5Glove()
    glove_server.start()
    glove_server.join()