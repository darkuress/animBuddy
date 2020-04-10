import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
import QtUISelectionGrp
reload(QtUISelectionGrp)
import Core
reload(Core)

class UIData():
    """
    """
    button = None

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
    #- Selection Group---------------------------------------------------------------
    mainLayout = parent
    iconImagePath = os.path.join(imagesPath, 'manager.png').replace('\\', '/')
    iconHoverImagePath = os.path.join(imagesPath, 'manager_hi.png').replace('\\', '/')
    UIData.button = QtWidgets.QPushButton('')
    UIData.button.clicked.connect(expandToolbar)
    UIData.button.setToolTip('Creating Seiection groups')
    UIData.button.setStyleSheet(
    '''
    QPushButton{image:url(%s); border:0px; width:%s; height:%s}
    QPushButton:hover{image:url(%s); border:0px;}
    QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
    ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
    )             
    UIData.button.show()

    mainLayout.addWidget(UIData.button)


def expandToolbar(*args):
    """
    """
    ui = QtUISelectionGrp.main() 