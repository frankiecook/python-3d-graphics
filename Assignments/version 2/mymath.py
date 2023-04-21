import math

################
# Matrix Class #
################
class m4x4:
    def __init__(self):
        # original matrix is an identity matrix
        self.matrix = [[1,0,0,0],
                      [0,1,0,0],
                      [0,0,1,0],
                      [0,0,0,1]]

    # translation of the original matrix by a displacement vector
    def translate(self, dispVector):
        # new identity matrix
        m = m4x4()
        
        # tranlate applies to bottom row of matrix
        m.matrix[3][0] += dispVector.x
        m.matrix[3][1] += dispVector.y
        m.matrix[3][2] += dispVector.z

        self.dotM(m.matrix)

    # matrix scaling of the original matrix
    def scale(self, scaleFactor=1.0):
        # new identity matrix
        m = m4x4()
        
        # scale matrix
        m.matrix[0][0] *= scaleFactor
        m.matrix[1][1] *= scaleFactor
        m.matrix[2][2] *= scaleFactor

        self.dotM(m.matrix)

    # matrix rotation of the original matrix
    def rotateZ(self, degrees):
        # new identity matrix
        m = m4x4()
        
        # rotate matrix
        m.matrix[0][0] = math.cos(degrees)
        m.matrix[0][1] = math.sin(degrees)
        m.matrix[1][0] = -math.sin(degrees)
        m.matrix[1][1] = math.cos(degrees)

        self.dotM(m.matrix)

    # matrix rotation of the original matrix
    def rotateY(self, degrees):
        # new identity matrix
        m = m4x4()
        
        # rotate matrix
        m.matrix[0][0] = math.cos(degrees)
        m.matrix[0][2] = -math.sin(degrees)
        m.matrix[2][0] = math.sin(degrees)
        m.matrix[2][2] = math.cos(degrees)

        self.dotM(m.matrix)

    # matrix rotation of the original matrix
    def rotateX(self, degrees):
        # new identity matrix
        m = m4x4()
        
        # rotate matrix
        m.matrix[1][1] = math.cos(degrees)
        m.matrix[1][2] = math.sin(degrees)
        m.matrix[2][1] = -math.sin(degrees)
        m.matrix[2][2] = math.cos(degrees)

        self.dotM(m.matrix)
        

    # dot product between two 4x4 matrices
    def dotM(self,m):
        # self.matrix shorthand
        sm = self.copy().matrix

        # update row 1 of self.matrix
        self.matrix[0][0] = sm[0][0] * m[0][0] + sm[0][1] * m[1][0] + sm[0][2] * m[2][0] + sm[0][3] * m[3][0]
        self.matrix[0][1] = sm[0][0] * m[0][1] + sm[0][1] * m[1][1] + sm[0][2] * m[2][1] + sm[0][3] * m[3][1]
        self.matrix[0][2] = sm[0][0] * m[0][2] + sm[0][1] * m[1][2] + sm[0][2] * m[2][2] + sm[0][3] * m[3][2]
        self.matrix[0][3] = sm[0][0] * m[0][3] + sm[0][1] * m[1][3] + sm[0][2] * m[2][3] + sm[0][3] * m[3][3]
        # update row 2 of self.matrix
        self.matrix[1][0] = sm[1][0] * m[0][0] + sm[1][1] * m[1][0] + sm[1][2] * m[2][0] + sm[1][3] * m[3][0]
        self.matrix[1][1] = sm[1][0] * m[0][1] + sm[1][1] * m[1][1] + sm[1][2] * m[2][1] + sm[1][3] * m[3][1]
        self.matrix[1][2] = sm[1][0] * m[0][2] + sm[1][1] * m[1][2] + sm[1][2] * m[2][2] + sm[1][3] * m[3][2]
        self.matrix[1][3] = sm[1][0] * m[0][3] + sm[1][1] * m[1][3] + sm[1][2] * m[2][3] + sm[1][3] * m[3][3]
        # update row 3 of self.matrix
        self.matrix[2][0] = sm[2][0] * m[0][0] + sm[2][1] * m[1][0] + sm[2][2] * m[2][0] + sm[2][3] * m[3][0]
        self.matrix[2][1] = sm[2][0] * m[0][1] + sm[2][1] * m[1][1] + sm[2][2] * m[2][1] + sm[2][3] * m[3][1]
        self.matrix[2][2] = sm[2][0] * m[0][2] + sm[2][1] * m[1][2] + sm[2][2] * m[2][2] + sm[2][3] * m[3][2]
        self.matrix[2][3] = sm[2][0] * m[0][3] + sm[2][1] * m[1][3] + sm[2][2] * m[2][3] + sm[2][3] * m[3][3]
        # update row 4 of self.matrix
        self.matrix[3][0] = sm[3][0] * m[0][0] + sm[3][1] * m[1][0] + sm[3][2] * m[2][0] + sm[3][3] * m[3][0]
        self.matrix[3][1] = sm[3][0] * m[0][1] + sm[3][1] * m[1][1] + sm[3][2] * m[2][1] + sm[3][3] * m[3][1]
        self.matrix[3][2] = sm[3][0] * m[0][2] + sm[3][1] * m[1][2] + sm[3][2] * m[2][2] + sm[3][3] * m[3][2]
        self.matrix[3][3] = sm[3][0] * m[0][3] + sm[3][1] * m[1][3] + sm[3][2] * m[2][3] + sm[3][3] * m[3][3]

    # return a copy of matrix
    def copy(self):
        m = m4x4()

        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix[0])):
                m.matrix[i][j] = self.matrix[i][j]
        
        return m

        
################
# 3D Vector Class #
################
class vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    # returns magnitude of vector
    def magnitude(self):
        x = self.x
        y = self.y
        z = self.z
        
        return math.sqrt(x*x+y*y+z*z)

    # normalizes the vector
    def normalize(self):
        mag = self.magnitude()
        
        self.x /= mag
        self.y /= mag
        self.z /= mag

    # multiply vector by scalar
    def scale(self, scaleFactor=1.0):
        self.x *= scaleFactor
        self.y *= scaleFactor
        self.z *= scaleFactor

    # cross product between two 3D vectors
    def crossProduct(self, vector):
        Px = self.x
        Py = self.y
        Pz = self.z
        Qx = vector.x
        Qy = vector.y
        Qz = vector.z

        self.x = Py * Qz - Pz * Qy
        self.y = Pz * Qx - Px * Qz
        self.z = Px * Qy - Py * Qx

    # dot product between two 3D vectors
    def dotV(self, vector):
        Px = self.x
        Py = self.y
        Pz = self.z
        Qx = vector.x
        Qy = vector.y
        Qz = vector.z

        dotV = Px * Qx + Py * Qy + Pz * Qz
        return dotV

    # dot product of 3D vector and 4x4 matrix
    # vector (x, y, z, 1)
    def dotM(self, matrix):       
        x = self.x
        y = self.y
        z = self.z
        a = 1
        
        self.x = (matrix[0][0] * x + matrix[1][0] * y + matrix[2][0] * z + matrix[3][0] * a)
        self.y = (matrix[0][1] * x + matrix[1][1] * y + matrix[2][1] * z + matrix[3][1] * a)
        self.z = (matrix[0][2] * x + matrix[1][2] * y + matrix[2][2] * z + matrix[3][2] * a)

    # useful for debugging
    def getArray(self):
        return [self.x, self.y, self.z]

##################
# 3D Point Class #
##################
class point3:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z





        
