##########################################
# Shape Class, Pyramid Class, Cube Class #
##########################################
import copy
from myMath import *
from myGeometry import *

# ***************************** Shape Class *************************** #
class shape:
    def __init__(self, name, renderSetting):
        self.name = name
        self.renderSetting = renderSetting
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
        self.updatePolygonNormals()
        self.updateVertexNormals()

    def update(self):
        self.updatePolys()
        self.calculateVisualCenter()
        self.updatePolygonNormals()
        self.updateVertexNormals()
        
    def updatePolys(self):
        # cycle through all verticess of the polygon
        for poly in self.polys:
            for i in range(len(poly.vertices)):
                # polygon's relative default vertex
                position = poly.defaultVertices[i].position.toCopy()
                # overarching transform for the entire shape
                transform = self.transformation.matrix
            
                # apply shape's transformation to the vertex
                position.dotM(transform)

                # save the vertex
                poly.vertices[i].position.setFromV(position)

    def updatePolygonNormals(self):
        # update normals of each polygon
        # do this on every update
        for poly in self.polys:
            # polygon vertices
            polyVertices = poly.vertices
            
            # polygon normal
            # first three polygonal points
            pointA = polyVertices[0].position
            pointB = polyVertices[1].position
            pointC = polyVertices[2].position
            
            # Two connected vectors from the frist three points
            vectorP = vector3(pointB.x-pointA.x, pointB.y-pointA.y, pointB.z-pointA.z)
            vectorQ = vector3(pointC.x-pointA.x, pointC.y-pointA.y, pointC.z-pointA.z)
            
            # dot product between vectors
            N = vectorP
            N.crossProduct(vectorQ)
            N.normalize()

            poly.normal = N
            
    # visual center is halfway between the min and max of all cubiodal container dimensions
    def calculateVisualCenter(self):
        # define the starting min and max values
        # (can be any corresponding x,y,z value from pointCloud)
        maxx = self.pointCloud[0].position.x
        minx = self.pointCloud[0].position.x
        maxy = self.pointCloud[0].position.y
        miny = self.pointCloud[0].position.y
        maxz = self.pointCloud[0].position.z
        minz = self.pointCloud[0].position.z

        # loop through all points checking for corresponding min and max values
        for point in self.pointCloud:
            x = point.position.x
            y = point.position.y
            z = point.position.z

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

    # This function resets the pyramid to its original size and location in 3D space
    # Note that you have to be careful to update the values in the existing PyramidPointCloud
    # structure rather than creating a new structure or just switching a pointer.  In other
    # words, you'll need manually update the value of every x, y, and z of every point in
    # point cloud (vertex list).
    def reset(self):
        for poly in self.polys:
            print(poly.defaultVertices)

        self.update()
        

# ***************************** Pyramid Class *************************** #
class pyramid(shape):

    def __init__(self, name):
        shape.__init__(self, name)
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

# ***************************** Cube Class *************************** #
class cube(shape):

    def __init__(self, name):
        shape.__init__(self, name)
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
        
        # Definition of the Pyramid's underlying point cloud.  No structure, just the points.
        self.pointCloud = [top1,top2,top3,top4,base1,base2,base3,base4]
        self.defaultPointCloud = copy.deepcopy(self.pointCloud)

        # 6 polygons, 6 colors
        self.colors = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]
        
