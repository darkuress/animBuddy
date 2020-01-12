import maya.cmds as cmds
import os
from functools import partial
from animBuddy.FkIkMatch import Core
reload(Core)

#- initialize window
if cmds.window('UIJustinToolBar', ex = True):
    cmds.deleteUI('UIJustinToolBar')    
try:
    cmds.deleteUI('justinToolbar')   
except:
    pass 

class UIJustinToolbar:
    """
    """
    def __init__(self):
        """
        initializing ui
        """
        filePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imagesPath = os.path.join(filePath, 'images')
        iconSize = 25
        marginSize = 0
        self.win = cmds.window('UIJustinToolBar', width=500, title = 'Justin Manager')
        self.frameLayoutMain = cmds.frameLayout(labelVisible = False, 
                                                w = 10, 
                                                borderVisible = False, 
                                                parent = self.win)
        self.rowLayoutMain = cmds.rowLayout(numberOfColumns = 3, 
                                            adjustableColumn = 1, 
                                            columnAttach = ([2, 'right', 0]), 
                                            parent = self.frameLayoutMain)       

        cmds.rowLayout(numberOfColumns = 1)
        cmds.button(label = 'FKIK', c = self.fkikSwitch)
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonClose = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'close.png'), 
                                               hi = os.path.join(imagesPath, 'close_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'close',
                                               annotation = 'Closing Selection ToolBar', 
                                               c = self.close)        
        cmds.setParent("..") 
    
    def fkikSwitch(self, *args):
        """
        """
        Core.convert(prefix = Core.getPrefix(), side = Core.getSide())

    def close(self, *args):
        """
        """
        try:
            cmds.deleteUI('justinToolbar')   
        except:
            pass        

    def loadInMaya(self, *args):
        """
        """
        try:
            cmds.deleteUI('justinToolbar')   
        except:
            pass 
        allowedAreas = ['top', 'bottom']
        justinToolBar = cmds.toolBar('justinToolbar', area='bottom', content=self.win, allowedArea=allowedAreas )
