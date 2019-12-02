import maya.cmds as cmds

def run(mode ='bake'):
    """
    """
    if cmds.ls(sl = True):
        sel = cmds.ls(sl = True)[0]
    else:
        "need to select controller"

    loc = cmds.spaceLocator(n = "{}_mgLoc".format(sel))
    
    pCon = cmds.parentConstraint(sel, loc, mo = False, weight = 1)

    if mode == 'constraint':
        return
    elif mode == 'bake':
        #- bake
        cmds.bakeResults(loc, simulation = True) 
        cmds.delete(pCon)
    elif mode == 'driver':
        pass