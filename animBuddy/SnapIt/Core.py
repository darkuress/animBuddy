import maya.cmds as cmds

def snap():
    """
    select target first then source
    """
    sels = cmds.ls(sl = True)
    
    firSel = sels[0]
    secSel = sels[1]
    
    const = cmds.parentConstraint(firSel, secSel, mo = False, weight = 1)

    tr = cmds.xform(secSel, q = True, t = True)
    ro = cmds.xform(secSel, q = True, ro = True)
    
    cmds.delete(const)

    cmds.xform(secSel, t = tr, ro = ro)