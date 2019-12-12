import os
import maya.cmds as cmds
from functools import partial
import Core
reload(Core)


class UIContainer():
    """
    """
    menuItemShiftKeyClear = None
    textFieldLockDown = None

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
    cmds.rowLayout(numberOfColumns=1, parent = parent)
    cmds.columnLayout()
    UIContainer.textFieldLockDown = cmds.textField(text=3, width=42)
    cmds.popupMenu()
    UIContainer.menuItemTranslation = cmds.menuItem(label='translate only', radioButton=True)
    UIContainer.menuItemRotation    = cmds.menuItem(label='rotation only', radioButton=False)
    UIContainer.menuItemBoth        = cmds.menuItem(label='both', radioButton=False)
    cmds.menuItem(divider=True)
    UIContainer.menuItemReset       = cmds.menuItem(label='clear key', c=clearKey)
    cmds.rowLayout(numberOfColumns=2)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(
                            imagesPath, 'left.png'),
                        hi=os.path.join(
                            imagesPath, 'left_hi.png'),
                        width=iconSize/1.5, mw=marginSize, height=iconSize/1.5, mh=marginSize,
                        label='lock reverse',
                        npm=1,
                        annotation='lock reverse',
                        c=partial(run, 'reverse'))
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(
                            imagesPath, 'right.png'),
                        hi=os.path.join(
                            imagesPath, 'right_hi.png'),
                        width=iconSize/1.5, mw=marginSize, height=iconSize/1.5, mh=marginSize,
                        label='lock forward',
                        npm=1,
                        annotation='lock forward',
                        c=partial(run, 'forward'))
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

def run(mode, *args):
    """
    """
    doReverse = False
    doTranslate = True
    doRotate = True

    frame = int(cmds.textField(UIContainer.textFieldLockDown, q=True, text=True))

    if mode == 'reverse':
        doReverse = True   
    if cmds.menuItem(UIContainer.menuItemTranslation, q=True, radioButton=True):
        doTranslate = True
        doRotate = False
    elif cmds.menuItem(UIContainer.menuItemRotation, q=True, radioButton=True):
        doTranslate = False
        doRotate = True
    
    Core.run(frame = frame,
             doTranslate = doTranslate, 
             doRotate = doRotate,
             doReverse = doReverse)

def clearKey(*args):
    """
    """
    Core.clearKey()