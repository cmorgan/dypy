import Pyro.core
import Pyro.naming
import threading
import time
import dypy

gl_lock = threading.Lock()

class PyroServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.starter = Pyro.naming.NameServerStarter()
        self.daemon = Pyro.core.Daemon(host='localhost')
        self.setDaemon(True)
                      
    def run(self):
        self.starter.start(hostname='localhost')
              
    def waitUntilStarted(self):
        self.starter.waitUntilStarted()
        self.daemon.useNameServer(Pyro.naming.NameServerLocator().getNS())
        dypy.debug("PyroServer", "Listening on port " + str(self.daemon.port))

class ToolServer(Pyro.core.ObjBase, threading.Thread):    
    def __init__(self, **kwds):
        Pyro.core.ObjBase.__init__(self)        
        threading.Thread.__init__(self)

        self.width = kwds['width']
        self.height = kwds['height']
        self.ready = 0
    
    def waitUntilStarted(self):
        while not self.ready:
            time.sleep(1)   
    
    def update_tool(self, tool):
        self.tool = tool
        self.tool_updated = True
    
    def get_tools(self):
        return self.tools
    
    def pause(self):
        self.window_paused = True
        self.window.set_visible(False)
    
    def unpause(self):
        self.window_paused = False
        self.window.set_visible(True)
    
    def run(self):
        import pyglet
        pyglet.options['debug_gl'] = False        
        
        from dypy.tools.PortraitTool import PortraitTool
        from dypy.tools.OrbitTool import OrbitTool
        from pyglet.gl import glBlendFunc, glEnable, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, \
            GL_BLEND, glClear, GL_COLOR_BUFFER_BIT, glMatrixMode, GL_PROJECTION, GL_MODELVIEW, \
            glLoadIdentity, glTranslatef, glRotatef, gl_info, glViewport, glOrtho
        import pyglet.clock
        import pyglet.window
        import select
        
        self.window = pyglet.window.Window(width=self.width, height=self.height, visible=False)
        self.window.set_location(450, 0)
        self.window.on_resize = self.on_resize
        self.window.on_close = self.on_close
        self.window.on_key_press = self.on_key_press
        self.window.on_mouse_drag = self.on_mouse_drag
        self.window.on_mouse_scroll = self.on_mouse_scroll
        
        # create and wait for object server
        self.server = PyroServer()
        self.server.start()
        self.server.waitUntilStarted()

        # for rotating points
        self.x_rotate = 0
        self.y_rotate = 0
        self.z_rotate = 0
        
        # visualization parameters
        self.clear_each_frame = False
        self.hide_axes = False
        self.rotation_velocity = 0.8
        self.iteration = 0
        self.set_axes_center()
        self.set_bounds((-1, 1), (-1, 1), (-1, 1), False)
        
        # don't hog more cpu than is useful
        pyglet.clock.set_fps_limit(30)
        
        # create tools and connect them to server
        self.server.daemon.connect(self, 'ToolServer')
        
        t = PortraitTool(server=self)
        self.server.daemon.connect(t, 'PortraitTool')
        
        t = OrbitTool(server=self)
        self.server.daemon.connect(t, 'OrbitTool')
        
        self.update_tool(t)
        
        # setup alpha blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        
        # gl diagnostics
        dypy.debug("ToolServer", "GL version is %s." % gl_info.get_version())
        dypy.debug("ToolServer", "GL renderer is %s." % gl_info.get_renderer())
        dypy.debug("ToolServer", "Pyglet version is %s." % pyglet.version)
        
        # event flags
        self.ready = True
        self.tool_updated = False
        self.window_resized = False
        self.window_paused = True

        while not self.window.has_exit:
            pyglet.clock.tick()          
            gl_lock.acquire()
            
            try:
                self.window.dispatch_events()
                
                if self.tool_updated:
                    self.tool_updated = False
                    self.tool.init_points()
                
                if self.window_resized:
                    self.window_resized = False
         
                    if (self.x_min == 0 and self.x_max == 0) or (self.y_min == 0 and self.y_max == 0):
                        continue
                    
                    glViewport(0, 0, self.width, self.height)
            
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    
                    dypy.debug("ToolServer", "Setting projection to %.1f %.1f %.1f %.1f %.1f %.1f" % (self.x_min, self.x_max, self.y_min, self.y_max, -self.dimension_max, self.dimension_max))
                    glOrtho(self.x_min, self.x_max, self.y_min, self.y_max, -self.dimension_max, self.dimension_max)             
                
                if self.clear_each_frame or self.iteration == 0:
                    glClear(GL_COLOR_BUFFER_BIT)
    		    
    			# reset model matrix
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
    			
                # translate to center
                glTranslatef(self.x_center, self.y_center, self.z_center)
    			
                # rotate around axes
                glRotatef(self.x_rotate, 1, 0, 0)
                glRotatef(self.y_rotate, 0, 1, 0)
                glRotatef(self.z_rotate, 0, 0, 1)
    			
                # draw reference axes
                if not self.hide_axes and (self.clear_each_frame or self.iteration == 0):
                    self.draw_axes() 
    			
                # translate back to lower left corner
                glTranslatef(-self.x_center, -self.y_center, -self.z_center)    
    
                # tell the tool to draw its content
                if not self.window_paused:
                    self.tool.draw_points()
    
                    # iteration is done, swap display buffers
                    self.iteration += 1
                    self.window.flip()
    
                # process server requests
                socks = self.server.daemon.getServerSockets()
                ins, outs, exs = select.select(socks, [], [], 0)
                
                for s in socks:
                    if s in ins:
                        self.server.daemon.handleRequests()
                        break
            except Exception, detail:
                print type(detail), detail
            finally:
                gl_lock.release()
            
        self.window.close()
        
    def set_axes_center(self, x_center=0, y_center=0, z_center=0):
        self.x_center = x_center
        self.y_center = y_center
        self.z_center = z_center
          
    def draw_axes(self):
        from pyglet.gl import glColor4f, glVertex3f, glBegin, glEnd, GL_LINES
        
        glColor4f(0xff/255.0, 0x99/255.0, 0x4d/255.0, 0.2)
	    
        glBegin(GL_LINES)
        glVertex3f(-self.dimension_max**2, 0, 0)
        glVertex3f(self.dimension_max**2, 0, 0)
        glEnd()
	    
        glBegin(GL_LINES)
        glVertex3f(0, -self.dimension_max**2, 0)
        glVertex3f(0, self.dimension_max**2, 0)
        glEnd()
	    
        glBegin(GL_LINES)
        glVertex3f(0, 0, -self.dimension_max**2)
        glVertex3f(0, 0, self.dimension_max**2)
        glEnd()

    def set_bounds(self, (x_min, x_max), (y_min, y_max), (z_min, z_max), resize=True):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.dimension_max = max(abs(self.x_min), abs(self.x_max), \
            abs(self.y_min), abs(self.y_max), abs(self.z_min), abs(self.z_max))
        
        if resize:
            self.on_resize(self.width, self.height) 
	
    def on_close(self):
        self.window.has_exit = True
        self.server.daemon.shutdown()
    
    def on_resize(self, width, height):        
        self.window_resized = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):    
	    self.y_rotate += (dx * self.rotation_velocity) # change in x rotates around y-axis
	    self.y_rotate %= 360
	    
	    self.x_rotate += (dy * self.rotation_velocity) # change in y rotates around x-axis
	    self.x_rotate %= 360
	    
	    self.iteration = 0
	
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
	    self.z_rotate += (scroll_y * self.rotation_velocity)
	    self.z_rotate %= 360
	    
	    self.iteration = 0
	
    def on_key_press(self, symbol, modifiers):  
        if symbol == 65293: # a button
	        self.x_rotate = self.y_rotate = self.z_rotate = self.iteration = 0
        elif symbol == 65289: # b button
	        self.hide_axes = not(self.hide_axes)
	        self.iteration = 0
        elif symbol == 65363: # right
	        self.on_mouse_drag(0, 0, -10, 0, 0 ,0)
        elif symbol == 65364: # down
	        self.on_mouse_drag(0, 0, 0, -10, 0 ,0)
        elif symbol == 65361: # left
	        self.on_mouse_drag(0, 0, 10, 0, 0 ,0)
        elif symbol == 65362: # up
	        self.on_mouse_drag(0, 0, 0, 10, 0 ,0)
        elif symbol == 65288: # backspace
            import sys
            sys.exit()