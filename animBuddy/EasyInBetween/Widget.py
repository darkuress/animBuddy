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
    undoChunk = False
    floatSliderEIBAmount = None
    radioMenuItemModeObject = None
    radioMenuItemModeKeyFrame = None
    pref = Preference.Preference()


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
    wdth = 266
    cmds.rowLayout(numberOfColumns=2, parent=parent)
    cmds.columnLayout(width=wdth)
    cmds.frameLayout(labelVisible=False,
                     borderVisible=False,
                     width=wdth,
                     marginHeight=0,
                     marginWidth=0,
                     labelIndent=0,
                     collapsable=False,)
    cmds.rowLayout(numberOfColumns=11,
                   adjustableColumn=1,
                   columnAttach=([2, 'both', 0]))
    cmds.text(label="0.0")
    cmds.separator(height=5, width=36, style='none')
    cmds.text(label="0.5")
    cmds.separator(height=5, width=70, style='none')
    cmds.text(label="1.0")
    cmds.separator(height=5, width=34, style='none')
    cmds.setParent("..")
    cmds.setParent("..")
    UIContainer.floatSliderEIBAmount = cmds.floatSlider(min=-0.2,
                                                        max=1.2,
                                                        width=wdth,
                                                        value=0.5,
                                                        step=0.1,
                                                        annotation='Easy Inbetween. Right click to reset the tool.',
                                                        cc=afterDrop,
                                                        dc=easyInBetweenChange)
    cmds.popupMenu()
    cmds.radioMenuItemCollection()
    UIContainer.radioMenuItemModeObject = cmds.menuItem(label='Object Mode',
                                                        radioButton=True,
                                                        c=partial(writeEIBMode, 'object'))
    UIContainer.radioMenuItemModeKeyFrame = cmds.menuItem(label='KeyFrame Mode',
                                                          radioButton=False,
                                                          c=partial(writeEIBMode, 'keyframe'))
    cmds.menuItem(divider=True)
    cmds.menuItem(label="Reset", command=afterDrop)

    cmds.frameLayout(labelVisible=False,
                     borderVisible=False,
                     width=wdth,
                     marginHeight=0,
                     marginWidth=0,
                     labelIndent=0,
                     collapsable=False,)
    cmds.rowLayout(width=wdth, numberOfColumns=30,
                   columnAttach=([2, 'both', 0]))
    for i in range(-2, 13, 1):
        value = i/10.0
        if i == 0 or i == 5 or i == 10:
            pic = 'dot_big.png'
        else:
            pic = 'dot_small.png'
        cmds.iconTextButton(style='iconOnly',
                            image1=os.path.join(imagesPath, pic),
                            label=str(value),
                            annotation="set inbetween : " + str(value),
                            c=partial(easyInBetweenChange2, value=value))
        cmds.separator(height=10, width=1, style='none')
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    readEIBMode()


def easyInBetweenChange(*args):
    """
    slider
    """
    if not UIContainer.undoChunk:
        UIContainer.undoChunk = True
        cmds.undoInfo(openChunk=True)
    amount = cmds.floatSlider(UIContainer.floatSliderEIBAmount, q=True, v=True)
    if cmds.menuItem(UIContainer.radioMenuItemModeObject, q=True, radioButton=True):
        Core.changeKey(amount)
    elif cmds.menuItem(UIContainer.radioMenuItemModeKeyFrame, q=True, radioButton=True):
        if amount > 1:
            Core.changeSelectedKey(1)
        elif amount < 0:
            Core.changeSelectedKey(0)
        else:
            Core.changeSelectedKey(amount)


def afterDrop(*args):
    """
    """
    UIContainer.undoChunk = False
    cmds.undoInfo(closeChunk=True)
    cmds.floatSlider(UIContainer.floatSliderEIBAmount, e=True, v=0.5)


def easyInBetweenChange2(value=None, *args):
    """
    dots
    """
    cmds.floatSlider(UIContainer.floatSliderEIBAmount, e=True, v=value)
    if cmds.menuItem(UIContainer.radioMenuItemModeObject, q=True, radioButton=True):
        Core.changeKey(value)
    elif cmds.menuItem(UIContainer.radioMenuItemModeKeyFrame, q=True, radioButton=True):
        if value > 1:
            Core.changeSelectedKey(1)
        elif value < 0:
            Core.changeSelectedKey(0)
        else:
            Core.changeSelectedKey(value)


def readEIBMode():
    """
    """
    if UIContainer.pref.eibMode == 'object':
        cmds.menuItem(UIContainer.radioMenuItemModeObject,
                      e=True, radioButton=True)
        cmds.menuItem(UIContainer.radioMenuItemModeKeyFrame,
                      e=True, radioButton=False)
    elif UIContainer.pref.eibMode == 'keyframe':
        cmds.menuItem(UIContainer.radioMenuItemModeObject,
                      e=True, radioButton=False)
        cmds.menuItem(UIContainer.radioMenuItemModeKeyFrame,
                      e=True, radioButton=True)


def writeEIBMode(mode, *args):
    """
    """
    UIContainer.pref = Preference.Preference()
    UIContainer.pref.eibMode = mode
    UIContainer.pref.construct()
    UIContainer.pref.write()
