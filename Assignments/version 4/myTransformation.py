###################################
# Object Transformation Functions #
###################################
from myMath import *

# This function translates an object by a displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    # uniform displacement in x,y,z directions
    dispVector = vector3(displacement[0], displacement[1], displacement[2])

    # translate object transformation matrix by the displacement vector
    object.transformation.translate(dispVector)

    # update the object's polys
    object.update()
        
# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object, scaleFactor):
    # new composite matrix
    ###################
    # COULD NOT INCOPORATE COMPOSITE MATRIX
    ##################
    composite = m4x4()
    
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)
    
    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)
    
    # scale composite matrix
    object.transformation.scale(scaleFactor)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)
    
    # apply composite matrix to object transform
    #object.transformation.dotM(composite.matrix)

    # finish
    object.update()

# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotateZ(object,degrees):
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)

    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # translate matrix
    object.transformation.rotateZ(degrees)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # finish
    object.update()
    
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object,degrees):
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)

    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # translate matrix
    object.transformation.rotateY(degrees)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # finish
    object.update()

# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object,degrees):
    # find the move vector from visual center to origin
    x = object.visualCenter[0]
    y = object.visualCenter[1]
    z = object.visualCenter[2]   
    moveVector = vector3(x,y,z)

    # translate composite matrix to the world origin
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # translate matrix
    object.transformation.rotateX(degrees)

    # translate composite matrix back to object position
    moveVector.scale(-1)
    object.transformation.translate(moveVector)

    # finish
    object.update()
