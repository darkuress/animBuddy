import maya.cmds as cmds
import os

class MotionTrail(object):
    """
    str motionTrailObject: maya motionTrail object's full name
    """
    
    def __init__(self, node, startTime, endTime):
        """
        """
        self.name = "MotionTrail_{}_main".format(node.split("|")[-1])
        self.mtName = None
        self._startTime = startTime
        self._endTime = endTime
        self.motionTrailObject = node
        
    @property
    def startTime(self):
        """
        """
        return _startTime
    
    def endTime(self):
        """
        """
        return self._endTime
    
    def build(self, dotSize = 0.2, keyFrameSize = 0.25, timeBuffer = 10):
        """
        """
        filePath = os.path.dirname(os.path.abspath(__file__))
        cmds.loadPlugin(os.path.join(filePath, "MotionTrailDraw.py"))
        
        self.mtName = cmds.createNode("DrawNode", name = self.name + "Handle")
        cmds.addAttr(self.mtName, shortName = "nodeName", dataType = "string")
        cmds.setAttr(self.mtName + ".nodeName", self.motionTrailObject, type = "string")
        cmds.addAttr(self.mtName, shortName = "startTime", attributeType = "float", defaultValue = 0.0)
        cmds.setAttr(self.mtName + ".startTime", self._startTime)
        cmds.addAttr(self.mtName, shortName = "endTime", attributeType = "float", defaultValue = 0.0)
        cmds.setAttr(self.mtName + ".endTime", self._endTime)
        
        cmds.setAttr(self.mtName + ".sz", dotSize)
        cmds.setAttr(self.mtName + ".ksz", keyFrameSize)
        cmds.setAttr(self.mtName + ".tb", timeBuffer)

        longName = cmds.ls(self.mtName, l = True)[0]
        transform = cmds.ls(longName.split("|")[-2])[0]
        cmds.rename(transform, self.name)
                
        translates = cmds.getAttr(self.motionTrailObject + ".wm", time = self._startTime)[12:15]
        
        cmds.setAttr(self.name + ".rotatePivotX", translates[0])
        cmds.setAttr(self.name + ".rotatePivotY", translates[1])
        cmds.setAttr(self.name + ".rotatePivotZ", translates[2])
        #cmds.setKeyframe(self.name, time = (self._startTime, ))
        #cmds.setKeyframe(self.name, time = (self._endTime, ))
        
        mtAllName = cmds.group(self.mtName, name = self.mtName + "_all")
        """
        cmds.connectAttr("{}.translate".format(self.motionTrailObject),
                          "{}.localPosition".format(self.mtName))
        cmds.connectAttr("{}.wm".format(self.motionTrailObject),
                          "{}.points".format(self.mtName))        
        """
        return self.mtName