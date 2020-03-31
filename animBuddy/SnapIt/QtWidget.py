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
    #- Snap It --------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'snapit.png')
    iconHoverImagePath = os.path.join(imagesPath, 'snapit.png')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(snapIt)
    UIData.button.setToolTip('Snap It : secondly selected thing will be snapped to the first selected thing')
    UIData.button.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    UIData.button.show()

    mainLayout.addWidget(UIData.button)

def snapIt(*args):
      """
      """
      Core.snap()