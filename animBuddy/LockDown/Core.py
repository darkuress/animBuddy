import maya.cmds as cmds
from animBuddy.Utils import Maya
reload(Maya)

def run(frame = 0,
        doTranslate = True, 
        doRotate = True,
        doReverse = False):
    """x
    """
    sel = cmds.ls(sl = True)
    if not sel:
        return
    else:
        sel = sel[0]

    # check if it timeline is selected
    timeline = (int(Maya.getSelectedTimeSlider()[0]), int(Maya.getSelectedTimeSlider()[1]))
    if timeline[1] - timeline[0] > 1:
        if doReverse:
            currentTime = timeline[1] - 1
        else:
            currentTime = timeline[0]
        frame = timeline[1] - timeline[0]
    else:
        currentTime = cmds.currentTime(q = True)

    # get object's current frame xform
    cmds.refresh(su = True)
    tempTime = cmds.currentTime(q = True)
    cmds.currentTime(currentTime)
    
    tr = cmds.xform(sel, q = True, t = True)
    ro = cmds.xform(sel, q = True, ro = True)

    # set keyframes
    attrs = []
    trAttrs = ['translateX', 'translateY', 'translateZ']
    roAttrs = ['rotateX', 'rotateY', 'rotateZ']
    if doTranslate:
        attrs = attrs + trAttrs
    if doRotate:
        attrs = attrs + roAttrs
   
    for attr in attrs:
        if attr == 'translateX':
            value = tr[0]
        elif attr == 'translateY':
            value = tr[1]
        elif attr == 'translateZ':
            value = tr[2]
        elif attr == 'rotateX':
            value = ro[0]
        elif attr == 'rotateY':
            value = ro[1]
        elif attr == 'rotateZ':
            value = ro[2]
        if doReverse:
            for fr in range(int(currentTime) - frame + 1, int(currentTime) + 1):
                cmds.setKeyframe(sel, attribute = attr, t = fr, v = value)
        else:
            print currentTime          
            for fr in range(int(currentTime), int(currentTime) + frame):
                cmds.setKeyframe(sel, attribute = attr, t = fr, v = value)
    
    cmds.currentTime(tempTime)
    cmds.refresh(su = False)

def clearKey():
    """
    """
    sel = cmds.ls(sl = True)
    if not sel:
        return
    else:
        sel = sel[0]

    minFrame = int(min(cmds.keyframe(sel, q = True)))
    maxFrame = int(max(cmds.keyframe(sel, q = True)))
    currTime = cmds.currentTime(q = True)

    cmds.refresh(su = True)
    attrs = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
    for fr in range(minFrame + 1, maxFrame):
        cmds.currentTime(fr)
        for attr in attrs:
            currVal = cmds.getAttr(sel + '.' + attr)
            cmds.currentTime(fr -1)
            prevVal = cmds.getAttr(sel + '.' + attr)
            cmds.currentTime(fr + 1)
            nextVal = cmds.getAttr(sel + '.' + attr)
            if prevVal == currVal == nextVal:
                cmds.cutKey(attribute = attr, time = (fr, fr))
    
    cmds.currentTime(currTime)
    cmds.refresh(su = False)            
            
