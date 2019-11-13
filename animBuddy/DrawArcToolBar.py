import maya.cmds as cmds
import os
from functools import partial

#- initialize window
if cmds.window('DrawArcToolBar', ex = True):
    cmds.deleteUI('DrawArcToolBar')    
try:
    cmds.deleteUI('daToolbar')   
except:
    pass 
    
class DrawArcToolBar:
    """
    """
    def __init__(self):
        """
        initializing ui
        """
        filePath = os.path.dirname(os.path.abspath(__file__))
        imagesPath = os.path.join(filePath, 'images')
        iconSize = 22
        marginSize = 5
               
        self.win = cmds.window('DrawArcToolBar', width=500, title = 'MotionTrail Tool Option')
        self.frameLayoutMain = cmds.frameLayout(labelVisible = False, 
                                                w = 10, 
                                                borderVisible = False, 
                                                parent = self.win)
        self.rowLayoutMain = cmds.rowLayout(numberOfColumns = 2, 
                                            adjustableColumn = 1, 
                                            columnAttach = ([2, 'right', 0]), 
                                            parent = self.frameLayoutMain)
                
        cmds.rowLayout(numberOfColumns = 4)
        cmds.columnLayout(width = 200)#
        cmds.text(label = "dot size")
        self.floatSliderDotSize = cmds.floatSlider(min = 0, 
                                                   max = 1, 
                                                   width = 200,
                                                   value = 0.2, 
                                                   step = 0.01,
                                                   annotation = 'Dot Size of the MotionTrail.',
                                                   dc = self.dotSize)
        cmds.setParent("..")#

        cmds.columnLayout(width = 200)#
        cmds.text(label = "keyframe size")
        self.floatSliderKeyFrameSize = cmds.floatSlider(min = 0, 
                                                        max = 1, 
                                                        width = 200,
                                                        value = 0.2, 
                                                        step = 0.01,
                                                        annotation = 'KeyFrame Size of the MotionTrail.',
                                                        dc = self.keyFrameSize)
        cmds.setParent("..")#

        cmds.columnLayout(width = 200)#
        cmds.text(label = "time buffer size")
        self.floatSliderTimeBufferSize = cmds.floatSlider(min = 0, 
                                                          max = 50, 
                                                          width = 200,
                                                          value = 10, 
                                                          step = 1,
                                                          annotation = 'Time Buffer size.',
                                                          dc = self.timeBufferSize)
        cmds.setParent("..")#

        self.buttonClose = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'close.png'), 
                                               hi = os.path.join(imagesPath, 'close_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'close',
                                               annotation = 'Closing Selection ToolBar', 
                                               c = self.close) 
        cmds.setParent("..")

    def allMotionTrails(self):
        """
        return all motion trails
        """
        return cmds.ls(type = "DrawNode")

    def dotSize(self, *args):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                value = cmds.floatSlider(self.floatSliderDotSize, q = True, v = True)
                cmds.setAttr(mt + '.size', value)

    def keyFrameSize(self, *args):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                value = cmds.floatSlider(self.floatSliderKeyFrameSize, q = True, v = True)
                cmds.setAttr(mt + '.ksz', value)

    def timeBufferSize(self, *args):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                value = cmds.floatSlider(self.floatSliderTimeBufferSize, q = True, v = True)
                cmds.setAttr(mt + '.tb', value)

    def close(self, *args):
        """
        """
        try:
            cmds.deleteUI('daToolbar')   
        except:
            pass     
            
    def loadInMaya(self, *args):
        """
        """
        #cmds.showWindow(self.win)
        allowedAreas = ['top', 'bottom']
        sgToolBar = cmds.toolBar('daToolbar', area='bottom', content=self.win, allowedArea=allowedAreas )
