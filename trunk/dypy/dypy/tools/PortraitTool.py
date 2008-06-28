from pyglet.gl import *
from random import uniform
from dypy.gui.DynamicsWindow import DynamicsWindow
from dypy.systems import *

# map parameters
#map = StandardMap.StandardMap()
#parameters = 1.2
map = HenonMap.HenonMap()
parameters = (1.4, 0.3)
#map = NeuronMap.NeuronMap()
#parameters = (7.0, 0.01, 0.33)
range1 = map.get_state_ranges()[0]
range2 = map.get_state_ranges()[1]

# visualization parameters
points_max = 100
age_max = 1000

# initial random state values
def create_point():
    return [uniform(range1[0], range1[1]), uniform(range2[0], range2[1]), uniform(0, age_max)]

points = []

for i in xrange(0, points_max):
    points.append(create_point())

def draw_points():
    global points
    
    glBegin(GL_POINTS)
    
    for i in xrange(0, points_max):
        # only iterate x,y component
        p = points[i]
        x, y = map.iterate(p[0:2], parameters)
        p[0] = x
        p[1] = y
        p[2] += 1
        
        glColor4f(1, 1, 1, p[2] / (age_max*4.0))
        glVertex3f(p[0], p[1], p[2])
        
        if p[2] >= age_max:
            points[i] = create_point()

    glEnd()

# dynamics window
w = DynamicsWindow(width=1000, height=800, caption=map.name, clear_each_frame=False)
w.set_viewport(range1, range2, [0, age_max])
w.set_axes_center(sum(range1)/2, sum(range2)/2, age_max/2.0)
w.loop(draw_points)