import os
import maya.cmds as cmds
from functools import partial
from animBuddy import UISelectionToolBar
reload(UISelectionToolBar)


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
    cmds.rowLayout(numberOfColumns=1)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'manager.png'),
                        hi=os.path.join(imagesPath, 'manager_hi.png'),
                        width=iconSize, mw=marginSize, height=iconSize, mh=marginSize,
                        label='manager',
                        c=expandSelectionToolbar)
    cmds.setParent("..")


def expandSelectionToolbar(*args):
    """
    """
    ui = UISelectionToolBar.UISelectionToolBar()
    ui.loadInMaya()
