##########################################
# Shape Class, Pyramid Class, Cube Class #
##########################################
import copy
import math
from myMath import *
from myGeometry import *
from myIlluminationModels import *

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

        self.phongIntensity = 0.5
        self.localWeight = 0.5
        self.reflectWeight = 0
        self.refractWeight = 0.6
        self.specIndex = 0.7
        self.reflect = 1
        self.refract = 0
        self.density = 2
        
        self.Ks = [0.5,0.5,0.5]
        self.Ia = [0.5,0.5,0.5]
        self.Ip = [0.5,0.5,0.5]
        self.Kd = [0.5,0.5,0.5]

    def setup(self,x=0,y=0,z=0,size=1):
        pass

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
        elif (2*a ==0):
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
            
        # calculate intersection point
        # X = X1 + i*t
        X = int(X1 + i*self.t)
        Y = int(Y1 + j*self.t)
        Z = int(Z1 + k*self.t)

        # set intersection point
        self.intersectionPoint = vector3(X,Y,Z)
        return True

    # modified equation for reflecting a traced ray for incident angles
    def reflectF(self):
        # variables
        intPoint = self.intersectionPoint.toCopy()
        camera = vector3(0,0,-500)
        radians90 = math.pi / 2
        
        # reflection vector
        R = vector3(0,0,0)
    
        # replace L, light, vector with -T, traced ray
        # T = intersection point - camera position
        T = intPoint.toCopy()
        T.subV(camera)
        T.normalize()

        # normal to surface
        N = intPoint.toCopy()
        N.subV(self.centerPoint)
        N.normalize()
        
        # R = N + T / (2*NdotT)
        # denominator
        Tminus = T.toCopy()
        Tminus.scale(-1)
        denominator = 2 * (N.dotV(Tminus))

        # calculate R
        # case 1: traced ray perpendicular to normal vector
        # 90 degree angle, so R = T
        if (denominator == 0):
            R = T.toCopy()
            pass
        # case 2: light source is below surface
        elif (denominator < 2*radians90):
            R = N.toCopy()
            Tscale = T.toCopy()
            Tscale.scale(1/denominator)
            R.addV(Tscale)
        else:
            print("ANGLE GREATER THAN 90 DEGREES")

        # normalize reflection vector
        R.normalize()

        return R

    def refractF(self):
        # variables
        intPoint = self.intersectionPoint.toCopy()
        camera = vector3(0,0,-500)
        radians90 = math.pi / 2
        d1 = 1
        d2 = self.density
        
        # traced ray T
        # T = intersection point - camera position
        T = intPoint.toCopy()
        T.subV(camera)
        #T = vector3(0.7,-0.7,0)
        T.normalize()

        # normal to surface
        N = intPoint.toCopy()
        N.subV(self.centerPoint)
        #N = vector3(0,1,0)
        N.normalize()

        # d
        d = d2 / d1

        # cos1
        Tminus = T.toCopy()
        Tminus.scale(-1)
        cos1 = Tminus.dotV(N)
        
        # cos2
        cos2 = math.sqrt(1 - (1/(d*d)) * (1-(cos1*cos1)))

        # transmitted ray
        Tscale = T.toCopy()
        Tscale.scale(1/d)
        Nscale = N.toCopy()
        Nscale.scale(cos2 - (1/d) * cos1)
        
        trans = Tscale.toCopy()
        trans.subV(Nscale)
        
        trans.normalize()

        return trans

    def phongIntensityF(self):
        intPoint = self.intersectionPoint.toCopy()
        model = phongIlluminationModel("test phong")
        model.addLightSource([1,1,-1])
        
        # normal to surface
        N = intPoint.toCopy()
        N.subV(self.centerPoint)
        N.normalize()

        # Ambient Light in Scene
        # Ia : incoming light source Intensity
        # Kd : objects diffuse reflectivity
        ambientRGB = model.ambient(self.Ia, self.Kd)

        # Diffuse Light in on Polygon
        # Ip : the point source intensity
        # cos(theta)
        # Kd : diffuse reflectivity of object
        diffuseRGB = model.diffuse(N, self.Ip, self.Kd)
        if diffuseRGB != [0,0,0]:
            #print(diffuseRGB)
            pass
        
        # Specular Light on Polygon
        # Ip : Point source light intensity
        # Ks : diffuse constant?
        # R : Reflection Vector
        # V : View Vector
        specularRGB = model.specular(N, self.Ip, self.Ks)

        # generate color and fill polygon
        #color = model.triColorHexCode(ambientRGB[0],diffuseRGB[0],specularRGB[0])
        intensity = ambientRGB[0] + diffuseRGB[0] + specularRGB[0]
        return intensity
        

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
            #print("DENOMINATOR == 0: "+str(denominator))
            return False
        # ray is not visible, but intersects
        #elif denominator < 0:
            #print("DENOMINATOR < 0: "+str(denominator))
            #return False

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
        
        if abs(X) % 200 > 100:
            colorFlag = not colorFlag
        if abs(Z) % 200 > 100:
            colorFlag = not colorFlag

        if colorFlag:
            self.localColor = self.firstColor
        else:
            self.localColor = self.secondColor
            
        return True

    def phongIntensityF(self):
        intPoint = self.intersectionPoint.toCopy()
        model = phongIlluminationModel("test phong")
        model.addLightSource([1,1,-1])
        
        # normal to surface
        N = self.surfaceNormal.toCopy()
        N.normalize()

        # Ambient Light in Scene
        # Ia : incoming light source Intensity
        # Kd : objects diffuse reflectivity
        ambientRGB = model.ambient(self.Ia, self.Kd)

        # Diffuse Light in on Polygon
        # Ip : the point source intensity
        # cos(theta)
        # Kd : diffuse reflectivity of object
        diffuseRGB = model.diffuse(N, self.Ip, self.Kd)
        if diffuseRGB != [0,0,0]:
            #print(diffuseRGB)
            pass
        
        # Specular Light on Polygon
        # Ip : Point source light intensity
        # Ks : diffuse constant?
        # R : Reflection Vector
        # V : View Vector
        specularRGB = model.specular(N, self.Ip, self.Ks)

        # generate color and fill polygon
        #color = model.triColorHexCode(ambientRGB[0],diffuseRGB[0],specularRGB[0])
        intensity = ambientRGB[0] + diffuseRGB[0] + specularRGB[0]
        return intensity

    # modified equation for reflecting a traced ray for incident angles
    def reflectF(self):
        # variables
        intPoint = self.intersectionPoint.toCopy()
        camera = vector3(0,0,-500)
        radians90 = math.pi / 2
        
        # reflection vector
        R = vector3(0,0,0)
    
        #  vector
        T = intPoint.toCopy()
        T.subV(camera)
        T.normalize()

        # normal to surface
        N = self.surfaceNormal.toCopy()
        N.normalize()
        
        # R = N + T / (2*NdotT)
        # denominator
        Tminus = T.toCopy()
        Tminus.scale(-1)
        denominator = 2 * (N.dotV(Tminus))

        # calculate R
        # case 1: traced ray perpendicular to normal vector
        # 90 degree angle, so R = T
        if (denominator == 0):
            print("ZERO DENOMINATOR")
            R = T.toCopy()
            pass
        # case 2: light source is below surface
        elif (denominator < 2*radians90):
            #print("AVERAGE D")
            R = N.toCopy()
            Tscale = T.toCopy()
            Tscale.scale(1/denominator)
            R.addV(Tscale)
        else:
            print("ANGLE GREATER THAN 90 DEGREES")

        # normalize reflection vector
        R.normalize()
        
        return R

    # assume vectors T and N are unit vectors
    def refractF(self):
        # check if object is translucent
        if (self.refract == 0):
            return vector3(0,0,0)

        

        
























        
