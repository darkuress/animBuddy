import maya.cmds as cmds

def changeSelectedKey(ratio):
    """
    mode 2 selected key only
    """
    selObjs = cmds.ls(sl = True)
    for selObj in selObjs:
        curves = cmds.keyframe(selObj, sl = True, n = True, q = True)
        if curves:
            for cv in curves:
                frames = cmds.keyframe(cv, sl = True, q = True)
                for frame in frames:
                    runChange(cv, ratio, frame = frame)
        

def changeKey(ratio):
    """
    mode 1 regular 
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
       
def runChange(selKey, ratio, frame = ''):
    """
    change key per ratio slider
    """
    selObj = cmds.ls(sl = True)[0]
    selAttr = selKey.split('_')[-1]
    
    if selKey:
        if not frame:
            frame = cmds.currentTime(q = True)
        nearByKeyFrames = findCloseByKeyFrame(selKey, frame)
        
        if nearByKeyFrames[0] and nearByKeyFrames[1]:
            nearBeforeValue = cmds.keyframe(selKey, q = True, vc = True, t = (nearByKeyFrames[0], nearByKeyFrames[0]))[0]
            nearAfterValue = cmds.keyframe(selKey, q = True, vc = True, t = (nearByKeyFrames[1], nearByKeyFrames[1]))[0]
            baseValue = nearBeforeValue
            diffValue = nearAfterValue - nearBeforeValue

            #cmds.setAttr(selObj + '.' + selAttr, baseValue + diffValue * ratio)
            cmds.evalDeferred("cmds.setAttr('%s' + '.' + '%s', %s)" %(selObj, selAttr, baseValue + diffValue * ratio))
            cmds.setKeyframe(selObj, attribute = selAttr, t = frame, v = baseValue + diffValue * ratio )
            #cmds.evalDeferred("cmds.setKeyframe('%s', attribute = '%s', t = %s, v = %s)" %(selObj, selAttr, frame, baseValue + diffValue * ratio))

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