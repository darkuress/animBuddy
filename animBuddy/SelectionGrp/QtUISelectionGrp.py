# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance
import maya.cmds as cmds 
import maya.mel as mel
import time 
import os
from functools import partial

from animBuddy.QtHelpers import Separator
reload(Separator)
from animBuddy.SelectionGrp import Core as SGP
reload(SGP)
import QtImportUI
reload(QtImportUI)

class MToolBar(QtWidgets.QWidget):

    def __init__(self, parent = None, name = None):
        super(MToolBar, self).__init__()

        self.SGP = SGP.SelectionGrp()

        filePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imagesPath = os.path.join(filePath, 'images')

        iconSize = 20

        self.setObjectName(name)

        self.setMinimumHeight(40)
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignRight) 
        self.setLayout(mainLayout)

        #- buttons layout
        self.buttonsLayout = QtWidgets.QHBoxLayout()

        #- add butotn
        iconImagePath = os.path.join(imagesPath, 'add.png').replace('\\', '/')
        iconHoverImagePath = os.path.join(imagesPath, 'add_hi.png').replace('\\', '/')
        buttonAdd = QtWidgets.QPushButton('')
        buttonAdd.clicked.connect(self.addDialog)
        buttonAdd.setToolTip("Close Toolbar")
        buttonAdd.setStyleSheet(
        '''
        QPushButton{image:url(%s); border:0px; width:%s; height:%s}
        QPushButton:hover{image:url(%s); border:0px;}
        QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
        ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
        )             
        buttonAdd.show()

        #- Import Export
        ioLayout = QtWidgets.QHBoxLayout()
        iconImagePath = os.path.join(imagesPath, 'savegrp.png').replace('\\', '/')
        iconHoverImagePath = os.path.join(imagesPath, 'savegrp_hi.png').replace('\\', '/')
        buttonExport = QtWidgets.QPushButton('')
        buttonExport.clicked.connect(self.exportToolbar)
        buttonExport.setToolTip("Export This Selection Group")
        buttonExport.setStyleSheet(
        '''
        QPushButton{image:url(%s); border:0px; width:%s; height:%s}
        QPushButton:hover{image:url(%s); border:0px;}
        QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
        ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
        )             
        buttonExport.show()

        iconImagePath = os.path.join(imagesPath, 'importgrp.png').replace('\\', '/')
        iconHoverImagePath = os.path.join(imagesPath, 'importgrp_hi.png').replace('\\', '/')
        buttonImport = QtWidgets.QPushButton('')
        buttonImport.clicked.connect(self.importToolbar)
        buttonImport.setToolTip("Import Selection Group")
        buttonImport.setStyleSheet(
        '''
        QPushButton{image:url(%s); border:0px; width:%s; height:%s}
        QPushButton:hover{image:url(%s); border:0px;}
        QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
        ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
        )             
        buttonImport.show()
        ioLayout.addWidget(buttonExport)
        ioLayout.addWidget(buttonImport)

        #- close toolbar
        iconImagePath = os.path.join(imagesPath, 'close.png').replace('\\', '/')
        iconHoverImagePath = os.path.join(imagesPath, 'close_hi.png').replace('\\', '/')
        button = QtWidgets.QPushButton('')
        button.clicked.connect(cleanUI)
        button.setToolTip("Close Toolbar")
        button.setStyleSheet(
        '''
        QPushButton{image:url(%s); border:0px; width:%s; height:%s}
        QPushButton:hover{image:url(%s); border:0px;}
        QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
        ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
        )             
        button.show()

        BuildButtons.buildButton(self.buttonsLayout)

        mainLayout.addLayout(self.buttonsLayout)
        mainLayout.addWidget(buttonAdd)
        mainLayout.addWidget(Separator.separator())
        mainLayout.addWidget(Separator.separator())
        mainLayout.addLayout(ioLayout)
        mainLayout.addWidget(button)

    def addDialog(self):
        if self.SGP.getSelection():
            text, okPressed = QtWidgets.QInputDialog.getText(self, "Adding Selection Group","Selection Group Name :", QtWidgets.QLineEdit.Normal, "")
            if okPressed and text != '':
                self.SGP.save(text)
                BuildButtons.buildButton(self.buttonsLayout)
            else:
                return

    def exportToolbar(self):
        """
        export current selection grp 
        """
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Exporting This Selectino Groups", "Enter Name : ", QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            # export
            self.SGP.export(text)

    def importToolbar(self):
        """
        opening import toolbar ui 
        """
        ui = QtImportUI.ImportUI()
        
        try:
            ui.create()
            ui.show()
        except:
            ui.deleteLater()

