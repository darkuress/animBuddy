import maya.cmds as cmds
      
def getAnimCurves(withFrame = False):
    """
    return selected objects' anim curves
    """
    selObjs = cmds.ls(sl = True)
    animCurves = []
    if withFrame and cmds.keyframe(selObjs, sl = True, n = True, q = True):
        animCurves = cmds.keyframe(selObjs, sl = True, n = True, q = True)
    else:
        for selObj in selObjs:
            if cmds.keyframe(sl = True, n = True, q = True):
                animCurves = cmds.keyframe(sl = True, n = True, q = True)
            else:    
                animCurves = cmds.keyframe(selObj, n = True, q = True)
                if animCurves:
                    animCurves = [x for x in animCurves if x.endswith("X") or x.endswith("Y") or x.endswith("Z")]
                else:
                    return []
    return animCurves

def runChange(objs, ratio, animCurveCalculatedInfo, withFrame = False):
    """
    change key per ratio slider
    """
    animCurves = animCurveCalculatedInfo.keys()
    selObj = objs[0]
    for animCurve in animCurves:
        selAttr = animCurve.split('_')[-1]
        
        if selAttr:
            if not withFrame:
                frame = cmds.currentTime(q = True)
                
                baseValue = animCurveCalculatedInfo[animCurve][0]
                diffValue = animCurveCalculatedInfo[animCurve][1]

                cmds.setAttr(selObj + '.' + selAttr, baseValue + diffValue * ratio)
                #cmds.evalDeferred("cmds.setAttr('%s' + '.' + '%s', %s)" %(selObj, selAttr, baseValue + diffValue * ratio))
                cmds.setKeyframe(selObj, attribute = selAttr, t = frame, v = baseValue + diffValue * ratio )
                #cmds.evalDeferred("cmds.setKeyframe('%s', attribute = '%s', t = %s, v = %s)" %(selObj, selAttr, frame, baseValue + diffValue * ratio))
            else:
                for frame in animCurveCalculatedInfo[animCurve].keys():
                    baseValue = animCurveCalculatedInfo[animCurve][frame][0]
                    diffValue = animCurveCalculatedInfo[animCurve][frame][1]                   
                    cmds.setAttr(selObj + '.' + selAttr, baseValue + diffValue * ratio)
                    #cmds.evalDeferred("cmds.setAttr('%s' + '.' + '%s', %s)" %(selObj, selAttr, baseValue + diffValue * ratio))
                    cmds.setKeyframe(selObj, attribute = selAttr, t = frame, v = baseValue + diffValue * ratio )
                    #cmds.evalDeferred("cmds.setKeyframe('%s', attribute = '%s', t = %s, v = %s)" %(selObj, selAttr, frame, baseValue + diffValue * ratio))

def getAllKeyFrames(cv):
    """
    """
    frames = cmds.keyframe(cv, sl = True, q = True)
    return frames

def findCloseKeyByFrame(animCurve, frame):
    allKeyFrames = cmds.keyframe(animCurve, q =True, tc = True)
    if [x for x in allKeyFrames if x < frame]:
        frameBefore = max([x for x in allKeyFrames if x < frame])
    else:
        frameBefore = None
    if [x for x in allKeyFrames if x > frame]:
        frameAfter = min([x for x in allKeyFrames if x > frame])
    else:
        frameAfter = None
    
    return frameBefore, frameAfter

def calculate(animCurveInfo, withFrame = False):
    """
    calulate new keyframe info and construct dict
    """
    newInfo = {}
    if withFrame:
        for animCurve in animCurveInfo.keys():
            newInfo[animCurve] = {}
            for frame in animCurveInfo[animCurve].keys():
                nearByKeyFrames = animCurveInfo[animCurve][frame]
                
                if nearByKeyFrames[0] and nearByKeyFrames[1]:
                    nearBeforeValue = cmds.keyframe(animCurve, q = True, vc = True, t = (nearByKeyFrames[0], nearByKeyFrames[0]))[0]
                    nearAfterValue = cmds.keyframe(animCurve, q = True, vc = True, t = (nearByKeyFrames[1], nearByKeyFrames[1]))[0]
                    baseValue = nearBeforeValue
                    diffValue = nearAfterValue - nearBeforeValue

                newInfo[animCurve][frame] = (baseValue, diffValue)
    else:
        for animCurve in animCurveInfo.keys():
            nearByKeyFrames = animCurveInfo[animCurve]
            
            if nearByKeyFrames[0] and nearByKeyFrames[1]:
                nearBeforeValue = cmds.keyframe(animCurve, q = True, vc = True, t = (nearByKeyFrames[0], nearByKeyFrames[0]))[0]
                nearAfterValue = cmds.keyframe(animCurve, q = True, vc = True, t = (nearByKeyFrames[1], nearByKeyFrames[1]))[0]
                baseValue = nearBeforeValue
                diffValue = nearAfterValue - nearBeforeValue

            newInfo[animCurve] = (baseValue, diffValue)
    
    return newInfo
