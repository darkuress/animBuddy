import maya.cmds as cmds

def run(mode ='bake'):
    """
    """
    if cmds.ls(sl = True):
        sel = cmds.ls(sl = True)[0]
    else:
        cmds.confirmDialog( title='Error :', message='You need to select a controller', button=['ok'])
        return

    loc = "{}_mgLoc".format(sel)
  
    loc = cmds.spaceLocator(n = "{}_mgLoc".format(sel))
    pCon = cmds.parentConstraint(sel, loc, mo = False, weight = 1)

    if mode == 'constraint':
        return
    elif mode == 'bake':
        #- bake
        bakeLoc(loc)
        cmds.delete(pCon)
        
    elif mode == 'driver':
        bakeLoc(loc)
        cmds.delete(pCon)
        cmds.cutKey(sel)
        cmds.parentConstraint(loc, sel, mo = False, weight = 1)

    cmds.select(sel, r = True)

def bakeLoc(loc):
    """
    """
    minTime = cmds.playbackOptions(q = True, minTime = True) 
    maxTime = cmds.playbackOptions(q = True, maxTime = True)
    cmds.refresh(su = True)
    cmds.bakeResults(loc, simulation = True, t = (minTime, maxTime)) 
    cmds.refresh(su = False)