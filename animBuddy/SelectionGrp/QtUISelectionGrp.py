# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
import maya.cmds as cmds 
import maya.mel as mel
import time 
import os

from animBuddy.FkIkMatch import Core
reload(Core)

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

        iconImagePath = os.path.join(imagesPath, 'close.png')
        iconHoverImagePath = os.path.join(imagesPath, 'close_hi.png')
        button = QtWidgets.QPushButton('')
        button.clicked.connect(cleanUI)
        button.setToolTip("asdf")
        button.setStyleSheet(
        '''
        QPushButton{image:url(%s); border:0px; width:%s; height:%s}
        QPushButton:hover{image:url(%s); border:0px;}
        QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
        ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
        )             
        button.show()
        mainLayout.addWidget(button)

def cleanUI(name = 'SelectionGrpToolbar'):

    wgtPtr = OpenMayaUI.MQtUtil.findControl(name)
    if wgtPtr:
        wgt = wrapInstance(long(wgtPtr), QtWidgets.QWidget)
        wgt.deleteLater()

def insertUI():

    ctrl = OpenMayaUI.MQtUtil.findControl('TimeSlider')
    ctrlWgt = wrapInstance(long(ctrl), QtWidgets.QWidget)
    
    x = ctrlWgt.parent().parent().parent()
    x.insertWidget(3, MToolBar(name = 'SelectionGrpToolbar'))# QSplitter [1,2,3,4,5,6,]

def main():
  
    cleanUI('SelectionGrpToolbar')
    insertUI()