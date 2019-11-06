import maya.cmds as cmds

def snap():
    """
    select target first then source
    """
    sels = cmds.ls(sl = True)
    
    firSel = sels[0]
    secSel = sels[1]
    
    const = cmds.parentConstraint(secSel, firSel, mo = False, weight = 1)
    
    cmds.delete(const)