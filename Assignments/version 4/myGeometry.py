###########################################
# Geometry Classes: Edge, Polygon, Vertex #
###########################################
import copy
from myMath import *

# ************** Edge Class **************# 
class edge:
    
    def __init__(self, Xstart, Ystart, Yend, dX, Zstart, dZ):
        self.Xstart = Xstart
        self.Ystart = Ystart
        self.Yend = Yend
        self.dX = dX
        self.Zstart = Zstart
        self.dZ = dZ
        
# ************** Polygon Class **************# 
class polygon:
    
    def __init__(self, name, vertices):
        self.name = name
        self.vertices = vertices
        self.normal = []
        self.defaultVertices = copy.deepcopy(vertices)
        
    # Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
    # Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
    # draw the actual line using the built-in create_line method
    def displayCoordinates(self,point):
        # convert to projection space
        persProjection = self.perspectiveProjection(point)
        
        # convert to display space
        dispProjection = self.convertToDisplayCoordinates(persProjection)
        
        return dispProjection

    # This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
    # will return a NEW list of points.  We will not want to keep around the projected points in our object as
    # they are only used in rendering
    def perspectiveProjection(self,point,d=500):
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
    def convertToDisplayCoordinates(self,point):
        displayPoint = []

        x = point[0]
        y = point[1]
        z = point[2]
        
        displayPoint.append((400 / 2) + x)
        displayPoint.append((400 / 2) - y)
        displayPoint.append(z)

        # round down
        displayPoint[0] = round(displayPoint[0])
        displayPoint[1] = round(displayPoint[1])
        
        return displayPoint

# ************** Vertex Class **************# 
class vertex:
    # position: 3D vector position of vertex
    # normal: 3D vector normal of vertex
    def __init__(self, position, normal=0):
        self.position = position.toCopy()
        self.normal = vector3(-1,-1,-1)


        
