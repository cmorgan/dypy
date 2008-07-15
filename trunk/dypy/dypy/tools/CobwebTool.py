from dypy.tools.Tool import Tool
import numpy
import random
import dypy

class CobwebPoint():
    def __init__(self, **kwds):
        self.tool = kwds['tool']
        
        self.state = self.get_random_state()
        self.parameters = self.pack_parameters()

    def get_random_state(self):
        state = numpy.zeros(len(self.tool.state_ranges))
        
        for i in xrange(0, len(state)):
            state[i] = random.uniform(self.tool.state_ranges[i][0], self.tool.state_ranges[i][1])
        
        return state
      
    def pack_parameters(self):
        parameters = numpy.zeros(len(self.tool.parameter_ranges))
            
        for i in xrange(0, len(parameters)):
            parameters[i] = self.tool.parameter_ranges[i][0]
        
        return parameters       

class CobwebTool(Tool):
    def __init__(self, **kwds):
        Tool.__init__(self, name='Cobweb Visualization', description='', server=kwds['server'])
        dypy.debug('CobwebTool', 'initialized')
    
    def get_bounds(self):
        x_bounds = y_bounds = self.state_ranges[self.state_index]
        z_bounds = [-1, 1]        
        return x_bounds, y_bounds, z_bounds

    def init_points(self):
        self.points_lock.acquire()
        
        try:
            from pyglet.gl import glGenLists, glNewList, GL_COMPILE, glBegin, GL_LINE_STRIP, GL_LINES, \
                glColor4f, glVertex2f, glEnd, glEndList, glEnable
                        
            self.server.clear_each_frame = False
            self.server.iteration = 0            

            # initial state/parameters
            self.point = CobwebPoint(tool=self)
     
            # create display list for first iterate of function
            self.iterate_list = glGenLists(1)
            
            glNewList(self.iterate_list, GL_COMPILE)
            glBegin(GL_LINE_STRIP)
            glColor4f(217/255.0, 115/255.0, 56/255.0, 0.9)
            
            p = CobwebPoint(tool=self)
            
            for i in numpy.arange(self.state_ranges[self.state_index][0], self.state_ranges[self.state_index][1], 0.001):
                p.state[self.state_index] = i
                state_new = self.system.iterate(p.state, p.parameters)
                glVertex2f(i, state_new[self.state_index])
            
            glEnd()
            glEndList()    
            
            # create display list for axis of reflection
            self.reflection_list = glGenLists(1)
            
            glNewList(self.reflection_list, GL_COMPILE)
            glBegin(GL_LINES)
            glColor4f(217/255.0, 88/255.0, 41/255.0, 0.9)
            
            glVertex2f(self.state_ranges[self.state_index][0], self.state_ranges[self.state_index][0])
            glVertex2f(self.state_ranges[self.state_index][1], self.state_ranges[self.state_index][1])
            
            glEnd()
            glEndList()
        except Exception, detail:
            print 'init_points()', type(detail), detail
        finally:
            self.points_lock.release()

    def draw_points(self):
        self.points_lock.acquire()
        
        try:
            from pyglet.gl import glCallList, glBegin, GL_LINE_STRIP, glColor4f, glVertex2f, glEnd                   
            
            # line from previous iterate to next iterate of function
            glBegin(GL_LINE_STRIP)            
            glColor4f(1, 1, 1, 0.3)
            
            for i in [1, 2]:
                state_previous = self.point.state[self.state_index]
                self.point.state = self.system.iterate(self.point.state, self.point.parameters)
            
                glVertex2f(state_previous, state_previous)
                glVertex2f(state_previous, self.point.state[self.state_index])
            
            glEnd()
            
            # call display lists, doesn't work in init_points()
            if self.server.iteration == 0:
                glCallList(self.iterate_list)            
                glCallList(self.reflection_list)
        except Exception, detail:
            print 'draw_points()', type(detail), detail
        finally:
            self.points_lock.release()