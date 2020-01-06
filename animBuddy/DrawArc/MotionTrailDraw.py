import sys
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaAnim as OpenMayaAnim
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
        sizeAttr          = OpenMaya.MFnNumericAttribute()
        keySizeAttr       = OpenMaya.MFnNumericAttribute()
        bufferAttr        = OpenMaya.MFnNumericAttribute()
        dotColorAttr      = OpenMaya.MFnNumericAttribute()
        keyFrameColorAttr = OpenMaya.MFnNumericAttribute()
        lineWidthAttr     = OpenMaya.MFnNumericAttribute()
        lineColorAttr     = OpenMaya.MFnNumericAttribute()
        DrawNodeDrawOverride.size            = sizeAttr.create("size", "sz", OpenMaya.MFnNumericData.kFloat, 0.15 )
        DrawNodeDrawOverride.keySize         = keySizeAttr.create("keyFrameSize", "ksz", OpenMaya.MFnNumericData.kFloat, 0.2 )
        DrawNodeDrawOverride.timeBuffer      = bufferAttr.create("timeBuffer", "tb", OpenMaya.MFnNumericData.kInt, 11)
        DrawNodeDrawOverride.dotColor        = dotColorAttr.create("dotColor", "dc", OpenMaya.MFnNumericData.k3Float, 0.0)
        DrawNodeDrawOverride.keyFrameColor   = keyFrameColorAttr.create("keyFrameColor", "kfc", OpenMaya.MFnNumericData.k3Float, 0.0)
        DrawNodeDrawOverride.lineWidth       = lineWidthAttr.create("lineWidth", "lw", OpenMaya.MFnNumericData.kFloat, 3.0)
        DrawNodeDrawOverride.lineColor       = lineColorAttr.create("lineColor", "lc", OpenMaya.MFnNumericData.k3Float, 0.0)
        sizeAttr.storable          = True
        keySizeAttr.storable       = True
        bufferAttr.storable        = True
        dotColorAttr.storable      = True
        keyFrameColorAttr.storable = True
        lineWidthAttr.storable     = True
        lineColorAttr.storable     = True
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.size)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.keySize)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.timeBuffer)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.dotColor)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.keyFrameColor)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.lineWidth)
        OpenMaya.MPxNode.addAttribute(DrawNodeDrawOverride.lineColor)

class DrawNodeData(OpenMaya.MUserData):
    def __init__(self):
        OpenMaya.MUserData.__init__(self, False) ## don't delete after draw
        self.name = None
        self.startFrame = 0
        self.endFrame = 0
        self.points= []

        self.dotColor = (1.0, 1.0, 0.0, 1.0)
        self.keyFrameColor = (1.0, 0.0, 0.0, 1.0)
        self.lineColor = (1.0, 0.0, 1.0, 1.0)
        self.lineWidth = None
        self.size      = None
        self.keySize   = None

