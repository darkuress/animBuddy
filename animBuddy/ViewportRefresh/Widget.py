import os
import maya.cmds as cmds
from functools import partial
import Core
reload(Core)


class UIContainer():
    frozen = False


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
    # - Freeze Viewport---------------------------------------------------------------
    cmds.rowLayout(numberOfColumns=1, parent=parent)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'freeze.png'),
                        hi=os.path.join(imagesPath, 'freeze_hi.png'),
                        width=iconSize, mw=marginSize, height=iconSize, mh=marginSize,
                        label='freeze',
                        annotation='Freeze / unFreeze viewport',
                        c=freeze)
    cmds.setParent("..")


def freeze(*args):
    """
    """
    print '......', UIContainer.frozen
    if UIContainer.frozen == True:
        cmds.refresh(su=False)
        UIContainer.frozen = False
    else:
        cmds.refresh(su=True)
        UIContainer.frozen = True
