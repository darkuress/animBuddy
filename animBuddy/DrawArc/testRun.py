import maya.cmds as cmds
import MotionTrail as mt
reload(mt)

def deleteAll():
    """
    """
    if cmds.ls("*MotionTrail*mainHandle_all"):
        cmds.delete(cmds.ls("*MotionTrail*mainHandle_all"))
    else:
        print "No Motion Trail in the Scene"

def run(dotSize = 0.2, keyFrameSize = 0.25, timeBuffer = 10):
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
            motionTrail.build(dotSize = dotSize, keyFrameSize = keyFrameSize, timeBuffer = timeBuffer)
        cmds.select(selection)
    
if __name__ == "__main__":
    run()