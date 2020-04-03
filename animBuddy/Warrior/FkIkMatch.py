import maya.cmds as cmds
import pymel.core as pm
import math

class Data(object):
    blend_node = "FKIKArm"
    blend_attr = ".FKIKBlend"
    fk_attr_value = 0
    ik_attr_value = 10
    shoulder_ctrl = "FKShoulder"
    elbow_ctrl = "FKElbow"
    wrist_ctrl = "FKWrist"
    ik_ctrl = "IKArm"
    pv_ctrl = "PoleArm"
    pv_attr = ".follow"
    shoulder_jnt = "IKXShoulder"
    elbow_jnt = "IKXElbow"
    wrist_jnt = "IKXWrist"
    @staticmethod
    def normalizeVector(vec = []):
        """
        """
        d = math.sqrt(math.pow(vec[0], 2) + math.pow(vec[1], 2) + math.pow(vec[2], 2))
        return [vec[0]/d, vec[1]/d, vec[2]/d]
        
def getSide():
    """
    """
    if cmds.ls(sl = True):
        sel = cmds.ls(sl = True)[0]
        return sel.split(":")[-1].split('_')[0] + '_'
    else:
        return ""

def getPrefix():
    if cmds.ls(sl = True):
        sel = cmds.ls(sl = True)[0]
        if len(sel.split(":")) == 2:
            return sel.split(":")[0] + ":"
        else:
            return ""
    else:
        return ""

def getChar():
    if cmds.ls(sl = True):
        sel = cmds.ls(sl = True, l = True)[0]
        char = sel.split("|")[0]

        return char 
    else:
        return ""   

def getFromSelected(char, obj):
    """
    """
    long_name = ''
    all_objs = cmds.ls(obj, l = True)
    for one_obj in all_objs:
        if one_obj.split("|")[0] == char:
            long_name = one_obj
    return long_name

def fkToIkConv(prefix = '', side = "LArm:", convert = True):
    """
    """
    char = getChar()
    shoulder_ctrl = prefix + side + Data.shoulder_ctrl
    elbow_ctrl = prefix + side + Data.elbow_ctrl
    wrist_ctrl = prefix + side + Data.wrist_ctrl
    ik_ctrl = prefix + side + Data.ik_ctrl
    
    shoulder_ctrl = getFromSelected(char, shoulder_ctrl)
    elbow_ctrl = getFromSelected(char, elbow_ctrl)
    wrist_ctrl = getFromSelected(char, wrist_ctrl)
    ik_ctrl = getFromSelected(char, ik_ctrl)
    pv_ctrl = getFromSelected(char, prefix + side + Data.pv_ctrl)

    shoulder_pos = cmds.xform(shoulder_ctrl, t = True, q = True, ws = True)
    elbow_pos = cmds.xform(elbow_ctrl, t = True, q = True, ws = True) 
    wrist_pos = cmds.xform(wrist_ctrl, t = True, q = True, ws = True)

    blend_node = getFromSelected(char, prefix + side + Data.blend_node)
    cmds.setAttr(blend_node + Data.blend_attr, Data.ik_attr_value)
    #cmds.setAttr(pv_ctrl + Data.pv_attr, 0)

    #cmds.xform(ik_ctrl, t = wrist_pos, ws = True)

    temp_loc = cmds.spaceLocator()
    temp_pc = cmds.parentConstraint(wrist_ctrl, temp_loc, mo = False, weight = 1)
    wrist_rot = cmds.xform(temp_loc, q = True, ro = True)
    cmds.delete(temp_pc)
    if convert:
        temp_pc = cmds.parentConstraint(temp_loc, ik_ctrl, mo = False, weight = 1)
        cmds.delete(temp_pc)

    cmds.delete(temp_loc) 
    
    vec_sh_el = [elbow_pos[0] - shoulder_pos[0], elbow_pos[1] - shoulder_pos[1], elbow_pos[2] - shoulder_pos[2]]
    vec_wr_el = [elbow_pos[0] - wrist_pos[0], elbow_pos[1] - wrist_pos[1], elbow_pos[2] - wrist_pos[2]]
    norm_vec_sh_el = Data.normalizeVector(vec_sh_el)
    norm_vec_wr_el = Data.normalizeVector(vec_wr_el)

    pv_destination = [norm_vec_sh_el[0] + norm_vec_wr_el[0], norm_vec_sh_el[1] + norm_vec_wr_el[1], norm_vec_sh_el[2] + norm_vec_wr_el[2]]
    pv_destination = [elbow_pos[0] + 10*pv_destination[0], elbow_pos[1] + 10*pv_destination[1], elbow_pos[2] + 10*pv_destination[2]]
    temp_loc = cmds.spaceLocator()
    cmds.xform(temp_loc, t = pv_destination)
    
    if convert:
        temp_pc = cmds.pointConstraint(temp_loc, pv_ctrl, mo = False, weight = 1)
        cmds.delete(temp_pc)
    else:
        cmds.setAttr(blend_node + Data.blend_attr, Data.fk_attr_value)

    cmds.delete(temp_loc)
  
    return {'ik_pos'  : wrist_pos, 
            'ik_rot'  : wrist_rot,
            'ik_ctrl' : ik_ctrl,
            'pv' : pv_destination,
            'pv_ctrl' : pv_ctrl}
    
