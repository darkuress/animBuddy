import maya.cmds as cmds
import maya.mel as mel
from animBuddy.Utils import Maya
reload(Maya)

def run(value):
    """
    micro control
    """
    sels = cmds.ls(sl = True)
    for sel in sels:
        channelBox = Maya.getSelectedChannelBox()
        try:
            attr = cmds.channelBox(channelBox, q = True, selectedMainAttributes = True)[0]
            cmds.setAttr('{}.{}'.format(sel, attr), cmds.getAttr('{}.{}'.format(sel, attr)) + value)
        except:
            pass