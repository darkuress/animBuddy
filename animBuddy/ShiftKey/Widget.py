import os
import maya.cmds as cmds
from functools import partial
import Core
reload(Core)


class UIContainer():
    """
    """
    textFieldShiftKey = None


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
    cmds.rowLayout(numberOfColumns=4, parent=parent)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'left.png'),
                        hi=os.path.join(imagesPath, 'left_hi.png'),
                        width=iconSize/1.2, mw=marginSize, height=iconSize/1.2, mh=marginSize,
                        label='sub',
                        npm=1,
                        annotation='shift key to left',
                        c=partial(shiftKey, "left"))
    UIContainer.textFieldShiftKey = cmds.textField(text=1, width=30)
    cmds.popupMenu()
    cmds.menuItem(label='reset', c=shiftKeyClear)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'right.png'),
                        hi=os.path.join(imagesPath, 'right_hi.png'),
                        width=iconSize/1.2, mw=marginSize, height=iconSize/1.2, mh=marginSize,
                        label='add',
                        npm=1,
                        annotation='shift key to right',
                        c=partial(shiftKey, "right"))
    cmds.separator(height=10, width=10, style='none')
    cmds.setParent("..")


def shiftKey(mode='right'):
    """
    """
    val = int(cmds.textField(UIContainer.textFieldShiftKey, q=True, text=True))
    if mode == 'right':
        Core.run(amount=val)
    elif mode == 'left':
        Core.run(amount=-1 * val)


def shiftKeyClear(*args):
    """
    """
    Core.clear()
