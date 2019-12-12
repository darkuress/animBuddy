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
    cmds.rowLayout(numberOfColumns=2, parent=parent)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'conit.png'),
                        hi=os.path.join(imagesPath, 'conit_hi.png'),
                        width=iconSize, mw=marginSize, height=iconSize, mh=marginSize,
                        label='conit',
                        npm=1,
                        annotation='Fake Constraint, select source and shift select destination. Right click for Reset Menu',
                        c=fakeConIt)
    cmds.popupMenu()
    cmds.menuItem(label="Reset", command=fakeConItReset)
    cmds.setParent("..")


def fakeConIt(*args):
    """
    """
    conRun = Core.FakeConIt()
    result = conRun.run()
    if result == 'Success':
        cmds.confirmDialog(title='Fake Conit',
                           message='Fake Constraint was generatec\nRight Click on button to reset connection',
                           button=['Ok'],
                           defaultButton='Ok',
                           dismissString='Ok')
    elif result == 'Failed':
        cmds.confirmDialog(title='Fake Conit',
                           message='please select source and destination(s) to create Fake Constraint',
                           button=['Ok'],
                           defaultButton='Ok',
                           dismissString='Ok')


def fakeConItReset(*args):
    """
    """
    conRun = Core.FakeConIt()
    conRun.reset()
