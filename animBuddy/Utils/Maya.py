import maya.cmds as cmds
import maya.mel as mel

def getSelectedTimeSlider():
    """
    return selected time slider
    """
    aTimeSlider = mel.eval('$tmpVar = $gPlayBackSlider')
    timeRange = cmds.timeControl(aTimeSlider, q = True, rangeArray = True)
    return timeRange

def getSelectedChannelBox():
    """
    """
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    return channelBox

def getHierarchyTopNode(node = "", type = ""):
    """
    # Search through the rootJoint's top most joint parent node
    """
    rootNode = node

    while (True):
        if type:
            parent = cmds.listRelatives(rootNode, parent=True, type = type)
        else:
            parent = cmds.listRelatives(rootNode, parent=True)
        if not parent:
            break;
        rootNode = parent[0]

    return rootNode 