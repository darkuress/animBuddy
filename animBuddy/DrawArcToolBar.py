import maya.cmds as cmds
import os
from functools import partial
import Preference
reload(Preference)

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

        #Preference
        self.pref = Preference.Preference()

        self.win = cmds.window('DrawArcToolBar', width=500, title = 'MotionTrail Tool Option')
        self.frameLayoutMain = cmds.frameLayout(labelVisible = False, 
                                                w = 10, 
                                                borderVisible = False, 
                                                parent = self.win)
        self.rowLayoutMain = cmds.rowLayout(numberOfColumns = 2, 
                                            adjustableColumn = 1, 
                                            columnAttach = ([2, 'right', 0]), 
                                            parent = self.frameLayoutMain)
                
        cmds.rowLayout(numberOfColumns = 5)
        cmds.columnLayout(width = 200)#
        cmds.rowLayout(numberOfColumns = 2)
        cmds.text(label = "dot size", width = 160)
        self.textFieldDotSize = cmds.textField(text = self.pref.dotSize, 
                                               width = 40,
                                               cc = self.dotSizeCB)
        cmds.setParent("..")
        self.floatSliderDotSize = cmds.floatSlider(min = 0, 
                                                   max = 1, 
                                                   width = 200,
                                                   value = self.pref.dotSize, 
                                                   step = 0.01,
                                                   annotation = 'Dot Size of the MotionTrail.',
                                                   dc = self.dotSize)
        cmds.setParent("..")#

        cmds.columnLayout(width = 200)#
        cmds.rowLayout(numberOfColumns = 2)
        cmds.text(label = "keyframe size", width = 160)
        self.textFieldKeyFrameSize = cmds.textField(text = self.pref.keyFrameSize, 
                                                    width = 40,
                                                    cc = self.keyFrameSizeCB)
        cmds.setParent("..")
        self.floatSliderKeyFrameSize = cmds.floatSlider(min = 0, 
                                                        max = 1, 
                                                        width = 200,
                                                        value = self.pref.keyFrameSize, 
                                                        step = 0.01,
                                                        annotation = 'KeyFrame Size of the MotionTrail.',
                                                        dc = self.keyFrameSize)
        cmds.setParent("..")#

        cmds.columnLayout(width = 200)#
        cmds.rowLayout(numberOfColumns = 2)
        cmds.text(label = "time buffer size", width = 160)
        self.textFieldTimeBuffer = cmds.textField(text = self.pref.timeBuffer, 
                                                  width = 40, 
                                                  cc = self.timeBufferSizeCB)
        cmds.setParent("..")
        self.floatSliderTimeBufferSize = cmds.floatSlider(min = 0, 
                                                          max = 50, 
                                                          width = 200,
                                                          value = self.pref.timeBuffer, 
                                                          step = 1,
                                                          annotation = 'Time Buffer size.',
                                                          dc = self.timeBufferSize)
        cmds.setParent("..")#

        self.buttonSave = cmds.button(label = "Save as Default",
                                      c = self.saveAsDefault)

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
        value = cmds.floatSlider(self.floatSliderDotSize, q = True, v = True)
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.size', value)

        cmds.textField(self.textFieldDotSize, e = True, text = round(value, 2))

    def dotSizeCB(self, *args):
        """
        """
        value = cmds.textField(self.textFieldDotSize, q = True, text = True)
        cmds.floatSlider(self.floatSliderDotSize, e = True, v = float(value))

        self.dotSize()

    def keyFrameSize(self, *args):
        """
        """
        value = cmds.floatSlider(self.floatSliderKeyFrameSize, q = True, v = True)
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.ksz', value)

        cmds.textField(self.textFieldKeyFrameSize, e = True, text = round(value, 2))

    def keyFrameSizeCB(self, *args):
        """
        """
        value = cmds.textField(self.textFieldKeyFrameSize, q = True, text = True)
        cmds.floatSlider(self.floatSliderKeyFrameSize, e = True, v = float(int(value)))

        self.keyFrameSize()

    def timeBufferSize(self, *args):
        """
        """
        value = cmds.floatSlider(self.floatSliderTimeBufferSize, q = True, v = True)
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.tb', value)
        cmds.textField(self.textFieldTimeBuffer, e = True, text = round(value, 0))

    def timeBufferSizeCB(self, *args):
        """
        """
        value = cmds.textField(self.textFieldTimeBuffer, q = True, text = True)
        cmds.floatSlider(self.floatSliderTimeBufferSize, e = True, v = int(value))

        self.timeBufferSize()

    def saveAsDefault(self, *args):
        """
        """
        self.pref.dotSize = cmds.floatSlider(self.floatSliderDotSize, q = True, v = True)
        self.pref.keyFrameSize = cmds.floatSlider(self.floatSliderKeyFrameSize, q = True, v = True)
        self.pref.timeBuffer = cmds.floatSlider(self.floatSliderTimeBufferSize, q = True, v = True)

        self.pref.construct()
        self.pref.write()

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
