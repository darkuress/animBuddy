import maya.cmds as cmds
import MotionTrail as mt
reload(mt)

def run():
    """
    """
    selection = cmds.ls(selection = True, long = True)
    if not selection:
        print "Please select a node to continue"
        return
    node = selection[0]
    shortName = node.split("|")[-1]
    motionTrails = cmds.ls("MotionTrail_{}_*".format(shortName))
    
    if motionTrails:
        cmds.delete(motionTrails)
    else:
        startTime = cmds.playbackOptions(q = True, min = True)
        endTime = cmds.playbackOptions(q = True, max = True)
        print "Creating MotionTrail on {}".format(node)
        motionTrail = mt.MotionTrail(node, startTime, endTime)
        motionTrail.build()
    cmds.select(selection)
    
if __name__ == "__main__":
    run()