def ikToFkConv(prefix = '', side = "LArm:", convert = True):
    """
    """
    char = getChar()
    shoulder_jnt = prefix + side + Data.shoulder_jnt
    elbow_jnt = prefix + side + Data.elbow_jnt
    shoulder_ctrl = prefix + side + Data.shoulder_ctrl
    elbow_ctrl = prefix + side + Data.elbow_ctrl
    wrist_ctrl = prefix + side + Data.wrist_ctrl
    ik_ctrl = prefix + side + Data.ik_ctrl

    shoulder_jnt = getFromSelected(char, shoulder_jnt)
    elbow_jnt = getFromSelected(char, elbow_jnt)
    shoulder_ctrl = getFromSelected(char, shoulder_ctrl)
    elbow_ctrl = getFromSelected(char, elbow_ctrl)
    wrist_ctrl = getFromSelected(char, wrist_ctrl)
    ik_ctrl = getFromSelected(char, ik_ctrl)

    shoulder_rot = cmds.xform(shoulder_jnt, q = True, ro = True)
    elbow_rot = cmds.xform(elbow_jnt, q = True, ro = True)
    
    blend_node = getFromSelected(char, prefix + side + Data.blend_node)
    cmds.setAttr(blend_node + Data.blend_attr, Data.fk_attr_value)

    #wrist
    temp_loc = cmds.spaceLocator()
    temp_pc = cmds.parentConstraint(ik_ctrl, temp_loc, mo = False, weight = 1)
    cmds.delete(temp_pc)
    wrist_rot = cmds.xform(temp_loc, q = True, ro = True)
    wrist_pos = cmds.xform(temp_loc, q = True, t = True, ws = True)

    pc = cmds.parentConstraint(shoulder_jnt, shoulder_ctrl, mo = False, weight = 1)
    cmds.delete(pc)
    pc = cmds.parentConstraint(elbow_jnt, elbow_ctrl, mo = False, weight = 1)
    cmds.delete(pc)
    pc = cmds.parentConstraint(ik_ctrl, wrist_ctrl, mo = False, weight = 1)
    cmds.delete(pc)

    if not convert:
        cmds.setAttr(blend_node + Data.blend_attr, Data.ik_attr_value)

    cmds.delete(temp_loc)

    shoulder_rot = cmds.xform(shoulder_ctrl, q = True, ro = True)
    elbow_rot = cmds.xform(elbow_ctrl, q = True, ro = True)
    wrist_rot = cmds.xform(wrist_ctrl, q = True, ro = True)

    return {'shoulder_rot'  : shoulder_rot, 
            'elbow_rot'     : elbow_rot,
            'wrist_rot'     : wrist_rot,
            'wrist_pos'     : wrist_pos,
            'shoulder_ctrl' : shoulder_ctrl,
            'elbow_ctrl'    : elbow_ctrl,
            'wrist_ctrl'    : wrist_ctrl}

def convert(prefix = "", side = "LArm:"):
    """
    """
    char = getChar()
    side = getSide()
    blend_node = prefix + side + Data.blend_node
    blend_node = getFromSelected(char, blend_node)
    if not blend_node:
        return 
    state = cmds.getAttr(blend_node + Data.blend_attr)

    if state == Data.fk_attr_value:
        fkToIkConv(prefix = prefix, side = side)
    else:
        ikToFkConv(prefix = prefix, side = side)