class BuildButtons():
    @staticmethod
    def buildButton(layout):
        sgp = SGP.SelectionGrp()
        #- delete layout first
        for i in reversed(range(layout.count())): 
            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

        allSelections = sgp.findSelections()

        for selection in allSelections:
            if sgp.findColor(selection):
                color = sgp.findColor(selection)
            else:
                color = [0.5, 0.5, 0.5]       

            button = SButton(parent    = layout, 
                             name      = selection, 
                             color     = color, 
                             selection = selection)
            button.addButton()        

class SButton(QtWidgets.QWidget):
    """
    selection group's button class
    """
    def __init__(self, parent, name, selection, color):
        """
        @param parent    : Qt Layout
        @param name      : str
        @param selection : str
        @param color     : [float, float, float]
        """
        super(SButton, self).__init__()

        self.SGP        = SGP.SelectionGrp()
        
        self._layout    = parent
        self._name      = name
        self._selection = selection
        self._color     = color

        self.button     = QtWidgets.QPushButton(self._name)

    def addButton(self):
        """
        create buttons for each selection group
        """
        color = [self._color[0]*255, self._color[1]*255, self._color[2]*255]
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.button.setStyleSheet("QPushButton{background-color: rgb(%s, %s, %s);}" %(color[0], color[1], color[2]))
        self.button.setToolTip('Opens color dialog') 
        self.button.clicked.connect(partial(self.select, self._selection))

        # ---- menuItem
        self.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.popupHandler)

        self.popupMenu = QtWidgets.QMenu()
        self.popupColor = self.popupMenu.addAction("Change color")
        self.popupAdd = self.popupMenu.addAction("Add to Selection")
        self.popupRemove = self.popupMenu.addAction("Remove from Selection")
        self.popupMenu.addSeparator()
        self.popupDelete = self.popupMenu.addAction("Delete")

        self._layout.addWidget(self.button)

        return self.button

    def popupHandler(self, position):

        action = self.popupMenu.exec_(self.button.mapToGlobal(position))  

        #- popup menus action
        if action == self.popupColor:
            self.color(self._selection)
        elif action == self.popupAdd:
            self.addToSelection(self._selection)
        elif action == self.popupRemove:
            self.removeFromSelection(self._selection)
        elif action == self.popupDelete:
            self.delete(self._selection)

    def select(self, selection):
        """
        select from button
        """
        self.SGP.select(selection)

    def addToSelection(self, selection):
        """
        """
        self.SGP.addToSelection(selection)
        BuildButtons.buildButton(self._layout)

    def removeFromSelection(self, selection):
        """
        """
        self.SGP.removeFromSelection(selection)
    
    def delete(self, selection):
        """
        delete button
        """
        self.SGP.deleteSelection(selection)
        BuildButtons.buildButton(self._layout)

    def color(self, selection):
        """
        change color of button
        """
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            colorRgb = color.getRgb()
            colorRgb = [round(colorRgb[0]/255.0, 3), round(colorRgb[1]/255.0, 3), round(colorRgb[2]/255.0, 3)]
            self.button.setStyleSheet("QPushButton{background-color: %s;}" %color.name())
        
        self.SGP.saveColor(selection, colorRgb)    

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

    if OpenMayaUI.MQtUtil.findControl("SelectionGrpToolbar"):
        cleanUI('SelectionGrpToolbar')
    else:
        insertUI()

def reopen():

    if OpenMayaUI.MQtUtil.findControl("SelectionGrpToolbar"):
        cleanUI('SelectionGrpToolbar')
        insertUI()