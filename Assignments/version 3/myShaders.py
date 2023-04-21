#################################
# Shaders: Flat, Gouraud, Phong #
#################################
from myIlluminationModels import *
from myGeometry import *
from myTables import *
from myBasicRenderers import *

# ************** Shader Class **************#
class shader:

    def __init__(self, name, canvas):
        self.name = name
        self.canvas = canvas
        self.model = phongIlluminationModel("Phong Illumination Model")
        self.model.addLightSource(L=[1,1,-1])
        self.Ia = [0.5,0.5,0.5]
        self.Kd = [0.5,0.5,0.5]
        self.Ip = [0.5,0.5,0.5]
        self.Ks = [0.5,0.5,0.5]
        
# ************** Flat Shader Class **************# 
class flat(shader):

    def __init__(self, name, canvas):
        super().__init__(name, canvas)

    # shade the polygon
    def shadePoly(self, poly, vertexData, zBuffer):
        N = poly.normal
        model = self.model

        # Ambient Light in Scene
        # Ia : incoming light source Intensity
        # Kd : objects diffuse reflectivity
        ambientRGB = model.ambient(self.Ia, self.Kd)

        # Diffuse Light in on Polygon
        # Ip : the point source intensity
        # cos(theta)
        # Kd : diffuse reflectivity of object
        # d : distnace between object and light source (constant of 1)
        diffuseRGB = model.diffuse(N, self.Ip, self.Kd)

        # Specular Light on Polygon
        # Ip : Point source light intensity
        # Ks : diffuse constant?
        # R : Reflection Vector
        # V : View Vector
        specularRGB = model.specular(N, self.Ip, self.Ks)

        # generate color and fill polygon
        color = model.triColorHexCode(ambientRGB[0],diffuseRGB[0],specularRGB[0])

        fillRender = fill("Fill", self.canvas)
        fillRender.draw(poly, vertexData, color, zBuffer)

# ************** Gouraud Shader Class **************# 
class gouraud(shader):

    def __init__(self, name, canvas):
        super().__init__(name, canvas)

    def shadePoly(self, poly, vertexData, zBuffer):
        color = "green"

        # Pre-compute the edge constants: XStart, Ystart, Yend, dX, Zstart, dZ
        eTable = edgeTable("Edge Table")
        eTable = eTable.compute(vertexData)
        # GS Counterpart #
        iTable = intensityTable("Intensity Table")
        iTable = iTable.compute(self, vertexData, poly)
                                                      
        # Very short polygons (less than a pixel high) are not drawn
        if (edgeTable == []):
            return

        # Painting proceeds line by line from the first to the last fill line
        FirstFillLine = eTable[0].Ystart # smallest Ystart in EdgeTable
        LastFillLine = eTable[len(eTable)-1].Yend # largest Yend in EdgeTable
        
        # Indices for the first (I=0), second (J=1), and next (next=2) edges
        I = 0
        J = 1
        Next = 2
        
        # Paint a fill line by setting all pixels between the first two edges
        EdgeIX = eTable[I].Xstart
        EdgeJX = eTable[J].Xstart
        
        EdgeIZ = eTable[I].Zstart
        EdgeJZ = eTable[J].Zstart

        # GS Counterpart #
        EdgeII = iTable[I].Zstart
        EdgeJI = iTable[J].Zstart

        # Paint one fill line at a time
        for Y in range(FirstFillLine, LastFillLine):
            # Determine which edge is Left and which is Right
            if (EdgeIX < EdgeJX):
                LeftX = EdgeIX
                LeftZ = EdgeIZ
                # GS CP #
                LeftI = EdgeII

                RightX = EdgeJX
                RightZ = EdgeJZ
                # GS CP #
                RightI = EdgeJI
            else:
                LeftX = EdgeJX
                LeftZ = EdgeJZ
                # GS CP #
                LeftI = EdgeJI

                RightX = EdgeIX
                RightZ = EdgeIZ
                # GS CP #
                RightI = EdgeII

            # The initial Z for the current fill line
            Z = LeftZ
            # GS CP #
            intensity = LeftI
            
            # integer
            LeftX = round(LeftX)
            RightX = round(RightX)

            # Compute dZ for the fill line. Can be 0 if line is 1 pixel long
            if ((RightX - LeftX) != 0):
                dZFillLine = (RightZ-LeftZ)/(RightX-LeftX)
                # GS CP #
                #dIFillLine = ((RightI[0]+RightI[1]+RightI[2])-(LeftI[0]+LeftI[1]+LeftI[2]))/(RightX-LeftX)
                dIFillLine = (RightI - LeftI) / (RightX-LeftX)
            else:
                dZFillLine = 0
                # GS CP #
                dIFillLine = 0

            # Paint across a fill line
            for X in range(LeftX, RightX):  
                if (Z < zBuffer[X][Y]):
                    color = self.model.triColorHexCode(0.25,intensity,-0.25)
                    self.canvas.w.create_line(X,Y,X+1,Y,fill=color) # Set a Pixel
                    zBuffer[X][Y] = Z
                Z = Z + dZFillLine
                intensity = intensity + dIFillLine

            # Update the X values of edges I and J for the next fill line
            EdgeIX = EdgeIX + eTable[I].dX
            EdgeJX = EdgeJX + eTable[J].dX

            EdgeIZ = EdgeIZ + eTable[I].dZ
            EdgeJZ = EdgeJZ + eTable[J].dZ

            # GS CP #
            EdgeII = EdgeII + iTable[I].dZ
            EdgeJI = EdgeJI + iTable[J].dZ


            # Upon reaching the bottom of an edge switch out with next edge
            if (Y >= eTable[I].Yend) and (Y < LastFillLine):
                I=Next
                EdgeIX = eTable[I].Xstart
                EdgeIZ = eTable[I].Zstart
                # GS CP #
                EdgeII = iTable[I].Zstart
                Next += 1
            if (Y >= eTable[J].Yend) and (Y < LastFillLine):
                J=Next
                EdgeJX = eTable[J].Xstart
                EdgeJZ= eTable[J].Zstart
                # GS CP #
                EdgeJI = iTable[J].Zstart
                Next += 1

