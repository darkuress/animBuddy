import maya.cmds as cmds
from animBuddy.Utils import Maya
reload(Maya)

def run():
    """
    making all the translation, rotation value to 0
    """
    sels = cmds.ls(sl = True)
    attrs = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ']
    for sel in sels:
        channelBox = Maya.getSelectedChannelBox()
        try:
            attr = cmds.channelBox(channelBox, q = True, selectedMainAttributes = True)[0]
            attr = '.' + attr
            zerofy(sel, attr)
        except:
            for attr in attrs:
                zerofy(sel, attr)

def zerofy(sel, attr):
    """
    """
    if cmds.getAttr(sel + attr, settable = True):
        cmds.setAttr(sel + attr, 0)