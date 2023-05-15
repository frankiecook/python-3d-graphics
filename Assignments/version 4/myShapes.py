##########################################
# Shape Class, Pyramid Class, Cube Class #
##########################################
import copy
import math
from myMath import *
from myGeometry import *
from myIlluminationModels import *
from myVariables import *

# ***************************** Shape Class *************************** #
class shape:
    def __init__(self, name):
        self.name = name
        self.renderSetting = 7
        self.defaultPointCloud = []
        self.transformation = m4x4()
        self.visualCenter = [0,0,0]
        self.selectColor = "black"
        self.selectWidth = 2

        self.t = 0
        self.intersectionPoint = vector3(0,0,0)

        self.phongIntensityWeight = 0.8
        self.localWeight = 0.5
        self.reflectWeight = 0
        self.refractWeight = 0
        self.specIndex = 0.5
        self.density = 2
        
        self.Ks = [0.5,0.5,0.5]
        self.Ia = [0.5,0.5,0.5]
        self.Ip = [0.5,0.5,0.5]
        self.Kd = [0.5,0.5,0.5]

        self.model = phongIlluminationModel("test phong")

    def setup(self,x=0,y=0,z=0,size=1):
        self.model.addLightSource([1,1,-1])

    def update(self):
        pass

    # This function resets the pyramid to its original size and location in 3D space
    # Note that you have to be careful to update the values in the existing PyramidPointCloud
    # structure rather than creating a new structure or just switching a pointer.  In other
    # words, you'll need manually update the value of every x, y, and z of every point in
    # point cloud (vertex list).
    def reset(self):
        for poly in self.polys:
            print(poly.defaultVertices)

        self.update()

    def reflect(self, T, N):
        # variables
        radians90 = math.pi / 2
        R = vector3(0,0,0)
        
        # R = N + T / (2*NdotT)
        # denominator
        Tminus = T.toCopy()
        Tminus.scale(-1)
        denominator = 2 * (N.dotV(Tminus))

        # calculate R
        # case 1: traced ray parallel to normal vector
        if (denominator == 0):
            R = N.toCopy()
        # case 2: traced ray perpendicular to normal
        elif (denominator == 2*radians90):
            R = T.toCopy()
        # case 2: traced ray 
        elif (denominator < 2*radians90):
            R = N.toCopy()
            Tscale = T.toCopy()
            Tscale.scale(1/denominator)
            R.addV(Tscale)
        else:
            print("ERROR: ANGLE GREATER THAN 90 DEGREES")

        # normalize reflection vector
        R.normalize()

        return R

    def refract(self, d1, d2, T, N):
        # density
        density = d2 / d1

        # cos1: part of calculation
        Tminus = T.toCopy()
        Tminus.scale(-1)
        cos1 = Tminus.dotV(N)
        
        # cos2: part of calculation
        cos2 = math.sqrt(1 - (1/(density*density)) * (1-(cos1*cos1)))

        # transmitted ray
        Tscale = T.toCopy()
        Tscale.scale(1/density)

        # normal vector
        Nscale = N.toCopy()
        Nscale.scale(cos2 - (1/density) * cos1)

        # transmitted ray
        trans = Tscale.toCopy()
        trans.subV(Nscale)
        trans.normalize()

        return trans

    def phongIntensity(self, N, L):

        # Ambient Light in Scene
        # Ia : incoming light source Intensity
        # Kd : objects diffuse reflectivity
        ambientRGB = self.model.ambient(self.Ia, self.Kd)

        # Diffuse Light in on Polygon
        # Ip : the point source intensity
        # cos(theta)
        # Kd : diffuse reflectivity of object
        diffuseRGB = self.model.diffuse(N, self.Ip, self.Kd)
        
        # Specular Light on Polygon
        # Ip : Point source light intensity
        # Ks : diffuse constant?
        # R : Reflection Vector
        # V : View Vector
        specularRGB = self.model.specular(N, self.Ip, self.Ks)

        # generate color and fill polygon
        intensity = ambientRGB[0] + diffuseRGB[0] + specularRGB[0]
        return intensity

