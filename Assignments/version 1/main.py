# ****NOTE: This framework defines a world with a single polygon: a pyramid ****
#

import math
import copy
from tkinter import *

CanvasWidth = 400
CanvasHeight = 400
d = 500
objects = []


##############
# object class
##############
class object:
    def __init__(self, name):
        self.name = name
        self.polys = []
        self.pointCloud = []
        self.defaultPointCloud = []
        self.visualCenter = [0,0,0]

    # This function resets the pyramid to its original size and location in 3D space
    # Note that you have to be careful to update the values in the existing PyramidPointCloud
    # structure rather than creating a new structure or just switching a pointer.  In other
    # words, you'll need manually update the value of every x, y, and z of every point in
    # point cloud (vertex list).
    def reset(self):
        for i in range(len(self.pointCloud)):
            for j in range(3):
                self.pointCloud[i][j] = self.defaultPointCloud[i][j]

        self.update()

    def update(self):
        self.calculateVisualCenter()

    # visual center is halfway between the min and max of all cubiodal container dimensions
    def calculateVisualCenter(self):
        # define the starting min and max values
        # (can be any corresponding x,y,z value from pointCloud)
        maxx = self.pointCloud[0][0]
        minx = self.pointCloud[0][0]
        maxy = self.pointCloud[0][1]
        miny = self.pointCloud[0][1]
        maxz = self.pointCloud[0][2]
        minz = self.pointCloud[0][2]

        # loop through all points checking for corresponding min and max values
        for point in self.pointCloud:
            x = point[0]
            y = point[1]
            z = point[2]

            if (x > maxx):
                maxx = x
            if (x < minx):
                minx = x
                
            if (y > maxy):
                maxy = y
            if (y < miny):
                miny = y
                
            if (z > maxz):
                maxz = z
            if (z < minz):
                minz = z

        # final calculations for reference point
        dx = (minx + maxx) / 2
        dy = (miny + maxy) / 2
        dz = (minz + maxz) / 2
        
        self.visualCenter[0] = dx
        self.visualCenter[1] = dy
        self.visualCenter[2] = dz

    def moveToOrigin(self):
        # calculate current visual center
        self.calculateVisualCenter()

        # find the movement vector to [0,0,0]
        moveVector = [0,0,0]
        moveVector[0] = -1 * self.visualCenter[0]
        moveVector[1] = -1 * self.visualCenter[1]
        moveVector[2] = -1 * self.visualCenter[2]

        # translate object to the world origin
        translate(self.pointCloud, moveVector)

        return moveVector

    # move object back to the original visual center from origin
    def moveFromOrigin(self):
        # find the movement vector from origin
        oppMoveVector = self.visualCenter

        # translate object to the original movement vector
        translate(self.pointCloud, oppMoveVector)
        
        
        

class pyramid(object):

    def __init__(self, name):
        object.__init__(self, name)
        self.pyramid = []
    
    def setPolys(self, x, y, z):
        apex = [x+0,y+50,z+100]
        base1 = [x+50,y-50,z+50]
        base2 = [x+50,y-50,z+150]
        base3 = [x-50,y-50,z+150]
        base4 = [x-50,y-50,z+50]

        frontpoly = [apex,base1,base4]
        rightpoly = [apex,base2,base1]
        backpoly = [apex,base3,base2]
        leftpoly = [apex,base4,base3]
        bottompoly = [base1,base2,base3,base4]

        self.polys = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]
        
        self.pointCloud = [apex, base1, base2, base3, base4]
        self.defaultPointCloud = copy.deepcopy(self.pointCloud)



