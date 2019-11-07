import sys
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender

import MotionTrailDrawNode as dn
reload(dn)
import MotionTrailUtil as util
reload(util)
import maya.cmds as cmds

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin roduces, and
    expects to be passed, objects created using the Maya Python API 2.0
    """
    pass

class DrawNodeData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False) ## don't delete after draw
        self.name = None
        self.startFrame = 0
        self.endFrame = 0
        self.points= []
        
class DrawNodeDrawOverride(OpenMayaRender.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return DrawNodeDrawOverride(obj)
 
    @staticmethod
    def draw(context, data):
        return
 
    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, DrawNodeDrawOverride.draw)
 
    def supportedDrawAPIs(self):
        ## this plugin supports both GL and DX
        return OpenMayaRender.MRenderer.kOpenGL | OpenMayaRender.MRenderer.kDirectX11 | OpenMayaRender.MRenderer.kOpenGLCoreProfile
 
    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        ## Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, DrawNodeData):
            data = DrawNodeData()
        
        #todo nicer way of getting attrs
        mtName = str(objPath)
        data.name = cmds.getAttr(mtName + ".nodeName")
        data.startFrame = int(cmds.getAttr(mtName + '.startTime'))
        data.endFrame = int(cmds.getAttr(mtName + '.endTime'))
        
        points = {}
        timeBuffer = 9
        keyFrames = list(set(cmds.keyframe(data.name, q = True, tc = True)))
        keyFrames = [int(x) for x in keyFrames]

        #for i in range(data.startFrame, data.endFrame + 1):
        for i in range(int(cmds.currentTime(q = True) - timeBuffer), int(cmds.currentTime(q = True) + timeBuffer)):
            point = cmds.getAttr("{}.wm".format(data.name), time = i)
            relativePoint = util.makeCameraRelative(point, util.getCam(), i)
                        
            if i in keyFrames:
                points[i] = (relativePoint, 1)
            else:
                points[i] = (relativePoint, 0)
                
        
        data.points = points
        
        return data
 
    def hasUIDrawables(self):
        return True
 
    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        locatordata = data
        if not isinstance(locatordata, DrawNodeData):
            return
        drawManager.beginDrawable()
 
        drawManager.setDepthPriority(10000)
        color1 = OpenMaya.MColor((0.5, 0.1, 0.8, 1.0))
        color2 = OpenMaya.MColor((1.0, 1.0, 1.0, 1.0))
        color3 = OpenMaya.MColor((1.0, 0.0, 0.0, 1.0))
        
        prev = None
        allFrames = data.points.keys()
        allFrames.sort()
        
        for frame in allFrames:
            point = data.points[frame][0]
            point1 = OpenMaya.MPoint(point[0], point[1], point[2], 1)
            
            if data.points[frame][1] == 1:
                #key frame
                drawManager.setColor(color3)
                drawManager.sphere(point1, 0.2, filled = True)
            else:
                drawManager.setColor(color1)
                drawManager.sphere(point1, 0.15, filled = True)

            if prev:
                drawManager.setColor(color2)
                drawManager.setLineWidth(3)
                drawManager.line(prev, point1)
            prev = point1
            
        drawManager.endDrawable()
        
        """
        drawManager.text( OpenMaya.MPoint(0, 1, 0), "3D SPACE TEXT", OpenMayaRender.MUIDrawManager.kLeft )
 
        textColor = OpenMaya.MColor((0.5, 0.3, 0.4, 1.0))
        drawManager.setColor( textColor )
 
        drawManager.text2d( OpenMaya.MPoint(500, 500), "2D SPACE TEXT", OpenMayaRender.MUIDrawManager.kLeft )
 
        drawManager.endDrawable()
        """
        
def initializePlugin(mobject):
    plugin = OpenMaya.MFnPlugin(mobject, "Jonghwan Hwang", "1.0", "Any")
    #plugin.registerNode("DrawNode", dn.DrawNode.id, dn.DrawNode.creator, dn.DrawNode.initialize, OpenMaya.MPxNode, dn.DrawNode.drawDbClassification)
    plugin.registerNode("DrawNode", 
                        dn.DrawNode.id, 
                        dn.DrawNode.creator,
                        dn.DrawNode.initialize,
                        OpenMaya.MPxNode.kLocatorNode,
                        dn.DrawNode.drawDbClassification)
    OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(dn.DrawNode.drawDbClassification,
                                                             dn.DrawNode.drawRegistrantId,
                                                             DrawNodeDrawOverride.creator)
    """
    try:
        plugin.registerNode("DrawNode", dn.DrawNode.id, dn.DrawNode.creator, 
                            dn.DrawNode.initialize, OpenMaya.MpxNode, 
                            dn.DrawNode.drawDbClassification)
    except:
        sys.stderr.write("Failed toregister node\n")
    
    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(dn.DrawNode.drawDbClassification,
                                                                 dn.DrawNode.drawRegistrantId,
                                                                 DrawNodeDrawOverride.creator)
    except:
        sys.stderr.write("Failed to register override\n")
    """    
def uninitializePlugin(mobject):
    plugin = OpenMaya.MFnPlugin(mobject)
    try:
        plugin.deregisterNode(dn.DrawNode.id)
    except:
        sys.stderr.write("Failed to deregisterNode\n")
    
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(dn.DrawNode.drawDbClassification, 
                                                                   dn.DrawNode.drawRegistrantId)
    except:
        sys.stderr.write("Failed to deregister override\n")
        
    
    
    