class DrawNodeDrawOverride(OpenMayaRender.MPxDrawOverride):
    size          = None
    keySize       = None
    timeBuffer    = None
    dotColor      = None
    keyFrameColor = None
    lineWidth     = None
    lineColor     = None

    @staticmethod
    def creator(obj):
        return DrawNodeDrawOverride(obj)
 
    @staticmethod
    def draw(context, data):
        return
 
    def __init__(self, obj):
        OpenMayaRender.MPxDrawOverride.__init__(self, obj, DrawNodeDrawOverride.draw)

    def getDepNode(self, n):
        return OpenMaya.MGlobal.getSelectionListByName(n).getDependNode(0)

    def supportedDrawAPIs(self):
        ## this plugin supports both GL and DX
        return OpenMayaRender.MRenderer.kOpenGL | OpenMayaRender.MRenderer.kDirectX11 | OpenMayaRender.MRenderer.kOpenGLCoreProfile
 
    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        ## Retrieve data cache (create if does not exist)
        data = oldData
        if not isinstance(data, DrawNodeData):
            data = DrawNodeData()

        mtObj = self.getDepNode(str(objPath))
        objMfn = OpenMaya.MFnDependencyNode(mtObj)
        data.name = objMfn.findPlug('nodeName', False).asString()
        data.startFrame = objMfn.findPlug('startTime', False).asInt()
        data.endFrame = objMfn.findPlug('endTime', False).asInt()

        points = {}
        thisNode   = objPath.node()
        timeBufferPlug   = OpenMaya.MPlug(thisNode, DrawNodeDrawOverride.timeBuffer)
        timeBuffer = timeBufferPlug.asInt()
        
        keyFrames = []
        if cmds.keyframe(data.name, q = True, tc = True):
            keyFrames  = list(set(cmds.keyframe(data.name, q = True, tc = True)))
            keyFrames  = [int(x) for x in keyFrames]

        currentTime = OpenMayaAnim.MAnimControl.currentTime()
        selection = OpenMaya.MSelectionList()
        selection.add(data.name)
        selectedNode = selection.getDependNode(0)
        fnThisNode = OpenMaya.MFnDependencyNode(selectedNode)
        worldMatrixAttr = fnThisNode.attribute("worldMatrix")
        pointPlug = OpenMaya.MPlug(selectedNode, worldMatrixAttr)
        pointPlug = pointPlug.elementByLogicalIndex(0)

        activeCam = util.getCam()
        for i in range(int(currentTime.value - timeBuffer), int(currentTime.value + timeBuffer + 1)):
            #Get matrix plug as MObject so we can get it's data.
            timeContext = OpenMaya.MDGContext(OpenMaya.MTime(i))
            pointObject = pointPlug.asMObject(timeContext)
            
            #Finally get the data
            worldMatrixData = OpenMaya.MFnMatrixData(pointObject)
            pointMMatrix = worldMatrixData.matrix()
            relativePoint = util.makeCameraRelative(pointMMatrix, activeCam, i)   

            if i in keyFrames:
                points[i] = (relativePoint, 1)
            else:
                points[i] = (relativePoint, 0)
        
        dotColorPlug      = OpenMaya.MPlug(thisNode, DrawNodeDrawOverride.dotColor)
        keyFrameColorPlug = OpenMaya.MPlug(thisNode, DrawNodeDrawOverride.keyFrameColor)
        lineColorPlug     = OpenMaya.MPlug(thisNode, DrawNodeDrawOverride.lineColor)
        sizePlug      = OpenMaya.MPlug(thisNode, DrawNodeDrawOverride.size)
        keySizePlug   = OpenMaya.MPlug(thisNode, DrawNodeDrawOverride.keySize)
        lineWidthPlug = OpenMaya.MPlug(thisNode, DrawNodeDrawOverride.lineWidth)    

        dotColor = (dotColorPlug.child(0).asFloat(), dotColorPlug.child(1).asFloat(), dotColorPlug.child(2).asFloat(), 1.0)
        keyFrameColor = (keyFrameColorPlug.child(0).asFloat(), keyFrameColorPlug.child(1).asFloat(), keyFrameColorPlug.child(2).asFloat(), 1.0)
        lineColor = (lineColorPlug.child(0).asFloat(), lineColorPlug.child(1).asFloat(), lineColorPlug.child(2).asFloat(), 1.0)

        data.dotColor      = OpenMaya.MColor(dotColor)
        data.lineColor     = OpenMaya.MColor(lineColor)
        data.keyFrameColor = OpenMaya.MColor(keyFrameColor) 

        data.points = points
        allFrames = data.points.keys()
        allFrames.sort()
        
        #making dot absolute value
        point     = data.points[allFrames[0]][0]
        sizeFactor = util.getDistance(point, activeCam)/1500
        
        data.size       = sizeFactor * round(sizePlug.asFloat(), 2)
        data.keySize    = sizeFactor * round(keySizePlug.asFloat(), 2)
        data.lineWidth  = round(lineWidthPlug.asFloat(), 2) 
        
        return data
 
    def hasUIDrawables(self):
        return True
 
    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        locatordata = data
        if not isinstance(locatordata, DrawNodeData):
            return
        drawManager.beginDrawable()
        drawManager.setDepthPriority(10000)

        prev = None
        allFrames = data.points.keys()
        allFrames.sort()

        for frame in allFrames:
            point     = data.points[frame][0]
            mpoint    = OpenMaya.MPoint(point[0], point[1], point[2], 1)

            if data.points[frame][1] == 1:
                #key frame
                drawManager.setColor(data.keyFrameColor)
                drawManager.sphere(mpoint, data.keySize, filled = True)
            else:
                drawManager.setColor(data.dotColor)
                drawManager.sphere(mpoint, data.size, filled = True)

            if prev:
                drawManager.setColor(data.lineColor)
                drawManager.setLineWidth(data.lineWidth)
                drawManager.line(prev, mpoint)
            prev = mpoint
            
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
        
    
    
    