# ***************************** Sphere Class *************************** #
class sphere(shape):

    # localColor : 
    def __init__(self, name):
        shape.__init__(self, name)
        self.centerPoint = vector3(0, 0, 0)
        self.radius = 100
        self.localColor = [0.1,0.9,0.5]

    # ray is normalized
    def intersect(self, startPoint, secondPoint):
        # second point along ray
        X2 = secondPoint.x
        Y2 = secondPoint.y
        Z2 = secondPoint.z
        
        # compute ray-sphere intesection equation
        X1 = startPoint.x
        Y1 = startPoint.y
        Z1 = startPoint.z
        
        # ijk : ray direction
        i = X2 - X1
        j = Y2 - Y1
        k = Z2 - Z1
        
        # lmn : sphere center
        l = self.centerPoint.x
        m = self.centerPoint.y
        n = self.centerPoint.z
        
        # sphere radius
        r = self.radius
        
        # a = i^2 + j^2 + k^2
        a = i*i + j*j + k*k
        # b = 2*i*(X1 - l) + 2*j*(Y1 - m) + 2*k*(Z1 - n)
        b = 2*i*(X1 - l) + 2*j*(Y1 - m) + 2*k*(Z1 - n)
        # c = l^2 + m^2 + n^2 + X1^2 + Y1^2 + Z1^2 + 2*(-l*X1 - m*Y1 - n*Z1) - r^2
        c = l*l + m*m + n*n + X1*X1 + Y1*Y1 + Z1*Z1 + 2*(-l*X1 - m*Y1 - n*Z1) - r*r

        # discriminant
        discriminant = b*b - 4*a*c
        #print("discriminant: "+str(discriminant))

        # no intersection
        if (discriminant < 0):# or 2*a==0:
            return False
        elif (2*a == 0):
            self.t = 9999999999
        # one intersection
        elif (discriminant == 0):
            t1 = (-b - math.sqrt(discriminant)) / (2*a)
            t2 = (-b + math.sqrt(discriminant)) / (2*a)
            print(str(t1)+","+str(t2))
        # two intersections
        elif (discriminant > 0):
            t1 = (-b - math.sqrt(discriminant)) / (2*a)
            t2 = (-b + math.sqrt(discriminant)) / (2*a)

            # pick smallest, closer, t
            if (t2 < t1):
                self.t = t2
            else:
                self.t = t1

        # check that intersection is not behind ray start
        if t1<0 and t2<0:
            return False
        elif t1<0:
            self.t=t2
        elif t2<0:
            self.t=t1
            
        # calculate intersection point
        # X = X1 + i*t
        X = int(X1 + i*self.t)
        Y = int(Y1 + j*self.t)
        Z = int(Z1 + k*self.t)

        # set intersection point
        self.intersectionPoint = vector3(X,Y,Z)
        return True

    # modified equation for reflecting a traced ray for incident angles
    def reflect(self, startPoint):
        # variables
        intPoint = self.intersectionPoint.toCopy()
    
        #  vector
        T = intPoint.toCopy()
        T.subV(startPoint)
        T.normalize()
        
        # normal to surface
        N = intPoint.toCopy()
        N.subV(self.centerPoint)
        N.normalize()

        return shape.reflect(self,T,N)


    def refract(self, startPoint):
        # variables
        intPoint = self.intersectionPoint.toCopy()
        radians90 = math.pi / 2
        d1 = 1
        d2 = self.density
        
        # traced ray T
        T = intPoint.toCopy()
        T.subV(startPoint)
        T.normalize()

        # normal to surface
        N = intPoint.toCopy()
        N.subV(self.centerPoint)
        N.normalize()

        return shape.refract(self,d1,d2,T,N)

    def phongIntensity(self):
        intPoint = self.intersectionPoint.toCopy()
        
        # normal to surface
        N = intPoint.toCopy()
        N.subV(self.centerPoint)
        N.normalize()

        # light source
        L = vector3(1,1,-1)

        return shape.phongIntensity(self,N,L)
        

# ***************************** Plane Class *************************** #
class plane(shape):

    def __init__(self, name):
        shape.__init__(self, name)
        self.surfaceNormal = vector3(0,1,0)
        self.anchorPoint = vector3(0,-175,0)
        self.firstColor = [0.1,0.9,0.5]
        self.secondColor = [0.9,0.5,0.1]

    # Intersection Check for Ray Tracing
    # Returns boolean based on intersection
    # rayStartPoint: starting point is the camera position
    # raySecondPoint: second point along ray that is on the view screen
    def intersect(self, rayStartPoint, raySecondPoint):
        # surface normal of plane
        A = self.surfaceNormal.x
        B = self.surfaceNormal.y
        C = self.surfaceNormal.z

        # anchor point of plane
        a = self.anchorPoint.x
        b = self.anchorPoint.y
        c = self.anchorPoint.z

        # ray start point
        X1 = rayStartPoint.x
        Y1 = rayStartPoint.y
        Z1 = rayStartPoint.z

        # second ray point
        X2 = raySecondPoint.x
        Y2 = raySecondPoint.y
        Z2 = raySecondPoint.z

        # ijk : ray direction
        i = X2 - X1
        j = Y2 - Y1
        k = Z2 - Z1
        
        # denominator = A*i + B*j + C*k
        denominator = A*i+B*j+C*k

        # ray is parallel to plane
        if denominator == 0:
            return False
        # ray is not visible, but intersects
        #elif denominator < 0:
        #    return False

        # calculate t
        D = A*a + B*b + C*c
        self.t = -(A*X1 + B*Y1 + C*Z1 - D) / denominator

        # check if intersection is in camera view
        if (self.t < 0):
            return False
        
        # solve for intersection point
        X = int(X1 + i*self.t)
        Y = int(Y1 + j*self.t)
        Z = int(Z1 + k*self.t)

        self.intersectionPoint = vector3(X,Y,Z)
        
        # check where intersection places color
        if X >= 0:
            colorFlag = 1
        else:
            colorFlag = 0

        # render distance
        if (Z > 3000 or Z < -300) or (X > 1000 or X < -1000):# and abs(X) > 300:
            #print(Z)
            return False

        # set color of checkerboard pattern
        if abs(X) % 200 > 100:
            colorFlag = not colorFlag
        if abs(Z) % 200 > 100:
            colorFlag = not colorFlag

        if colorFlag:
            self.localColor = self.firstColor
        else:
            self.localColor = self.secondColor
            
        return True

    def phongIntensity(self):
        # normal to surface
        N = self.surfaceNormal.toCopy()
        N.normalize()

        # light vector
        L = vector3(500,500,0)
        
        return shape.phongIntensity(self, N, L)

    # modified equation for reflecting a traced ray for incident angles
    def reflect(self, startPoint):
        # variables
        intPoint = self.intersectionPoint.toCopy()
        
        # reflection vector
        R = vector3(0,0,0)
    
        #  vector
        T = intPoint.toCopy()
        T.subV(startPoint)
        T.normalize()

        # normal to surface
        N = self.surfaceNormal.toCopy()
        N.normalize()

        return shape.reflect(self,T,N)
    
    # assume vectors T and N are unit vectors
    def refract(self):
        return vector3(0,0,0)

        

        
























        
