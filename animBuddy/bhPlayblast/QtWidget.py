import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

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
      #- Playblast ---------------------------------------------------------------
      mainLayout = parent
      iconImagePath = os.path.join(imagesPath, 'play1_hi.png')
      iconHoverImagePath = os.path.join(imagesPath, 'play1.png')
      button = QtWidgets.QPushButton('')
      button.clicked.connect(playblast)
      button.setToolTip("Beverhouse exclusive Playblast Tool")
      button.setStyleSheet(
      '''
      QPushButton{image:url(%s); border:0px; width:%s; height:%s}
      QPushButton:hover{image:url(%s); border:0px;}
      QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
      ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
      )             
      button.show()
      mainLayout.addWidget(button)

def playblast(*args):
    """
    """
    from animBuddy.bhPlayblast import ui
    reload(ui)

    run = ui.UI()
    run.loadInMaya()