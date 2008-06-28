from numpy import array
from pyglet.gl import *
from random import uniform
from dypy.gui.DynamicsWindow import DynamicsWindow
from dypy.systems import *

# map parameters
ode = LorenzODE.LorenzODE()
parameters = (10, 28, -8/3.0)
x_min = -40
x_max = 40
y_min = -40
y_max = 40
z_min = 0
z_max = 40
#ode = RosslerODE.RosslerODE()
#parameters = (0.2, 0.2, 5.7)
#x_min = -20
#x_max = 20
#y_min = -10
#y_max = 10
#z_min = 0
#z_max = 80

# dynamic visualization parameters
points_max = 50

# static visualization parameters
state_initial = array([.3, .3, .3])
dt = 0.005
iterations = int(300 * (1/dt))
attractor_list = 0

# initial random state values
def create_point():
    return [uniform(x_min, x_max), uniform(y_min, y_max), uniform(z_min, z_max)]

points = []

for i in xrange(0, points_max):
    points.append(create_point())

def draw_points():
    global points, parameters, dt
    
    glBegin(GL_POINTS)
    glColor4f(1, 1, 1, 0.2)
        
    for i in xrange(0, points_max):
        p = points[i]
        p = ode.integrate(p, parameters, dt)
        points[i] = p
        glVertex3f(p[0], p[1], p[2])

    glEnd()
    
# pre-compile attractor as display list
def create_attractor():
    global state_initial, parameters, dt
    
    list = glGenLists(1)
    
    glNewList(list, GL_COMPILE)
    glBegin(GL_LINE_STRIP)
 
    glColor4f(1, 1, 1, 0.2)
    state = state_initial
    
    for i in xrange(iterations):
        glVertex3f(state[0], state[1], state[2])
        state = ode.integrate(state, parameters, dt)
        
    glEnd()
    glEndList()
    
    return list

def draw_attractor():
    global attractor_list
    
    if attractor_list == 0:
        attractor_list = create_attractor()
        
    glCallList(attractor_list)

# dynamics window
w = DynamicsWindow(width=1000, height=800, caption=ode.name, clear_each_frame=False)
#w = DynamicsWindow(width=1000, height=800, caption=ode.name, clear_each_frame=True)
w.set_bounds((x_min, x_max), (y_min, y_max), (z_min, z_max))
#w.set_axes_center(0, 0, 20)
#w.loop(draw_attractor)
w.loop(draw_points)