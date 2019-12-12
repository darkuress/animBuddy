import os
import maya.cmds as cmds
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
      @param parent : parent layout in maya
      @imagesPath : str path
      """
      cmds.rowLayout(numberOfColumns = 1, parent = parent)
      cmds.iconTextButton(style = 'iconOnly', 
                          image1 = os.path.join(imagesPath, 'snapit.png'), 
                          hi = os.path.join(imagesPath, 'snapit_hi.png'), 
                          width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                          label = 'manager',
                          annotation = 'second selected thing will be snapped to the first selected thing',
                          c = snapIt)
      cmds.setParent("..")

def snapIt(*args):
      """
      """
      Core.snap()