# ************** Phong Shader Class **************# 
class phong(shader):

    def __init__(self, name, canvas):
        super().__init__(name, canvas)

    def shadePoly(self, polyO, vertexData, zBuffer):
        color = "green"
        
        # Pre-compute the edge constants: XStart, Ystart, Yend, dX, Zstart, dZ
        eTable = edgeTable("Edge Table")
        eTable = eTable.compute(vertexData)
        # PS Counterpart #
        nTable = normalTable("Normal Table")
        nTable = nTable.compute(self, vertexData, polyO, self.canvas)
                                                      
        # Very short polygons (less than a pixel high) are not drawn
        if (edgeTable == [] or None):
            return
        
        # Painting proceeds line by line from the first to the last fill line
        FirstFillLine = eTable[0].Ystart # smallest Ystart in EdgeTable
        LastFillLine = eTable[len(eTable)-1].Yend # largest Yend in EdgeTable
        
        # Indices for the first (I=0), second (J=1), and next (next=2) edges
        I = 0
        J = 1
        Next = 2
        
        # Paint a fill line by setting all pixels between the first two edges
        EdgeIX = eTable[I].Xstart
        EdgeJX = eTable[J].Xstart
        
        EdgeIZ = eTable[I].Zstart
        EdgeJZ = eTable[J].Zstart

        # PS Counterpart #
        EdgeIN = nTable[I].Zstart.toCopy()
        EdgeJN = nTable[J].Zstart.toCopy()

        # Paint one fill line at a time
        for Y in range(FirstFillLine, LastFillLine):
            # Determine which edge is Left and which is Right
            if (EdgeIX < EdgeJX):
                LeftX = EdgeIX
                LeftZ = EdgeIZ
                # PS CP #
                LeftN = EdgeIN.toCopy()

                RightX = EdgeJX
                RightZ = EdgeJZ
                # PS CP #
                RightN = EdgeJN.toCopy()
            else:
                LeftX = EdgeJX
                LeftZ = EdgeJZ
                # PS CP #
                LeftN = EdgeJN.toCopy()

                RightX = EdgeIX
                RightZ = EdgeIZ
                # PS CP #
                RightN = EdgeIN.toCopy()

            # The initial Z for the current fill line
            Z = LeftZ
            # PS CP #
            normal = LeftN.toCopy()
            
            # integer
            LeftX = round(LeftX)
            RightX = round(RightX)

            # Compute dZ for the fill line. Can be 0 if line is 1 pixel long
            if ((RightX - LeftX) != 0):
                dZFillLine = (RightZ-LeftZ)/(RightX-LeftX)
                
                # PS CP #
                # (RighN - LeftN)
                dNFillLine = RightN.toCopy()
                dNFillLine.subV(LeftN)
                # divide by (RightX-LeftX)
                dNFillLine.scale(1/(RightX-LeftX))
            else:
                dZFillLine = 0
                # PS CP #
                dNFillLine = vector3(0,0,0)

            # Paint across a fill line
            for X in range(LeftX, RightX):  
                if (Z < zBuffer[X][Y]):
                    # calculate intensity with changing normals
                    # Ambient Light in Scene
                    ambientRGB = self.model.ambient(self.Ia, self.Kd)
                    # Diffuse Light in on Polygon
                    diffuseRGB = self.model.diffuse(normal, self.Ip, self.Kd)
                    # Specular Light on Polygon
                    specularRGB = self.model.specular(normal, self.Ip, self.Ks)

                    color = self.model.triColorHexCode(ambientRGB[0],diffuseRGB[0],specularRGB[0])
                    
                    self.canvas.w.create_line(X,Y,X+1,Y,fill=color) # Set a Pixel
                    zBuffer[X][Y] = Z
                Z = Z + dZFillLine
                normal.addV(dNFillLine)

            # Update the X values of edges I and J for the next fill line
            EdgeIX = EdgeIX + eTable[I].dX
            EdgeJX = EdgeJX + eTable[J].dX

            EdgeIZ = EdgeIZ + eTable[I].dZ
            EdgeJZ = EdgeJZ + eTable[J].dZ

            # PS CP #
            EdgeIN.addV(nTable[I].dZ)
            EdgeJN.addV(nTable[J].dZ)


            # Upon reaching the bottom of an edge switch out with next edge
            if (Y >= eTable[I].Yend) and (Y < LastFillLine):
                I=Next
                EdgeIX = eTable[I].Xstart
                EdgeIZ = eTable[I].Zstart
                # PS CP #
                EdgeIN = nTable[I].Zstart
                Next += 1
            if (Y >= eTable[J].Yend) and (Y < LastFillLine):
                J=Next
                EdgeJX = eTable[J].Xstart
                EdgeJZ=eTable[J].Zstart
                # PS CP #
                EdgeJN = nTable[J].Zstart
                Next += 1
