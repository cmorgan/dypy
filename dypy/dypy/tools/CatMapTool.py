from copy import copy
from pyglet import image
from pyglet.gl import *
from dypy.gui.DynamicsWindow import DynamicsWindow

img = image.load('proshness-small.png')
width = img.width
height = img.height

channels = 1
pixels = (GLbyte*(width*height*channels))()
iteration = -1

def read_pixels(pixels, width, height):
    glReadPixels(0, 0, width, height, GL_GREEN, GL_UNSIGNED_BYTE, pixels)
    
def write_pixels(pixels, width, height):
    glDrawPixels(width, height, GL_GREEN, GL_UNSIGNED_BYTE, pixels)
    
def draw_image():
    global iteration, pixels, width, height
    
     # we don't count reading initial pixels into buffer as an iteration
    if iteration == -1:
        img.blit(0, 0)
        read_pixels(pixels, width, height)
        iteration += 1
        return    
    
    write_pixels(pixels, width, height)
    
    if iteration == 3*width:
        return

    pixels_new = (GLbyte*(width*height*channels))()
    
    for y in xrange(0, height):
        for x in xrange(0, width):
            pixel = pixels[y*width + x]
            x_new = (2*x + y) % width
            y_new = (x + y) % width           
            pixels_new[y_new*width + x_new] = pixel
    
    pixels = pixels_new
    iteration += 1

w = DynamicsWindow(width=width, height=height, caption="Cat Map", clear_each_frame=True)
w.set_viewport(0, width, 0, height)
w.set_axes_center(width/2.0, height/2.0)
w.hide_axes = True
w.loop(draw_image)