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
    menuItemLDNTranslation = None
    menuItemLDNRotation    = None
    menuItemLDNBoth        = None
    textFieldLockDown   = None

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
    UIContainer.textFieldLockDown = cmds.textField(text=3, width=43)
    cmds.popupMenu()
    cmds.radioMenuItemCollection()
    UIContainer.menuItemLDNTranslation = cmds.menuItem(label='translate only', 
                                                    radioButton=True,
                                                    c=partial(writeLDNMode, 'translate'))
    UIContainer.menuItemLDNRotation    = cmds.menuItem(label='rotation only', 
                                                    radioButton=False,
                                                    c=partial(writeLDNMode, 'rotate'))
    UIContainer.menuItemLDNBoth        = cmds.menuItem(label='both', 
                                                    radioButton=False,
                                                    c=partial(writeLDNMode, 'both'))
    cmds.menuItem(divider=True)
    UIContainer.menuItemReset       = cmds.menuItem(label='clear key', c=clearKey)
    cmds.rowLayout(numberOfColumns=2)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(
                            imagesPath, 'lockdown_reverse.png'),
                        hi=os.path.join(
                            imagesPath, 'lockdown_reverse_hi.png'),
                        width=iconSize/1.5, mw=marginSize, height=iconSize/1.5, mh=marginSize,
                        label='lock reverse',
                        npm=1,
                        annotation='lock reverse',
                        c=partial(run, 'reverse'))
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(
                            imagesPath, 'lockdown_forward.png'),
                        hi=os.path.join(
                            imagesPath, 'lockdown_forward_hi.png'),
                        width=iconSize/1.5, mw=marginSize, height=iconSize/1.5, mh=marginSize,
                        label='lock forward',
                        npm=1,
                        annotation='lock forward',
                        c=partial(run, 'forward'))
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    readLDNMode()

def run(mode, *args):
    """
    """
    doReverse = False
    doTranslate = True
    doRotate = True

    frame = int(cmds.textField(UIContainer.textFieldLockDown, q=True, text=True))

    if mode == 'reverse':
        doReverse = True   
    if cmds.menuItem(UIContainer.menuItemLDNTranslation, q=True, radioButton=True):
        doTranslate = True
        doRotate = False
    elif cmds.menuItem(UIContainer.menuItemLDNRotation, q=True, radioButton=True):
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

def readLDNMode():
    """
    """
    UIContainer.pref = Preference.Preference()
    if UIContainer.pref.ldnMode == 'translate':
        cmds.menuItem(UIContainer.menuItemLDNTranslation,
                      e=True, radioButton=True)
        cmds.menuItem(UIContainer.menuItemLDNRotation,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.menuItemLDNBoth,
                      e=True, radioButton=False)
    elif UIContainer.pref.ldnMode == 'rotate':
        cmds.menuItem(UIContainer.menuItemLDNTranslation,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.menuItemLDNRotation,
                      e=True, radioButton=True)
        cmds.menuItem(UIContainer.menuItemLDNBoth,
                      e=True, radioButton=False)
    elif UIContainer.pref.ldnMode == 'both':
        cmds.menuItem(UIContainer.menuItemLDNTranslation,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.menuItemLDNRotation,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.menuItemLDNBoth,
                      e=True, radioButton=True)


def writeLDNMode(mode, *args):
    """
    """
    UIContainer.pref = Preference.Preference()
    UIContainer.pref.ldnMode = mode
    UIContainer.pref.construct()
    UIContainer.pref.write()