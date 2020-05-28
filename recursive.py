import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib.patches as patches
from scipy.ndimage.interpolation import rotate
from run import Pin
points = []
def isWithinRange( x, y, points):
    return (points['x1'] <= x <= points['x2']) and (points['y1'] <= y <= points['y2'])

def getProjection(left, top, width, height, x, y):
    right = left + width
    bottom = top + height
    clamp = lambda value, minv, maxv: max(min(value, maxv), minv)
    x = clamp(x, left, right)
    y = clamp(y, top, bottom)
    dl = abs(x - left)
    dr = abs(x - right)
    dt = abs(y - top)
    db = abs(y - bottom)
    m = min(dl, dr, dt, db)
    if m == dt:
        result = (x, top)
    elif m == db:
        result = (x, bottom)
    elif m == dl:
        result = (left, y)
    else:
        result = (right, y)
    return result    

def recursive(points, positions, originalPins):
    pins = []
    for pin in originalPins:
        if(isWithinRange(pin.x, pin.y, points)):
            pins.append(pin)
        else:
            newX, newY = getProjection( points['x1'], points['y2'], points['x2'] - points['x1'], points['y2'] - points['y1'], pin.x, pin.y)
            pins.append(Pin(pin.name,newX, newY, pin.gates))

        

