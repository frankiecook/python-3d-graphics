#######################
# Illumination Models #
#######################
import math
from myMath import *

class phongIlluminationModel:

    def __init__(self, name):
        self.name = name
        self.lightSources = []
        self.I = []
        self.K = []

    # Add a light source to the light sources array
    # TODO: does not support multiple light sources
    def addLightSource(self, L):
        self.lightSources.append(L)

    ### Ambient ###
    # ambient light is constant throughout the scene
    # Ia : incoming light source Intensity
    # Kd : objects diffuse reflectivity
    def ambient(self, Ia, Kd):        
        # red ambient
        ambientR = Ia[0] * Kd[0]
        # green ambient
        ambientG = Ia[1] * Kd[1]
        # red ambient
        ambientB = Ia[2] * Kd[2]

        ambientRGB = [ambientR, ambientG, ambientB]
        return ambientRGB


    ### Diffuse ###
    # RGB values for multiple emitter point source + ambient model
    # when cos(theta) < 0, set Diffuse = 0
    # Ip : the point source intensity
    # Kd : diffuse reflectivity of object
    # d : distnace between object and light source (constant of 1)
    def diffuse(self, N, Ip, Kd, d=1, intersectionPoint = "__NONE__"):
        diffuseR = 0
        diffuseG = 0
        diffuseB = 0

        # normal vector
        N.normalize()
            
        # cylce through light sources
        for L in self.lightSources:

            # light source vector
            vectorL = vector3(L[0], L[1], L[2])
            vectorL.normalize()

            # exception for planes
            if L[0] == 500:
                vectorL = vector3.computeUnitVector(intersectionPoint, vectorL)

            diffuseR += Ip[0] * Kd[0] * (N.dotV(vectorL)) / d
            diffuseG += Ip[1] * Kd[1] * (N.dotV(vectorL)) / d
            diffuseB += Ip[2] * Kd[2] * (N.dotV(vectorL)) / d

        diffuseRGB = [diffuseR, diffuseG, diffuseB]
        return diffuseRGB

    ### Specular ###
    # specular reflection accounts for mirror reflection
    # Ip : Point source light intensity
    # Ks : diffuse constant?
    # R : Reflection Vector
    # V : View Vector
    def specular(self, N, Ip, Ks, intersectionPoint):
        # default
        specularR = 0
        specularG = 0
        specularB = 0
        
        # polygon normal vector
        N.normalize()

        # view vector, camera is fixed
        V = vector3(0,0,-1)

        for L in self.lightSources:
            # reflection vector
            R = []
        
            # light source vector    
            vectorL = vector3(L[0], L[1], L[2])
            vectorL.normalize()

            # exception for planes
            if L[0] == 500:
                vectorL = vector3.computeUnitVector(intersectionPoint, vectorL)
            
            # angle between N and L
            twoCosPhi = 2 * (N.dotV(vectorL))
            
            # calculate R
            # case 1: light source above surface
            if (twoCosPhi > 0):
                for i in range(3):
                    R.append(N.index(i) - (vectorL.index(i) / twoCosPhi))
            # case 2: light source parallel to surface
            elif (twoCosPhi == 0):
                for i in range(3):
                    R.append(-vectorL.index(i))
            # case 3: light source is below surface
            else:# (twoCosPhi < 0):
                for i in range(3):
                    R.append(-N.index(i) + (vectorL.index(i) / twoCosPhi))

            # cycle
            Rbefore = vector3(R[0], R[1], R[2])
            R = vector3(R[0], R[1], R[2])
            
            R.normalize()
            # specular index
            specIndex = R.dotV(V)

            specularR += Ip[0] * Ks[0] * (specIndex)
            specularG += Ip[1] * Ks[1] * (specIndex)
            specularB += Ip[2] * Ks[2] * (specIndex)
        
        specularRGB = [specularR, specularG, specularB]
        return specularRGB

    # generate a color hex code string form the illumination components
    # intensities should range from 0-1
    def triColorHexCode(self, ambient, diffuse, specular):
        #combinedColorCode = self.colorHexCode(ambient + diffuse + specular)
        ambientColorCode = self.colorHexCode(ambient)
        diffuseColorCode = self.colorHexCode(diffuse)
        specularColorCode = self.colorHexCode(specular)
        colorString = "#" + ambientColorCode + diffuseColorCode + specularColorCode
        
        return colorString

    # intenstiy input should range from 0-1
    # returns a hex string that trims to the first two values (after 0x)
    def colorHexCode(self, intensity):
        if intensity > 1 or intensity < 0:
            print("INTENSITY INPUT OUTSIDE RANGE (0-1): "+str(intensity))
            return
        
        hexString = str(hex(round(255 * intensity)))

        if hexString[0] == "-": #illumination intensity should not be negative
            #print("illumination intensity is Negative. Setting to 00.")
            trimmedHexString = "00"
        else:
            trimmedHexString = hexString[2:] # get rid of "0x" at beginning of hex strings
            # convert single digit hex strings to two digit hex strings
            if len(trimmedHexString) == 1:
                trimmedHexString = "0" + trimmedHexString
            # we will use the green color component to display our monochrome illumination results
        return trimmedHexString























