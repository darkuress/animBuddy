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
    dragInProgress = False
    objs = False
    animCurves = None
    animCurveInfo = {} #dict {animcurve : []}
    animCurveCalculatedInfo = {}
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
    cmds.separator(height=5, width=66, style='none')
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
                            c=partial(easyInBetweenChange, value=value))
        cmds.separator(height=10, width=1, style='none')
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    readEIBMode()


def easyInBetweenChange(value = None, *args):
    """
    slider
    """
    if not UIContainer.undoChunk:
        UIContainer.undoChunk = True
        cmds.undoInfo(openChunk=True)
    
    if not UIContainer.dragInProgress:
        #pass initial values
        UIContainer.objs = cmds.ls(sl = True)
        if cmds.menuItem(UIContainer.radioMenuItemModeObject, q=True, radioButton=True):
            UIContainer.animCurves = Core.getAnimCurves()
            for curve in UIContainer.animCurves:
                UIContainer.animCurveInfo[curve] = Core.findCloseKeyByFrame(curve, cmds.currentTime(q = True))
            UIContainer.animCurveCalculatedInfo = Core.calculate(UIContainer.animCurveInfo)
        elif cmds.menuItem(UIContainer.radioMenuItemModeKeyFrame, q=True, radioButton=True):
            UIContainer.animCurves = Core.getAnimCurves(withFrame = True)
            for curve in UIContainer.animCurves:
                frames = Core.getAllKeyFrames(curve)
                UIContainer.animCurveInfo[curve] = {}
                for frame in frames:
                    UIContainer.animCurveInfo[curve][frame] = Core.findCloseKeyByFrame(curve, frame)          
            UIContainer.animCurveCalculatedInfo = Core.calculate(UIContainer.animCurveInfo, withFrame = True)

        UIContainer.dragInProgress = True

    if value:
        amount = value
    else:
        amount = cmds.floatSlider(UIContainer.floatSliderEIBAmount, q=True, v=True)

    if cmds.menuItem(UIContainer.radioMenuItemModeObject, q=True, radioButton=True):
        Core.runChange(UIContainer.objs, amount, UIContainer.animCurveCalculatedInfo)
    elif cmds.menuItem(UIContainer.radioMenuItemModeKeyFrame, q=True, radioButton=True):
        if amount > 1:
            Core.runChange(UIContainer.objs, 1, UIContainer.animCurveCalculatedInfo, withFrame = True)
        elif amount < 0:
            Core.runChange(UIContainer.objs, 0, UIContainer.animCurveCalculatedInfo, withFrame = True)
        else:
            Core.runChange(UIContainer.objs, amount, UIContainer.animCurveCalculatedInfo, withFrame = True)


def afterDrop(*args):
    """
    """
    UIContainer.undoChunk = False
    cmds.undoInfo(closeChunk=True)
    cmds.floatSlider(UIContainer.floatSliderEIBAmount, e=True, v=0.5)
    UIContainer.dragInProgress = False
    UIContainer.objs = None
    UIContainer.animCurves = None
    UIContainer.nearByKeyFrame = {}
    UIContainer.animCurveCalculatedInfo = {}


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
