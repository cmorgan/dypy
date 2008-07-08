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
            self.state = numpy.zeros(len(self.state_ranges))
        
            for i in xrange(0, len(self.state)):
                self.state[i] = random.uniform(self.state_ranges[i][0], self.state_ranges[i][1])
        except Exception, detail:
            print 'init_points()', type(detail), detail
        finally:
            self.points_lock.release()

    def draw_points(self):
        self.points_lock.acquire()
        
        try:
            from pyglet.gl import glBegin, GL_LINE_STRIP, glVertex2f, glEnd
           
            parameters = numpy.zeros(len(self.system.get_parameter_names()))
            
            for i in range(0, len(parameters)):
                parameters[i] = self.parameter_ranges[i][0]        
            
            glBegin(GL_LINE_STRIP)
            
            state_previous = self.state
            self.state = self.system.iterate(self.state, parameters)
            
            glVertex2f(state_previous[self.state_index], state_previous[self.state_index])
            glVertex2f(state_previous[self.state_index], self.state[self.state_index])
            
            glEnd()
        except Exception, detail:
            print 'draw_points()', type(detail), detail
        finally:
            self.points_lock.release()