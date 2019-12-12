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
      #- Reset It---------------------------------------------------------------
      cmds.rowLayout(numberOfColumns = 1, parent = parent)
      cmds.iconTextButton(style = 'iconOnly', 
                          image1 = os.path.join(imagesPath, 'reset.png'), 
                          hi = os.path.join(imagesPath, 'reset_hi.png'),
                          width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                          label = 'reset',
                          annotation = 'Resets values of current selected controller or any object', 
                          c = resetIt)
      cmds.setParent("..") 

def resetIt(self, *args):
      """
      reset it 
      """
      Core.run()  