def bake(frame = []):
    """
    """
    char = getChar()
    prefix = getPrefix()
    side = getSide()
    blend_node = prefix + side + Data.blend_node
    blend_node = getFromSelected(char, blend_node)
    state = cmds.getAttr(blend_node + Data.blend_attr)

    sel = cmds.ls(sl = True)[0]

    if not frame:
        frame = [int(cmds.playbackOptions(q = True, min = True)), int(cmds.playbackOptions(q = True , max = True)) + 1]
    
    data = {}
    cmds.refresh(su = True)
    
    if state == Data.fk_attr_value:
        #copy data
        for fr in range(frame[0], frame[1] + 1):
            cmds.currentTime(fr)
            data[fr] = fkToIkConv(prefix = prefix, side = side, convert = False)
            cmds.select(sel)
        cmds.setKeyframe(blend_node, attribute = Data.blend_attr, t = [frame[0] - 1, frame[0] -1])
        
        #paste data
        temp_loc_ctrl = cmds.spaceLocator()
        temp_loc_pv = cmds.spaceLocator()
        for fr in range(frame[0], frame[1] + 1):
            #fk to ik
            cmds.currentTime(fr)
            cmds.setAttr(blend_node + Data.blend_attr, Data.ik_attr_value)
            cmds.setKeyframe(blend_node, attribute = Data.blend_attr, t = [fr, fr])
            cmds.xform(temp_loc_ctrl, t = data[fr]['ik_pos'], ro = data[fr]['ik_rot'])
            cmds.xform(temp_loc_pv, t = data[fr]['pv'], ws = True)
            cmds.setKeyframe(temp_loc_ctrl)
            cmds.setKeyframe(temp_loc_pv)
        temp_con_ctrl = cmds.parentConstraint(temp_loc_ctrl, data[fr]['ik_ctrl'], mo = False, weight = 1)
        temp_con_pv = cmds.pointConstraint(temp_loc_pv, data[fr]['pv_ctrl'], mo = False, weight = 1)
        for item in [data[fr]['ik_ctrl'], data[fr]['pv_ctrl']]:
            cmds.bakeResults(item, 
                             simulation = True,
                             t = (frame[0], frame[1]),
                             sampleBy = 1, 
                             oversamplingRate = 1, 
                             disableImplicitControl= True,
                             preserveOutsideKeys = True,
                             sparseAnimCurveBake = False,
                             removeBakedAttributeFromLayer = False,
                             removeBakedAnimFromLayer = False,
                             minimizeRotation = True,
                             controlPoints = False,
                             shape = True)
        
        cmds.delete(temp_con_ctrl + temp_con_pv)
        cmds.delete(temp_loc_ctrl + temp_loc_pv)
        cmds.refresh(su = False)
        cmds.setAttr(blend_node + Data.blend_attr, Data.fk_attr_value)
        cmds.setKeyframe(blend_node, attribute = Data.blend_attr, t = [frame[1] + 1, frame[1] + 1])
    
    elif state == Data.ik_attr_value:
        #copy data
        for fr in range(frame[0], frame[1] + 1):
            cmds.currentTime(fr)
            data[fr] = ikToFkConv(prefix = prefix, side = side, convert = False)
            cmds.select(sel)
        cmds.setKeyframe(blend_node, attribute = Data.blend_attr, t = [frame[0] - 1, frame[0] -1])
        #paste data
        for fr in range(frame[0], frame[1] + 1):
            #fk to ik
            cmds.currentTime(fr)
            cmds.setAttr(blend_node + Data.blend_attr, Data.fk_attr_value)
            cmds.setKeyframe(blend_node, attribute = Data.blend_attr, t = [fr, fr])
            cmds.xform(data[fr]['shoulder_ctrl'], ro = data[fr]['shoulder_rot'])
            cmds.xform(data[fr]['elbow_ctrl'], ro = data[fr]['elbow_rot'])
            cmds.xform(data[fr]['wrist_ctrl'], ro = data[fr]['wrist_rot'])
            cmds.setKeyframe(data[fr]['shoulder_ctrl'])
            cmds.setKeyframe(data[fr]['elbow_ctrl'])
            cmds.setKeyframe(data[fr]['wrist_ctrl'])

        cmds.refresh(su = False)
        cmds.setAttr(blend_node + Data.blend_attr, Data.ik_attr_value)
        cmds.setKeyframe(blend_node, attribute = Data.blend_attr, t = [frame[1] + 1, frame[1] + 1])           