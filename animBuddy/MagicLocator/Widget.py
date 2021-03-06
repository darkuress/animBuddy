import os
import maya.cmds as cmds
from functools import partial
from animBuddy import Preference
reload(Preference)
import Core
reload(Core)


class UIContainer():
    """
    """
    radioMenuItemModeCont = None
    radioMenuItemModeBake = None
    radioMenuItemModeDrive = None
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
    cmds.rowLayout(numberOfColumns=1, parent=parent)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'mgloc.png'),
                        hi=os.path.join(imagesPath, 'mgloc_hi.png'),
                        width=iconSize*1.2, mw=marginSize, height=iconSize, mh=marginSize,
                        label='magic locator',
                        annotation='select object and it will craete locator per option',
                        c=runMagicLocator)
    cmds.popupMenu()
    cmds.radioMenuItemCollection()
    UIContainer.radioMenuItemModeCont = cmds.menuItem(label='Constraint to object',
                                                      radioButton=True,
                                                      c=partial(writeMGLMode, 'constraint'))
    UIContainer.radioMenuItemModeBake = cmds.menuItem(label='Bake',
                                                      radioButton=False,
                                                      c=partial(writeMGLMode, 'bake'))
    UIContainer.radioMenuItemModeDrive = cmds.menuItem(label='Drive Object',
                                                       radioButton=False,
                                                       c=partial(writeMGLMode, 'driver'))
    cmds.setParent("..")
    readMGLMode()


def runMagicLocator():
    """
    """
    mode = 'constraint'
    if cmds.menuItem(UIContainer.radioMenuItemModeBake, q=True, radioButton=True):
        mode = 'bake'
    elif cmds.menuItem(UIContainer.radioMenuItemModeDrive, q=True, radioButton=True):
        mode = 'driver'
    Core.run(mode=mode)


def readMGLMode():
    """
    """
    UIContainer.pref = Preference.Preference()
    if UIContainer.pref.mglMode == 'constraint':
        cmds.menuItem(UIContainer.radioMenuItemModeCont,
                      e=True, radioButton=True)
        cmds.menuItem(UIContainer.radioMenuItemModeBake,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.radioMenuItemModeDrive,
                      e=True, radioButton=False)
    elif UIContainer.pref.mglMode == 'bake':
        cmds.menuItem(UIContainer.radioMenuItemModeCont,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.radioMenuItemModeBake,
                      e=True, radioButton=True)
        cmds.menuItem(UIContainer.radioMenuItemModeDrive,
                      e=True, radioButton=False)
    elif UIContainer.pref.mglMode == 'driver':
        cmds.menuItem(UIContainer.radioMenuItemModeCont,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.radioMenuItemModeBake,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.radioMenuItemModeDrive,
                      e=True, radioButton=True)


def writeMGLMode(mode, *args):
    """
    """
    UIContainer.pref = Preference.Preference()
    UIContainer.pref.mglMode = mode
    UIContainer.pref.construct()
    UIContainer.pref.write()
