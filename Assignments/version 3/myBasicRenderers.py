#####################################
# Basic Renderers: Wire Frame, Fill #
#####################################
from myTables import *

# ************** Basic Render Class **************#
class basicRenderer:

    def __init__(self, name, canvas):
        self.name = name
        self.canvas = canvas
        
# ************** Wireframe Class **************# 
class wireframe(basicRenderer):

    def __init__(self, name, canvas):
        super().__init__(name, canvas)

    def draw(self, vertexData, selectColor, selectWidth):
        for i in range(0, len(vertexData)):
            PA = vertexData[i]
            PB = vertexData[(i+1)%len(vertexData)]
            self.canvas.drawLine(PA, PB, selectColor, selectWidth)
        
# ************** Fill Class **************# 
class fill(basicRenderer):

    def __init__(self, name, canvas):
        super().__init__(name, canvas)

    def draw(self, poly, vertexData, color, zBuffer):
        # variables
        edges = []

        # Pre-compute the edge constants: XStart, Ystart, Yend, dX, Zstart, dZ
        eTable = edgeTable(vertexData)
        eTable = eTable.compute(vertexData)

        # Very short polygons (less than a pixel high) are not drawn
        if (eTable == []):
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
            
            # Paint across a fill line
            for X in range(LeftX, RightX):  
                if (Z < zBuffer[X][Y]):
                    self.canvas.w.create_line(X,Y,X+1,Y,fill=color) # Set a Pixel
                    zBuffer[X][Y] = Z
                Z = Z + dZFillLine

            # Update the X values of edges I and J for the next fill line
            EdgeIX = EdgeIX + eTable[I].dX
            EdgeJX = EdgeJX + eTable[J].dX

            EdgeIZ = EdgeIZ + eTable[I].dZ
            EdgeJZ = EdgeJZ + eTable[J].dZ


            # Upon reaching the bottom of an edge switch out with next edge
            if (Y >= eTable[I].Yend) and (Y < LastFillLine):
                I=Next
                EdgeIX = eTable[I].Xstart
                EdgeIZ = eTable[I].Zstart
                Next += 1
            if (Y >= eTable[J].Yend) and (Y < LastFillLine):
                J=Next
                EdgeJX = eTable[J].Xstart
                EdgeJZ=eTable[J].Zstart
                Next += 1

