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
      #- Misc---------------------------------------------------------------
      mainLayout = parent
      iconImagePath = os.path.join(imagesPath, 'preference.png').replace('\\', '/')
      iconHoverImagePath = os.path.join(imagesPath, 'preference_hi.png').replace('\\', '/')
      button = QtWidgets.QPushButton('')
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

