#############
# Main File #
#############
import math
from myMath import *
from myShapes import *
from myCanvas import *
from myTransformation import *
from myIlluminationModels import *
from myShaders import *
from myBasicRenderers import *
from myGeometry import *
from myTables import *
from tkinter import *

# ****** variables ****** #
CanvasWidth = 400
CanvasHeight = 400
d = 500
objects = []
curObject = 0
curPointCloud = 0
curDefualtPointCloud = 0
renderSetting = 6

# ************************ Initialize Pyramid and Cube Objects ********************* #
#pyramid = pyramid("objPyramid")
#pyramid.setup(0,0,0,50)
#objects.append(pyramid)

#firstCube = cube("objFirstCube")
#firstCube.setup(0,-130,0,15)
#objects.append(firstCube)

#secondCube = cube("objSecondCube")
#secondCube.setup(50,0,50,10)
#objects.append(secondCube)

cylinder = cylinder("objCylinder",renderSetting)
cylinder.setup(0,0,0,1)
rotateX(cylinder, 10)
rotateY(cylinder, 0.5)
#rotateX(cylinder, -10)
#translate(cylinder, [0,0,-40])
scale(cylinder, 0.6)
objects.append(cylinder)
# ************** #

# ************************ Clutter of Random Functions ********************* #
# Z buffer creation
# zBuffer should not be on objects, it's for the entire scene
# to clean code, put in scene-type class
def createZBuffer(row, col):
    arr = []
    
    for r in range(row):
        tempArr = []
        for c in range(col):
            # fill with default
            tempArr.append(d)
        arr.append(tempArr)
    
    return arr
    
def drawObjects(objects):
    # define zBuffer for all objects to be drawn
    zBuffer = createZBuffer(CanvasHeight, CanvasWidth)
    
    for object in objects:
        drawObject(object, zBuffer)

# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object, zBuffer):
    for i in range(0, len(object.polys)):
        drawPoly(object.polys[i], object.colors[i%len(object.colors)], object.selectColor, object.selectWidth, zBuffer)

# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly, color, selectColor, selectWidth, zBuffer):
    
    # check if poly needs to be culled
    if (cullPolygon(poly) and renderSetting != 1):
        return

    # holder for polygon projected to display screen
    displayVertexData = []

    # Display Vertex Data #
    # project polygon onto the display screen
    for vertex in poly.vertices:
        # project coordinates to diaplsy screen
        point = vertex.position
        displayPoint = poly.displayCoordinates(point.toArray())
        displayVertexData.append(displayPoint)

    # Color Converted Vertex Data #
    # wireframe graphics, setting 1
    if (renderSetting == 1):
        wireframeRender = wireframe("Wireframe", c)
        wireframeRender.draw(displayVertexData, selectColor, selectWidth)
        
    # wireframe + polygon fill, setting 2
    elif (renderSetting == 2):
        fillRender = fill("Fill", c)
        wireframeRender = wireframe("Wireframe", c)
        fillRender.draw(poly, displayVertexData, color, zBuffer)
        wireframeRender.draw(displayVertexData, selectColor, selectWidth)

    # Polygon Fill, setting 3
    elif (renderSetting == 3):
        fillRender = fill("Fill", c)
        fillRender.draw(poly, displayVertexData, color, zBuffer)

    # setting 4: Flat Shading
    elif (renderSetting == 4):
        flatShader = flat("Flat Shader", c)
        flatShader.shadePoly(poly, displayVertexData, zBuffer)

    # setting 5: Gourand Shading
    elif (renderSetting == 5):
        # calculate the normal for every vertex
        # this is done when the object is updated
        gouraudShader = gouraud("Gouraud Shader", c)
        gouraudShader.shadePoly(poly, displayVertexData, zBuffer)

    # setting 6: Phong Shading
    elif (renderSetting == 6):
        # calculate the normal for every vertex
        # this is done when the object is updated
        phongShader = phong("Phong Shader", c)
        phongShader.shadePoly(poly, displayVertexData, zBuffer)

