import maya.cmds as cmds

def setVariation(variation):
    """
    """
    prefix = ''
    if cmds.ls("*:warrior"):
        prefix = cmds.ls("*:warrior")[0].split(":")[0] + ':'
    
    if variation == 'Warrior':
        cmds.setAttr(prefix + "skin_mat.color", 0.39500001072883606, 0.2898096442222595, 0.16708499193191528)
        cmds.setAttr(prefix + "armor_mat.color", 0.06145251542329788, 0.0441889651119709, 0.019726259633898735)
        cmds.setAttr(prefix + "leather_mat.color", 0.12099999934434891, 0.08700807392597198, 0.03884099796414375)

    elif variation == 'Hero':
        cmds.setAttr(prefix + "skin_mat.color", 0.011249996721744537, 0.01455254852771759, 0.125)
        cmds.setAttr(prefix + "armor_mat.color", 0.0023856402840465307, 0.002075000200420618, 0.02500000037252903)
        cmds.setAttr(prefix + "leather_mat.color", 0.0023856402840465307, 0.002075000200420618, 0.02500000037252903)
        

