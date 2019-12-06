import maya.cmds as cmds

def exFootStep():
    selObj = cmds.ls(sl = True)
    if selObj:
        selObj = selObj[0]
        try:
            allKeyFrames = set(cmds.keyframe(selObj, q = True, tc = True))
        
            frame = cmds.currentTime(q = True)
            if [x for x in allKeyFrames if x < frame]:
                frameBefore = max([x for x in allKeyFrames if x < frame])

            #set to previous key
            cmds.refresh(su = True)
            cmds.currentTime(frameBefore)

            allAttrs = cmds.listAttr(selObj, k = True)
            newVal = {}
            for attr in allAttrs:
                newVal[attr] = cmds.getAttr(selObj + '.' + attr)

            cmds.currentTime(frame)

            for attr, v in newVal.iteritems():
                cmds.setAttr(selObj + '.' + attr, v)
                
            cmds.refresh(su = False)
        except:
            pass