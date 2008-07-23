import dypy
import socket
import threading

class Device(threading.Thread):
    def __init__(self, **kwds):
        threading.Thread.__init__(self)
        self.setDaemon(True)     
        
        self.device_name = kwds['device_name']
        self.tool_server = kwds['tool_server']
        self.port = kwds['port']
        self.speed = kwds['speed']
        self.initialized = False
        self.stopped = False
    
    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', self.port))           
        dypy.debug(self.device_name, 'Started server on port ' + str(self.port))
        
        while not self.stopped:
            data, address = self.s.recvfrom(1024)
           
            self.parse_function(data)           
        
        dypy.debug(self.device_name, 'Stopped server')
       
    def stop(self):
        self.stopped = True
        self.s.close()
    
    def parse_function(self, data):
        assert 0, "must be defined"

class FakeServer():
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):    
        if dx != 0:
            print "rotating [x] by", dx
        
        if dy != 0:
            print "rotating [y] by", dy
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        print "rotating [z] by", scroll_y