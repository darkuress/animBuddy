import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
import Core
reload(Core)

class UIContainer():
    frozen = False

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
      #- Viewport Refresh---------------------------------------------------------------
      mainLayout = parent
      iconImagePath = os.path.join(imagesPath, 'freeze.png').replace('\\', '/')
      iconHoverImagePath = os.path.join(imagesPath, 'freeze_hi.png').replace('\\', '/')
      button = QtWidgets.QPushButton('')
      button.setIconSize(QtCore.QSize(iconSize, iconSize))
      button.clicked.connect(freeze)
      button.setToolTip("Freeze / Unfreeze viewport")
      button.setStyleSheet(
      '''
      QPushButton{image:url(%s); border:0px; width:%s; height:%s}
      QPushButton:hover{image:url(%s); border:0px;}
      QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
      ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
      )             
      button.show()
      mainLayout.addWidget(button)

def freeze(*args):
    """
    """
    if UIContainer.frozen == True:
        cmds.refresh(su=False)
        print('Viewport is unfrozen')
        UIContainer.frozen = False
    else:
        cmds.refresh(su=True)
        print('Viewport is frozen')
        UIContainer.frozen = True
