import os
import maya.cmds as cmds


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
    cmds.rowLayout(numberOfColumns=1, parent=parent)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'play1_hi.png'),
                        hi=os.path.join(imagesPath, 'play1.png'),
                        width=iconSize, mw=marginSize, height=iconSize, mh=marginSize,
                        label='playblast',
                        annotation='Beverhouse exclusive Playblast Tool',
                        c=playblast)
    cmds.setParent("..")


def playblast(*args):
    """
    """
    from animBuddy.bhPlayblast import ui
    reload(ui)

    run = ui.UI()
    run.loadInMaya()
