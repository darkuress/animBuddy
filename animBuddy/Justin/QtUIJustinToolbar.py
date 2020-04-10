# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
import maya.cmds as cmds 
import maya.mel as mel
import time 
import os

import FkIkMatch
reload(FkIkMatch)

class MToolBar(QtWidgets.QWidget):

    def __init__(self, parent = None, name = None):
        super(MToolBar, self).__init__()

        filePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imagesPath = os.path.join(filePath, 'images')

        iconSize = 30
        marginSize = 0

        self.setObjectName(name)

        self.setMinimumHeight(40)
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignRight) 
        self.setLayout(mainLayout)

        iconImagePath = os.path.join(imagesPath, 'close.png').replace('\\', '/')
        iconHoverImagePath = os.path.join(imagesPath, 'close_hi.png').replace('\\', '/')

        #- FKIK button
        self.fkikLayout = QtWidgets.QHBoxLayout()
        buttonFkIk = QtWidgets.QPushButton('FKIK')
        buttonFkIk.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        buttonFkIk.setMinimumHeight(20)
        buttonFkIk.setMinimumWidth(50)
        buttonFkIk.setStyleSheet(
        '''
        QPushButton{background-color: #3A506B; padding : 3px; 
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 6px;
                    border-color: #2D6060;}
        QPushButton:hover{background-color: #1C2541;}
        QPushButton:pressed { background-color: #0B132B;}
        '''   
        )
        font = QtGui.QFont('Monaco', 9, QtGui.QFont.Light)
        font.setBold(True)
        font.setPointSize(12)
        buttonFkIk.setFont(font)
        buttonFkIk.setToolTip('FKIK switch')
        buttonFkIk.clicked.connect(self.fkikSwitch)
        buttonFkIk.show() 

        #----fkik bake option
        self.checkboxBake = QtWidgets.QCheckBox("Bake",self)
        self.checkboxBake.stateChanged.connect(self.isBake)

        #----bake frame
        self.qLineEditStartFrame = QtWidgets.QLineEdit()
        self.qLineEditStartFrame.setFixedWidth(60)
        self.qLineEditStartFrame.setFixedHeight(25)
        self.qLineEditStartFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.qLineEditStartFrame.setText(str(cmds.playbackOptions(minTime = True, q = True)))
        self.qLineEditStartFrame.setAlignment(QtCore.Qt.AlignCenter)  
        self.qLineEditStartFrame.setToolTip('Start Frame')
        self.qLineEditStartFrame.setStyleSheet(
        '''
        QLineEdit { background-color: #333333; }
        '''   
        )
        self.qLineEditStartFrame.setEnabled(False)

        self.qLineEditEndFrame = QtWidgets.QLineEdit()
        self.qLineEditEndFrame.setFixedWidth(60)
        self.qLineEditEndFrame.setFixedHeight(25)
        self.qLineEditEndFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.qLineEditEndFrame.setText(str(cmds.playbackOptions(maxTime = True, q = True)))
        self.qLineEditEndFrame.setAlignment(QtCore.Qt.AlignCenter)  
        self.qLineEditEndFrame.setToolTip('End Frame')
        self.qLineEditEndFrame.setStyleSheet(
        '''
        QLineEdit { background-color: #333333; }
        '''   
        )
        self.qLineEditEndFrame.setEnabled(False)

        self.fkikLayout.addWidget(buttonFkIk)
        self.fkikLayout.addWidget(self.checkboxBake)
        self.fkikLayout.addWidget(self.qLineEditStartFrame)
        self.fkikLayout.addWidget(self.qLineEditEndFrame)


        #- close button
        buttonClose = QtWidgets.QPushButton('')
        buttonClose.clicked.connect(cleanUI)
        buttonClose.setToolTip("Close Toolbar")
        buttonClose.setStyleSheet(
        '''
        QPushButton{image:url(%s); border:0px; width:%s; height:%s}
        QPushButton:hover{image:url(%s); border:0px;}
        QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
        ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
        )             
        buttonClose.show()


        mainLayout.addLayout(self.fkikLayout)
        mainLayout.addWidget(self.separator())
        mainLayout.addWidget(buttonClose)

    def isBake(self):
        result = False
        if self.checkboxBake.isChecked():
            result = True
        
        if result:
            self.qLineEditStartFrame.setEnabled(True)
            self.qLineEditEndFrame.setEnabled(True)
        else:
            self.qLineEditStartFrame.setEnabled(False)
            self.qLineEditEndFrame.setEnabled(False)            

    def separator(self):
        """
        vertical separator
        """
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        return separator

    def fkikSwitch(self, *args):
        """
        """
        bake = False
        if self.checkboxBake.isChecked():
            bake = True
        if bake:
            startFrame = int(float(self.qLineEditStartFrame.text()))
            endFrame = int(float(self.qLineEditEndFrame.text()))
            FkIkMatch.bake(frame = [startFrame, endFrame])
        else:
            FkIkMatch.convert(prefix = FkIkMatch.getPrefix(), side = FkIkMatch.getSide())

def cleanUI(name = 'JustinToolbar'):

    wgtPtr = OpenMayaUI.MQtUtil.findControl(name)
    if wgtPtr:
        wgt = wrapInstance(long(wgtPtr), QtWidgets.QWidget)
        wgt.deleteLater()

def insertUI():

    ctrl = OpenMayaUI.MQtUtil.findControl('TimeSlider')
    ctrlWgt = wrapInstance(long(ctrl), QtWidgets.QWidget)
    
    x = ctrlWgt.parent().parent().parent()
    x.insertWidget(3, MToolBar(name = 'JustinToolbar'))# QSplitter [1,2,3,4,5,6,]

def main():
    if OpenMayaUI.MQtUtil.findControl("JustinToolbar"):
        cleanUI('JustinToolbar')
    else:
        insertUI()