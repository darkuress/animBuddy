import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
from animBuddy import Preference
reload(Preference)
import Core
reload(Core)

class UIData():
    """
    """
    button = None
    popupMenu = None
    menuConstraint = None
    menuBake = None
    menuDriver = None
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
    #- Reset It---------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'mgloc.png')
    iconHoverImagePath = os.path.join(imagesPath, 'mgloc_hi.png')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(run)
    UIData.button.setToolTip("select object and run, it will craete locator per option")
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
    UIData.menuConstraint = ag.addAction(QtWidgets.QAction('Constrain to Object', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuConstraint)
    UIData.menuBake = ag.addAction(QtWidgets.QAction('Bake', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuBake)
    UIData.menuDriver = ag.addAction(QtWidgets.QAction('Drive Object', UIData.popupMenu, checkable=True))
    UIData.popupMenu.addAction(UIData.menuDriver)

    UIData.button.show()
    mainLayout.addWidget(UIData.button)
    readMGLMode()

def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.button.mapToGlobal(position))  
    
    if action == UIData.menuConstraint:
        writeMGLMode('constraint')
    elif action == UIData.menuBake:
        writeMGLMode('bake')
    elif action == UIData.menuDriver:
        writeMGLMode('driver')

def run():
    mode = 'constraint'
    if UIData.menuBake.isChecked():
        mode = 'bake'
    elif UIData.menuDriver.isChecked():
        mode = 'driver'

    Core.run(mode=mode)

def readMGLMode():
    """
    """
    UIData.pref = Preference.Preference()
    if UIData.pref.mglMode == 'constraint':
        UIData.menuConstraint.setChecked(True)
        UIData.menuBake.setChecked(False)
        UIData.menuDriver.setChecked(False)
    elif UIData.pref.mglMode == 'bake':
        UIData.menuConstraint.setChecked(False)
        UIData.menuBake.setChecked(True)
        UIData.menuDriver.setChecked(False)
    elif UIData.pref.mglMode == 'driver':
        UIData.menuConstraint.setChecked(False)
        UIData.menuBake.setChecked(False)
        UIData.menuDriver.setChecked(True)
    
def writeMGLMode(mode, *args):
    """
    """
    UIData.pref = Preference.Preference()
    UIData.pref.mglMode = mode
    UIData.pref.construct()
    UIData.pref.write()