import os
import json
import maya.cmds as cmds
from animBuddy.Utils import Maya
from animBuddy.Utils import System
reload(Maya)

def run(amount = 1):
    """
    """
    sels = cmds.ls(sl = True)
    allAttrs = []
    for sel in sels:
        channelBox = Maya.getSelectedChannelBox()
        attrs = []
        try:    
            attrs = cmds.channelBox(channelBox, q = True, selectedMainAttributes = True)
        except:
            attrs = cmds.listAttr(sel, keyable = True)
        if not attrs:
            attrs = cmds.listAttr(sel, keyable = True)
        for attr in attrs:
            allAttrs.append(sel + '.' + attr)

    dataPath = os.path.join(System.dataPath(), 'shiftKey.json')
    data = {}
    if not os.path.exists(dataPath):
        time = getTime()
    else:
        with open(dataPath) as jsonFile:
            data = json.load(jsonFile)   
        if data.has_key('allAttrs'):
            prevSel = data['allAttrs']
            if not allAttrs == prevSel:
                time = getTime()
            else:
                time = (data['time'][0], data['time'][1])

    for attr in allAttrs:  
        cmds.keyframe(attr, edit = True, time = time, relative = True, timeChange = amount)

    data['time'] = (time[0] + amount, time[1] + amount )
    data['allAttrs'] = allAttrs
    
    #- writing
    with open(dataPath, 'w') as outfile:
        json.dump(data, outfile, indent = 2)   

def getTime():
    """
    """
    time = tuple(Maya.getSelectedTimeSlider())
    if time[1] - time[0] == 1:
        time = (cmds.playbackOptions(q = True, minTime = True), cmds.playbackOptions(q = True, maxTime = True))
    return time

def clear():
    """
    """
    dataPath = os.path.join(System.dataPath(), 'shiftKey.json')
    if os.path.exists(dataPath):
        os.remove(dataPath)