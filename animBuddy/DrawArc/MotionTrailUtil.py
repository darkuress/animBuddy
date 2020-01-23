import maya.cmds as cmds
import maya.mel as mm
#from maya import OpenMaya
import maya.api.OpenMaya as OpenMaya
import math

def getApiMatrix(matrix):
    """
    """
    mat = OpenMaya.MMatrix(matrix)
    
    return mat

def getCam():
    """
    """
    panel = cmds.getPanel(wf = True)
    #cam = cmds.modelEditor(panel, q = True, camera = True)
    cam = cmds.lookThru(q = True)
    return cam    
    
def makeCameraRelative(pointMatrix, camera, time, currentTime):
    """
    sets points of given motionTrail to projected points to given camera from 
    given startTime to length of motionTrail Points
    
    @param [(float, float, float)] points
    @param str camera : name of camera to project points on
    @param int startTime : start of MotionTrail
    """
    if not cmds.objExists(camera):
        return (pointMatrix[12], pointMatrix[13], pointMatrix[14])
    
    camLocal = getApiMatrix(cmds.getAttr(camera + ".wm", time = time))
    camWorldCurrent = getApiMatrix(cmds.getAttr(camera + '.wm', time = currentTime))
    localMatrix = pointMatrix * camLocal.inverse()
    worldMatrix = localMatrix * camWorldCurrent
    mt = OpenMaya.MTransformationMatrix(worldMatrix)
    translation = mt.translation(OpenMaya.MSpace.kWorld) 
    relativePoint = (translation[0], translation[1], translation[2])
    
    return relativePoint

def getDistance(point1, obj2):
    """
    """
    obj1Trans = point1
    obj2Trans = cmds.xform(obj2, q = True, t = True, ws = True)
    dx = obj2Trans[0] - obj1Trans[0]
    dy = obj2Trans[1] - obj1Trans[1]
    dz = obj2Trans[2] - obj1Trans[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)
