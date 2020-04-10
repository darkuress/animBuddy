import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
import Core
reload(Core)

class UIData():
    """
    """
    button = None
    popupMenu = None
    popupReset = None

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
    #- Ex Foot step---------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'footstep.png').replace('\\', '/')
    iconHoverImagePath = os.path.join(imagesPath, 'footstep_hi.png').replace('\\', '/')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(exFootStep)
    UIData.button.setToolTip('Ex Footstep : snaps to the last keyframe')
    UIData.button.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    UIData.button.show()

    mainLayout.addWidget(UIData.button)

def exFootStep(*args):
    """
    """
    Core.exFootStep()