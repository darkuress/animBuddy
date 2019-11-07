import maya.cmds as cmds

def run():
    """
    making all the translation, rotation value to 0
    """
    sels = cmds.ls(sl = True)
    attrs = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ']
    for sel in sels:
        for attr in attrs:
            if cmds.getAttr(sel + attr, settable = True):
                cmds.setAttr(sel + attr, 0)