import re
import math
import maya.cmds as cmds
from animBuddy.Utils import Maya

def prefix(sel):
    prefix = ()
    if sel.startswith('l'):
        if sel.startswith('left'):
            prefix = ('left', 'right')
        elif sel.startswith('lf'):
            prefix = ('lf', 'rt')
        else:
            prefix = ('l', 'r')
    elif sel.startswith('L'):
        if sel.startswith('Left'):
            prefix = ('Left', 'Right')
        elif sel.startswith('Lf'):
            prefix = ('Lf', 'Rt')
        else:
            prefix = ('L', 'R')    
    elif sel.startswith('r'):
        if sel.startswith('right'):
            prefix = ('right', 'left')
        elif sel.startswith('rt'):
            prefix = ('rt', 'lf')
        else:
            prefix = ('r', 'l') 
    elif sel.startswith('R'):
        if sel.startswith('Right'):
            prefix = ('Right', 'Left')
        elif sel.startswith('Rt'):
            prefix = ('Rt', 'Lf')
        else:
            prefix = ('R', 'L')
    else:
        prefix = ("", "")
    return prefix     

def run(mode = 'pose'):
    """
    """
    #- copy part
    sels = cmds.ls(sl = True)
    data = {}
    if mode == 'pose':
        for sel in sels:
            attrs = cmds.listAttr(sel, keyable = True)
            if sel[0] in ['l', 'L', 'r', 'R']:
                result = re.match("^{}+".format(prefix(sel)[0]), sel)
                selCut = sel[len(result.group(0)):]
                selRep = prefix(sel)[1] + selCut
                data[selRep] = {}
                for attr in attrs:
                    data[selRep][attr] = cmds.getAttr(sel + '.' + attr)
            else:
                data[sel] = {}
                revAttr = ['rotateY']
                for attr in attrs:
                    if attr in revAttr: 
                        data[sel][attr] = cmds.getAttr(sel + '.' + attr) * -1
                    else:
                        data[sel][attr] = cmds.getAttr(sel + '.' + attr)                

        #- paste part
        for sel in sels:
            for obj in data.keys():
                for attr in data[obj].keys():
                    try:
                        cmds.setAttr(obj + '.' + attr, data[obj][attr])
                    except:
                        pass
    elif mode == 'anim':
        for sel in sels:
            attrs = cmds.listAttr(sel, keyable = True)
            if sel[0] in ['l', 'L', 'r', 'R'] and 'root' not in sel.lower():
                result = re.match("^{}+".format(prefix(sel)[0]), sel)
                selCut = sel[len(result.group(0)):]
                selRep = prefix(sel)[1] + selCut
                data[selRep] = {}
                for attr in attrs:
                    data[selRep][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                            'vc' : cmds.keyframe(sel + '.' + attr, q = True, vc = True),
                                            'inTangentType' : cmds.keyTangent(sel + '.' + attr, inTangentType = True, q = True),
                                            'outTangentType' : cmds.keyTangent(sel + '.' + attr, outTangentType = True, q = True),
                                            'inAngle' : cmds.keyTangent(sel + '.' + attr, inAngle = True, q = True),
                                            'outAngle' : cmds.keyTangent(sel + '.' + attr, outAngle = True, q = True),
                                            'inWeight' : cmds.keyTangent(sel + '.' + attr, inWeight = True, q = True),
                                            'outWeight' : cmds.keyTangent(sel + '.' + attr, outWeight = True, q = True),
                                            'weightedTangents' : cmds.keyTangent(sel + '.' + attr, weightedTangents = True, q = True)}
            else:
                data[sel] = {}
                revAttr = ['rotateY']
                for attr in attrs:
                    if attr in revAttr: 
                        data[sel][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                           'vc' : [-1 * x for x in cmds.keyframe(sel + '.' + attr, q = True, vc = True)],
                                           'inTangentType' : cmds.keyTangent(sel + '.' + attr, inTangentType = True, q = True),
                                           'outTangentType' : cmds.keyTangent(sel + '.' + attr, outTangentType = True, q = True),
                                           'inAngle' : cmds.keyTangent(sel + '.' + attr, inAngle = True, q = True),
                                           'outAngle' : cmds.keyTangent(sel + '.' + attr, outAngle = True, q = True),
                                           'inWeight' : cmds.keyTangent(sel + '.' + attr, inWeight = True, q = True),
                                           'outWeight' : cmds.keyTangent(sel + '.' + attr, outWeight = True, q = True),
                                           'weightedTangents' : cmds.keyTangent(sel + '.' + attr, weightedTangents = True, q = True)}
                    else:
                        data[sel][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                           'vc' : cmds.keyframe(sel + '.' + attr, q = True, vc = True),
                                           'inTangentType' : cmds.keyTangent(sel + '.' + attr, inTangentType = True, q = True),
                                           'outTangentType' : cmds.keyTangent(sel + '.' + attr, outTangentType = True, q = True),
                                           'inAngle' : cmds.keyTangent(sel + '.' + attr, inAngle = True, q = True),
                                           'outAngle' : cmds.keyTangent(sel + '.' + attr, outAngle = True, q = True),
                                           'inWeight' : cmds.keyTangent(sel + '.' + attr, inWeight = True, q = True),
                                           'outWeight' : cmds.keyTangent(sel + '.' + attr, outWeight = True, q = True),
                                           'weightedTangents' : cmds.keyTangent(sel + '.' + attr, weightedTangents = True, q = True)}
        #- paste part
        for sel in sels:
            for obj in data.keys():
                for attr in data[obj].keys():
                    # check if data is anim data or pose data
                    if isinstance(data[obj][attr], dict):
                        if not data[obj][attr]['tc'] == None:
                            for i in range(len(data[obj][attr]['tc'])):
                                try:
                                    cmds.setKeyframe(obj + '.' + attr, 
                                                    t = data[obj][attr]['tc'][i],
                                                    v = data[obj][attr]['vc'][i])
                                    cmds.keyTangent(obj + '.' + attr,
                                                    inTangentType = data[obj][attr]['inTangentType'][i],
                                                    outTangentType = data[obj][attr]['outTangentType'][i],
                                                    inAngle = data[obj][attr]['inAngle'][i],
                                                    outAngle = data[obj][attr]['outAngle'][i],
                                                    inWeight = data[obj][attr]['inWeight'][i],
                                                    outWeight = data[obj][attr]['outWeight'][i],
                                                    weightedTangents = data[obj][attr]['weightedTangents'][i])
                                except:
                                    pass