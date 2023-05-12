######################
# All Draw Functions #
######################
from tkinter import *

# canvas object
class myCanvas:

    def __init__(self, nice, width, height):
        self.w = 0
        
    # draw a single pixel on canvas
    def drawPixel(self, point, color):
        x = point[0]
        y = point[1]
        
        self.w.create_line(x, y, x+1, y, fill=color, width=2)

    # draw a single line on canvas
    def drawLine(self, PA, PB, color, newWidth):
        Ax = PA[0]
        Ay = PA[1]
        Bx = PB[0]
        By = PB[1]
        
        self.w.create_line(Ax, Ay, Bx, By, fill=color, width=newWidth)
