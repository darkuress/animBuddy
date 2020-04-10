import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from animBuddy import Preference
from functools import partial
import Core
reload(Core)

class UIData():
    """
    """
    button = None
    popupMenu = None
    menuPose = None
    menuAnim = None
    pref = None

def build(parent, 
          imagesPath, 
          iconSize = 25,
          height = 20, 
          marginSize = 5):
    """
    build widget
    @param parent : parent qt layout
    @imagesPath : str path
    """
    #- Decalcomanie---------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'decalcomanie.png').replace('\\', '/')
    iconHoverImagePath = os.path.join(imagesPath, 'decalcomanie_hi.png').replace('\\', '/')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(run)
    UIData.button.setToolTip("Copy Left or Right anim to Right or Left")
    UIData.button.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )            

    # ---- menuItem
    UIData.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    UIData.button.customContextMenuRequested.connect(popupHandler)
    UIData.popupMenu = QtWidgets.QMenu()
    ag = QtWidgets.QActionGroup(UIData.button, exclusive=True)
    UIData.menuPose = ag.addAction(QtWidgets.QAction('Mirror Pose of Current Frame', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuPose)
    UIData.menuAnim = ag.addAction(QtWidgets.QAction('Mirror Animation', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuAnim)


    UIData.button.show()
    mainLayout.addWidget(UIData.button)
    readDCNMode()

def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.button.mapToGlobal(position))  
    
    if action == UIData.menuPose:
        writeDCNMode('pose')
    elif action == UIData.menuAnim:
        writeDCNMode('anim')

def run():
    """
    """
    mode = 'pose'
    if  UIData.menuAnim.isChecked() == True:
        mode = 'anim'
    Core.run(mode = mode)

def readDCNMode():
    """
    """
    UIData.pref = Preference.Preference()
    if UIData.pref.dcnMode == 'pose':
        UIData.menuPose.setChecked(True)
        UIData.menuAnim.setChecked(False)
    elif UIData.pref.dcnMode == 'anim':
        UIData.menuPose.setChecked(False)
        UIData.menuAnim.setChecked(True)

def writeDCNMode(mode, *args):
    """
    """
    UIData.pref = Preference.Preference()
    UIData.pref.dcnMode = mode
    UIData.pref.construct()
    UIData.pref.write()