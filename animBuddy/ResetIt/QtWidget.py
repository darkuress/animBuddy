import os
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
import Core
reload(Core)

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
      iconImagePath = os.path.join(imagesPath, 'reset.png').replace('\\', '/')
      iconHoverImagePath = os.path.join(imagesPath, 'reset_hi.png').replace('\\', '/')
      button = QtWidgets.QPushButton('')
      button.clicked.connect(resetIt)
      button.setToolTip("Making All the attributes as 0")
      button.setStyleSheet(
      '''
      QPushButton{image:url(%s); border:0px; width:%s; height:%s}
      QPushButton:hover{image:url(%s); border:0px;}
      QPushButton:pressed { background-color: rgba(0, 255,255, 10);}
      ''' %(iconImagePath, iconSize, iconSize, iconHoverImagePath)       
      )             
      button.show()
      mainLayout.addWidget(button)

def resetIt(*args):
      """
      reset it 
      """
      Core.run()  