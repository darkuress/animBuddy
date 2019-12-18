from animBuddy import DrawArcToolBar
import testRun
import os
import maya.cmds as cmds
from functools import partial
from animBuddy import Preference
reload(Preference)
reload(testRun)
reload(DrawArcToolBar)


class UIContainer():
    """
    """
    pref = None


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
    cmds.rowLayout(numberOfColumns=2)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'add_hi.xpm'),
                        hi=os.path.join(imagesPath, 'add.xpm'),
                        width=iconSize, mw=marginSize, height=iconSize, mh=marginSize,
                        label='arc',
                        annotation='MotionTrail tool',
                        c=drawArc)
    cmds.popupMenu()
    cmds.menuItem(label="Setting", c=drawArcToolbar)
    cmds.menuItem(label="---------------", c=drawArcToolbar)
    cmds.menuItem(label="Delete All", c=deleteAll)
    cmds.setParent("..")

# ---------------------------------------------------------------------------------


def drawArc(*args):
    """
    Motion trail 
    """
    UIContainer.pref = Preference.Preference()

    testRun.run(dotSize=UIContainer.pref.dotSize,
                keyFrameSize=UIContainer.pref.keyFrameSize,
                timeBuffer=UIContainer.pref.timeBuffer,
                lineWidth=UIContainer.pref.lineWidth,
                lineColor=UIContainer.pref.lineColor,
                dotColor=UIContainer.pref.dotColor,
                keyFrameColor=UIContainer.pref.keyFrameColor)


def deleteAll(*args):
    """
    delete all motion trails
    """
    testRun.deleteAll()


def drawArcToolbar(*args):
    """
    """
    ui = DrawArcToolBar.DrawArcToolBar()
    ui.loadInMaya()
