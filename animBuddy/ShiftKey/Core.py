import os
import json
import maya.cmds as cmds
from animBuddy.Utils import Maya
from animBuddy.Utils import System
reload(Maya)

def run(amount = 1):
    """
    """
    animEditorSelection = False
    sels = cmds.ls(sl = True)
    allAttrs = []
    for sel in sels:
        #animation edior selection
        curves = cmds.keyframe(sel, sl = True, n = True, q = True)
        if curves:
            for cv in curves:
                frames = cmds.keyframe(cv, sl = True, q = True)
                if frames:
                    animEditorSelection = True
                    for frame in frames:
                        cmds.keyframe(sel + '.' + cv.split('_')[-1], edit = True, time = (frame, frame), relative = True, timeChange = amount)
        else:
            #channelbox selection   
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
                
    if not animEditorSelection:
        dataPath = os.path.join(System.dataPath(), 'shiftKey.json')
        data = {}
        if not os.path.exists(dataPath):
            time = getTime()[0]
            timeLineSelection = getTime()[1]
        else:
            timeLineSelection = getTime()[1]
            with open(dataPath) as jsonFile:
                data = json.load(jsonFile)   
            if data.has_key('allAttrs'):
                prevSel = data['allAttrs']
                prevTimeLineSelection = int(data['timeLineSelection'])
                time = (data['time'][0], data['time'][1])
                if not allAttrs == prevSel:
                    time = getTime()[0]
                else:
                    if prevTimeLineSelection == 0 and timeLineSelection == 1:
                        time = getTime()[0]                   

        for attr in allAttrs:  
            cmds.keyframe(attr, edit = True, time = time, relative = True, timeChange = amount)

        data['time'] = (time[0] + amount, time[1] + amount )
        data['allAttrs'] = allAttrs
        data['timeLineSelection'] = timeLineSelection
        
        #- writing
        with open(dataPath, 'w') as outfile:
            json.dump(data, outfile, indent = 2)   

def getTime():
    """
    timeLineSelection : check if selected from tileline slider
    time : tuple selection range
    """
    timeLineSelection = 1
    time = tuple(Maya.getSelectedTimeSlider())
    if time[1] - time[0] == 1:
        time = (cmds.playbackOptions(q = True, minTime = True), cmds.playbackOptions(q = True, maxTime = True))
        timeLineSelection = 0
    return time, timeLineSelection

def clear():
    """
    """
    dataPath = os.path.join(System.dataPath(), 'shiftKey.json')
    if os.path.exists(dataPath):
        os.remove(dataPath)