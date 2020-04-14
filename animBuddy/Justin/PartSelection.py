import maya.cmds as cmds

def glasses(*args):
    """
    """
    if not cmds.ls('Flag_Flag_01_ann') and cmds.ls('*:Flag_Flag_01_ann'):
        return
    if cmds.ls('Flag_Flag_01_ann'):
        cmds.setAttr('Flag_Flag_01_ann.glasses', not cmds.getAttr('Flag_Flag_01_ann.glasses'))
    elif cmds.ls('*:Flag_Flag_01_ann'):
        node = cmds.ls('*:Flag_Flag_01_ann')[0]
        cmds.setAttr(node + '.glasses', not cmds.getAttr(node + '.glasses'))

def tie(*args):
    """
    """
    if not cmds.ls('Flag_Flag_01_ann') and cmds.ls('*:Flag_Flag_01_ann'):
        return
    if cmds.ls('Flag_Flag_01_ann'):
        cmds.setAttr('Flag_Flag_01_ann.neckTie', not cmds.getAttr('Flag_Flag_01_ann.neckTie'))
    elif cmds.ls('*:Flag_Flag_01_ann'):
        node = cmds.ls('*:Flag_Flag_01_ann')[0]
        cmds.setAttr(node + '.neckTie', not cmds.getAttr(node + '.neckTie'))