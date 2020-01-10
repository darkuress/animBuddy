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
    
    def build(self, 
              dotSize = 0.2, 
              keyFrameSize = 0.25, 
              timeBuffer = 10,
              dotColor = [1.0, 1.0, 0.0],
              keyFrameColor = [0.0, 1.0, 0.0],
              lineWidth = 3,
              lineColor = [1.0, 1.0, 1.0],
              style = 'Double'):
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
        cmds.setAttr(self.mtName + ".dotColor0", dotColor[0])
        cmds.setAttr(self.mtName + ".dotColor1", dotColor[1])
        cmds.setAttr(self.mtName + ".dotColor2", dotColor[2])
        cmds.setAttr(self.mtName + ".keyFrameColor0", keyFrameColor[0])
        cmds.setAttr(self.mtName + ".keyFrameColor1", keyFrameColor[1])
        cmds.setAttr(self.mtName + ".keyFrameColor2", keyFrameColor[2])
        cmds.setAttr(self.mtName + ".lw", lineWidth)
        cmds.setAttr(self.mtName + ".lineColor0", lineColor[0])
        cmds.setAttr(self.mtName + ".lineColor1", lineColor[1])
        cmds.setAttr(self.mtName + ".lineColor2", lineColor[2])
        if style == 'Double':
            mode = 1
        elif style == 'Single':
            mode = 2
        cmds.setAttr(self.mtName + ".mode", mode)

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