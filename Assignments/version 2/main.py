# ****NOTE: This framework defines a world with a single polygon: a pyramid ****
#
##########################
# CULLING DOESN'T CHANGE WITH TRNASLATION AND SCALING
###########################

import math
import copy
from mymath import *
from tkinter import *

CanvasWidth = 400
CanvasHeight = 400
d = 500
objects = []
curObject = 0
curPointCloud = 0
curDefualtPointCloud = 0
curRender = 3

# Z buffer creation
def createZBuffer(row, col):
    arr = []
    
    for r in range(row):
        tempArr = []
        for c in range(col):
            # fill with default
            tempArr.append(d)
        arr.append(tempArr)
    return arr

##############
# object class
##############
class object:
    def __init__(self, name):
        self.name = name
        self.polys = []
        self.pointCloud = []
        self.defaultPointCloud = []
        self.transformation = m4x4()
        self.visualCenter = [0,0,0]
        self.selectColor = "black"
        self.selectWidth = 2

    def setup(self,x=0,y=0,z=0,size=1):
        self.setPolys(x,y,z,size)
        self.calculateVisualCenter()

    # This function resets the pyramid to its original size and location in 3D space
    # Note that you have to be careful to update the values in the existing PyramidPointCloud
    # structure rather than creating a new structure or just switching a pointer.  In other
    # words, you'll need manually update the value of every x, y, and z of every point in
    # point cloud (vertex list).
    def reset(self):
        for i in range(len(self.pointCloud)):
            for j in range(3):
                self.pointCloud[i][j] = self.defaultPointCloud[i][j]
                self.transformation = m4x4()

        self.update()

    def update(self):
        # debug
        #print("pyramid")
        #print(objects[0].z)
        self.updatePolys()
        self.calculateVisualCenter()
        

    def updatePolys(self):
        # update all points int pointcloud 
        for i in range(0, len(self.pointCloud)):
            # create a point into a vector3
            point = self.defaultPointCloud[i]
            vector = vector3(point[0], point[1], point[2])
            transform = self.transformation.matrix
            
            # update vector(point) using the transformation matrix
            # transformation matrix acts as a composite matrix maintaining previous calculations
            vector.dotM(transform)

            # update 
            self.pointCloud[i][0] = vector.x
            self.pointCloud[i][1] = vector.y
            self.pointCloud[i][2] = vector.z
    
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

# ***************************** Polygon Class *************************** #
class polygon:

    def __init__(self, name, pointA, pointB, pointC):
        pass
        

# ***************************** Pyramid Class *************************** #
class pyramid(object):

    def __init__(self, name):
        object.__init__(self, name)
        self.pyramid = []
    
    def setPolys(self, x=0, y=0, z=0, size=1):
        # Definition  of the five underlying points
        #apex = [x+0,y+50,z+100]
        #base1 = [x+50,y-50,z+50]
        #base2 = [x+50,y-50,z+150]
        #base3 = [x-50,y-50,z+150]
        #base4 = [x-50,y-50,z+50]
        defaultSize = size * 1
        #apex = [x+0,y+defaultSize,z+0]
        #base1 = [x-defaultSize,y+0,z+defaultSize]
        #base2 = [x+defaultSize,y+0,z+defaultSize]
        #base3 = [x-defaultSize,y+0,z-defaultSize]
        #base4 = [x+defaultSize,y+0,z-defaultSize]
        apex = [0,-100,100]
        base1 = [-50,-150,150]
        base2 = [50,-150,150]
        base3 = [-50,-150,50]
        base4 = [50,-150,50]

        # Definition of the five polygon faces using the meaningful point names
        # Polys are defined in clockwise order when viewed from the outside
        frontpoly = [apex,base4,base3]
        backpoly = [apex,base1,base2]
        leftpoly = [apex,base3,base1]
        rightpoly = [apex,base2,base4]
        bottompoly = [base3,base4,base2,base1]

        self.polys = [frontpoly, backpoly, leftpoly, rightpoly, bottompoly]

        # Definition of the Pyramid's underlying point cloud.  No structure, just the points.
        self.pointCloud = [apex, base1, base2, base3, base4]
        self.defaultPointCloud = copy.deepcopy(self.pointCloud)

        # 5 polygons, 5 colors
        self.colors =  ["red", "black", "green", "blue", "yellow"]



