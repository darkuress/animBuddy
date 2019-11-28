import maya.cmds as cmds
import maya.mel as mel

def run(value):
    """
    micro control
    """
    sels = cmds.ls(sl = True)
    for sel in sels:
        channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
        try:
            attr = cmds.channelBox(channelBox, q = True, sma = True)[0]
            cmds.setAttr('{}.{}'.format(sel, attr), cmds.getAttr('{}.{}'.format(sel, attr)) + value)
        except:
            pass