import re
import maya.cmds as cmds

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
    revAttr = ['translateX', 'rotateY', 'rotateZ']
    #- no change value
    arms = ['clavicle', 'scapula', 'shoulder', 'elbow', 'wrist']
    if mode == 'pose':
        for sel in sels:
            attrs = cmds.listAttr(sel, keyable = True)
            if sel[0] in ['l', 'L', 'r', 'R']:
                result = re.match("^{}+".format(prefix(sel)[0]), sel)
                selCut = sel[len(result.group(0)):]
                selRep = prefix(sel)[1] + selCut
                data[selRep] = {}

                #- so many cases
                if any(word in sel.lower() for word in arms):
                    for attr in attrs:
                        data[selRep][attr] = cmds.getAttr(sel + '.' + attr)
                else:
                    for attr in attrs:
                        if attr in revAttr: 
                            data[selRep][attr] = cmds.getAttr(sel + '.' + attr) * -1
                        else:
                            data[selRep][attr] = cmds.getAttr(sel + '.' + attr)
                        
            #- paste part
            for obj in data.keys():
                for attr in data[obj].keys():
                    cmds.setAttr(obj + '.' + attr, data[obj][attr])

    elif mode == 'anim':
        for sel in sels:
            attrs = cmds.listAttr(sel, keyable = True)
            if sel[0] in ['l', 'L', 'r', 'R']:
                result = re.match("^{}+".format(prefix(sel)[0]), sel)
                selCut = sel[len(result.group(0)):]
                selRep = prefix(sel)[1] + selCut
                data[selRep] = {}

                #- so many cases
                if any(word in sel.lower() for word in arms):
                    for attr in attrs:
                        data[selRep][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                                   'vc' : cmds.keyframe(sel + '.' + attr, q = True, vc = True)}
                else:
                    for attr in attrs:
                        if attr in revAttr: 
                            data[selRep][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                                  'vc' : [-1 * x for x in cmds.keyframe(sel + '.' + attr, q = True, vc = True)]}
                        else:
                            data[selRep][attr] = {'tc' : cmds.keyframe(sel + '.' + attr, q = True, tc = True), 
                                                  'vc' : cmds.keyframe(sel + '.' + attr, q = True, vc = True)}
                        
            #- paste part
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
                                except:
                                    pass