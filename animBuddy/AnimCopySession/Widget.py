import Core
import os
import maya.cmds as cmds
from functools import partial
from animBuddy import Preference
reload(Preference)
reload(Core)


class UIContainer():
    """
    """
    pref = None
    radioMenuItemACSModePose = None
    radioMenuItemACSModeAnim = None


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
    # - Copy Paste Animation--------------------------------------------------
    cmds.rowLayout(numberOfColumns=2)
    cmds.iconTextButton(style='iconOnly',
                        image1=os.path.join(imagesPath, 'copy.png'),
                        hi=os.path.join(imagesPath, 'copy_hi.png'),
                        width=iconSize, mw=marginSize, height=iconSize, mh=marginSize,
                        label='cv',
                        npm=1,
                        annotation='copy current animation or pose. Right click for reset tool. Preserves current session',
                        c=copySession)
    cmds.popupMenu()
    cmds.radioMenuItemCollection()
    UIContainer.radioMenuItemACSModePose = cmds.menuItem(label='Copy Pose of Current Frame',
                                                         radioButton=True,
                                                         c=partial(writeACSMode, 'pose'))
    UIContainer.radioMenuItemACSModeAnim = cmds.menuItem(label='Copy Animation',
                                                         radioButton=False,
                                                         c=partial(writeACSMode, 'anim'))
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Reset", command=copyReset)
    cmds.setParent("..")

    readACSMode()

# ---------------------------------------------------------------------------------


def copySession(*args):
    """
    """
    mode = 'pose'
    if cmds.menuItem(UIContainer.radioMenuItemACSModeAnim, q=True, radioButton=True):
        mode = 'anim'
    copy = Core.AnimCopySession()
    result = copy.run(mode=mode)
    cmds.confirmDialog(title='Anim Copy Session',
                       message='Anim {} done!'.format(result),
                       button=['Ok'],
                       defaultButton='Ok',
                       dismissString='Ok')


def copyReset(*args):
    """
    """
    copy = Core.AnimCopySession()
    copy.reset()


def readACSMode():
    """
    """
    UIContainer.pref = Preference.Preference()
    if UIContainer.pref.acsMode == 'pose':
        cmds.menuItem(UIContainer.radioMenuItemACSModePose,
                      e=True, radioButton=True)
        cmds.menuItem(UIContainer.radioMenuItemACSModeAnim,
                      e=True, radioButton=False)
    elif UIContainer.pref.acsMode == 'anim':
        cmds.menuItem(UIContainer.radioMenuItemACSModePose,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.radioMenuItemACSModeAnim,
                      e=True, radioButton=True)


def writeACSMode(mode, *args):
    """
    """
    UIContainer.pref = Preference.Preference()
    UIContainer.pref.acsMode = mode
    UIContainer.pref.construct()
    UIContainer.pref.write()