# ***************************** Cube Class ***************************
class cube(object):

    def __init__(self, name):
        object.__init__(self, name)
        self.cube = []

    def setPolys(self, x=0, y=0, z=0, size=1):
        # Definition  of the six underlying points
        defaultSize = 10
        defaultSize += size
        
        #top1 = [x-defaultSize,y+defaultSize,z+defaultSize]
        #top2 = [x+defaultSize,y+defaultSize,z+defaultSize]
        #top3 = [x+defaultSize,y+defaultSize,z-defaultSize]
        #top4 = [x-defaultSize,y+defaultSize,z-defaultSize]
        #base1 = [x-defaultSize,y-defaultSize,z+defaultSize]
        #base2 = [x+defaultSize,y-defaultSize,z+defaultSize]
        #base3 = [x+defaultSize,y-defaultSize,z-defaultSize]
        #base4 = [x-defaultSize,y-defaultSize,z-defaultSize]
        top1 = [x-defaultSize,y+defaultSize,z+defaultSize]
        top2 = [x+defaultSize,y+defaultSize,z+defaultSize]
        top3 = [x-defaultSize,y+defaultSize,z-defaultSize]
        top4 = [x+defaultSize,y+defaultSize,z-defaultSize]
        base1 = [x-defaultSize,y-defaultSize,z+defaultSize]
        base2 = [x+defaultSize,y-defaultSize,z+defaultSize]
        base3 = [x-defaultSize,y-defaultSize,z-defaultSize]
        base4 = [x+defaultSize,y-defaultSize,z-defaultSize]
        
        # Definition of the six polygon faces using the meaningful point names
        # Polys are defined in clockwise order when viewed from the outside
        frontpoly = [top3, top4, base4, base3,]
        backpoly = [top2, top1, base1, base2]
        toppoly = [top1, top2, top4, top3]
        bottompoly = [base2, base1, base3, base4]
        leftsidepoly = [top1, top3, base3, base1]
        rightsidepoly = [top4, top2, base2, base4]

        self.polys = [frontpoly, backpoly, toppoly, bottompoly, leftsidepoly, rightsidepoly]

        # adjust original points by the size given
        for poly in self.polys:
            for point in poly:
                for i in range(0,len(point)):
                    pass
                    #point[i] *= size
        
        # Definition of the Pyramid's underlying point cloud.  No structure, just the points.
        self.pointCloud = [top1,top2,top3,top4,base1,base2,base3,base4]
        self.defaultPointCloud = copy.deepcopy(self.pointCloud)

        # 6 polygons, 6 colors
        self.colors = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]

# ***************************** Initialize Pyramid and Cube Objects ***************************

objPyramid = pyramid("objPyramid")
objPyramid.setup(0,0,0,50)
objects.append(objPyramid)

objFirstCube = cube("objFirstCube")
objFirstCube.setup(0,-130,0,15)
objects.append(objFirstCube)

objSecondCube = cube("objSecondCube")
#objSecondCube.setup(50,0,50,70)
#objects.append(objSecondCube)

#************************************************************************************

# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    # uniform displacement in x,y,z directions
    dispVector = vector3(displacement[0], displacement[1], displacement[2])

    # translate object transformation matrix by the displacement vector
    object.transformation.translate(dispVector)

    # update the object's polys
    object.update()
        
# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object, scaleFactor):
    # new composite matrix
    ###################
    # COULD NOT INCOPORATE COMPOSITE MATRIX
    ##################
    composite = m4x4()
    
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)
    
    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)
    
    # scale composite matrix
    object.transformation.scale(scaleFactor)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)
    
    # apply composite matrix to object transform
    #object.transformation.dotM(composite.matrix)

    # finish
    object.update()

# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotateZ(object,degrees):
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)

    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # translate matrix
    object.transformation.rotateZ(degrees)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # finish
    object.update()
    
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object,degrees):
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)

    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # translate matrix
    object.transformation.rotateY(degrees)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # finish
    object.update()

# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object,degrees):
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)

    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # translate matrix
    object.transformation.rotateX(degrees)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # finish
    object.update()

