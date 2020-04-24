from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

class Fractal(object):

    def __init__(self, zoom_point=(0,0), resolution=(720,720), x_range=(-2.0,2.0), y_range=(-2.0,2.0), maxIterations=255, zoom=0, zoomRate=0):
        self.zoom_point = zoom_point
        self.resolution = resolution
        self.x_range = x_range
        self.y_range = y_range
        self.maxIterations = maxIterations
        self.zoom = zoom
        self.zoomRate = zoomRate
        
    def computePixel(self, x, y):
        z = complex(0.0,0.0)
        c = complex(x,y)
        iterations = 0
        while iterations < self.maxIterations and abs(z)<2:
            z = z*z + c
            iterations += 1
        pixelHue = iterations/self.maxIterations
        RGB = (hsv_to_rgb(pixelHue, 1.0, 1.0))
        return RGB

    
    def generateFrame(self):
        #x_max, x_min, y_max, y_min = self.zoom()
        x_max, x_min, y_max, y_min = (self.x_range[1],self.x_range[0],self.y_range[1],self.y_range[0])
        x_increment = (x_max - x_min)/self.resolution[0]
        y_increment = (y_max - y_min)/self.resolution[1]
        frame = []
        for y in np.arange(y_min, y_max, y_increment):
            xPixels = []
            for x in np.arange(x_min, x_max, x_increment):
                pixel_RGB= self.computePixel(x,y)
                xPixels.append(pixel_RGB)
            frame.append(xPixels)
        return np.array(frame)

    def zoom(self):
        '''this is the change that will happen in one second'''
        x_max = self.x_range[1]-(self.zoomRate/2)
        x_min = self.x_range[0]+(self.zoomRate/2)
        y_max = self.y_range[1]-(self.zoomRate/2)
        y_min = self.y_range[0]+(self.zoomRate/2)
        return (x_max, x_min, y_max, y_min)

def hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

