import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
from animBuddy.Justin import QtUIJustinToolbar
reload(QtUIJustinToolbar)

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
      #- Justin ---------------------------------------------------------------
      mainLayout = parent
      iconImagePath = os.path.join(imagesPath, 'justin.png').replace('\\', '/')
      iconHoverImagePath = os.path.join(imagesPath, 'justin_hi.png').replace('\\', '/')
      button = QtWidgets.QPushButton('')
      button.clicked.connect(expandToolBar)
      button.setToolTip("Justin Toolbar Expand")
      button.setStyleSheet(
      '''
      QPushButton{image:url(%s); border:0px; width:%s; height:%s}
      QPushButton:hover{image:url(%s); border:0px;}
      QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
      ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
      )             
      button.show()
      mainLayout.addWidget(button)

def expandToolBar(*args):
    """
    """
    ui = QtUIJustinToolbar.main() 