def drawObjects(objects):
    # define zBuffer for all objects to be drawn
    zBuffer = createZBuffer(CanvasHeight, CanvasWidth)
    for object in objects:
        drawObject(object, zBuffer)

# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object, zBuffer):

    for i in range(0, len(object.polys)):
        drawPoly(object.polys[i], object.colors[i], object.selectColor, object.selectWidth, zBuffer)

# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly, color, selectColor, selectWidth, zBuffer):
    # check if poly needs to be culled
    if (cullPolygon(poly) and curRender != 1):
        return

    # holder for vectors projected to display screen
    displayVertexData = []

    # ################### #
    # Display Vertex Data #
    # ################### #
    # project polygon onto the display screen
    i = 0
    for point in poly:
        #point = poly[i]
        #PB = poly[i+1+((i+1)//len(poly))*-len(poly)]

        # project coordinates to diaplsy screen
        displayPoint = displayCoordinates(point)
        displayVertexData.append(displayPoint)
        i +=1

    # debug data
    #data = [
     #   [0,-100,100],
    #    [50,-150,50],
     #   [-50,-150,]
     #   ]
    #displayVertexData = displayVertexData[0:2]

    # ########################### #
    # Color Converted Vertex Data #
    # ########################### #
    # wireframe graphics, setting 1
    if (curRender == 1):
        wirePolygon(displayVertexData, selectColor, selectWidth)
        
    # wireframe + polygon fill, setting 2
    elif (curRender == 2):
        wirePolygon(displayVertexData, selectColor, selectWidth)
        fillPolygon(displayVertexData, color, zBuffer)

    # Polygon Fill, setting 3
    elif (curRender == 3):
        fillPolygon(displayVertexData, color, zBuffer)
        


def wirePolygon(vertexData, selectColor, selectWidth):
    for i in range(0, len(vertexData)):
        PA = vertexData[i]
        PB = vertexData[(i+1)%len(vertexData)]
        drawLine(PA, PB, selectColor, selectWidth)

# edge class
class edge:
    def __init__(self, Xstart, Ystart, Yend, dX, Zstart, dZ):
        self.Xstart = Xstart
        self.Ystart = Ystart
        self.Yend = Yend
        self.dX = dX
        self.Zstart = Zstart
        self.dZ = dZ
        
# sorting algorithm
def sortEdges(edges):
    # return if empty list
    if (len(edges) == 0):
        return

    n = len(edges)

    for i in range(n):
        already_sorted = True

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            if edges[j].Ystart > edges[j + 1].Ystart:
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                edges[j], edges[j + 1] = edges[j + 1], edges[j]

                # Since you had to swap two elements,
                # set the `already_sorted` flag to `False` so the
                # algorithm doesn't finish prematurely
                already_sorted = False

        # If there were no swaps during the last iteration,
        # the array is already sorted, and you can terminate
        if already_sorted:
            break

    return edges