# ***************************** Cylinder Class *************************** #
class cylinder(shape):

    def __init__(self, name,renderSetting):
        shape.__init__(self, name, renderSetting)
        self.cylinder = []

    def setPolys(self, x=0, y=0, z=0, size=1):
        # Definition of the 16 underlying points
        front1 = [-50,120.7107,50]
        front2 = [50,120.7107,50]
        front3 = [120.7107,50,50]
        front4 = [120.7107,-50,50]
        front5 = [50,-120.7107,50]
        front6 = [-50,-120.7107,50]
        front7 = [-120.7107,-50,50]
        front8 = [-120.7107,50,50]
        back1 = [-50,120.7107,450]
        back2 = [50,120.7107,450]
        back3 = [120.7107,50,450]
        back4 = [120.7107,-50,450]
        back5 = [50,-120.7107,450]
        back6 = [-50,-120.7107,450]
        back7 = [-120.7107,-50,450]
        back8 = [-120.7107,50,450]

        # define the points as vertex objects
        front1P = vertex(vector3(front1[0], front1[1], front1[2]),vector3(1,1,1))
        front2P = vertex(vector3(front2[0], front2[1], front2[2]))
        front3P = vertex(vector3(front3[0], front3[1], front3[2]))
        front4P = vertex(vector3(front4[0], front4[1], front4[2]))
        front5P = vertex(vector3(front5[0], front5[1], front5[2]))
        front6P = vertex(vector3(front6[0], front6[1], front6[2]))
        front7P = vertex(vector3(front7[0], front7[1], front7[2]))
        front8P = vertex(vector3(front8[0], front8[1], front8[2]))
        back1P = vertex(vector3(back1[0], back1[1], back2[2]))
        back2P = vertex(vector3(back2[0], back2[1], back2[2]))
        back3P = vertex(vector3(back3[0], back3[1], back3[2]))
        back4P = vertex(vector3(back4[0], back4[1], back4[2]))
        back5P = vertex(vector3(back5[0], back5[1], back5[2]))
        back6P = vertex(vector3(back6[0], back6[1], back6[2]))
        back7P = vertex(vector3(back7[0], back7[1], back7[2]))
        back8P = vertex(vector3(back8[0], back8[1], back8[2]))

        # Definition of the ten polygon faces using the meaningful point names
        # Polys are defined in clockwise order when viewed from the outside
        northPoly = [copy.deepcopy(front1P), copy.deepcopy(back1P), copy.deepcopy(back2P), copy.deepcopy(front2P)]
        northEastPoly = [copy.deepcopy(front2P), copy.deepcopy(back2P), copy.deepcopy(back3P), copy.deepcopy(front3P)]
        eastPoly = [copy.deepcopy(front3P), copy.deepcopy(back3P), copy.deepcopy(back4P), copy.deepcopy(front4P)]
        southEastPoly = [copy.deepcopy(front4P), copy.deepcopy(back4P), copy.deepcopy(back5P), copy.deepcopy(front5P)]
        southPoly = [copy.deepcopy(front5P), copy.deepcopy(back5P), copy.deepcopy(back6P), copy.deepcopy(front6P)]
        southWestPoly = [copy.deepcopy(front6P), copy.deepcopy(back6P), copy.deepcopy(back7P), copy.deepcopy(front7P)]
        westPoly = [copy.deepcopy(front7P), copy.deepcopy(back7P), copy.deepcopy(back8P), copy.deepcopy(front8P)]
        northWestPoly = [copy.deepcopy(front8P), copy.deepcopy(back8P), copy.deepcopy(back1P), copy.deepcopy(front1P)]
        frontPoly = [copy.deepcopy(front1P), copy.deepcopy(front2P), copy.deepcopy(front3P), copy.deepcopy(front4P), copy.deepcopy(front5P), copy.deepcopy(front6P), copy.deepcopy(front7P), copy.deepcopy(front8P)]
        backPoly = [copy.deepcopy(back1P), copy.deepcopy(back8P), copy.deepcopy(back7P), copy.deepcopy(back6P), copy.deepcopy(back5P), copy.deepcopy(back4P), copy.deepcopy(back3P), copy.deepcopy(back2P)]
        
        # set objects for poly
        northPolyO = polygon("northPoly", northPoly)
        northEastPolyO = polygon("northEastPoly", northEastPoly)
        eastPolyO = polygon("eastPoly", eastPoly)
        southEastPolyO = polygon("southEastPoly", southEastPoly)
        southPolyO = polygon("southPoly", southPoly)
        southWestPolyO = polygon("southWestPoly", southWestPoly)
        westPolyO = polygon("westPoly", westPoly)
        northWestPolyO = polygon("northWestPoly", northWestPoly)
        frontPolyO = polygon("frontPoly", frontPoly)
        backPolyO = polygon("backPoly", backPoly)
        
        # Definition of the cylinder object
        self.polys = [northPolyO, northEastPolyO, eastPolyO, southEastPolyO, southPolyO, southWestPolyO, westPolyO, northWestPolyO,frontPolyO, backPolyO]

        # Definition of the Cylinder's underlying point cloud. No structure, just points
        self.pointCloud = [front1P, front2P, front3P, front4P, front5P, front6P, front7P, front8P, back1P, back2P, back3P, back4P, back5P, back6P, back7P, back8P]
        self.defaultPointCloud = copy.deepcopy(self.pointCloud)

        # face colors, mostly for flat shading
        self.colors = ["green", "white", "red", "black", "blue", "yellow", "magenta", "teal"]
                

    # update normal for each vertex if the render setting is Gouraud or Phong (5 or 6)
    def updateVertexNormals(self):
        # return if not correct renderSetting
        if (self.renderSetting != 5 and self.renderSetting != 6):
            return
        
        # number of sides
        SIDES = 8
                
        # exclude last two polys, end-caps are flat planes
        for i in range(SIDES):
            # current and adjacent polygon objects
            #curPoly = self.polys[i]
            rightPoly = self.polys[(i+1)%SIDES]
            leftPoly = self.polys[(i+SIDES-1)%SIDES]

            # polygon normals
            curN = self.polys[i].normal.toCopy()
            rightN = rightPoly.normal.toCopy()
            leftN = leftPoly.normal.toCopy()

            # left average normal
            leftAvgN = vector3(curN.x,curN.y,curN.z)
            leftAvgN.addV(leftN)
            leftAvgN.normalize()

            # right average normal
            rightAvgN = vector3(curN.x,curN.y,curN.z)
            rightAvgN.addV(rightN)
            rightAvgN.normalize()

            # update vertex objects that hold 3D position and Normal
            
            # append vertex normals
            self.polys[i].vertices[0].normal.setFromV(leftAvgN.toCopy())
            self.polys[i].vertices[1].normal.setFromV(leftAvgN.toCopy())
            self.polys[i].vertices[2].normal.setFromV(rightAvgN.toCopy())
            self.polys[i].vertices[3].normal.setFromV(rightAvgN.toCopy())
      
        # attach frontPoly and backPoly Normals
        tempArr1 = []
        tempArr2 = []
        for i in range(8):
            self.polys[8].vertices[i].normal.setFromV(self.polys[8].normal.toCopy())
        for i in range(8):
            self.polys[9].vertices[i].normal.setFromV(self.polys[9].normal.toCopy())
