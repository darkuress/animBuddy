import os
import maya.cmds as cmds
from functools import partial
import Core
reload(Core)

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
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'footstep.png'),
                        hi=os.path.join(imagesPath, 'footstep_hi.png'),
                        width=iconSize, mw=marginSize, height=iconSize, mh=marginSize,
                        label='manager',
                        annotation='Ex Footstep : snaps to the last keyframe',
                        c=exFootStep)


def exFootStep(*args):
    """
    """
    Core.exFootStep()
