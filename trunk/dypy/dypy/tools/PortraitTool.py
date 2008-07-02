from dypy.tools.Tool import Tool
import numpy
import random
import dypy

class PhasePoint():
    def __init__(self, **kwds):
        tool = kwds['tool']

        x_random = random.uniform(tool.state_ranges[tool.state_index][0], tool.state_ranges[tool.state_index][1])
        y_random = random.uniform(tool.state_ranges[tool.state_index+1][0], tool.state_ranges[tool.state_index+1][1])
        self.state = [x_random, y_random]
        self.age = random.uniform(0, tool.age_max)

class PortraitTool(Tool):
    def __init__(self, **kwds):
        Tool.__init__(self, name='Phase Portrait', description='bla', server=kwds['server'])
        dypy.debug('PortraitTool', 'initialized')
        
        self.density = 100
        self.age_max = 1000
        self.server.hide_axes = False
        self.server.clear_each_frame = False
        self.server.update_tool(self)
    
    def set_parameter_ranges(self, parameter_ranges):
        Tool.set_parameter_ranges(self, parameter_ranges)
    
    def set_state_ranges(self, state_ranges):
        Tool.set_state_ranges(self, state_ranges)
        
        sr1 = self.state_ranges[self.state_index]
        sr2 = self.state_ranges[self.state_index+1]

        self.server.set_bounds(sr1, sr2, [0, self.age_max])
        self.server.set_axes_center(sum(sr1)/2.0, sum(sr2)/2.0, 0)

    def init_points(self):
        self.points_lock.acquire()
        
        try:
            self.points = []
    
            for i in xrange(0, self.density):
                self.points.append(PhasePoint(tool=self))
        except Exception, detail:
            print 'init_points()', type(detail), detail
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
                p.state = self.system.iterate(p.state, parameters)
                p.age += 1
                
                glColor4f(1, 1, 1, p.age / (self.age_max*4.0))
                glVertex3f(p.state[self.state_index], p.state[self.state_index+1], p.age)
                
                if p.age >= self.age_max:
                    self.points[i] = PhasePoint(tool=self)
        
            glEnd()
        except AttributeError, detail:
            print detail
        except Exception, detail:
            print 'draw_points()', type(detail), detail
        finally:
            self.points_lock.release()