class cube(object):

    def __init__(self, name):
        object.__init__(self, name)
        self.cube = []

    def setPolys(self, x, y, z):
        top1 = [x-200,y+100,z+100]
        top2 = [x+0,y+100,z+100]
        top3 = [x+0,y+100,z-100]
        top4 = [x-200,y+100,z-100]
        base1 = [x-200,y-100,z+100]
        base2 = [x+0,y-100,z+100]
        base3 = [x+0,y-100,z-100]
        base4 = [x-200,y-100,z-100]

        frontpoly = [top4, top3, base3, base4,]
        backpoly = [top2, top1, base1, base2]
        toppoly = [top1, top2, top3, top4]
        bottompoly = [base1, base2, base3, base4]
        leftsidepoly = [top1, top4, base4, base1]
        rightsidepoly = [top3, top2, base2, base3]

        self.polys = [frontpoly, backpoly, toppoly, bottompoly, leftsidepoly, rightsidepoly]

        self.pointCloud = [top1,top2,top3,top4,base1,base2,base3,base4]
        self.defaultPointCloud = copy.deepcopy(self.pointCloud)

# ***************************** Initialize Pyramid Object ***************************
# Definition  of the five underlying points
apex = [0,50,100]
base1 = [50,-50,50]
base2 = [50,-50,150]
base3 = [-50,-50,150]
base4 = [-50,-50,50]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
frontpoly = [apex,base1,base4]
rightpoly = [apex,base2,base1]
backpoly = [apex,base3,base2]
leftpoly = [apex,base4,base3]
bottompoly = [base1,base2,base3,base4]

# Definition of the object
#Pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.

objPyramid = pyramid("objPyramid")
objPyramid.setPolys(0,0,0)

objects.append(objPyramid)

curObject = objPyramid
curPointCloud = curObject.pointCloud
curDefualtPointCloud = curObject.defaultPointCloud

# ***************************** Initialize Cube Object ***************************
# Definition  of the five underlying points
top1 = [-200,100,100]
top2 = [0,100,100]
top3 = [0,100,-100]
top4 = [-200,100,-100]
base1 = [-200,-100,100]
base2 = [0,-100,100]
base3 = [0,-100,-100]
base4 = [-200,-100,-100]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
frontpoly = [top4, top3, base3, base4,]
backpoly = [top2, top1, base1, base2]
toppoly = [top1, top2, top3, top4]
bottompoly = [base1, base2, base3, base4]
leftsidepoly = [top1, top4, base4, base1]
rightsidepoly = [top3, top2, base2, base3]

# Definition of the object
#Cube = [frontpoly, backpoly, toppoly, bottompoly, leftsidepoly, rightsidepoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.

objFirstCube = cube("objFirstCube")
objFirstCube.setPolys(0,0,0)
objects.append(objFirstCube)


# ***************************** Initialize Second Cube Object ***************************
# Definition  of the five underlying points
f=4
top1 = [0,100/f,100/f]
top2 = [200/f,100/f,100/f]
top3 = [200/f,100/f,-100/f]
top4 = [0,100/f,-100/f]
base1 = [0,-100/f,100/f]
base2 = [200/f,-100/f,100/f]
base3 = [200/f,-100/f,-100/f]
base4 = [0,-100/f,-100/f]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
frontpoly = [top4, top3, base3, base4,]
backpoly = [top2, top1, base1, base2]
toppoly = [top1, top2, top3, top4]
bottompoly = [base1, base2, base3, base4]
leftsidepoly = [top1, top4, base4, base1]
rightsidepoly = [top3, top2, base2, base3]

# Definition of the object
#SecondCube = [frontpoly, backpoly, toppoly, bottompoly, leftsidepoly, rightsidepoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.

objSecondCube = cube("objSecondCube")
objSecondCube.setPolys(250,0,0)
objects.append(objSecondCube)

for obj in objects:
    obj.update()

#************************************************************************************


# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(pointCloud, displacement):
    m = M4x4()

    m.matrix[3][0] = displacement[0]
    m.matrix[3][1] = displacement[1]
    m.matrix[3][2] = displacement[2]
    
    for i in range(0, len(pointCloud)):
        point = pointCloud[i]
        
        x = point[0]
        y = point[1]
        z = point[2]

        pointCloud[i][0] = (m.matrix[0][0] * x + m.matrix[3][0])
        pointCloud[i][1] = (m.matrix[1][1] * y + m.matrix[3][1])
        pointCloud[i][2] = (m.matrix[2][2] * z + m.matrix[3][2])
        
    
# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object,scalefactor):
    # move to origin
    orgMoveVector = object.moveToOrigin()

    # scale each point value
    for i in range(0, len(object.pointCloud)):
        object.pointCloud[i][0] *= scalefactor
        object.pointCloud[i][1] *= scalefactor
        object.pointCloud[i][2] *= scalefactor

    # move from origin
    object.moveFromOrigin()



# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotateZ(object,degrees):
    pointCloud = object.pointCloud

    # move to origin
    object.moveToOrigin()

    # calculate new positions using matrix math
    for i in range(0, len(pointCloud)):
    
        x = pointCloud[i][0]
        y = pointCloud[i][1]
        z = pointCloud[i][2]
        
        xrz = x*math.cos(degrees) - y*math.sin(degrees)
        yrz = x*math.sin(degrees) + y*math.cos(degrees)
        zrz = 1*z

        curObject.pointCloud[i][0] = xrz
        curObject.pointCloud[i][1] = yrz
        curObject.pointCloud[i][2] = zrz

    # move from origin
    object.moveFromOrigin()
    
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object,degrees):
    pointCloud = object.pointCloud

    # move to origin
    object.moveToOrigin()

    # calculate new positions using matrix math
    for i in range(0, len(pointCloud)):
    
        x = pointCloud[i][0]
        y = pointCloud[i][1]
        z = pointCloud[i][2]
        
        xrz = x*math.cos(degrees) + z*math.sin(degrees)
        yrz = 1*y
        zrz = x*-math.sin(degrees) + z*math.cos(degrees)

        curObject.pointCloud[i][0] = xrz
        curObject.pointCloud[i][1] = yrz
        curObject.pointCloud[i][2] = zrz

    # move from origin
    object.moveFromOrigin()

# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object,degrees):
    pointCloud = object.pointCloud

    # move to origin
    object.moveToOrigin()

    # calculate new positions using matrix math
    for i in range(0, len(pointCloud)):
    
        x = pointCloud[i][0]
        y = pointCloud[i][1]
        z = pointCloud[i][2]
        
        xrz = 1*x
        yrz = y*math.cos(degrees) - z*math.sin(degrees)
        zrz = y*math.sin(degrees) + z*math.cos(degrees)

        curObject.pointCloud[i][0] = xrz
        curObject.pointCloud[i][1] = yrz
        curObject.pointCloud[i][2] = zrz

    # move from origin
    object.moveFromOrigin()

def drawObjects(objects):
    for object in objects:
        drawObject(object)

# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object):
    for poly in object.polys:
        drawPoly(poly)

# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly):
    for i in range(0, len(poly)):
        pointA = poly[i]
        pointB = poly[i+1+((i+1)//len(poly))*-len(poly)]
        drawLine(pointA, pointB)
    

# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(start,end):
    # w.create_line(startdisplay[0],startdisplay[1],enddisplay[0],enddisplay[1])
    # convert to projection space
    startProject = project(start)
    endProject = project(end)

    # convert to display space
    startDisplay = convertToDisplayCoordinates(startProject)
    endDisplay = convertToDisplayCoordinates(endProject)

    sx = startDisplay[0]
    sy = startDisplay[1]
    ex = endDisplay[0]
    ey = endDisplay[1]
    
    w.create_line(sx, sy, ex, ey, fill="black", width=2)

# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
    ps = []

    x = point[0]
    y = point[1]
    z = point[2]

    ps.append(d * (x/(d+z)))
    ps.append(d * (y/(d+z)))
    #ps.append(d * (z/(d+z)))

    return ps

# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    displayXY = []

    x = point[0]
    y = point[1]

    displayXY.append((CanvasWidth / 2) + x)
    displayXY.append((CanvasHeight / 2) - y)
    
    return displayXY
    

# **************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    curObject.reset()
    drawObjects(objects)

def larger():
    w.delete(ALL)
    scale(curObject,1.1)
    curObject.update()
    drawObjects(objects)

def smaller():
    w.delete(ALL)
    scale(curObject,.9)
    curObject.update()
    drawObjects(objects)

def forward():
    w.delete(ALL)
    translate(curObject.pointCloud,[0,0,50])
    curObject.update()
    drawObjects(objects)

def backward():
    w.delete(ALL)
    translate(curObject.pointCloud,[0,0,-5])
    curObject.update()
    drawObjects(objects)

def left():
    w.delete(ALL)
    translate(curObject.pointCloud,[-50,0,0])
    curObject.update()
    drawObjects(objects)

def right():
    w.delete(ALL)
    translate(curObject.pointCloud,[50,0,0])
    curObject.update()
    drawObjects(objects)

def up():
    w.delete(ALL)
    translate(curObject.pointCloud,[0,5,0])
    curObject.update()
    drawObjects(objects)

def down():
    w.delete(ALL)
    translate(curObject.pointCloud,[0,-5,0])
    curObject.update()
    drawObjects(objects)

def xPlus():
    w.delete(ALL)
    rotateX(curObject,5)
    curObject.update()
    drawObjects(objects)

def xMinus():
    w.delete(ALL)
    rotateX(curObject,-5)
    curObject.update()
    drawObjects(objects)

def yPlus():
    w.delete(ALL)
    rotateY(curObject,5)
    curObject.update()
    drawObjects(objects)

def yMinus():
    w.delete(ALL)
    rotateY(curObject,-5)
    curObject.update()
    drawObjects(objects)

def zPlus():
    w.delete(ALL)
    rotateZ(curObject,5)
    curObject.update()
    drawObjects(objects)

def zMinus():
    w.delete(ALL)
    rotateZ(curObject,-5)
    curObject.update()
    drawObjects(objects)

#################################
# left / right keyboard arrow selection
################################
def newSelection(value=1):
    global curObject

    index = objects.index(curObject)
    index += value
    
    objsLength = len(objects)

    if (index > objsLength-1):
        index -= (objsLength)
    elif (index < 0):
        index += (objsLength)

    updateCurObject(objects[index])

def updateCurObject(obj):
    global curObject
    curObject = obj
    global curPointCloud
    curPointCloud = obj.pointCloud
    global curDefualtPointCloud
    curDefualtPointCloud = obj.defaultPointCloud

# temporary selection function for buttons
def newSelectionL():
    newSelection(-1)
def newSelectionR():
    newSelection(1)

#############################
# Matrix Class
####################
class M4x4:
    def __init__(self):
        self.matrix = [[1,0,0,0],
                      [0,1,0,0],
                      [0,0,1,0],
                      [0,0,0,1]]

        

root = Tk()
outerframe = Frame(root)
outerframe.pack()
# update
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
drawObjects(objects)
w.pack()

controlpanel = Frame(outerframe)
controlpanel.pack()

resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

downButton = Button(translatecontrols, text="DN", command=down)
downButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=xPlus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=xMinus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=yPlus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=yMinus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=zPlus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=zMinus)
zMinusButton.pack(side=LEFT)

selectioncontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
selectioncontrols.pack(side=LEFT)

selectioncontrolslabel = Label(selectioncontrols, text="Selection")
selectioncontrolslabel.pack()

leftSelect = Button(selectioncontrols, text="left", command=newSelectionL)
leftSelect.pack(side=LEFT)

rightSelect = Button(selectioncontrols, text="right", command=newSelectionR)
rightSelect.pack(side=LEFT)



#################################
##
################################
test = [3,4,5]

#newSelection(1)

#scale(curObject.pointCloud, 0.5)
#newSelection(1)
#newSelection(-1, curObject)
#newSelection(-1, curObject)
#newSelection(-1, curObject)
root.mainloop()
