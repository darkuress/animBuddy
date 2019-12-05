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