# entry point for culling polygons of an object
# polygons have their points defined counterclockwise
# the first three points will be pulled to create vectors
def cullPolygon(poly):
    # first polygonal point
    pointA = poly.vertices[0].position

    # Establish polygon's position in space
    vectorP0 = pointA

    normal = poly.normal
    cameraView = vector3(0,0,-d)
    
    D = normal.dotV(vectorP0)
    visibilty = normal.dotV(cameraView) - D
    
    # check visibilty
    if (visibilty > 0):
        return False
    return True
    
rScale = 0.5
# **************************************************************************
# Everything below this point implements the interface
def reset():
    c.w.delete(ALL)
    curObject.reset()
    drawObjects(objects)

def larger():
    c.w.delete(ALL)
    scale(curObject,1.1)
    drawObjects(objects)

def smaller():
    c.w.delete(ALL)
    scale(curObject,.9)
    drawObjects(objects)

def forward():
    c.w.delete(ALL)
    translate(curObject,[0,0,-10])
    drawObjects(objects)

def backward():
    c.w.delete(ALL)
    translate(curObject,[0,0,10])
    drawObjects(objects)

def left():
    c.w.delete(ALL)
    translate(curObject,[-10,0,0])
    drawObjects(objects)

def right():
    c.w.delete(ALL)
    translate(curObject,[10,0,0])
    drawObjects(objects)

def up():
    c.w.delete(ALL)
    translate(curObject,[0,10,0])
    drawObjects(objects)

def down():
    c.w.delete(ALL)
    translate(curObject,[0,-10,0])
    drawObjects(objects)

def xPlus():
    c.w.delete(ALL)
    rotateX(curObject,rScale)
    curObject.update()
    drawObjects(objects)

def xMinus():
    c.w.delete(ALL)
    rotateX(curObject,-rScale)
    curObject.update()
    drawObjects(objects)

def yPlus():
    c.w.delete(ALL)
    rotateY(curObject,rScale)
    curObject.update()
    drawObjects(objects)

def yMinus():
    c.w.delete(ALL)
    rotateY(curObject,-rScale)
    curObject.update()
    drawObjects(objects)

def zPlus():
    c.w.delete(ALL)
    rotateZ(curObject,rScale)
    curObject.update()
    drawObjects(objects)

def zMinus():
    c.w.delete(ALL)
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

# canvas creation is attached to a canvas object
# canvas object has access to draw functions
#w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
c = myCanvas("nice", CanvasWidth, CanvasHeight)
c.w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)

drawObjects(objects)
c.w.pack()

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

################
##  Bind Keys #
###############
def one(event):
    global renderSetting
    renderSetting = 1
    c.w.delete(ALL)
    zbu = createZBuffer(CanvasHeight, CanvasWidth)
    drawObjects(objects)
def two(event):
    global renderSetting
    renderSetting = 2
    c.w.delete(ALL)
    zbu = createZBuffer(CanvasHeight, CanvasWidth)
    drawObjects(objects)
def three(event):
    global renderSetting
    renderSetting = 3
    c.w.delete(ALL)
    zbu = createZBuffer(CanvasHeight, CanvasWidth)
    drawObjects(objects)
def four(event):
    global renderSetting
    renderSetting = 4
    c.w.delete(ALL)
    zbu = createZBuffer(CanvasHeight, CanvasWidth)
    drawObjects(objects)
def five(event):
    global renderSetting
    renderSetting = 5
    c.w.delete(ALL)
    zbu = createZBuffer(CanvasHeight, CanvasWidth)
    drawObjects(objects)
def six(event):
    global renderSetting
    renderSetting = 6
    c.w.delete(ALL)
    zbu = createZBuffer(CanvasHeight, CanvasWidth)
    drawObjects(objects)

root.bind('1',one)
root.bind('2',two)
root.bind('3',three)
root.bind('4',four)
root.bind('5',five)
root.bind('6',six)

root.mainloop()
