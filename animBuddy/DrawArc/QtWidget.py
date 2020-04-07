import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
import QtUIDrawArcToolbar
reload(QtUIDrawArcToolbar)
import Core
reload(Core)

class UIData():
    """
    """
    button = None
    popupMenu = None
    popUpSettings = None
    popUpDeleteAll = None

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
    #- Draw Arc---------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'arc_hi.png')
    iconHoverImagePath = os.path.join(imagesPath, 'arc.png')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(drawArc)
    UIData.button.setToolTip('MotionTrail tool')
    UIData.button.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    UIData.button.show()

    # ---- menuItem
    UIData.button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    UIData.button.customContextMenuRequested.connect(popupHandler)
    UIData.popupMenu = QtWidgets.QMenu()
    UIData.popUpSettings = UIData.popupMenu.addAction("Settings")
    UIData.popupMenu.addSeparator()
    UIData.popUpDeleteAll = UIData.popupMenu.addAction("Delete All")

    mainLayout.addWidget(UIData.button)

def popupHandler(position):
    action = UIData.popupMenu.exec_(UIData.button.mapToGlobal(position))  

    #- reset popup
    if action == UIData.popUpSettings:
        drawArcToolbar()
    elif action == UIData.popUpDeleteAll:
        deleteAll()

def drawArc(*args):
    """
    Motion trail 
    """
    from animBuddy import Preference
    reload(Preference)
    UIData.pref = Preference.Preference()

    Core.run(dotSize=UIData.pref.dotSize,
             keyFrameSize=UIData.pref.keyFrameSize,
             timeBuffer=UIData.pref.timeBuffer,
             lineWidth=UIData.pref.lineWidth,
             lineColor=UIData.pref.lineColor,
             dotColor=UIData.pref.dotColor,
             keyFrameColor=UIData.pref.keyFrameColor,
             style = UIData.pref.mtStyle)


def deleteAll(*args):
    """
    delete all motion trails
    """
    Core.deleteAll()


def drawArcToolbar(*args):
    """
    """
    ui = QtUIDrawArcToolbar.main() 