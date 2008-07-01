from dypy.tools.Tool import Tool
import random
import dypy

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

        self.server.set_bounds(sr1, sr2, [0, age_max])
        self.server.set_axes_center(sum(sr1)/2.0, sum(sr2)/2.0, 0)
        
    def create_point(self):
        x_random = random.uniform(self.state_ranges[self.state_index][0], self.state_ranges[self.state_index][1])
        y_random = random.uniform(self.state_ranges[self.state_index+1][0], self.state_ranges[self.state_index+1][1])
        age_random = random.uniform(0, self.age_max)
        
        return [x_random, y_random, age_random]

    def init_points(self):
        self.points_lock.acquire()
        
        try:
            self.points = []
    
            for i in xrange(0, self.density):
                self.points.append(self.create_point())
        except Exception, detail:
            print 'init_points()', type(detail), detail
        finally:
            self.points_lock.release()

    def draw_points(self):
        self.points_lock.acquire()
        i = 0
        
        try:
            from pyglet.gl import glBegin, GL_POINTS, glColor4f, glVertex3f, glEnd
            
            glBegin(GL_POINTS)
            
            for i in xrange(0, self.density):
                # only iterate x,y component
                p = self.points[i]
                x, y = self.system.iterate(p[0:2], parameters)
                p[0] = x
                p[1] = y
                p[2] += 1
                
                glColor4f(1, 1, 1, p[2] / (self.age_max*4.0))
                glVertex3f(p[0], p[1], p[2])
                
                if p[2] >= self.age_max:
                    self.points[i] = self.create_point()
        
            glEnd()
        except AttributeError, detail:
            pass
        except Exception, detail:
            print 'draw_points()', type(detail), detail
            print len(self.points), i
        finally:
            self.points_lock.release()