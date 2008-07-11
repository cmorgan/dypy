from dypy.tools.Tool import Tool
import numpy
import random
import dypy

class CobwebTool(Tool):
    def __init__(self, **kwds):
        Tool.__init__(self, name='Cobweb Visualization', description='', server=kwds['server'])
        dypy.debug('CobwebTool', 'initialized')
    
    def set_state_ranges(self, state_ranges):
        Tool.set_state_ranges(self, state_ranges)
        
        sr = self.state_ranges[self.state_index]

        self.server.set_bounds(sr, sr, sr)
    
    def init_points(self):
        self.points_lock.acquire()
        
        try:
            from pyglet.gl import glGenLists, glNewList, GL_COMPILE, glBegin, GL_LINE_STRIP, GL_LINES, \
                glColor4f, glVertex2f, glEnd, glEndList, \
                glEnable, GL_LINE_SMOOTH, glHint, GL_LINE_SMOOTH_HINT, GL_NICEST
            import copy
                        
            self.server.clear_each_frame = False
            self.server.iteration = 0            
            
            # create random initial state
            self.state = numpy.zeros(len(self.state_ranges))
        
            for i in xrange(0, len(self.state)):
                self.state[i] = random.uniform(self.state_ranges[i][0], self.state_ranges[i][1])

            # pack parameters into array
            parameters = numpy.zeros(len(self.system.get_parameter_names()))
            
            for i in xrange(0, len(parameters)):
                parameters[i] = self.parameter_ranges[i][0]
     
            # enable line anti-aliasing
            #glEnable(GL_LINE_SMOOTH)
            #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
     
            # create display list for first iterate of function
            self.iterate_list = glGenLists(1)
            
            glNewList(self.iterate_list, GL_COMPILE)
            glBegin(GL_LINE_STRIP)
            glColor4f(0, 0.8, 0, 0.5)
            
            for i in numpy.arange(self.state_ranges[self.state_index][0], self.state_ranges[self.state_index][1], 0.01):
                s = copy.copy(self.state)
                s[self.state_index] = i
                glVertex2f(i, self.system.iterate(s, parameters))
            
            glEnd()
            glEndList()    
            
            # create display list for axis of reflection
            self.reflection_list = glGenLists(1)
            
            glNewList(self.reflection_list, GL_COMPILE)
            glBegin(GL_LINES)
            glColor4f(0, 0, 1, 0.5)
            
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
            
            # pack parameters into array
            parameters = numpy.zeros(len(self.system.get_parameter_names()))
            
            for i in xrange(0, len(parameters)):
                parameters[i] = self.parameter_ranges[i][0]            
            
            # line from previous iterate to next iterate of function
            glBegin(GL_LINE_STRIP)            
            glColor4f(1, 1, 1, 0.1)
            
            for i in [1, 2]:
                state_previous = self.state[self.state_index]
                self.state = self.system.iterate(self.state, parameters)
            
                glVertex2f(state_previous, state_previous)
                glVertex2f(state_previous, self.state[self.state_index])
            
            glEnd()
            
            # call display lists
            glCallList(self.iterate_list)            
            glCallList(self.reflection_list)            
        except Exception, detail:
            print 'draw_points()', type(detail), detail
        finally:
            self.points_lock.release()