# Polygon fill algorithm
def fillPolygon(vertexData, color, zBuffer):
    # variables
    edges = []

    # Pre-compute the edge constants: XStart, Ystart, Yend, dX, Zstart, dZ
    edgeTable = ComputeEdgeTable(vertexData)

    # Very short polygons (less than a pixel high) are not drawn
    if (edgeTable == []):
        return

    # Painting proceeds line by line from the first to the last fill line
    FirstFillLine = edgeTable[0].Ystart # smallest Ystart in EdgeTable
    LastFillLine = edgeTable[len(edgeTable)-1].Yend # largest Yend in EdgeTable
    
    # Indices for the first (I=0), second (J=1), and next (next=2) edges
    I = 0
    J = 1
    Next = 2
    
    # Paint a fill line by setting all pixels between the first two edges
    EdgeIX = edgeTable[I].Xstart
    EdgeJX = edgeTable[J].Xstart
    
    EdgeIZ = edgeTable[I].Zstart
    EdgeJZ = edgeTable[J].Zstart

    # Paint one fill line at a time
    for Y in range(FirstFillLine, LastFillLine):
        # Determine which edge is Left and which is Right
        if (EdgeIX < EdgeJX):
            LeftX = EdgeIX
            LeftZ = EdgeIZ

            RightX = EdgeJX
            RightZ = EdgeJZ
        else:
            LeftX = EdgeJX
            LeftZ = EdgeJZ

            RightX = EdgeIX
            RightZ = EdgeIZ

        # The initial Z for the current fill line
        Z = LeftZ

        
        # integer
        LeftX = round(LeftX)
        RightX = round(RightX)

        # Compute dZ for the fill line. Can be 0 if line is 1 pixel long
        if ((RightX - LeftX) != 0):
            dZFillLine = (RightZ-LeftZ)/(RightX-LeftX)
        else:
            dZFillLine = 0
        
        #print("check-0"+str((RightX - LeftX) != 0))
        #print("dZFillLine"+str(dZFillLine))
        # Paint across a fill line
        for X in range(LeftX, RightX):  
            if (Z < zBuffer[X][Y]):
                w.create_line(X,Y,X+1,Y,fill=color) # Set a Pixel
                zBuffer[X][Y] = Z
            Z = Z + dZFillLine

        # Update the X values of edges I and J for the next fill line
        EdgeIX = EdgeIX + edgeTable[I].dX
        EdgeJX = EdgeJX + edgeTable[J].dX

        EdgeIZ = EdgeIZ + edgeTable[I].dZ
        EdgeJZ = EdgeJZ + edgeTable[J].dZ


        # Upon reaching the bottom of an edge switch out with next edge
        if (Y >= edgeTable[I].Yend) and (Y < LastFillLine):
            I=Next
            EdgeIX = edgeTable[I].Xstart
            EdgeIZ = edgeTable[I].Zstart
            Next += 1
        if (Y >= edgeTable[J].Yend) and (Y < LastFillLine):
            J=Next
            EdgeJX = edgeTable[J].Xstart
            EdgeJZ=edgeTable[J].Zstart
            Next += 1

# creation of edged table
# Xstart, Ystart, Yend, dx, Zstart, dz
def ComputeEdgeTable(displayPoly):
    edgeTable = []

    for i in range(0,len(displayPoly)):
        # given points
        PA = displayPoly[i]
        PB = displayPoly[(i+1) % len(displayPoly)] #loop back around to 0

        # find minimum and maximum Y value
        if (PA[1] < PB[1]):
            # PA holds minimum Y value
            Xstart = PA[0] # corresponds to Ystart
            Ystart = PA[1]
            Zstart = PA[2]
            Xend = PB[0]
            Yend = PB[1]
            Zend = PB[2]
        else:
            # PB holds minimum Y value
            Xstart = PB[0] # corresponds to Ystart
            Ystart = PB[1]
            Zstart = PB[2]
            Xend = PA[0]
            Yend = PA[1]
            Zend = PA[2]

        # calculate inverse slope (dX)
        dx = Xend - Xstart
        dy = Yend - Ystart
        dz = Zend - Zstart

        if (dy == 0):
            # dX and dZ are infinite
            # don't create an edge
            pass
        else:
            dX = dx / dy
            dZ = dz / dy
            
            # create edges
            newEdge = edge(Xstart, Ystart, Yend, dX, Zstart, dZ)
            edgeTable.append(newEdge)

    # order edges by increasing y values
    edgeTable = sortEdges(edgeTable)
    return edgeTable

# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def displayCoordinates(point):
    # convert to projection space
    persProjection = perspectiveProjection(point)
    
    # convert to display space
    dispProjection = convertToDisplayCoordinates(persProjection)
    
    return dispProjection

    
def drawPixel(point, color):
    x = point[0]
    y = point[1]
    
    w.create_line(x, y, x+1, y, fill=color, width=2)

def drawLine(PA, PB, color, newWidth):
    Ax = PA[0]
    Ay = PA[1]
    Bx = PB[0]
    By = PB[1]
    
    w.create_line(Ax, Ay, Bx, By, fill=color, width=newWidth)

# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def perspectiveProjection(point):
    persProjectionPoint = []

    x = point[0]
    y = point[1]
    z = point[2]

    persProjectionPoint.append(d * (x/(d+z)))
    persProjectionPoint.append(d * (y/(d+z)))
    # maximum render distance is equal to viewing distance, d
    persProjectionPoint.append(d * (z/(d+z)))

    return persProjectionPoint

# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    displayPoint = []

    x = point[0]
    y = point[1]
    z = point[2]
    
    displayPoint.append((CanvasWidth / 2) + x)
    displayPoint.append((CanvasHeight / 2) - y)
    displayPoint.append(z)

    # round down
    displayPoint[0] = round(displayPoint[0])
    displayPoint[1] = round(displayPoint[1])
    
    return displayPoint

# entry point for culling polygons of an object
# polygons have their points defined counterclockwise
# the first three points will be pulled to create vectors
def cullPolygon(poly):
    # first three polygonal points
    pointA = poly[0]
    pointB = poly[1]
    pointC = poly[2]
    
    # vectors AB and AC
    vectorP = vector3(pointB[0]-pointA[0], pointB[1]-pointA[1], pointB[2]-pointA[2])
    vectorQ = vector3(pointC[0]-pointA[0], pointC[1]-pointA[1], pointC[2]-pointA[2])
    
    # dot product between vectors
    normal = vector3(vectorP.x, vectorP.y, vectorP.z)
    normal.crossProduct(vectorQ)

    # Establish polygon's position in space
    vectorP0 = vector3(pointA[0], pointA[1], pointA[2])
    normalNorm = vector3(normal.x, normal.y, normal.z)
    normalNorm.normalize()
    cameraView = vector3(0,0,-d)
    
    D = normalNorm.dotV(vectorP0)
    visibilty = normalNorm.dotV(cameraView) - D
    
    # check visibilty
    if (visibilty > 0):
        return False
    return True
    
rScale = 0.1
# **************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    curObject.reset()
    drawObjects(objects)

def larger():
    w.delete(ALL)
    scale(curObject,1.1)
    drawObjects(objects)

def smaller():
    w.delete(ALL)
    scale(curObject,.9)
    drawObjects(objects)

def forward():
    w.delete(ALL)
    translate(curObject,[0,0,-10])
    drawObjects(objects)

def backward():
    w.delete(ALL)
    translate(curObject,[0,0,10])
    drawObjects(objects)

def left():
    w.delete(ALL)
    translate(curObject,[-10,0,0])
    drawObjects(objects)

def right():
    w.delete(ALL)
    translate(curObject,[10,0,0])
    drawObjects(objects)

def up():
    w.delete(ALL)
    translate(curObject,[0,10,0])
    drawObjects(objects)

def down():
    w.delete(ALL)
    translate(curObject,[0,-10,0])
    drawObjects(objects)

def xPlus():
    w.delete(ALL)
    rotateX(curObject,rScale)
    curObject.update()
    drawObjects(objects)

def xMinus():
    w.delete(ALL)
    rotateX(curObject,-rScale)
    curObject.update()
    drawObjects(objects)

def yPlus():
    w.delete(ALL)
    rotateY(curObject,rScale)
    curObject.update()
    drawObjects(objects)

def yMinus():
    w.delete(ALL)
    rotateY(curObject,-rScale)
    curObject.update()
    drawObjects(objects)

def zPlus():
    w.delete(ALL)
    rotateZ(curObject,rScale)
    curObject.update()
    drawObjects(objects)

def zMinus():
    w.delete(ALL)
    rotateZ(curObject,-rScale)
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
    # update selection color
    if (curObject != 0):
        curObject.selectColor = "black"
        curObject.selectWidth = 2
    obj.selectColor = "white"
    obj.selectWidth = 5
    curObject = obj
    
    global curPointCloud
    curPointCloud = obj.pointCloud
    
    global curDefualtPointCloud
    curDefualtPointCloud = obj.defaultPointCloud

# temporary selection function for buttons
def newSelectionL():
    newSelection(-1)
    drawObjects(objects)
def newSelectionR():
    newSelection(1)
    drawObjects(objects)

# set current object
updateCurObject(objects[0])

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
#rotateY(objects[1],45)
#drawObjects(objects)
#newSelection(1)
#drawPoly([[5.7,3.8,1.7],[5.7,15,1.7],[2,3.8,1.7]],"black")
#scale(curObject.pointCloud, 0.5)
#newSelection(1)
#newSelection(-1, curObject)
#newSelection(-1, curObject)
#newSelection(-1, curObject)
root.mainloop()
