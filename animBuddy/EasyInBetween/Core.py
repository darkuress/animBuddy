import maya.cmds as cmds

def changeKey(ratio):
    """
    """
    selObjs = cmds.ls(sl = True)
    for selObj in selObjs:
        if cmds.keyframe(sl = True, n = True, q = True):
            animCurves = cmds.keyframe(sl = True, n = True, q = True)
        else:    
            animCurves = cmds.keyframe(selObj, n = True, q = True)
            if animCurves:
                animCurves = [x for x in animCurves if x.endswith("X") or x.endswith("Y") or x.endswith("Z")]
            else:
                return
                
        for animCurve in animCurves:
            runChange(animCurve, ratio)
       
def runChange(selKey, ratio):
    """
    change key per ratio slider
    """
    selObj = cmds.ls(sl = True)[0]
    """
    try:
        selKey = cmds.keyframe(sl = True, n = True, q = True)[0]
    except:
        "warning : please select anim curve"
        cmds.confirmDialog( title='Confirm', 
                            message='Please select anim curve', 
                            button=['ok'], 
                            defaultButton='ok', 
                            cancelButton='ok', 
                            dismissString='ok' )
        return
    """
    selAttr = selKey.split('_')[-1]
    
    if selKey:
        currentFrame = cmds.currentTime(q = True)
        nearByKeyFrames = findCloseByKeyFrame(selKey, currentFrame)
        
        if nearByKeyFrames[0] and nearByKeyFrames[1]:
            nearBeforeValue = cmds.keyframe(selKey, q = True, vc = True, t = (nearByKeyFrames[0], nearByKeyFrames[0]))[0]
            nearAfterValue = cmds.keyframe(selKey, q = True, vc = True, t = (nearByKeyFrames[1], nearByKeyFrames[1]))[0]
            baseValue = nearBeforeValue
            diffValue = nearAfterValue - nearBeforeValue
            '''
            elif not nearByKeyFrames[0]:
                baseValue = cmds.keyframe(selKey, q = True, vc = True, t = (nearByKeyFrames[1], nearByKeyFrames[1]))[0]
                diffValue = baseValue
            elif not nearByKeyFrames[1]:
                baseValue = cmds.keyframe(selKey, q = True, vc = True, t = (nearByKeyFrames[0], nearByKeyFrames[0]))[0]
                diffValue = baseValue
            '''
        
            cmds.setKeyframe(selObj, attribute = selAttr, t = currentFrame, v = baseValue + diffValue * ratio )
       

def findCloseByKeyFrame(selKey, frame):
    allKeyFrames = cmds.keyframe(selKey, q =True, tc = True)
    if [x for x in allKeyFrames if x < frame]:
        frameBefore = max([x for x in allKeyFrames if x < frame])
    else:
        frameBefore = None
    if [x for x in allKeyFrames if x > frame]:
        frameAfter = min([x for x in allKeyFrames if x > frame])
    else:
        frameAfter = None
    
    return frameBefore, frameAfter