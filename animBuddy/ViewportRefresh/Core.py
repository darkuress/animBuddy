import maya.cmds as cmds

def freeze():
    """
    """
    cmds.refresh(su = True)
    
def unfreeze():
    """
    """
    cmds.refresh(su = False)