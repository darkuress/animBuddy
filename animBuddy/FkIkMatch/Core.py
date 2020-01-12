import maya.cmds as cmds
import pymel.core as pm
import math

class Data(object):
    blend_node = "AttriBank_xx_ctrl"
    blend_attr = ".ikfkBlend"
    shoulder_ctrl = "ShFK_xx_ctrl"
    elbow_ctrl = "ElFK_xx_ctrl"
    wrist_ctrl = "WrFK_xx_ctrl"
    ik_ctrl = "IK_xx_ctrl"
    pv_ctrl = "Pv_xx_ctrl"
    pv_attr = ".PoleVectorMode"
    l_prifi = "LArm:"
    shoulder_jnt = "ShIK_xx_joint"
    elbow_jnt = "ElIK_xx_joint"
    wrist_jnt = "WrIK_xx_joint"
    @staticmethod
    def normalizeVector(vec = []):
        """
        """
        d = math.sqrt(math.pow(vec[0], 2) + math.pow(vec[1], 2) + math.pow(vec[2], 2))
        return [vec[0]/d, vec[1]/d, vec[2]/d]
        
def getSide():
    """
    """
    sel = cmds.ls(sl = True)[0]
    
    return sel.split(":")[-2] + ":"

def getPrefix():
    sel = cmds.ls(sl = True)[0]
    if len(sel.split(":")) == 2:
        return ""
    else:
        return sel.split(":")[0] + ":"

def fkToIkConv(prefix = '', side = "LArm:"):
    """
    """   
    shoulder_ctrl = prefix + side + Data.shoulder_ctrl
    elbow_ctrl = prefix + side + Data.elbow_ctrl
    wrist_ctrl = prefix + side + Data.wrist_ctrl
    ik_ctrl = prefix + side + Data.ik_ctrl

    shoulder_pos = cmds.xform(shoulder_ctrl, t = True, q = True, ws = True)
    elbow_pos = cmds.xform(elbow_ctrl, t = True, q = True, ws = True) 
    wrist_pos = cmds.xform(wrist_ctrl, t = True, q = True, ws = True)

    cmds.setAttr(prefix + side + Data.blend_node + Data.blend_attr, 0)
    cmds.setAttr(prefix + side + Data.blend_node + Data.pv_attr, 0)

    cmds.xform(ik_ctrl, t = wrist_pos, ws = True)

    temp_loc = cmds.spaceLocator()
    temp_pc = cmds.parentConstraint(wrist_ctrl, temp_loc, mo = False, weight = 1)
    cmds.delete(temp_pc)
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

    temp_pc = cmds.pointConstraint(temp_loc, prefix + side + Data.pv_ctrl, mo = False, weight = 1)
    cmds.delete(temp_pc)
    cmds.delete(temp_loc)
    
def ikToFkConv(prefix = '', side = "LArm:"):
    """
    """
    shoulder_jnt = prefix + side + Data.shoulder_jnt
    elbow_jnt = prefix + side + Data.elbow_jnt
    shoulder_ctrl = prefix + side + Data.shoulder_ctrl
    elbow_ctrl = prefix + side + Data.elbow_ctrl
    wrist_ctrl = prefix + side + Data.wrist_ctrl
    ik_ctrl = prefix + side + Data.ik_ctrl

    shoulder_rot = cmds.xform(shoulder_jnt, q = True, ro = True)
    elbow_rot = cmds.xform(elbow_jnt, q = True, ro = True)

    cmds.setAttr(prefix + side + Data.blend_node + Data.blend_attr, 1)

    cmds.xform(shoulder_ctrl, ro = shoulder_rot)
    cmds.xform(elbow_ctrl, ro = elbow_rot)

    #wrist
    temp_loc = cmds.spaceLocator()
    temp_pc = cmds.parentConstraint(ik_ctrl, temp_loc, mo = False, weight = 1)
    cmds.delete(temp_pc)
    temp_rc = cmds.orientConstraint(temp_loc, wrist_ctrl, mo = False, weight = 1)
    cmds.delete(temp_rc)
    cmds.delete(temp_loc)

def convert(prefix = "", side = "LArm:"):
    """
    """
    blend_node = prefix + side + Data.blend_node
    state = cmds.getAttr(blend_node + Data.blend_attr)

    if state == 1:
        fkToIkConv(prefix = prefix, side = side)
    else:
        ikToFkConv(prefix = prefix, side = side)
    