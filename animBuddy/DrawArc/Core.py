import maya.cmds as cmds

def draw():
    st = cmds.playbackOptions(q = True, min = True)
    et = cmds.playbackOptions(q = True, max = True)
    cmds.snapshot(motionTrail = True, increment  = 1, startTime = st, endTime = et)