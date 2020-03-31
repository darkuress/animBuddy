# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
import maya.cmds as cmds 
import maya.mel as mel
import time 
import os

class MToolBar(QtWidgets.QWidget):

    def __init__(self, parent = None, name = None):
        super(MToolBar, self).__init__()

        filePath = os.path.dirname(os.path.abspath(__file__))
        self.imagesPath = os.path.join(filePath, "images")

        self.iconSize = 30
        self.height = 25
        self.marginSize = 0

        self.setObjectName(name)

        self.setMinimumHeight(40)
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        #logo
        self.logoLayout = QtWidgets.QHBoxLayout()
        self.logoLayout.setAlignment(QtCore.Qt.AlignLeft) 
        logoLabel = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(os.path.join(self.imagesPath, "beaverLogo.png"))
        logoLabel.setPixmap(pixmap)
        self.logoLayout.addWidget(logoLabel)

        #wigets layout
        self.widgetLayout = QtWidgets.QHBoxLayout()
        self.widgetLayout.setAlignment(QtCore.Qt.AlignRight)
        self.widgetLayout.setSpacing(5)
        
        self.mainLayout.addLayout(self.logoLayout)
        self.mainLayout.addLayout(self.widgetLayout)

        modules = ['Justin', 'Warrior', 'separator', 
                   'ShiftKey', 'MicroControl', 'separator', 
                   'EasyInBetween', 'separator',  
                   'MagicLocator', 'FakeConIt', 'ExFootStep', 'SnapIt', 'LockDown', 'vertical', 
                   'ResetIt', 'ViewportRefresh' ]
        for module in modules:
            self.addWidget(module)

    def addWidget(self, module):
        """
        """
        if module == 'separator':
            self.widgetLayout.addWidget(self.separator())
        elif module == 'vertical':
            self.widgetLayout.addWidget(self.separator(vertical = True))
        else:
            exec("from {} import QtWidget".format(module))
            exec("reload(QtWidget)")
            QtWidget.build(self.widgetLayout, 
                           self.imagesPath,
                           iconSize = self.iconSize,
                           height = self.height, 
                           marginSize = self.marginSize)

    def separator(self, vertical = False):
        """
        """
        if vertical:
            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.VLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        else:
            separator = QtWidgets.QSplitter() 
        
        separator.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        return separator
        
def cleanUI(name):

    wgtPtr = OpenMayaUI.MQtUtil.findControl(name)
    if wgtPtr:
        wgt = wrapInstance(long(wgtPtr), QtWidgets.QWidget)
        wgt.deleteLater()

def insertUI():

    ctrl = OpenMayaUI.MQtUtil.findControl('TimeSlider')
    ctrlWgt = wrapInstance(long(ctrl), QtWidgets.QWidget)
    
    x = ctrlWgt.parent().parent().parent()
    x.insertWidget(3, MToolBar(name = 'AnimBuddyWindow'))# QSplitter [1,2,3,4,5,6,]

def main():
  
    cleanUI('AnimBuddyWindow')
    insertUI()