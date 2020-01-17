import os
import maya.cmds as cmds
from functools import partial
from animBuddy.Justin import UIJustinToolbar
reload(UIJustinToolbar)

def build(parent,
          imagesPath,
          iconSize=25,
          height=20,
          marginSize=5):
    """
    build widget
    @param parent : parent layout in maya
    @imagesPath : str path
    """
    cmds.rowLayout(numberOfColumns=2, parent=parent)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'justin.png'),
                        hi=os.path.join(imagesPath, 'justin_hi.png'),
                        width=35, mw=marginSize, height=35, mh=marginSize,
                        label='Justin',
                        npm=1,
                        annotation=' Menu for Justin rig',
                        c = expandToolBar)
    cmds.setParent("..")

def expandToolBar(*args):
    """
    """
    if cmds.window('UIJustinToolBar', ex=True):
        cmds.deleteUI('UIJustinToolBar')
    else:
        ui = UIJustinToolbar.UIJustinToolbar()
        ui.loadInMaya()    

