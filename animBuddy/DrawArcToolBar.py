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
        iconSize = 25
        marginSize = 0

        #Preference
        self.pref = Preference.Preference()

        self.win = cmds.window('DrawArcToolBar', width=500, title = 'MotionTrail Tool Option')
        self.frameLayoutMain = cmds.frameLayout(labelVisible = False, 
                                                w = 10, 
                                                borderVisible = False, 
                                                parent = self.win)
        self.rowLayoutMain = cmds.rowLayout(numberOfColumns = 3, 
                                            adjustableColumn = 1, 
                                            columnAttach = ([1, 'right', 0]), 
                                            parent = self.frameLayoutMain)  
        cmds.rowLayout(numberOfColumns = 5)###    
        cmds.columnLayout(width = 200)##
        cmds.rowLayout(numberOfColumns = 3)#
        self.buttonLineColor = cmds.button(width = 15,
                                           height = 15, 
                                           label = '', 
                                           backgroundColor = self.pref.lineColor, 
                                           c = self.lineColor)
        cmds.text(label = "line width", width = 130)
        self.textFieldLineWidth = cmds.textField(text = round(self.pref.lineWidth, 2), 
                                                 width = 40,
                                                 cc = self.lineWidthCB)
        cmds.setParent("..")#
        self.floatSliderLineWidth = cmds.floatSlider(min = 0, 
                                                    max = 20, 
                                                    width = 200,
                                                    value = self.pref.lineWidth, 
                                                    step = 0.1,
                                                    annotation = 'Line Width of the MotionTrail.',
                                                    dc = self.lineWidth)
        cmds.setParent("..")##

        cmds.columnLayout(width = 200)##
        cmds.rowLayout(numberOfColumns = 3)#
        self.buttonDotColor = cmds.button(width = 15,
                                          height = 15, 
                                          label = '', 
                                          backgroundColor = self.pref.dotColor, 
                                          c = self.dotColor)
        cmds.text(label = "dot size", width = 130)
        self.textFieldDotSize = cmds.textField(text = round(self.pref.dotSize, 2), 
                                               width = 40,
                                               cc = self.dotSizeCB)
        cmds.setParent("..")#
        self.floatSliderDotSize = cmds.floatSlider(min = 0, 
                                                   max = 20, 
                                                   width = 200,
                                                   value = self.pref.dotSize, 
                                                   step = 0.01,
                                                   annotation = 'Dot Size of the MotionTrail.',
                                                   dc = self.dotSize)
        cmds.setParent("..")##
        
        cmds.columnLayout(width = 200)##
        cmds.rowLayout(numberOfColumns = 3)#
        self.buttonKeyFrameColor = cmds.button(width = 15,
                                               height = 15, 
                                               label = '', 
                                               backgroundColor = self.pref.keyFrameColor, 
                                               c = self.keyFrameColor)
        cmds.text(label = "keyframe size", width = 130)
        self.textFieldKeyFrameSize = cmds.textField(text = round(self.pref.keyFrameSize, 2), 
                                                    width = 40,
                                                    cc = self.keyFrameSizeCB)
        cmds.setParent("..")#
        self.floatSliderKeyFrameSize = cmds.floatSlider(min = 0, 
                                                        max = 20, 
                                                        width = 200,
                                                        value = self.pref.keyFrameSize, 
                                                        step = 0.01,
                                                        annotation = 'KeyFrame Size of the MotionTrail.',
                                                        dc = self.keyFrameSize)
        cmds.setParent("..")##

        cmds.columnLayout(width = 200)##
        cmds.rowLayout(numberOfColumns = 3)#
        self.buttonTimeBufferColor = cmds.button(width = 15,
                                                  height = 15, 
                                                  label = '', 
                                                  backgroundColor = self.pref.timeBufferColor, 
                                                  c = self.timeBufferColor)
        cmds.text(label = "timebuffer size", width = 140)
        self.textFieldTimeBuffer = cmds.textField(text = round(self.pref.timeBuffer, 0), 
                                                  width = 40, 
                                                  cc = self.timeBufferSizeCB)
        cmds.setParent("..")#
        self.floatSliderTimeBufferSize = cmds.floatSlider(min = 0, 
                                                          max = 50, 
                                                          width = 200,
                                                          value = self.pref.timeBuffer, 
                                                          step = 1,
                                                          annotation = 'Time Buffer size.',
                                                          dc = self.timeBufferSize)
        cmds.setParent("..")##
        cmds.setParent("..")###

        cmds.rowLayout(numberOfColumns = 5)
        cmds.separator(hr= False, height = 10, width = 10, style = "none")
        self.buttonSave = cmds.button(label = "Save as Default",
                                      c = self.saveAsDefault)
        cmds.separator(hr= False, height = 10, width = 10, style = "none")
        self.buttonClose = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'close.png'), 
                                               hi = os.path.join(imagesPath, 'close_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'close',
                                               annotation = 'Closing Selection ToolBar', 
                                               c = self.close) 

        

    def allMotionTrails(self):
        """
        return all motion trails
        """
        return cmds.ls(type = "DrawNode")

    def color(self, button, *args):
        """
        change color of button
        """
        result = cmds.colorEditor()
        color = result.split(" ")
        color = [float(x) for x in color if x]
        color = color[:-1]
        
        cmds.button(button, e = True, backgroundColor = color)

        return color

    def lineWidth(self, *args):
        """
        """
        value = cmds.floatSlider(self.floatSliderLineWidth, q = True, v = True)
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.lineWidth', round(value, 2))

        cmds.textField(self.textFieldLineWidth, e = True, text = round(value, 2))

    def lineWidthCB(self, *args):
        """
        change line width of motion trail
        """
        value = cmds.textField(self.textFieldLineWidth, q = True, text = True)
        cmds.floatSlider(self.floatSliderLineWidth, e = True, v = float(value))

        self.lineWidth()

    def lineColor(self, *args):
        """
        """
        color = self.color(self.buttonLineColor)

        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.lineColor0', color[0])
                cmds.setAttr(mt + '.lineColor1', color[1])
                cmds.setAttr(mt + '.lineColor2', color[2])
                
    def dotSize(self, *args):
        """
        """
        value = cmds.floatSlider(self.floatSliderDotSize, q = True, v = True)
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.size', round(value, 2))

        cmds.textField(self.textFieldDotSize, e = True, text = round(value, 2))

    def dotSizeCB(self, *args):
        """
        """
        value = cmds.textField(self.textFieldDotSize, q = True, text = True)
        cmds.floatSlider(self.floatSliderDotSize, e = True, v = float(value))

        self.dotSize()

    def dotColor(self, *args):
        """
        """
        color = self.color(self.buttonDotColor)

        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.dotColor0', color[0])
                cmds.setAttr(mt + '.dotColor1', color[1])
                cmds.setAttr(mt + '.dotColor2', color[2])

    def keyFrameSize(self, *args):
        """
        """
        value = cmds.floatSlider(self.floatSliderKeyFrameSize, q = True, v = True)
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.ksz', round(value, 2))

        cmds.textField(self.textFieldKeyFrameSize, e = True, text = round(value, 2))

    def keyFrameSizeCB(self, *args):
        """
        """
        value = cmds.textField(self.textFieldKeyFrameSize, q = True, text = True)
        cmds.floatSlider(self.floatSliderKeyFrameSize, e = True, v = float(int(value)))

        self.keyFrameSize()

    def keyFrameColor(self, *args):
        """
        """
        color = self.color(self.buttonKeyFrameColor)

        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.keyFrameColor0', color[0])
                cmds.setAttr(mt + '.keyFrameColor1', color[1])
                cmds.setAttr(mt + '.keyFrameColor2', color[2])

    def timeBufferSize(self, *args):
        """
        """
        value = cmds.floatSlider(self.floatSliderTimeBufferSize, q = True, v = True)
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.tb', int(round(value, 2)))
        cmds.textField(self.textFieldTimeBuffer, e = True, text = round(value, 0))

    def timeBufferSizeCB(self, *args):
        """
        """
        value = cmds.textField(self.textFieldTimeBuffer, q = True, text = True)
        cmds.floatSlider(self.floatSliderTimeBufferSize, e = True, v = int(value))

        self.timeBufferSize()

    def timeBufferColor(self, *args):
        """
        """
        color = self.color(self.buttonTimeBufferColor)

        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.travelerColor0', color[0])
                cmds.setAttr(mt + '.travelerColor1', color[1])
                cmds.setAttr(mt + '.travelerColor2', color[2])

    def saveAsDefault(self, *args):
        """
        """
        self.pref.lineWidth         = round(cmds.floatSlider(self.floatSliderLineWidth, q = True, v = True), 2)
        self.pref.dotSize           = round(cmds.floatSlider(self.floatSliderDotSize, q = True, v = True), 2)
        self.pref.keyFrameSize      = round(cmds.floatSlider(self.floatSliderKeyFrameSize, q = True, v = True), 2)
        self.pref.timeBuffer        = round(cmds.floatSlider(self.floatSliderTimeBufferSize, q = True, v = True), 0)
        self.pref.lineColor         = cmds.button(self.buttonLineColor, q = True, backgroundColor = True) 
        self.pref.lineColor         = [round(x, 2) for x in self.pref.lineColor]
        self.pref.dotColor          = cmds.button(self.buttonDotColor, q = True, backgroundColor = True) 
        self.pref.dotColor          = [round(x, 2) for x in self.pref.dotColor]
        self.pref.keyFrameColor     = cmds.button(self.buttonKeyFrameColor, q = True, backgroundColor = True) 
        self.pref.keyFrameColor     = [round(x, 2) for x in self.pref.keyFrameColor]

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
