import maya.cmds as cmds
import maya.mel as mm
from maya import OpenMaya

def getApiMatrix(matrix):
    """
    """
    mat = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList(matrix, mat)
    
    return mat

def getCam():
    """
    """
    panel = cmds.getPanel(wf = True)
    #cam = cmds.modelEditor(panel, q = True, camera = True)
    cam = cmds.lookThru(q = True)
    return cam    
    
def makeCameraRelative(point, camera, time):
    """
    sets points of given motionTrail to projected points to given camera from 
    given startTime to length of motionTrail Points
    
    @param [(float, float, float)] points
    @param str camera : name of camera to project points on
    @param int startTime : start of MotionTrail
    """
    if not cmds.objExists(camera):
        return (point[12], point[13], point[14])
    
    camLocal = getApiMatrix(cmds.getAttr(camera + ".wm", time = time))
    camWorldCurrent = getApiMatrix(cmds.getAttr(camera + '.wm', time = cmds.currentTime(q = True)))
    pointMatrix = getApiMatrix(point)
    localMatrix = pointMatrix * camLocal.inverse()
    worldMatrix = localMatrix * camWorldCurrent
    mt = OpenMaya.MTransformationMatrix(worldMatrix)
    translation = mt.translation(OpenMaya.MSpace.kWorld) 
    relativePoint = (translation[0], translation[1], translation[2])
    
    return relativePoint