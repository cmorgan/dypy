from dypy.tools.Tool import Tool
import numpy
import random
import dypy

class OrbitPoint():
    def __init__(self, **kwds):
        self.tool = kwds['tool']
        self.state = self.get_random_state()
        self.age = self.get_random_age()
        
        # set non-varying parameters to their respective minimum,
        # else set the varying parameter to value passed in        
        self.parameters = numpy.zeros(len(self.tool.parameter_ranges))
        
        for i in xrange(0, len(self.parameters)):
            if i == self.tool.parameter_index:
                self.parameters[i] = kwds['varying_parameter']
            else:
                self.parameters[i] = self.tool.parameter_ranges[i][0]
    
    def get_random_age(self):
        return random.uniform(0, self.tool.age_max)
    
    def get_random_state(self):    
        size = len(self.tool.system.get_state_names())
        state = numpy.zeros(size)
        
        for i in xrange(0, size):
            state[i] = random.uniform(self.tool.state_ranges[i][0], \
                                      self.tool.state_ranges[i][1])
        
        return state   

class OrbitTool(Tool):
    def __init__(self, **kwds):
        Tool.__init__(self, name='Orbit Visualization', description='An animated orbit diagram.', server=kwds['server'])
        dypy.debug("OrbitTool", "Initialized.")
        
        self.age_max = 1000  
        self.density = 3
        self.server.hide_axes = True
        self.server.clear_each_frame = True
        self.server.update_tool(self)

    def set_age_max(self, age_max):
        self.points_lock.acquire()
        
        try:
            self.age_max = age_max
            self.server.update_tool(self)
        finally:
            self.points_lock.release()
    
    def set_density(self, density):
        self.points_lock.acquire()
        
        try:
            self.density = density
            self.server.update_tool(self)
        finally:
            self.points_lock.release()
    
    def set_show_history(self, show_history):
        self.server.clear_each_frame = not(show_history)
    
    def set_state_ranges(self, state_ranges):
        Tool.set_state_ranges(self, state_ranges)
        
        pr = self.parameter_ranges[self.parameter_index]
        sr = self.state_ranges[self.state_index]        
    
        self.server.set_bounds(pr, sr, [0, 0])
        self.server.set_axes_center(sum(pr)/2.0, sum(sr)/2.0, 0)

    def set_parameter_ranges(self, parameter_ranges):
        Tool.set_parameter_ranges(self, parameter_ranges)
        
        pr = self.parameter_ranges[self.parameter_index]
        sr = self.state_ranges[self.state_index]        
    
        self.server.set_bounds(pr, sr, [0, 0])
        self.server.set_axes_center(sum(pr)/2.0, sum(sr)/2.0, 0)

    def init_points(self):
        self.points_lock.acquire()
        
        try:
            self.points = []
            parameter_increment = (self.parameter_ranges[self.parameter_index][1] - \
                                   self.parameter_ranges[self.parameter_index][0]) / float(self.server.width)
            parameter = self.parameter_ranges[self.parameter_index][0]
            
            for i in xrange(0, self.server.width):
                for j in xrange(0, self.density):
                    self.points.append(OrbitPoint(tool=self, varying_parameter=parameter))
                
                parameter += parameter_increment        
        except Exception, detail:
            pass
        finally:
            self.points_lock.release()

    def draw_points(self):
        self.points_lock.acquire()
        
        try:
            from pyglet.gl import glBegin, glEnd, GL_POINTS, glColor4f, glVertex2f
            
            point_count = len(self.points)
            
            if point_count == 0:
                return
                   
            glBegin(GL_POINTS)
               
            for i in xrange(0, point_count):
                p = self.points[i]

                glColor4f(1, 1, 1, p.age / self.age_max*2.0)
                glVertex2f(p.parameters[self.parameter_index], p.state[self.state_index])
                
                p.state = self.system.iterate(p.state, p.parameters)
                p.age += 1
                
                if p.age >= self.age_max:
                    self.points[i] = OrbitPoint(tool=self, varying_parameter=p.parameters[self.parameter_index])
            
            glEnd()
        except AttributeError, detail:
            pass
        except Exception, detail:
            print 'draw_points()', type(detail), detail
        finally:
            self.points_lock.release()