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
      pref = Preference.Preference()

def build(parent, 
          imagesPath, 
          iconSize = 25,
          height = 20, 
          marginSize = 5):
      """
      build widget
      @param parent : parent layout in maya
      @imagesPath : str path
      """
      cmds.rowLayout(numberOfColumns = 1, parent = parent)
      cmds.iconTextButton(style = 'iconOnly', 
                          image1 = os.path.join(imagesPath, 'decalcomanie.png'), 
                          hi = os.path.join(imagesPath, 'decalcomanie_hi.png'),
                          width = iconSize*1.2, mw = marginSize, height = iconSize, mh = marginSize,
                          label = 'decalcomanie',
                          annotation = 'Copy Left or Right anim to Right or Left', 
                          c = runDecalComanie)
      cmds.popupMenu()
      cmds.radioMenuItemCollection()
      UIContainer.radioMenuItemDCNModePose = cmds.menuItem(label='Mirror Pose of Current Frame', 
                                               radioButton = True,
                                               c = partial(writeDCNMode, 'pose') )
      UIContainer.radioMenuItemDCNModeAnim = cmds.menuItem(label='Mirror Animation', 
                                               radioButton = False,
                                               c = partial(writeDCNMode, 'anim') )
      cmds.setParent("..") 
      readDCNMode()

def runDecalComanie():
    """
    """
    mode = 'pose'
    if cmds.menuItem(UIContainer.radioMenuItemDCNModeAnim, q = True, radioButton = True):
        mode = 'anim'
    Core.run(mode =mode)

def readDCNMode():
    """
    """
    UIContainer.pref = Preference.Preference()
    if UIContainer.pref.acsMode == 'pose':
        cmds.menuItem(UIContainer.radioMenuItemDCNModePose, e = True, radioButton = True)
        cmds.menuItem(UIContainer.radioMenuItemDCNModeAnim, e = True, radioButton = False)
    elif UIContainer.pref.acsMode == 'anim':
        cmds.menuItem(UIContainer.radioMenuItemDCNModePose, e = True, radioButton = False)
        cmds.menuItem(UIContainer.radioMenuItemDCNModeAnim, e = True, radioButton = True)

def writeDCNMode(mode, *args):
    """
    """
    UIContainer.pref = Preference.Preference()
    UIContainer.pref.dcnMode = mode
    UIContainer.pref.construct()
    UIContainer.pref.write()