###################################
# Tables: Edge, Normal, Intensity #
###################################
from myGeometry import *

# ************** Table Class **************#
class table:

    def __init__(self, name):
        self.name = name

# ************** Edge Table Class **************#
class edgeTable(table):

    def __init__(self, name):
        self.table = []
        super().__init__(name)

    # append edge to table
    def addEdge(self, edge):
        self.table.append(edge)

    # computation of edge table
    # Xstart, Ystart, Yend, dx, Zstart, dz
    def compute(self, displayPoly):
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
                self.addEdge(newEdge)
                
        # order edges by increasing y values
        self.sort()
        return self.table

    # sorting algorithm for edges
    # sorts by starting Y values
    def sort(self):
        edges = self.table
        
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

        self.table = edges
    
# ************** Intensity Table Class **************#
class intensityTable(table):

    def __init__(self, name):
        super().__init__(name)

    # creation of Intensity table
    # Xstart, Ystart, Yend, dx, Zstart, dz
    def compute(self, shader, displayPolyVertices, originalPoly):
        model = shader.model # model for gouraud shader
        eTable = edgeTable("Edge Table")
        
        for i in range(0, len(displayPolyVertices)):
            # given points
            PA = displayPolyVertices[(i) % len(displayPolyVertices)]
            PB = displayPolyVertices[(i+1) % len(displayPolyVertices)]
            # given point normals
            PAN = originalPoly.vertices[(i) % len(displayPolyVertices)].normal
            PBN = originalPoly.vertices[(i+1) % len(displayPolyVertices)].normal
            
            # intensity of points
            # Ambient Light in Scene
            ambientRGB = model.ambient(shader.Ia, shader.Kd)
            # Diffuse Light in on Polygon
            PAdiffuseRGB = model.diffuse(PAN, shader.Ip, shader.Kd)
            PBdiffuseRGB = model.diffuse(PBN, shader.Ip, shader.Kd)
            # Specular Light on Polygon
            PAspecularRGB = model.specular(PAN, shader.Ip, shader.Ks)
            PBspecularRGB = model.specular(PBN, shader.Ip, shader.Ks)
            # intensity at points
            PAI = ambientRGB[0]+PAdiffuseRGB[0]+PAspecularRGB[0]
            PBI = ambientRGB[0]+PBdiffuseRGB[0]+PBspecularRGB[0]
            
            # find minimum and maximum Y value
            if (PA[1] < PB[1]):
                # PA holds minimum Y value
                Xstart = PA[0] # corresponds to Ystart
                Ystart = PA[1]
                Istart = PAI # Z replaced with Intensity
                Xend = PB[0]
                Yend = PB[1]
                Iend = PBI
            else:
                # PB holds minimum Y value
                Xstart = PB[0] # corresponds to Ystart
                Ystart = PB[1]
                Istart = PBI
                Xend = PA[0]
                Yend = PA[1]
                Iend = PAI

            # calculate inverse slope (dX)
            dx = Xend - Xstart
            dy = Yend - Ystart
            di = Iend - Istart
           
            if (dy == 0):
                # dX and dI are infinite
                # don't create an edge
                pass
            else:
                dX = dx / dy
                dI = di / dy
                
                # create edges
                newEdge = edge(Xstart, Ystart, Yend, dX, Istart, dI)
                eTable.addEdge(newEdge)
            
        # order edges by increasing y values
        eTable.sort()
        return eTable.table

# ************** Normal Table Class **************# 
class normalTable(table):

    def __init__(self, name):
        super().__init__(name)
        
    # Computation of Normal table
    # Xstart, Ystart, Yend, dx, Zstart, dz
    def compute(self, shader, displayPolyVertices, originalPoly,c):
        model = shader#.model # model for phong shader
        eTable = edgeTable("Edge Table")
        
        for i in range(0, len(displayPolyVertices)):
            # given points
            test1 = 0
            PA = displayPolyVertices[(i+test1) % len(displayPolyVertices)]
            PB = displayPolyVertices[(i+1+test1) % len(displayPolyVertices)]
            # given point normals
            test = 0
            
            PAN = originalPoly.vertices[(i+test) % len(displayPolyVertices)].normal.toCopy()
            PBN = originalPoly.vertices[(i+1+test) % len(displayPolyVertices)].normal.toCopy()
            
            # find minimum and maximum Y value
            # X, Y coordinates as well as Normals (N)
            if (PA[1] < PB[1]):
                # PA holds minimum Y value
                Xstart = PA[0]
                Ystart = PA[1]
                Nstart = PAN
                Xend = PB[0]
                Yend = PB[1]
                Nend = PBN.toCopy()
            else:
                # PB holds minimum Y value
                Xstart = PB[0] # corresponds to Ystart
                Ystart = PB[1]
                Nstart = PBN
                Xend = PA[0]
                Yend = PA[1]
                Nend = PAN.toCopy()

            # calculate inverse slope (dX)
            dx = Xend - Xstart
            dy = Yend - Ystart

            dn = Nend.toCopy()
            dn.subV(Nstart)
            #dn = Nend - Nstart
           
            if (dy == 0):
                # dX and dI are infinite
                # don't create an edge
                pass
            else:
                dX = dx / dy
                dN = dn.toCopy()
                dN.scale(1/dy)
                
                # create edges
                newEdge = edge(Xstart, Ystart, Yend, dX, Nstart, dN)
                eTable.addEdge(newEdge)
            
        # order edges by increasing y values
        eTable.sort()
        return eTable.table
