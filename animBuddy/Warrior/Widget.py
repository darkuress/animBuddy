import os
import maya.cmds as cmds
from functools import partial
from animBuddy.Warrior import UIWarriorToolbar
reload(UIWarriorToolbar)

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
                        image1=os.path.join(imagesPath, 'warrior.png'),
                        hi=os.path.join(imagesPath, 'warrior_hi.png'),
                        width=35, mw=marginSize, height=35, mh=marginSize,
                        label='Warrior',
                        npm=1,
                        annotation=' Menu for Warrior rig',
                        c = expandToolBar)
    cmds.setParent("..")

def expandToolBar(*args):
    """
    """
    ui = UIWarriorToolbar.UIWarriorToolbar()
    ui.loadInMaya()    

