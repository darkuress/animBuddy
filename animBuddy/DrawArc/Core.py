import maya.cmds as cmds
import pymel.core as pm
import MotionTrail as mt
reload(mt)

def deleteAll():
    """
    """
    deleted = False
    if cmds.ls("*MotionTrail*mainHandle_all"):
        cmds.delete(cmds.ls("*MotionTrail*mainHandle_all"))
        deleted = True

    if pm.ls("*:*mainHandle_all"):
        for x in pm.ls("*:*mainHandle_all"):
            cmds.delete(x.name())
            deleted = True

    if pm.ls("*:*:*mainHandle_all"):
        for x in pm.ls("*:*:*mainHandle_all"):
            cmds.delete(x.name())
            deleted = True

    if not deleted:
        print("no Motion trail in the scene")

def run(dotSize = 5, 
        keyFrameSize = 750.25, 
        timeBuffer = 10,
        dotColor = [0.5, 0, 0.5],
        keyFrameColor = [0.0, 1.0, 0.0],
        lineWidth = 3,
        lineColor = [1.0, 1.0, 1.0],
        style = 'Double'):
    """
    """
    selection = cmds.ls(selection = True, long = True)
    if not selection:
        print "Please select a node to continue"
        return
    for node in selection:
        shortName = node.split("|")[-1]
        motionTrails = cmds.ls("MotionTrail_{}_*".format(shortName))
        
        if motionTrails:
            cmds.delete(motionTrails)
        else:
            startTime = cmds.playbackOptions(q = True, min = True)
            endTime = cmds.playbackOptions(q = True, max = True)
            print "Creating MotionTrail on {}".format(node)
            motionTrail = mt.MotionTrail(node, startTime, endTime)
            motionTrail.build(dotSize = dotSize, 
                              keyFrameSize = keyFrameSize, 
                              timeBuffer = timeBuffer,
                              dotColor = dotColor,
                              keyFrameColor = keyFrameColor,
                              lineWidth = lineWidth,
                              lineColor = lineColor,
                              style = style)
        cmds.select(selection)
    
if __name__ == "__main__":
    run()