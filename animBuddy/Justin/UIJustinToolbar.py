import maya.cmds as cmds
import os
from functools import partial
import FkIkMatch
reload(FkIkMatch)
import FacialCam
reload(FacialCam)
import PartSelection
reload(PartSelection)

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
        if cmds.window('UIJustinToolBar', ex = True):
            return
        self.win = cmds.window('UIJustinToolBar', width=500, title = 'Justin Manager')
        self.frameLayoutMain = cmds.frameLayout(labelVisible = False, 
                                                w = 10, 
                                                borderVisible = False, 
                                                parent = self.win)
        self.rowLayoutMain = cmds.rowLayout(numberOfColumns = 4, 
                                            adjustableColumn = 1, 
                                            columnAttach = ([2, 'right', 0]), 
                                            parent = self.frameLayoutMain)
    
        cmds.rowLayout(numberOfColumns = 1)
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns = 12)

        cmds.button(label = 'GLASSES',
                    annotation = 'hide / unhide glasses', 
                    c = PartSelection.glasses)     

        cmds.button(label = 'TIE',
                    annotation = 'hide / unhide tie', 
                    c = PartSelection.tie)    
        cmds.separator(hr= False, height = 20, width = 20, style = 'in')

        cmds.button(label = 'FACIAL PANEL',
                    annotation = 'Opening facial panel cam', 
                    c = self.facialPanel)
        cmds.separator(hr= False, height = 20, width = 20, style = 'in')

        cmds.button(label = 'FKIK',
                    annotation = 'select any arm controller and run', 
                    c = self.fkikSwitch)
        cmds.separator(height = 10, width = 10, style = 'none')
        self.checkBoxBake = cmds.checkBox(label = "bake", cc = self.bakeTextBoxEnable)
        self.textFieldStartFrame = cmds.textField(width = 50, text = cmds.playbackOptions(minTime = True, q = True))
        self.textFieldEndFrame = cmds.textField(width = 50, text = cmds.playbackOptions(maxTime = True, q = True))
        self._bakeTextBoxCB()
        cmds.separator(height = 10, width = 10, style = 'none')
        cmds.rowLayout(numberOfColumns = 1)
        self.buttonClose = cmds.iconTextButton(style = 'iconOnly', 
                                               image1 = os.path.join(imagesPath, 'close.png'), 
                                               hi = os.path.join(imagesPath, 'close_hi.png'),
                                               width = iconSize, mw = marginSize, height = iconSize, mh = marginSize,
                                               label = 'close',
                                               annotation = 'Closing Selection ToolBar', 
                                               c = self.close)        
        cmds.setParent("..") 
        cmds.setParent("..")
    
    def fkikSwitch(self, *args):
        """
        """
        bake = False
        if cmds.checkBox(self.checkBoxBake, q = True, v = True):
            bake = True
        if bake:
            startFrame = int(float(cmds.textField(self.textFieldStartFrame, q = True, text = True)))
            endFrame = int(float(cmds.textField(self.textFieldEndFrame, q = True, text = True)))
            FkIkMatch.bake(frame = [startFrame, endFrame])
        else:
            FkIkMatch.convert(prefix = FkIkMatch.getPrefix(), side = FkIkMatch.getSide())

    def facialPanel(self, *args):
        """
        """
        if FacialCam.isExists():
            FacialCam.deletePanelCam()
        else:
            FacialCam.createPanelCam()

    def close(self, *args):
        """
        """
        try:
            cmds.deleteUI('justinToolbar')   
        except:
            pass        

    def _bakeTextBoxCB(self):
        """
        """
        enable = False
        if cmds.checkBox(self.checkBoxBake, q = True, v = True):
            enable = True
        cmds.textField(self.textFieldStartFrame, e = True, en = enable)
        cmds.textField(self.textFieldEndFrame, e = True, en = enable)
        

    def bakeTextBoxEnable(self, args):
        """
        """
        self._bakeTextBoxCB()

    def loadInMaya(self, *args):
        """
        """
        if not cmds.toolBar('justinToolbar', exists = True):  
            allowedAreas = ['top', 'bottom']
            cmds.toolBar('justinToolbar', area='bottom', content=self.win, allowedArea=allowedAreas )
