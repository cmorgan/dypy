from dypy.tools.Tool import Tool
import numpy
import random
import dypy

class PortraitPoint():
    def __init__(self, **kwds):
        tool = kwds['tool']
        
        self.state = numpy.zeros(len(tool.state_ranges))
        
        for i in xrange(0, len(self.state)):
            self.state[i] = random.uniform(tool.state_ranges[i][0], tool.state_ranges[i][1])

        self.age = random.uniform(0, tool.age_max)

class PortraitTool(Tool):
    def __init__(self, **kwds):
        Tool.__init__(self, name='Phase Portrait Visualization', description='An animated phase space portrait.', server=kwds['server'])
        dypy.debug('PortraitTool', 'initialized')
        
        self.density = 100
        self.age_max = 1000
        self.server.hide_axes = False
 
    def set_state_ranges(self, state_ranges):
        x_bounds = y_bounds = z_bounds = self.state_ranges[self.state_index]
            
        if len(self.state_ranges) > 1:
            y_bounds = self.state_ranges[self.state_index+1]
        
        if len(self.state_ranges) > 2:
            z_bounds = self.state_ranges[self.state_index+2]
                
        Tool.set_state_ranges(self, state_ranges, x_bounds, y_bounds, z_bounds)

    def init_points(self):
        self.points_lock.acquire()
        
        try:
            # disable clearing points each frame when portrait tool is used,
            # set here since it's not toggleable via the gui
            self.server.clear_each_frame = False
            self.server.iteration = 0
            
            # create and initialize random points
            self.points = []
    
            for i in xrange(0, self.density):
                self.points.append(PortraitPoint(tool=self))
        except Exception, detail:
            pass
            #print 'init_points()', type(detail), detail
        finally:
            self.points_lock.release()

    def draw_points(self):
        self.points_lock.acquire()

        try:
            from pyglet.gl import glBegin, GL_POINTS, glColor4f, glVertex3f, glEnd
            
            parameters = numpy.zeros(len(self.system.get_parameter_names()))
        
            for i in range(0, len(parameters)):
                parameters[i] = self.parameter_ranges[i][0]          
            
            glBegin(GL_POINTS)
            
            for i in xrange(0, self.density):
                p = self.points[i]
                
                x = p.state[self.state_index]
                y = 0
                z = 0
                
                if len(self.state_ranges) > 1:
                    y = p.state[self.state_index+1]
                
                if len(self.state_ranges) > 2:
                    z = p.state[self.state_index+2]
                
                glColor4f(1, 1, 1, p.age / (self.age_max*4.0))
                glVertex3f(x, y, z)
                
                p.state = self.system.iterate(p.state, parameters)
                p.age += 1
                
                if p.age >= self.age_max:
                    self.points[i] = PortraitPoint(tool=self)
        
            glEnd()
        except Exception, detail:
            print 'draw_points()', type(detail), detail
        finally:
            self.points_lock.release()