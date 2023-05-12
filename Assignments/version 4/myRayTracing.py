##############
# Raytracing #
##############
from myIlluminationModels import *
from myMath import *
from myVariables import *

# Traces a single ray, returning the color of the pixel as an [R,G,B] list, using a 0-1 scale
def traceRay(startPoint, ray, depth, curObjectName="__NONE__"):
    # sky color is grey blue
    skyColor = [182/255,180/255,235/255]

    # find second point along given ray
    secondPoint = ray.toCopy()
    secondPoint.addV(startPoint)
    
    # return "black" when you reach the bottom of the the recursive calls
    if depth == 0:
        return [0,0,0]

    # interset the ray with all objects to determine nearestObject (if any)
    tMin = 999999 # intialize t to a very large number
    for object in objects:
        # do not check for collision with the object reflected off of
        if (depth == 2-1):
            pass
            #print(curObjectName)
            #print(object.name)
        if object.name == curObjectName:
            # do nothing
            pass
        
        elif object.intersect(startPoint, secondPoint):
            if object.t < tMin:
                tMin = object.t
                nearestObject = object

    # return skyColor if no intersection
    if tMin == 999999:
        return skyColor
    
    # determine localColor and the weight for that color at the intersection point
    color = nearestObject.localColor
    intensity = nearestObject.phongIntensityF()
    #f inShadow(nearestObject, nearestObject.intersectionPoint):
        #intensity *= 0.25

    localColor = [color[0]*intensity*2, color[1]*intensity*2, color[2]*intensity*2] # the *2 is a hack
    localWeight = nearestObject.localWeight

    # compute the color returned from the reflected ray
    reflectWeight = nearestObject.reflectWeight
    reflectRay = nearestObject.reflectF()
    reflectStartPoint = nearestObject.intersectionPoint
    nextObjectName = nearestObject.name
    
    if (nearestObject.refractWeight != 0):
        refractWeight = nearestObject.refractWeight
        refractRay = nearestObject.refractF()
        refractColor = traceRay(reflectStartPoint, refractRay, depth-1, nextObjectName)
    else:
        refractWeight = 0
        refractColor = [0,0,0]

    reflectColor = traceRay(reflectStartPoint, reflectRay, depth-1, nextObjectName)
    
    if (nearestObject.name == "Green Sphere"):
        if (reflectWeight > 0):
            print("UGHSL")
            print(nearestObject.name)
            print(reflectWeight)
            print(reflectColor)
            print(refractWeight)
            print(refractColor)
            
    # combine the local and reflected colors together using their respective weights
    returnColor = [0,0,0]

    for i in range(3):
        returnColor[i] = localColor[i]*localWeight + reflectColor[i]*reflectWeight + refractColor[i]*refractWeight
        # check if outside range
        if (returnColor[i] > 1):
            #print("COLOR INPUT OUTSIDE RANGE (>1): "+str(returnColor[i]))
            returnColor[i] = 1

        if (returnColor[i] < 0):
            #print("COLOR INPUT OUTSIDE RANGE (<0): "+str(returnColor[i]))
            returnColor[i] = 0

    return returnColor

# This method interates over each pixel of the image, one row of pixels at a time
def renderImage(L, c, canvasHeight, canvasWidth):
    d = 500  
    model = phongIlluminationModel("Phong Illumination Model")
    illuminationSaturationCounter = 0
    L.normalize()

    # define dimensions of view screen
    top = round(canvasHeight/2)
    bottom = round(-canvasHeight/2)
    left = round(-canvasWidth/2)
    right = round(canvasWidth/2)

    # cycle through every pixel of view screen
    for y in range(top,bottom,-1):
        for x in range(left, right):
            # compute the ray
            screenPoint = vector3(x,y,0)
            centerOfProjection = vector3(0,0,-d)
            ray = vector3.computeUnitVector(centerOfProjection, screenPoint)

            # recursively compute color
            color = traceRay(centerOfProjection, ray, 4)
            c.w.create_line(right+x, top-y, right+x+1, top-y, fill=model.triColorHexCode(color[0],color[1],color[2]))

    #x=0
    #y=-200
    #point = vector3(x,y,0)
    #centerOfProjection = vector3(0,0,-d)
    #ray = vector3.computeUnitVector(centerOfProjection, point)
    #color = traceRay(centerOfProjection, ray, 1, objects, point)
    #c.w.create_line(right+x, top-y, right+x+1, top-y, fill=model.triColorHexCode(color[0],color[1],color[2]))

    overSat = illuminationSaturationCounter / (canvasWidth * canvasHeight) * 100
    print(illuminationSaturationCounter, " pixel color values were oversaturated: ", overSat, "%.")

# shadow detection
def inShadow(nearestObject, intersectionPoint):
    # variables
    L = vector3(1,1,-1)
    L.normalize()

    startPoint = intersectionPoint
    secondPoint = L.toCopy()
    secondPoint.addV(startPoint)

    # cycle through all objects
    # check if traced ray intersects an object
    # if the object intersection is not the one the ray is emitted from then return true
    for object in objects:
        if object.name == nearestObject.name:
            # do nothing
            return False
        
        if object.intersect(startPoint, secondPoint):
            return True
            
    # no intersection, no shadow
    return False









