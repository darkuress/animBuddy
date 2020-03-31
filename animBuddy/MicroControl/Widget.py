import os
import maya.cmds as cmds
from functools import partial
import Core
reload(Core)


class UIContainer():
    """
    """
    textFieldMicroControl = None


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
    cmds.rowLayout(numberOfColumns=3, parent=parent)
    UIContainer.textFieldMicroControl = cmds.textField(text=0.01, width=50)
    cmds.columnLayout()
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'uparrow.png'),
                        hi=os.path.join(imagesPath, 'uparrow_hi.png'),
                        width=iconSize/1.3, mw=marginSize, height=iconSize/2, mh=marginSize,
                        label='add',
                        npm=1,
                        annotation='add this value to current channel selection',
                        c=partial(microControlRun, "add"))
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'dnarrow.png'),
                        hi=os.path.join(imagesPath, 'dnarrow_hi.png'),
                        width=iconSize/1.3, mw=marginSize, height=iconSize/2, mh=marginSize,
                        label='sub',
                        npm=1,
                        annotation='substract this value from current channel selection',
                        c=partial(microControlRun, "sub"))
    cmds.setParent("..")
    cmds.setParent("..")


def microControlRun(mode, *args):
    """
    @param mode string "add" or "sub"
    """
    val = round(float(cmds.textField(
        UIContainer.textFieldMicroControl, q=True, text=True)), 3)
    if mode == "add":
        Core.run(val)
    else:
        Core.run(val*-1)
