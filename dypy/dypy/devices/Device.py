import dypy
import socket
import threading

class Device(threading.Thread):
    def __init__(self, **kwds):
        threading.Thread.__init__(self)
        self.setDaemon(True)
               
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', kwds['port']))        
        
        self.name = kwds['name']
        self.tool_server = kwds['tool_server']
        self.speed = kwds['speed']
        self.initialized = False
        self.stopped = False
    
    def run(self):
        dypy.debug(self.name, 'Started server')
        
        while not self.stopped:
           data, address = self.s.recvfrom(128)
           
           self.parse_function(data)           
        
        dypy.debug(self.name, 'Stopped server')
       
    def stop(self):
        self.stopped = True
        self.s.close()
    
    def parse_function(self, data):
        assert 0, "must be defined"

class FakeServer():
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):    
        print "rotating [x] by", dx, ", [y] by", dy
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        print "rotating [z] by", scroll_y