import sys
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender

import MotionTrailUtil as util
reload(util)
import maya.cmds as cmds

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin roduces, and
    expects to be passed, objects created using the Maya Python API 2.0
    """
    pass

class DrawNode(OpenMayaUI.MPxLocatorNode):
    id = OpenMaya.MTypeId(0x82307)
    drawDbClassification = "drawdb/geometry/DrawNode"
    drawRegistrantId = "DrawNodePlugin"

    def __init__(self):
        """
        """
        print "initializing MpxLocatorNode"
        #OpenMaya.MPxNode.__init__(self)
        OpenMayaUI.MPxLocatorNode.__init__(self)
        #test points
        self.points = [OpenMaya.MPoint([0.0, 0.0, 0.0]), 
                      OpenMaya.MPoint([0.0, 10.0, 10.0])]   
                      
    @staticmethod
    def creator():
        return DrawNode()

    @staticmethod
    def drawNodeInitializer():
        # input
        sizeAttr = OpenMaya.MFnNumericAttribute()
        keySizeAttr = OpenMaya.MFnNumericAttribute()
        bufferAttr = OpenMaya.MFnNumericAttribute()
        DrawNodeDrawOverride.size = sizeAttr.create("size", "sz", OpenMaya.MFnNumericData.kFloat, 0.15 )
        DrawNodeDrawOverride.keySize = keySizeAttr.create("keyFrameSize", "ksz", OpenMaya.MFnNumericData.kFloat, 0.2 )
        DrawNodeDrawOverride.timeBuffer = bufferAttr.create("timeBuffer", "tb", OpenMaya.MFnNumericData.kInt, 11)
        sizeAttr.storable = True
        keySizeAttr.storable = True
        bufferAttr.storable = True
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.size)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.keySize)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.timeBuffer)

class DrawNodeData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False) ## don't delete after draw
        self.name = None
        self.startFrame = 0
        self.endFrame = 0
        self.points= []

class DrawNodeDrawOverride(OpenMayaRender.MPxDrawOverride):
    size = None
    keySize = None
    timeBuffer = None

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
        timeBuffer = cmds.getAttr(str(objPath) + '.tb')
        keyFrames = list(set(cmds.keyframe(data.name, q = True, tc = True)))
        keyFrames = [int(x) for x in keyFrames]

        #for i in range(data.startFrame, data.endFrame + 1):
        for i in range(int(cmds.currentTime(q = True) - timeBuffer), int(cmds.currentTime(q = True) + timeBuffer + 1)):
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
            size = cmds.getAttr(str(objPath) + '.sz')
            keySize = cmds.getAttr(str(objPath) + '.ksz')

            if data.points[frame][1] == 1:
                #key frame
                drawManager.setColor(color3)
                drawManager.sphere(point1, keySize, filled = True)
            else:
                drawManager.setColor(color1)
                drawManager.sphere(point1, size, filled = True)

            if prev:
                drawManager.setColor(color2)
                drawManager.setLineWidth(3)
                drawManager.line(prev, point1)
            prev = point1
            
        drawManager.endDrawable()

def initializePlugin(mobject):
    plugin = OpenMaya.MFnPlugin(mobject, "Jonghwan Hwang", "1.0", "Any")
    plugin.registerNode("DrawNode", 
                        DrawNode.id, 
                        DrawNode.creator,
                        DrawNode.drawNodeInitializer,
                        OpenMaya.MPxNode.kLocatorNode,
                        DrawNode.drawDbClassification)
    OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(DrawNode.drawDbClassification,
                                                             DrawNode.drawRegistrantId,
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
        plugin.deregisterNode(DrawNode.id)
    except:
        sys.stderr.write("Failed to deregisterNode\n")
    
    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(DrawNode.drawDbClassification, 
                                                                   DrawNode.drawRegistrantId)
    except:
        sys.stderr.write("Failed to deregister override\n")
        
    
    
    