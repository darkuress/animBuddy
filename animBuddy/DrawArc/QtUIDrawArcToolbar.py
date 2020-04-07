# -*- coding: utf-8 -*-
import maya.OpenMayaUI as OpenMayaUI
from functools import partial
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.cmds as cmds 
import maya.mel as mel
import time 
import os

from animBuddy.FkIkMatch import Core
reload(Core)
from animBuddy.QtHelpers import ASlider
reload(ASlider)
from animBuddy.QtHelpers import CSlider
reload(CSlider)
from animBuddy import Preference
reload(Preference)
from animBuddy.QtHelpers import Separator
reload(Separator)

class MToolBar(QtWidgets.QWidget):

    def __init__(self, parent = None, name = None):
        super(MToolBar, self).__init__()

        filePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imagesPath = os.path.join(filePath, 'images')

        iconSize = 30

        self.pref = Preference.Preference()
        self.setObjectName(name)

        self.setMinimumHeight(40)
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignRight) 
        self.setLayout(mainLayout)

        #- Line Width
        lineLayout = QtWidgets.QHBoxLayout()
        labelline = QtWidgets.QLabel()
        labelline.setText('Line ')
        buttonLine = self.createButton(attr = 'line', color = self.pref.lineColor)
        buttonLine.show()
        self.sliderLine = ASlider.ASlider(colorEnum = "pgreen", 
                                          width = 150, 
                                          height = 15,
                                          handleSticked = False, 
                                          presetsShow = False,
                                          minValue=0, 
                                          maxValue=20, 
                                          startValue=self.pref.lineWidth, 
                                          presetsStep=1,
                                          trail = False,)
        self.sliderLine.valueChanged.connect(self.lineWidthCB)
        lineLayout.addWidget(labelline)
        lineLayout.addWidget(buttonLine)
        lineLayout.addWidget(self.sliderLine)

        #- Dot size
        dotLayout = QtWidgets.QHBoxLayout()
        labelDot = QtWidgets.QLabel()
        labelDot.setText(' Dot ')
        buttonDot = self.createButton(attr = 'dot', color = self.pref.dotColor)
        buttonDot.show()
        self.sliderDot = ASlider.ASlider(colorEnum = "pgreen", 
                                         width = 150, 
                                         height = 15,
                                         handleSticked = False, 
                                         presetsShow = False,
                                         minValue=0, 
                                         maxValue=20, 
                                         startValue=self.pref.dotSize, 
                                         presetsStep=1,
                                         trail = False,)
        self.sliderDot.valueChanged.connect(self.dotSizeCB)
        dotLayout.addWidget(labelDot)
        dotLayout.addWidget(buttonDot)
        dotLayout.addWidget(self.sliderDot)        

        #- Keyframe size
        keyframeLayout = QtWidgets.QHBoxLayout()
        labelKeyframe = QtWidgets.QLabel()
        labelKeyframe.setText(' Keyframe ')
        buttonKeyframe = self.createButton(attr = 'keyFrame', color = self.pref.keyFrameColor)
        buttonKeyframe.show()
        self.sliderKeyframe = ASlider.ASlider(colorEnum = "pgreen", 
                                              width = 150, 
                                              height = 15,
                                              handleSticked = False, 
                                              presetsShow = False,
                                              minValue=0, 
                                              maxValue=20, 
                                              startValue=self.pref.keyFrameSize, 
                                              presetsStep=1,
                                              trail = False,)
        self.sliderKeyframe.valueChanged.connect(self.keyframeSizeCB)
        keyframeLayout.addWidget(labelKeyframe)
        keyframeLayout.addWidget(buttonKeyframe)
        keyframeLayout.addWidget(self.sliderKeyframe)   

        #- Timebuffer size
        timebufferLayout = QtWidgets.QHBoxLayout()
        labelTimebuffer = QtWidgets.QLabel()
        labelTimebuffer.setText('Timebuffer ')
        buttonTimebuffer = self.createButton(attr = 'traveler', color = self.pref.timeBufferColor)
        buttonTimebuffer.show()
        self.sliderTimebuffer = CSlider.CSlider(colorEnum = "pgreen", 
                                                width = 150,
                                                height = 15, 
                                                handleSticked = False, 
                                                presetsShow = False,
                                                minValue=0, 
                                                maxValue=20, 
                                                startValue=self.pref.timeBuffer, 
                                                presetsStep=1,
                                                trail = False,)
        self.sliderTimebuffer.valueChanged.connect(self.timeBufferCB)
        timebufferLayout.addWidget(labelTimebuffer)
        timebufferLayout.addWidget(buttonTimebuffer)
        timebufferLayout.addWidget(self.sliderTimebuffer)   

        #- Style
        comboBoxStyle = QtWidgets.QComboBox(self)
        comboBoxStyle.addItem("Single")
        comboBoxStyle.addItem("Double")
        comboBoxStyle.activated[str].connect(self.styleCB)   
        index = comboBoxStyle.findText(self.pref.mtStyle, QtCore.Qt.MatchFixedString)
        if index >= 0:
            comboBoxStyle.setCurrentIndex(index)

        mainLayout.addLayout(lineLayout)
        mainLayout.addWidget(Separator.separator(vertical = True))
        mainLayout.addLayout(dotLayout)
        mainLayout.addWidget(Separator.separator(vertical = True))
        mainLayout.addLayout(keyframeLayout)
        mainLayout.addWidget(Separator.separator(vertical = True))
        mainLayout.addLayout(timebufferLayout)
        mainLayout.addWidget(Separator.separator(vertical = True))
        mainLayout.addWidget(comboBoxStyle)

        # close button
        iconImagePath = os.path.join(imagesPath, 'close.png')
        iconHoverImagePath = os.path.join(imagesPath, 'close_hi.png')
        button = QtWidgets.QPushButton('')
        button.clicked.connect(cleanUI)
        button.setToolTip("Closing Toolbar")
        button.setStyleSheet(
        '''
        QPushButton{image:url(%s); border:0px; width:%s; height:%s}
        QPushButton:hover{image:url(%s); border:0px;}
        QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
        ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
        )             
        button.show()
        mainLayout.addWidget(button)

    def createButton(self, attr = 'line', color = [1, 1, 1]):
        """
        creating qt button
        """
        color = [color[0]*255, color[1]*255, color[2]*255]
        button = QtWidgets.QPushButton('')
        button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button.setMaximumHeight(10)
        button.setMaximumWidth(15)
        button.setStyleSheet("QPushButton{background-color: rgb(%s, %s, %s);}" %(color[0], color[1], color[2]))
        button.setToolTip('Opens color dialog') 
        button.clicked.connect(partial(self.openColorDialog, button, attr))

        return button

    def editButton(self, button, attr, color):
        """
        """
        button.setStyleSheet("QPushButton{background-color: %s;}" %color.name())
        colorRgb = color.getRgb()
        colorRgb = [round(colorRgb[0]/255.0, 3), round(colorRgb[1]/255.0, 3), round(colorRgb[2]/255.0, 3)]
        self.changeColor(attr, colorRgb)

    def openColorDialog(self, button, attr):
        """
        """
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.editButton(button, attr, color)
            return color

    def changeColor(self, attr, color):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.%sColor0' %attr, color[0])
                cmds.setAttr(mt + '.%sColor1' %attr, color[1])
                cmds.setAttr(mt + '.%sColor2' %attr, color[2])
        
        if attr == 'line':
            self.pref.lineColor = color
        elif attr == 'dot':
            self.pref.dotColor = color
        elif attr == 'keyFrame':
            self.pref.keyFrameColor = color
        elif attr == 'traveler':
            self.pref.timeBufferColor = color
        self.saveAsDefault()

    def allMotionTrails(self):
        """
        return all motion trails
        """
        return cmds.ls(type = "DrawNode")

    def lineWidthCB(self, value):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.lineWidth', round(value, 2))
        
        # save value as preference
        self.pref.lineWidth = round(value, 2)
        self.saveAsDefault()

    def dotSizeCB(self, value):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.size', round(value, 2))

        # save value as preference
        self.pref.dotSize = round(value, 2)
        self.saveAsDefault()

    def keyframeSizeCB(self, value):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.keyFrameSize', round(value, 2))

        # save value as preference
        self.pref.keyFrameSize = round(value, 2)
        self.saveAsDefault()

    def timeBufferCB(self, value):
        """
        """
        if self.allMotionTrails():
            for mt in self.allMotionTrails():
                cmds.setAttr(mt + '.tb', int(round(value, 2)))

        # save value as preference
        self.pref.timeBuffer = round(value, 2)
        self.saveAsDefault()

    def styleCB(self, value):
        """
        """
        for mt in self.allMotionTrails():
            if value == 'Double':
                cmds.setAttr(mt + '.mode', 1)
            elif value == 'Single':
                cmds.setAttr(mt + '.mode', 2)
        
        # save value as preference
        self.pref.mtStyle = value
        self.saveAsDefault()


    def saveAsDefault(self, *args):
        """
        """
        """
        self.pref.lineColor         = cmds.button(self.buttonLineColor, q = True, backgroundColor = True) 
        self.pref.lineColor         = [round(x, 2) for x in self.pref.lineColor]
        self.pref.dotColor          = cmds.button(self.buttonDotColor, q = True, backgroundColor = True) 
        self.pref.dotColor          = [round(x, 2) for x in self.pref.dotColor]
        self.pref.keyFrameColor     = cmds.button(self.buttonKeyFrameColor, q = True, backgroundColor = True) 
        self.pref.keyFrameColor     = [round(x, 2) for x in self.pref.keyFrameColor]
        self.pref.timeBufferColor     = cmds.button(self.buttonTimeBufferColor, q = True, backgroundColor = True) 
        self.pref.timeBufferColor     = [round(x, 2) for x in self.pref.timeBufferColor]
        """
        self.pref.construct()
        self.pref.write()

def cleanUI(name = 'DrawArcToolbar'):

    wgtPtr = OpenMayaUI.MQtUtil.findControl(name)
    if wgtPtr:
        wgt = wrapInstance(long(wgtPtr), QtWidgets.QWidget)
        wgt.deleteLater()

def insertUI():

    ctrl = OpenMayaUI.MQtUtil.findControl('TimeSlider')
    ctrlWgt = wrapInstance(long(ctrl), QtWidgets.QWidget)
    
    x = ctrlWgt.parent().parent().parent()
    x.insertWidget(3, MToolBar(name = 'DrawArcToolbar'))# QSplitter [1,2,3,4,5,6,]

def main():
  
    cleanUI('DrawArcToolbar')
    insertUI()